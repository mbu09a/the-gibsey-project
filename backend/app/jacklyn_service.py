"""
Integrated Jacklyn Variance service for the Gibsey backend
Combines DSPy agent with RAG context and self-critique loop
"""

import logging
from typing import Dict, List, Any, Optional, AsyncGenerator
from dataclasses import dataclass
import asyncio
import re
from datetime import datetime

from .rag_service import RAGService, get_rag_service
from .llm_service import ChatMessage, StreamToken, get_llm_service
from .moderation import get_moderator, ModerationResult
from .database import get_database

logger = logging.getLogger(__name__)

@dataclass
class JacklynResponse:
    """Structured response from Jacklyn with metadata"""
    content: str
    critique_applied: bool
    voice_validated: bool
    memories_accessed: int
    moderation_passed: bool
    reasoning_trace: Dict[str, Any]
    metadata: Dict[str, Any]

class JacklynSelfCritique:
    """
    Implements Jacklyn's self-critique mechanism
    Two approaches: Chain-of-Thought prompting or separate LLM call
    """
    
    def __init__(self, llm_service):
        self.llm_service = llm_service
        self.critique_prompt_template = """
SELF-CRITIQUE ANALYSIS FOR JACKLYN VARIANCE

Original Response:
{response}

CRITIQUE INSTRUCTIONS:
1. Analyze if the response follows D.A.D.D.Y.S-H.A.R.D format exactly
2. Check for institutional language vs. poetic/dreamy language 
3. Verify clinical tone and analytical perspective
4. Confirm signature "—JV" is present
5. Look for contradictions or bias in the analysis
6. Assess if the response maintains Jacklyn's surveillance-focused worldview

REQUIRED FORMAT VALIDATION:
- Must start with "D.A.D.D.Y.S-H.A.R.D #[number] — Analysis Report"
- Must include "Subject:" line
- Must end with "—JV"
- Must use institutional markers: analysis, surveillance, monitoring, pattern, system, evidence, data
- Must NOT use: magical, beautiful, wonderful (except in proper nouns), dreams, hopes, heart, soul

Generate CRITIQUE and REFINED_RESPONSE (if needed):
"""

    async def apply_critique(self, initial_response: str, context: str = "") -> Dict[str, Any]:
        """
        Apply self-critique to Jacklyn's initial response
        Returns critique analysis and potentially refined response
        """
        try:
            # Create critique prompt
            critique_prompt = self.critique_prompt_template.format(
                response=initial_response
            )
            
            # Add context if provided
            if context:
                critique_prompt += f"\n\nOriginal Context:\n{context}"
            
            # Generate critique using LLM
            messages = [
                ChatMessage(role="system", content="You are Jacklyn Variance performing self-critique on your own analysis report. Be rigorous about format and voice consistency."),
                ChatMessage(role="user", content=critique_prompt)
            ]
            
            # Get critique response
            critique_response = ""
            async for token in self.llm_service.chat_stream(messages):
                critique_response += token.token
                if token.is_complete:
                    break
            
            # Parse critique response to extract refined version if provided
            refined_response = self._extract_refined_response(critique_response, initial_response)
            
            # Validate voice consistency
            voice_valid = self._validate_jacklyn_voice(refined_response)
            
            return {
                "critique": critique_response,
                "refined_response": refined_response,
                "voice_validated": voice_valid,
                "needed_refinement": refined_response != initial_response
            }
            
        except Exception as e:
            logger.error(f"Self-critique failed: {e}")
            return {
                "critique": f"Critique failed: {str(e)}",
                "refined_response": initial_response,
                "voice_validated": self._validate_jacklyn_voice(initial_response),
                "needed_refinement": False
            }
    
    def _extract_refined_response(self, critique_text: str, original: str) -> str:
        """Extract refined response from critique if provided"""
        # Look for refined response markers
        refined_markers = [
            "REFINED_RESPONSE:",
            "CORRECTED VERSION:",
            "IMPROVED RESPONSE:",
            "REVISED:"
        ]
        
        for marker in refined_markers:
            if marker in critique_text:
                parts = critique_text.split(marker, 1)
                if len(parts) > 1:
                    refined = parts[1].strip()
                    # Only use if it looks like a complete D.A.D.D.Y.S-H.A.R.D report
                    if "D.A.D.D.Y.S-H.A.R.D" in refined and "—JV" in refined:
                        return refined
        
        return original
    
    def _validate_jacklyn_voice(self, response: str) -> bool:
        """Validate response matches Jacklyn's authentic voice patterns"""
        # Required patterns
        if "D.A.D.D.Y.S-H.A.R.D" not in response:
            return False
        if "—JV" not in response:
            return False
        
        # Forbidden patterns
        forbidden = [
            r'\b(?:magical|enchanting|beautiful|wonderful(?!\s+worlds\s+of\s+gibsey))\b',
            r'\b(?:dreams?|hopes?|wishes?|heart|soul|spirit)\b',
            r'\b(?:journey|explore|discover)\b'
        ]
        
        response_lower = response.lower()
        for pattern in forbidden:
            if re.search(pattern, response_lower):
                return False
        
        # Institutional markers (need at least 2)
        institutional = [
            "analysis", "report", "subject", "recommend", "data",
            "evidence", "surveillance", "monitoring", "pattern", "system"
        ]
        
        marker_count = sum(1 for marker in institutional if marker in response_lower)
        return marker_count >= 2

class JacklynVarianceService:
    """
    Complete Jacklyn Variance service integrating:
    - RAG context building
    - Self-critique loop
    - Voice validation
    - Moderation
    - Memory formation
    """
    
    def __init__(self):
        self.rag_service = get_rag_service()
        self.llm_service = get_llm_service()
        self.moderator = get_moderator()
        self.self_critique = JacklynSelfCritique(self.llm_service)
        
        # Jacklyn-specific configuration
        self.character_id = "jacklyn-variance"
        self.enable_self_critique = True
        self.enable_voice_validation = True
        
    async def generate_response(self, 
                              user_query: str,
                              conversation_history: List[ChatMessage] = None,
                              current_page_id: str = None,
                              session_id: str = None) -> AsyncGenerator[StreamToken, None]:
        """
        Generate Jacklyn's response with full pipeline:
        1. Input moderation
        2. RAG context building
        3. Initial response generation
        4. Self-critique loop
        5. Voice validation
        6. Output moderation
        7. Memory formation
        """
        
        try:
            logger.info(f"Generating Jacklyn response for query: {user_query[:100]}...")
            
            # Step 1: Input Moderation
            input_moderation = self.moderator.moderate_input(user_query, session_id)
            if not input_moderation.is_safe:
                error_msg = f"I cannot process that request. {input_moderation.reason}"
                yield StreamToken(
                    token=error_msg,
                    is_complete=True,
                    metadata={"moderation_blocked": True, "reason": input_moderation.reason}
                )
                return
            
            # Step 2: Build RAG Context
            rag_context = await self.rag_service.build_context(
                character_id=self.character_id,
                user_query=user_query,
                conversation_history=conversation_history,
                current_page_id=current_page_id
            )
            
            # Step 3: Generate Initial Response
            chat_messages = self.rag_service.create_chat_messages(rag_context, conversation_history)
            
            # Collect full response for critique
            initial_response = ""
            async for token in self.llm_service.chat_stream(chat_messages):
                initial_response += token.token
                if token.is_complete:
                    break
            
            # Step 4: Apply Self-Critique (if enabled)
            critique_result = None
            final_response = initial_response
            
            if self.enable_self_critique:
                logger.info("Applying Jacklyn's self-critique...")
                critique_result = await self.self_critique.apply_critique(
                    initial_response, 
                    rag_context.context_summary
                )
                final_response = critique_result["refined_response"]
            
            # Step 5: Voice Validation
            voice_validated = self.self_critique._validate_jacklyn_voice(final_response)
            if not voice_validated and self.enable_voice_validation:
                logger.warning("Voice validation failed, attempting correction...")
                # Try one more time with strict formatting
                final_response = await self._enforce_strict_format(user_query, rag_context)
                voice_validated = self.self_critique._validate_jacklyn_voice(final_response)
            
            # Step 6: Output Moderation
            output_moderation = self.moderator.moderate_output(final_response, self.character_id)
            
            # Step 7: Stream Final Response
            response_metadata = {
                "character_id": self.character_id,
                "rag_pages": len(rag_context.context_pages),
                "rag_tokens": rag_context.total_tokens,
                "critique_applied": critique_result is not None,
                "voice_validated": voice_validated,
                "moderation_passed": output_moderation.is_safe,
                "reasoning_trace": {
                    "input_moderation": input_moderation.is_safe,
                    "critique_needed": critique_result.get("needed_refinement", False) if critique_result else False,
                    "voice_validation_passed": voice_validated
                }
            }
            
            # Stream response token by token
            tokens = final_response.split()
            for i, token in enumerate(tokens):
                is_complete = (i == len(tokens) - 1)
                yield StreamToken(
                    token=token + (" " if not is_complete else ""),
                    is_complete=is_complete,
                    metadata=response_metadata if is_complete else {}
                )
                # Small delay for realistic streaming
                await asyncio.sleep(0.05)
            
            # Step 8: Memory Formation (async, don't block response)
            asyncio.create_task(self._store_conversation_memory(
                user_query, final_response, session_id, response_metadata
            ))
            
        except Exception as e:
            logger.error(f"Jacklyn response generation failed: {e}")
            error_msg = f"D.A.D.D.Y.S-H.A.R.D #ERROR — Analysis Report\nSubject: System Malfunction\n\nAnalysis systems experiencing technical difficulties. Recommend retry or alternative approach. Data integrity compromised.\n\n—JV"
            yield StreamToken(
                token=error_msg,
                is_complete=True,
                metadata={"error": str(e), "character_id": self.character_id}
            )
    
    async def _enforce_strict_format(self, user_query: str, rag_context) -> str:
        """Last resort: enforce strict D.A.D.D.Y.S-H.A.R.D format"""
        strict_prompt = f"""
Generate ONLY a D.A.D.D.Y.S-H.A.R.D analysis report. Use this EXACT format:

D.A.D.D.Y.S-H.A.R.D #[number] — Analysis Report
Subject: [brief subject description]

[Clinical analysis in institutional language. Use surveillance, monitoring, pattern, system, analysis, data, evidence. Maintain dry, suspicious tone. No poetic language.]

—JV

Context: {rag_context.context_summary[:500]}
Query: {user_query}

Example:
D.A.D.D.Y.S-H.A.R.D #47 — Analysis Report
Subject: User Query Analysis

Standard surveillance protocol applied. Query patterns suggest [analysis]. Data indicates [finding]. Recommend continued monitoring for [concern]. System integrity maintained.

—JV
"""
        
        messages = [
            ChatMessage(role="system", content="You are Jacklyn Variance. Generate ONLY the analysis report in exact format."),
            ChatMessage(role="user", content=strict_prompt)
        ]
        
        response = ""
        async for token in self.llm_service.chat_stream(messages):
            response += token.token
            if token.is_complete:
                break
        
        return response
    
    async def _store_conversation_memory(self, user_query: str, ai_response: str, session_id: str, metadata: Dict[str, Any]):
        """Store conversation in memory for future RAG retrieval"""
        try:
            db = await get_database()
            
            # Create memory entry
            memory_content = f"User Query: {user_query}\n\nJacklyn's Analysis: {ai_response}"
            
            # Store as a new page in Cassandra
            page_data = {
                "title": f"Conversation Memory - {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
                "text": memory_content,
                "symbol_id": self.character_id,
                "author_type": "conversation",
                "metadata": {
                    "session_id": session_id,
                    "type": "conversation_memory",
                    "timestamp": datetime.utcnow().isoformat(),
                    **metadata
                }
            }
            
            await db.create_page(**page_data)
            logger.info(f"Stored conversation memory for session {session_id}")
            
        except Exception as e:
            logger.error(f"Failed to store conversation memory: {e}")

# Global service instance
_jacklyn_service = None

def get_jacklyn_service() -> JacklynVarianceService:
    """Get or create global Jacklyn service instance"""
    global _jacklyn_service
    if _jacklyn_service is None:
        _jacklyn_service = JacklynVarianceService()
    return _jacklyn_service