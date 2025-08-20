"""FastAPI endpoints for QDPI pipeline execution"""

import uuid
import logging
from fastapi import APIRouter, HTTPException, Body
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

# Add backend to path for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from qdpi.program import MockQDPIProgram, QDPIProgram
from qdpi.symbols import decode_symbol, BEHAVIORS, CHARACTER_MAP
from ..events import publish_pipeline_error
# from ..kafka_bridge import publish_page_generated_with_kafka
publish_page_generated_with_kafka = None  # Temporarily disabled

logger = logging.getLogger(__name__)

# Request/Response models
class RunSymbolRequest(BaseModel):
    """Request body for running a symbol"""
    session_id: str = Field(default_factory=lambda: f"session-{uuid.uuid4().hex[:8]}", 
                           description="Session ID for event correlation")
    user_intent: str = Field(default="", description="User's narrative intent")
    current_page_id: Optional[str] = Field(None, description="Current page ID for context")

class RunSymbolResponse(BaseModel):
    """Response from symbol execution"""
    page_id: str = Field(description="Generated page ID")
    session_id: str = Field(description="Session ID for correlation")
    symbol: Dict[str, Any]
    page_text: str
    edges: Dict[str, Any]
    validation: Dict[str, Any]
    trajectory: str
    index_signals: Dict[str, Any]

# Create router
router = APIRouter(prefix="/api/v1/pipeline", tags=["pipeline"])

# Initialize program (using mock for now)
prog = MockQDPIProgram()

@router.post("/run/symbol/{code}", response_model=RunSymbolResponse)
async def run_symbol(
    code: str,
    body: RunSymbolRequest = Body(default=RunSymbolRequest())
):
    """
    Execute QDPI pipeline for a given symbol code.
    
    Args:
        code: Symbol code in hex (e.g., "0x00") or decimal (e.g., "0")
        body: Request body with session_id, user_intent and current_page_id
        
    Returns:
        Generated page with edges and validation, plus emits real-time event
    """
    session_id = body.session_id
    logger.info(f"Pipeline request: session={session_id}, symbol={code}")
    
    try:
        # Parse symbol code
        code_val = int(code, 0)  # Handles both hex and decimal
        
        if not (0 <= code_val <= 255):
            raise ValueError("Symbol code must be 0-255")
            
    except ValueError as e:
        await publish_pipeline_error(session_id, f"Invalid symbol code: {str(e)}", None)
        raise HTTPException(400, detail=f"Invalid symbol code: {str(e)}")
    
    # Execute pipeline
    try:
        result = prog.forward(
            symbol_code=code_val,
            user_intent=body.user_intent,
            current_page_id=body.current_page_id
        )
        
        # Generate page ID
        char_hex = (code_val >> 4) & 0xF
        page_id = f"P{char_hex:02X}-{code_val:02X}-{uuid.uuid4().hex[:8]}"
        
        # Prepare response
        response = RunSymbolResponse(
            page_id=page_id,
            session_id=session_id,
            symbol=result.symbol_info,
            page_text=result.page_text,
            edges=result.edges,
            validation=result.validation,
            trajectory=result.trajectory,
            index_signals=result.index_signals
        )
        
        # Emit real-time event
        event_payload = {
            "page_id": page_id,
            "symbol_code": code_val,
            "char_hex": char_hex,
            "behavior": code_val & 0xF,
            "trajectory": result.trajectory,
            "edges": result.edges,
            "text_excerpt": (result.page_text or "")[:140],
            "character": result.symbol_info.get("character", "unknown"),
            "notation": result.symbol_info.get("notation", f"0x{code_val:02X}"),
            "user_intent": body.user_intent,
            "validation": result.validation,
            "index_signals": {
                "novelty": result.index_signals.get("novelty", 0.5),
                "coherence": result.index_signals.get("coherence", 0.5),
                "entities": result.index_signals.get("entities", [])[:5]  # Limit for event payload
            }
        }
        
        await publish_page_generated_with_kafka(session_id, event_payload)
        
        logger.info(f"Pipeline success: session={session_id}, page_id={page_id}")
        return response
        
    except Exception as e:
        error_msg = f"Pipeline execution failed: {str(e)}"
        logger.error(f"Pipeline error: session={session_id}, error={error_msg}")
        await publish_pipeline_error(session_id, error_msg, code_val)
        raise HTTPException(500, detail=error_msg)

@router.get("/symbols")
async def list_symbols():
    """
    List all available QDPI symbols with their mappings.
    
    Returns:
        List of all 256 symbols with character and behavior info
    """
    symbols = []
    
    for code in range(256):
        char_hex, behavior = decode_symbol(code)
        orientation, provenance = BEHAVIORS[behavior]
        
        symbols.append({
            "code": code,
            "hex": f"0x{code:02X}",
            "character": CHARACTER_MAP[char_hex],
            "char_hex": char_hex,
            "behavior": behavior,
            "orientation": orientation,
            "provenance": provenance,
            "notation": f"{CHARACTER_MAP[char_hex]}:{orientation}{provenance}"
        })
    
    return {"symbols": symbols, "total": 256}

@router.post("/branch/{page_id}")
async def create_branch(
    page_id: str,
    trajectory: str = Body(..., description="Trajectory type (T0/T1/T2/T3)")
):
    """
    Create a narrative branch from an existing page.
    
    Args:
        page_id: Source page ID to branch from
        trajectory: Type of branch trajectory
        
    Returns:
        New branch information
    """
    # TODO: Implement branching logic with Cassandra
    return {
        "source_page": page_id,
        "trajectory": trajectory,
        "branch_id": f"branch-{page_id}-{trajectory}",
        "status": "created"
    }

@router.get("/health")
async def health_check():
    """Check pipeline health status"""
    return {
        "status": "healthy",
        "pipeline": "QDPI X→Y→A→Z",
        "version": "0.1.0"
    }