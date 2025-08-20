"""QDPI DSPy Program implementing X→Y→A→Z cycle"""

import dspy
import json
from typing import Dict, Any, Optional
from .pipeline_signatures import ReadSignature, IndexSignature, AskSignature, ReceiveSignature
from .symbols import decode_symbol, BEHAVIORS, CHARACTER_MAP, get_symbol_info
from .policy import calculate_trajectory_weight, allow_fork

class QDPIProgram(dspy.Module):
    """Main QDPI program implementing the X→Y→A→Z narrative cycle"""
    
    def __init__(self, lm=None):
        super().__init__()
        
        # Set language model if provided
        if lm:
            dspy.settings.configure(lm=lm)
            
        # Initialize pipeline stages
        self.read = dspy.Predict(ReadSignature)
        self.index = dspy.Predict(IndexSignature) 
        self.ask = dspy.Predict(AskSignature)
        self.receive = dspy.Predict(ReceiveSignature)
        
        # Trajectory selector
        self.select = dspy.Select(options=["T0", "T1", "T2", "T3"])
        
    def forward(self, symbol_code: int, user_intent: str = "", current_page_id: Optional[str] = None):
        """Execute the full X→Y→A→Z cycle"""
        
        # Get symbol info
        symbol_info = get_symbol_info(symbol_code)
        
        # X: Read phase
        x_result = self.read(
            symbol_code=symbol_code,
            current_page_id=current_page_id
        )
        
        # Y: Index phase
        y_result = self.index(text=x_result.render)
        
        # Prepare state for Ask phase
        state = {
            "symbol": symbol_info,
            "x": {
                "render": x_result.render,
                "summary": x_result.summary,
                "edges": x_result.edges,
                "context": x_result.context
            },
            "y": {
                "entities": y_result.entities,
                "motifs": y_result.motifs,
                "anchors": y_result.anchors,
                "scores": y_result.scores
            }
        }
        
        # A: Ask phase
        a_result = self.ask(
            state=state,
            user_intent=user_intent
        )
        
        # Select trajectory based on scores and policy
        trajectory_context = {
            "scores": y_result.scores,
            "intent": user_intent,
            "current_trajectory": a_result.trajectory,
            "symbol": symbol_info["notation"]
        }
        
        selected_trajectory = self.select(
            context=json.dumps(trajectory_context)
        ) or a_result.trajectory
        
        # Prepare plan for Receive phase
        plan = {
            "symbol": symbol_info,
            "trajectory": selected_trajectory,
            "voice": a_result.voice,
            "constraints": a_result.constraints,
            "sources": a_result.sources,
            "context": {
                "summary": x_result.summary,
                "entities": y_result.entities,
                "motifs": y_result.motifs
            }
        }
        
        # Z: Receive phase
        z_result = self.receive(plan=plan)
        
        # Index the generated content for validation
        z_index = self.index(text=z_result.page_text)
        
        # Return complete result
        return QDPIResult(
            symbol_info=symbol_info,
            page_text=z_result.page_text,
            edges=z_result.edges,
            validation=z_result.validation,
            trajectory=selected_trajectory,
            index_signals={
                "entities": z_index.entities,
                "motifs": z_index.motifs,
                "novelty": z_index.scores.get("novelty", 0.5),
                "coherence": z_index.scores.get("coherence", 0.5)
            },
            plan=plan
        )

class QDPIResult:
    """Container for QDPI program results"""
    
    def __init__(self, symbol_info: Dict, page_text: str, edges: Dict, 
                 validation: Dict, trajectory: str, index_signals: Dict, plan: Dict):
        self.symbol_info = symbol_info
        self.page_text = page_text
        self.edges = edges
        self.validation = validation
        self.trajectory = trajectory
        self.index_signals = index_signals
        self.plan = plan
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            "symbol": self.symbol_info,
            "page_text": self.page_text,
            "edges": self.edges,
            "validation": self.validation,
            "trajectory": self.trajectory,
            "index_signals": self.index_signals,
            "plan": self.plan
        }

# Stub implementations for testing without LLM
class MockQDPIProgram(QDPIProgram):
    """Mock implementation for testing without LLM"""
    
    def __init__(self):
        # Don't call super().__init__() to avoid DSPy initialization
        pass
        
    def forward(self, symbol_code: int, user_intent: str = "", current_page_id: Optional[str] = None):
        """Mock implementation returning test data"""
        
        symbol_info = get_symbol_info(symbol_code)
        char_name = symbol_info["character"]
        orientation = symbol_info["orientation"]
        
        # Generate mock page text
        page_text = f"[{char_name} in {orientation} mode]\n\nThis is a test page generated for symbol {symbol_code}. "
        page_text += f"The narrative continues with {char_name}'s perspective...\n\n"
        page_text += f"User intent: {user_intent or 'continue'}"
        
        # Mock edges
        edges = {
            "next_within": f"page-{symbol_code:03d}-next",
            "fork_to": f"page-{(symbol_code + 16) % 256:03d}-fork" if symbol_code < 240 else None,
            "return_to": current_page_id if current_page_id else "canon-01-001"
        }
        
        # Mock validation
        validation = {
            "character_consistency": True,
            "trajectory_valid": True,
            "edges_valid": True
        }
        
        # Mock index signals
        index_signals = {
            "entities": [char_name, "Gibsey", "The Vault"],
            "motifs": ["identity", "recursion"],
            "novelty": 0.7,
            "coherence": 0.8
        }
        
        return QDPIResult(
            symbol_info=symbol_info,
            page_text=page_text,
            edges=edges,
            validation=validation,
            trajectory="T0",
            index_signals=index_signals,
            plan={"mock": True, "symbol": symbol_info}
        )