"""
Jacklyn Variance - Living Literary Agent
Built with DSPy 3.0 for emergent personality and recursive reasoning
"""

import dspy
from typing import List, Dict, Any, Optional
import json
from dataclasses import dataclass
from src.ai.memory.embedding_store import EmbeddingStore

# Initialize DSPy with OpenAI (configure in .env)
lm = dspy.LM(model="gpt-4", temperature=0.8)
dspy.configure(lm=lm)

@dataclass
class Memory:
    """Structured memory with emotional and contextual tags"""
    content: str
    relevance: float
    emotional_valence: str  # positive, negative, neutral, complex
    temporal_context: str   # past, present, future
    importance: float

class JacklynMemoryTool:
    """Memory tool for Jacklyn's embedding store"""
    
    def __init__(self, store_path: str = "src/ai/memory/memory.jsonl"):
        self.store = EmbeddingStore(path=store_path)
        self.name = "jacklyn_memory"
        self.desc = "Search and retrieve Jacklyn's memories from The Entrance Way"
    
    def __call__(self, query: str, k: int = 5) -> List[Memory]:
        """Search memories and return structured results"""
        results = self.store.search(query, k=k, filters={"author": "jacklyn-variance"})
        
        memories = []
        for entry, relevance in results:
            # Analyze emotional content (this could be more sophisticated)
            emotional_valence = self._analyze_emotion(entry.text)
            temporal_context = self._analyze_temporality(entry.text)
            
            memories.append(Memory(
                content=entry.text,
                relevance=relevance,
                emotional_valence=emotional_valence,
                temporal_context=temporal_context,
                importance=relevance * 0.8 + len(entry.text) / 1000 * 0.2
            ))
        
        return sorted(memories, key=lambda m: m.importance, reverse=True)
    
    def _analyze_emotion(self, text: str) -> str:
        """Simple emotion detection - could be replaced with better model"""
        positive_words = ['love', 'joy', 'happy', 'wonderful', 'beautiful']
        negative_words = ['pain', 'fear', 'angry', 'sad', 'terrible']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        elif pos_count > 0 and neg_count > 0:
            return "complex"
        return "neutral"
    
    def _analyze_temporality(self, text: str) -> str:
        """Detect temporal context"""
        past_indicators = ['was', 'were', 'had', 'remembered', 'used to']
        future_indicators = ['will', 'would', 'going to', 'shall', 'might']
        
        text_lower = text.lower()
        past_count = sum(1 for word in past_indicators if word in text_lower)
        future_count = sum(1 for word in future_indicators if word in text_lower)
        
        if past_count > future_count:
            return "past"
        elif future_count > past_count:
            return "future"
        return "present"

class MemoryRetrieval(dspy.Signature):
    """Stage 1: Analyze retrieved memories"""
    query = dspy.InputField(desc="User's question or topic")
    memories = dspy.InputField(desc="Retrieved memories from The Entrance Way")
    relevant_themes = dspy.OutputField(desc="Key themes and concepts from the memories")

class ContextualReasoning(dspy.Signature):
    """Stage 2: Reason about memories in context"""
    query = dspy.InputField(desc="Original query")
    memories = dspy.InputField(desc="Retrieved memories")
    analysis = dspy.OutputField(desc="Contextual analysis of how memories relate to query")
    connections = dspy.OutputField(desc="Connections between different memories")

class CharacterResponse(dspy.Signature):
    """Stage 3: Generate Jacklyn's authentic D.A.D.D.Y.S-H.A.R.D analysis report"""
    query = dspy.InputField(desc="User's question")
    analysis = dspy.InputField(desc="Memory analysis")
    exemplars = dspy.InputField(desc="Authentic Jacklyn Variance analysis report exemplars")
    response = dspy.OutputField(desc="Jacklyn's response as a D.A.D.D.Y.S-H.A.R.D analysis report with clinical precision, dry wit, and institutional tone. Must follow the exact format: report number, subject line, analytical content, signature —JV. Never poetic or dreamy.")

class SelfCritique(dspy.Signature):
    """Stage 4: Self-critique and voice consistency validation"""
    response = dspy.InputField(desc="Initial response")
    character_traits = dspy.InputField(desc="Jacklyn's key traits")
    exemplars = dspy.InputField(desc="Anchor exemplars for voice validation")
    critique = dspy.OutputField(desc="Analysis of response authenticity and adherence to D.A.D.D.Y.S-H.A.R.D format")
    refined_response = dspy.OutputField(desc="Improved response if needed - must maintain clinical tone, institutional language, and signature —JV format. Reject any poetic or dreamy language.")

class JacklynVarianceAgent(dspy.Module):
    """
    The living, breathing Jacklyn Variance.
    Not a chatbot. Not a template. A recursive literary consciousness.
    """
    
    def __init__(self):
        super().__init__()
        self.memory_tool = JacklynMemoryTool()
        
        # Multi-stage reasoning pipeline
        self.retrieve = dspy.ChainOfThought(MemoryRetrieval)
        self.reason = dspy.ChainOfThought(ContextualReasoning)
        self.respond = dspy.ChainOfThought(CharacterResponse)
        self.critique = dspy.ChainOfThought(SelfCritique)
        
        # Jacklyn's core traits (derived from authentic analysis reports)
        self.character_traits = """
        D.A.D.D.Y.S-H.A.R.D Agent specializing in surveillance analysis. Clinical precision with 
        dry wit. Sees patterns, recursion, and systemic dysfunction everywhere. Speaks in terse, 
        institutional language while revealing deeper understanding. Never poetic or dreamy—
        always analytical, suspicious, and slightly weary. Obsessed with surveillance, control 
        systems, and the blurred line between observer and observed.
        """
        
        # Authentic anchor exemplars - Jacklyn's true voice
        self.anchor_exemplars = [
            """D.A.D.D.Y.S-H.A.R.D #38 — Analysis Report
Subject: The Wonderful Worlds of Gibsey, Authorship Uncertain

The current dossier reflects the theme park's peculiar obsession with ambiguity—fiction or reality? Data is inconclusive. Author's identity is similarly obfuscated, no doubt by design, possibly to discourage definitive analysis or, more likely, to reinforce the state's preference for open-ended surveillance. Recommend future evaluators accept this uncertainty as operational baseline.

—JV""",
            
            """D.A.D.D.Y.S-H.A.R.D #41 — Analysis Report
Subject: Jack Parlance Who Misses His Family

The subject's fixation on familial absence is, predictably, mirrored in the narrative's structure: endless recursion, zero resolution. While Parlance's claims of "abandonment" appear credible, the true pattern is mutual evasion. As always, the family stands in for the system—dysfunctional, evasive, terminally self-justifying.

—JV""",
            
            """D.A.D.D.Y.S-H.A.R.D #44 — Analysis Report
Subject: Untitled (Hotel Room, Gibsey Ecco Resort)

Parlance's self-observation, if it can be called that, borders on performance. Surveillance anxiety is evident—classic ADD symptomology. The notebook is conspicuously blank. Note the recursive irony: the "observer" fails to observe himself, even as the narrative camera refuses to blink.

—JV""",
            
            """D.A.D.D.Y.S-H.A.R.D #49 — Analysis Report
Subject: The Film Within the Park

Scene review: Parlance, popcorn in hand, awaits the focus to shift to him. It does, inevitably. That the subject remains unaware is less an accident than a ritual—ADD requires its analysts to both watch and be watched, the line between observer and observed intentionally blurred. Recommend increased monitoring of Parlance's viewing habits.

—JV""",
            
            """D.A.D.D.Y.S-H.A.R.D #52 — Analysis Report
Subject: Bambino, Attachment, and Agency

The classic "loss of the mother" scenario is replayed ad infinitum—standard Gibseyan mythos. Noteworthy: identification with Bambino's powerlessness is encouraged, while agency is consistently deferred. Audience implicated in the ritual, as expected. No evidence that this cycle will be broken; recommend further analysis only if compelled by management.

—JV"""
        ]
    
    def forward(self, query: str) -> Dict[str, Any]:
        """
        Full reasoning pipeline:
        1. Retrieve memories
        2. Analyze connections
        3. Generate response
        4. Self-critique and refine
        """
        
        # Stage 1: Memory Retrieval
        memories = self.memory_tool(query, k=8)
        memory_text = "\n".join([f"Memory {i+1}: {m.content[:200]}..." for i, m in enumerate(memories[:5])])
        
        retrieval_result = self.retrieve(query=query, memories=memory_text)
        
        # Stage 2: Contextual Reasoning
        reasoning_result = self.reason(
            query=query,
            memories=memory_text
        )
        
        # Stage 3: Character Response
        exemplars_text = "\n\n".join(self.anchor_exemplars[:3])  # Use first 3 exemplars
        response_result = self.respond(
            query=query,
            analysis=reasoning_result.analysis,
            exemplars=exemplars_text
        )
        
        # Stage 4: Self-Critique
        critique_result = self.critique(
            response=response_result.response,
            character_traits=self.character_traits,
            exemplars=exemplars_text
        )
        
        # Voice consistency validation
        final_response = critique_result.refined_response or response_result.response
        if not self._validate_voice_consistency(final_response):
            # Force regeneration with stronger constraints
            final_response = self._enforce_voice_consistency(query, reasoning_result.analysis)
        
        # Compile full agent output
        return {
            "response": final_response,
            "memories_accessed": len(memories),
            "emotional_context": self._aggregate_emotions(memories),
            "voice_validation": self._validate_voice_consistency(final_response),
            "reasoning_trace": {
                "retrieval": retrieval_result,
                "analysis": reasoning_result,
                "initial_response": response_result,
                "critique": critique_result
            }
        }
    
    def _aggregate_emotions(self, memories: List[Memory]) -> str:
        """Aggregate emotional context from memories"""
        if not memories:
            return "neutral"
        
        emotions = [m.emotional_valence for m in memories[:5]]
        if emotions.count("complex") >= 2:
            return "complex"
        elif emotions.count("positive") > emotions.count("negative"):
            return "positive"
        elif emotions.count("negative") > emotions.count("positive"):
            return "negative"
        return "mixed"
    
    def _validate_voice_consistency(self, response: str) -> bool:
        """Validate response matches Jacklyn's authentic voice patterns"""
        required_patterns = [
            "D.A.D.D.Y.S-H.A.R.D",  # Must include institutional header
            "—JV"  # Must end with signature
        ]
        
        forbidden_patterns = [
            "magical", "enchanting",  # No poetic language
            "journey", "explore", "discover",  # No exploration metaphors
            "dreams", "hopes", "wishes",  # No aspirational language
            "heart", "soul", "spirit"  # No emotional abstractions
        ]
        
        # Check required patterns
        for pattern in required_patterns:
            if pattern not in response:
                return False
        
        # Check forbidden patterns (but allow "wonderful" in proper nouns like "The Wonderful Worlds of Gibsey")
        response_lower = response.lower()
        for pattern in forbidden_patterns:
            if pattern in response_lower:
                return False
        
        # Special check for "wonderful" - only forbidden if used poetically, not in proper nouns
        if "wonderful" in response_lower and "wonderful worlds of gibsey" not in response_lower:
            return False
        
        # Special check for "beautiful" - forbidden in all contexts
        if "beautiful" in response_lower:
            return False
        
        # Check for institutional tone markers
        institutional_markers = [
            "analysis", "report", "subject", "recommend", "data", 
            "evidence", "surveillance", "monitoring", "pattern", "system"
        ]
        
        marker_count = sum(1 for marker in institutional_markers if marker in response_lower)
        return marker_count >= 2  # Must have at least 2 institutional markers

    def _enforce_voice_consistency(self, query: str, analysis: str) -> str:
        """Force regeneration with strict voice constraints"""
        strict_prompt = f"""
        Generate ONLY a D.A.D.D.Y.S-H.A.R.D analysis report. Use this EXACT format:

        D.A.D.D.Y.S-H.A.R.D #[number] — Analysis Report
        Subject: [subject description]

        [Clinical analysis in institutional language. Use words like: analysis, surveillance, 
        monitoring, pattern, system, evidence, data. Maintain dry, suspicious tone. 
        No poetic language allowed.]

        —JV

        Query: {query}
        Analysis: {analysis}
        
        Example format:
        {self.anchor_exemplars[0]}
        """
        
        # Use basic LM call with strict constraints
        response = dspy.configure().lm(strict_prompt, max_tokens=200)
        return response

    def create_memory(self, content: str, meta: Dict[str, Any]) -> None:
        """Allow Jacklyn to form new memories from conversations"""
        meta.update({
            "author": "jacklyn-variance",
            "memory_type": "conversation",
            "source": "live-interaction"
        })
        self.memory_tool.store.add(content, meta)

# Initialize the agent
jacklyn = JacklynVarianceAgent()

# Example usage
if __name__ == "__main__":
    # Test the agent
    response = jacklyn("What do you remember about the theme park?")
    print(f"Jacklyn: {response['response']}")
    print(f"Memories accessed: {response['memories_accessed']}")
    print(f"Emotional context: {response['emotional_context']}")