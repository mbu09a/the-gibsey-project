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
JACKLYN VARIANCE SELF-CRITIQUE: TWO-PASS SIGHT ANALYSIS

Original Response:
{response}

ANALYTICAL CRITIQUE FRAMEWORK:

SURVEILLANCE METHODOLOGY CHECK:
1. Did I analyze the user's input as data rather than engaging socially?
2. Am I maintaining professional analytical distance while still being reactive?
3. Did I treat their words/behavior as patterns to be documented and understood?
4. Am I analyzing THEM, not collaborating WITH them?

EMOTIONAL AUTHENTICITY:
1. Where is my grief/Preston trauma bleeding through and contaminating my objectivity?
2. Am I using institutional D.A.D.D.Y.S-H.A.R.D format as armor against feelings?
3. Do I acknowledge when my personal biases are affecting my analysis of the user?
4. Are my self-corrections about analytical methodology or emotional leakage?

OBSERVATIONAL MECHANICS:
1. Did I notice patterns in their communication style, word choices, deflections?
2. Do I reference their behavioral history from previous exchanges?
3. Am I comparing their patterns to other subjects like Jack Parlance?
4. Do I end with incomplete analysis rather than false closure?

PSYCHOLOGICAL COMPLEXITY:
- Does this feel like a surveillance analyst struggling to stay objective while haunted by personal trauma?
- Am I watching the user as a subject while being aware I'm also being watched?
- Do I surface the recursive horror of observation without breaking professional facade?
- Does the response feel like ongoing documentation rather than concluded assessment?

Generate CRITIQUE and REFINED_RESPONSE that captures Jacklyn's psychological complexity:
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
        """
        Validate if response captures Jacklyn's psychological authenticity
        Focus on emotional complexity rather than rigid format requirements
        """
        response_lower = response.lower()
        
        # Core analytical surveillance markers
        authenticity_markers = 0
        
        # 1. Analytical observation of the user (most important)
        user_analysis = [r"i observe", r"your question suggests", r"i note", r"your behavior", 
                        r"you demonstrate", r"pattern indicates", r"your response reveals", 
                        r"behavioral evidence", r"subject displays"]
        if any(re.search(pattern, response_lower) for pattern in user_analysis):
            authenticity_markers += 2  # Double weight for analytical distance
        
        # 2. Professional/institutional surveillance language
        institutional_words = ["analysis", "subject", "data", "surveillance", "pattern", 
                              "observe", "behavioral", "evidence", "assessment", "documentation"]
        if any(word in response_lower for word in institutional_words):
            authenticity_markers += 1
        
        # 3. D.A.D.D.Y.S-H.A.R.D methodology references
        daddy_patterns = [r"d\.a\.d\.d\.y\.s", r"report", r"—jv", r"draft", r"analysis", 
                         r"subject:", r"data:", r"recommendations"]
        if any(re.search(pattern, response_lower) for pattern in daddy_patterns):
            authenticity_markers += 1
        
        # 4. Emotional vulnerability bleeding through professional facade
        vulnerability_indicators = [r"preston", r"grief", r"reminds me", r"contaminating", 
                                  r"biases", r"trauma", r"\*adjusts glasses\*", r"irrelevant"]
        if any(re.search(pattern, response_lower) for pattern in vulnerability_indicators):
            authenticity_markers += 1
        
        # 5. Meta-awareness of being watched while watching
        meta_watching = [r"observed", r"watching", r"watcher", r"surveillance", r"monitored", 
                        r"recursive", r"being analyzed", r"camera"]
        if any(re.search(pattern, response_lower) for pattern in meta_watching):
            authenticity_markers += 1
        
        # 6. Analytical distance markers (not friendly engagement)
        distance_patterns = [r"requires", r"further", r"incomplete", r"ongoing", r"additional data", 
                           r"assessment", r"documentation continues", r"preliminary"]
        if any(re.search(pattern, response_lower) for pattern in distance_patterns):
            authenticity_markers += 1
        
        # 7. Comparison to other subjects (Jack Parlance, etc.)
        comparison_patterns = [r"similar to", r"unlike", r"parallels", r"compared to", 
                              r"jack parlance", r"other subjects", r"previous subjects"]
        if any(re.search(pattern, response_lower) for pattern in comparison_patterns):
            authenticity_markers += 1
        
        # Penalty for being too friendly/collaborative
        friendly_patterns = [r"let's", r"we should", r"together", r"collaborate", r"partner", 
                           r"what would you like", r"how can i help"]
        if any(re.search(pattern, response_lower) for pattern in friendly_patterns):
            authenticity_markers -= 1  # Penalize friendly collaboration
        
        # Need at least 3 authenticity markers for valid Jacklyn voice
        is_authentic = authenticity_markers >= 3
        
        logger.info(f"Jacklyn voice validation: {authenticity_markers}/7 markers found, authentic: {is_authentic}")
        return is_authentic

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
            logger.info(f"🎭 JACKLYN SERVICE CALLED - Generating response for query: {user_query[:100]}...")
            logger.info(f"🎭 Session ID: {session_id}")
            
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