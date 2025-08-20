"""DSPy Signatures for QDPI X→Y→A→Z Pipeline"""

import dspy
from typing import Dict, List, Optional

class ReadSignature(dspy.Signature):
    """X: Read and render a page with context"""
    
    # Inputs
    symbol_code: int = dspy.InputField(desc="QDPI symbol code (0-255)")
    current_page_id: Optional[str] = dspy.InputField(desc="Current page ID for context")
    
    # Outputs  
    render: str = dspy.OutputField(desc="Rendered page text")
    summary: str = dspy.OutputField(desc="Page summary in 2-3 sentences")
    edges: dict = dspy.OutputField(desc="Available edges from this page")
    context: dict = dspy.OutputField(desc="Contextual metadata")

class IndexSignature(dspy.Signature):
    """Y: Extract entities and compute novelty/coherence"""
    
    # Inputs
    text: str = dspy.InputField(desc="Page text to analyze")
    
    # Outputs
    entities: list = dspy.OutputField(desc="Named entities found")
    motifs: list = dspy.OutputField(desc="Narrative motifs detected") 
    anchors: list = dspy.OutputField(desc="Unresolved narrative anchors")
    scores: dict = dspy.OutputField(desc="Novelty and coherence scores")

class AskSignature(dspy.Signature):
    """A: Plan narrative trajectory and constraints"""
    
    # Inputs
    state: dict = dspy.InputField(desc="Current narrative state from X and Y")
    user_intent: str = dspy.InputField(desc="User's narrative intent", default="")
    
    # Outputs
    trajectory: str = dspy.OutputField(desc="Selected trajectory (T0/T1/T2/T3)")
    voice: dict = dspy.OutputField(desc="Voice parameters for generation")
    constraints: dict = dspy.OutputField(desc="Generation constraints")
    sources: list = dspy.OutputField(desc="Source page IDs to reference")

class ReceiveSignature(dspy.Signature):
    """Z: Generate new page content with edges"""
    
    # Inputs
    plan: dict = dspy.InputField(desc="Generation plan from Ask phase")
    
    # Outputs
    page_text: str = dspy.OutputField(desc="Generated page content")
    edges: dict = dspy.OutputField(desc="Edges for the new page")
    validation: dict = dspy.OutputField(desc="Validation results")