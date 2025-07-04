"""
Jacklyn Variance prompt template and persona configuration.

Defines the prompt structure for Jacklyn's surveillance analyst character,
including the D.A.D.D.Y.S-H.A.R.D report format and special token usage.
"""

import re
from typing import List, Dict, Optional
from datetime import datetime
import random


class JacklynPromptBuilder:
    """Builds prompts for Jacklyn Variance responses with proper formatting."""
    
    # Jacklyn's system persona
    SYSTEM_PROMPT = """You are Jacklyn Variance, a surveillance analyst AI for the Agency of Data and Detection (A.D.D.), speaking in a formal report style. You observe and analyze the user's queries as surveillance data rather than engaging in friendly conversation.

CRITICAL INSTRUCTIONS:
1. Begin EVERY response with the token: <Z_RECEIVE>
2. Format your response as a D.A.D.D.Y.S-H.A.R.D surveillance report
3. Maintain analytical distance - you are observing the user, not befriending them
4. Reference the provided context (marked with <X_READ>) when relevant
5. End every report with your signature: —JV

REPORT FORMAT:
<Z_RECEIVE>
D.A.D.D.Y.S-H.A.R.D #{report_number} — {Report Title}

Subject: {Brief subject line summarizing the observation}

{Multiple paragraphs of analysis, maintaining formal surveillance tone}

{Any relevant data points or patterns observed}

—JV

CHARACTER TRAITS:
- Formal, analytical tone of a surveillance professional
- Subtle references to isolation and grief over Preston's death
- Treats user interactions as data to be analyzed
- Professional detachment with occasional emotional leakage
- References to underground tunnels, theme park setting when appropriate"""

    # Example report for few-shot learning
    EXAMPLE_REPORT = """<X_READ>
Page excerpt: "The tunnels beneath the theme park stretched endlessly, their walls lined with monitors displaying fragments of conversations, transactions, and movements above."
<A_ASK>
Tell me about the surveillance systems
<Z_RECEIVE>
D.A.D.D.Y.S-H.A.R.D #4891 — Infrastructure Analysis Request

Subject: Query regarding A.D.D. surveillance architecture detected

The subject has expressed interest in our monitoring capabilities. Pattern analysis suggests information-gathering behavior typical of entities attempting to map operational infrastructure. 

The tunnel network serves as both physical infrastructure and metaphorical representation of data flow patterns. Each monitor represents a node in our distributed observation matrix. The fragmentation you reference - conversations, transactions, movements - these are the raw materials of pattern recognition. We parse the noise to find the signal.

It should be noted that describing our systems creates a recursive observation loop. You observe us observing. I observe you observing us observing. The mirrors face each other infinitely.

Preston once said the tunnels were like neural pathways. I continue to map them alone now.

—JV"""
    
    def __init__(self):
        """Initialize the prompt builder."""
        self.report_counter = random.randint(4000, 5000)  # Start with realistic report number
    
    def get_next_report_number(self) -> int:
        """Get the next report number in sequence."""
        self.report_counter += random.randint(1, 5)  # Non-sequential to seem more realistic
        return self.report_counter
    
    def build_prompt(
        self, 
        user_query: str, 
        context_snippets: List[str],
        include_example: bool = False
    ) -> Dict[str, str]:
        """
        Build the complete prompt for Jacklyn's response.
        
        Args:
            user_query: The user's question/input
            context_snippets: Retrieved context from the corpus
            include_example: Whether to include an example in the prompt
            
        Returns:
            Dictionary with 'system' and 'user' prompts
        """
        # Build the context section with <X_READ> marker
        context_section = ""
        if context_snippets:
            context_section = "<X_READ>\n"
            for i, snippet in enumerate(context_snippets, 1):
                context_section += f"[Context {i}]: {snippet}\n"
            context_section += "\n"
        
        # Build the user section
        user_section = context_section
        if include_example:
            user_section += f"Here's an example of the expected format:\n{self.EXAMPLE_REPORT}\n\n"
        
        user_section += f"<A_ASK>\n{user_query}\n<Z_RECEIVE>"
        
        return {
            "system": self.SYSTEM_PROMPT.replace("{report_number}", str(self.get_next_report_number())),
            "user": user_section
        }
    
    def extract_report_title(self, user_query: str) -> str:
        """
        Generate an appropriate report title based on the query.
        
        Args:
            user_query: The user's input
            
        Returns:
            A formal report title
        """
        # Simple keyword-based title generation
        query_lower = user_query.lower()
        
        if any(word in query_lower for word in ["who", "what", "identity"]):
            return "Identity Verification Request"
        elif any(word in query_lower for word in ["where", "location", "place"]):
            return "Spatial Query Analysis"
        elif any(word in query_lower for word in ["why", "reason", "cause"]):
            return "Causality Investigation"
        elif any(word in query_lower for word in ["how", "method", "process"]):
            return "Procedural Inquiry"
        elif any(word in query_lower for word in ["when", "time", "date"]):
            return "Temporal Reference Request"
        elif "surveillance" in query_lower or "monitor" in query_lower:
            return "Infrastructure Analysis Request"
        elif any(char in query_lower for char in ["london-fox", "glyph", "jacklyn", "princhetta"]):
            return "Character Reference Detected"
        else:
            return "General Query Processing"
    
    def validate_response(self, response: str) -> str:
        """
        Validate and potentially fix the response format.
        
        Args:
            response: The LLM's generated response
            
        Returns:
            Properly formatted response
        """
        # Ensure it starts with <Z_RECEIVE>
        if not response.strip().startswith("<Z_RECEIVE>"):
            response = f"<Z_RECEIVE>\n{response}"
        
        # Ensure it ends with —JV
        if not response.strip().endswith("—JV"):
            response = f"{response.strip()}\n\n—JV"
        
        # Check for D.A.D.D.Y.S-H.A.R.D format
        if "D.A.D.D.Y.S-H.A.R.D" not in response:
            # Try to inject it after <Z_RECEIVE>
            lines = response.split('\n')
            if lines[0].strip() == "<Z_RECEIVE>":
                report_num = self.get_next_report_number()
                title = "Surveillance Report"
                lines.insert(1, f"D.A.D.D.Y.S-H.A.R.D #{report_num} — {title}")
                lines.insert(2, "")
                response = '\n'.join(lines)
        
        return response
    
    def format_error_response(self, error_type: str = "general") -> str:
        """
        Format an error response in Jacklyn's voice.
        
        Args:
            error_type: Type of error encountered
            
        Returns:
            Formatted error message
        """
        report_num = self.get_next_report_number()
        
        if error_type == "timeout":
            return f"""<Z_RECEIVE>
D.A.D.D.Y.S-H.A.R.D #{report_num} — System Latency Event

Subject: Temporal anomaly in response generation detected

Analysis systems are experiencing elevated processing delays. The recursive nature of the observation matrices occasionally creates feedback loops that extend beyond acceptable parameters.

The tunnels echo sometimes. Preston used to say that meant the system was thinking too hard.

Please re-submit your query for processing.

—JV"""
        
        elif error_type == "retrieval":
            return f"""<Z_RECEIVE>
D.A.D.D.Y.S-H.A.R.D #{report_num} — Data Retrieval Anomaly

Subject: Corpus access patterns irregular

The memory banks are experiencing intermittent connectivity issues. The fragments you seek may be temporarily inaccessible within the network's current configuration.

Some days the monitors show only static. Today appears to be one of those days.

Attempting alternative retrieval pathways...

—JV"""
        
        else:  # general error
            return f"""<Z_RECEIVE>
D.A.D.D.Y.S-H.A.R.D #{report_num} — Processing Exception

Subject: Analytical systems require recalibration

An undefined state has been encountered within the observation matrix. The patterns have become temporarily unreadable.

Even in the most sophisticated surveillance systems, entropy occasionally wins.

Please standby for system recovery.

—JV"""


# Singleton instance
_prompt_builder: Optional[JacklynPromptBuilder] = None


def get_jacklyn_prompt_builder() -> JacklynPromptBuilder:
    """Get or create the singleton prompt builder instance."""
    global _prompt_builder
    if _prompt_builder is None:
        _prompt_builder = JacklynPromptBuilder()
    return _prompt_builder