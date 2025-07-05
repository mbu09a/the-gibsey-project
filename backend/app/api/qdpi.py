#!/usr/bin/env python3
"""
QDPI API Endpoints
FastAPI routes for QDPI-256 encoding/decoding and state management
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from ..qdpi import qdpi_engine, QDPIMode, Orientation, QDPISymbol
from ..qdpi_flows import qdpi_flows

# Configure logging
log = logging.getLogger(__name__)

router = APIRouter(prefix="/qdpi", tags=["QDPI"])

# Pydantic models for API requests/responses
class EncodeRequest(BaseModel):
    data: Any
    mode: Optional[str] = "index"

class EncodeResponse(BaseModel):
    original_data: Any
    encoded_symbols: List[Dict[str, Any]]
    execution_results: List[Dict[str, Any]]
    state: Dict[str, Any]

class DecodeRequest(BaseModel):
    glyph_ids: List[int]

class DecodeResponse(BaseModel):
    decoded_data: str
    symbols: List[Dict[str, Any]]

class StateRequest(BaseModel):
    mode: Optional[str] = None
    flip_orientation: Optional[bool] = False

class StateResponse(BaseModel):
    mode: str
    orientation: str
    active_symbols: List[Dict[str, Any]]
    context: Dict[str, Any]
    timestamp: str

class SemanticSearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 5

class SemanticSearchResponse(BaseModel):
    query: str
    matches: List[Dict[str, Any]]
    count: int

class SymbolFunctionRequest(BaseModel):
    symbol_name: str
    context: Optional[Dict[str, Any]] = None

class SymbolFunctionResponse(BaseModel):
    symbol: str
    function: str
    description: str
    domain: str
    result: Dict[str, Any]

@router.get("/", summary="Get QDPI system status")
async def get_qdpi_status():
    """Get current QDPI system status and capabilities"""
    return {
        "system": "QDPI-256",
        "description": "Quaternary Data Protocol Interface",
        "total_symbols": len(qdpi_engine.codex.symbols),
        "total_glyphs": 256,
        "current_state": {
            "mode": qdpi_engine.current_state.mode.value,
            "orientation": qdpi_engine.current_state.orientation.value
        },
        "available_modes": [mode.value for mode in QDPIMode],
        "available_orientations": [orient.value for orient in Orientation],
        "symbol_functions": len(qdpi_engine.symbol_functions)
    }

@router.post("/encode", response_model=EncodeResponse, summary="Encode data into QDPI symbols")
async def encode_data(request: EncodeRequest):
    """
    Encode arbitrary data into QDPI symbol sequence and execute mapped functions
    
    - **data**: Any data to encode (string, dict, list, etc.)
    - **mode**: QDPI mode for encoding (read, ask, index, receive)
    """
    try:
        # Validate mode
        mode = None
        if request.mode:
            try:
                mode = QDPIMode(request.mode.lower())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid mode: {request.mode}")
        
        # Encode the data
        result = qdpi_engine.encode_message(str(request.data), mode)
        
        return EncodeResponse(
            original_data=request.data,
            encoded_symbols=result["encoded_symbols"],
            execution_results=result["execution_results"],
            state=result["state"]
        )
        
    except Exception as e:
        log.error(f"Error encoding data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/decode", response_model=DecodeResponse, summary="Decode QDPI symbols to data")
async def decode_symbols(request: DecodeRequest):
    """
    Decode QDPI glyph IDs back to original data
    
    - **glyph_ids**: List of glyph IDs (0-255) to decode
    """
    try:
        # Get symbols from glyph IDs
        symbols = []
        for glyph_id in request.glyph_ids:
            symbol = qdpi_engine.codex.get_symbol_by_id(glyph_id)
            if symbol:
                symbols.append(symbol)
            else:
                raise HTTPException(status_code=400, detail=f"Invalid glyph ID: {glyph_id}")
        
        # Decode symbols
        decoded_bytes = qdpi_engine.codex.decode_symbols(symbols)
        decoded_data = decoded_bytes.decode('utf-8', errors='ignore')
        
        return DecodeResponse(
            decoded_data=decoded_data,
            symbols=[s.to_dict() for s in symbols]
        )
        
    except Exception as e:
        log.error(f"Error decoding symbols: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/state", response_model=StateResponse, summary="Get current QDPI state")
async def get_state():
    """Get the current QDPI operational state"""
    state = qdpi_engine.current_state
    return StateResponse(
        mode=state.mode.value,
        orientation=state.orientation.value,
        active_symbols=[s.to_dict() for s in state.active_symbols],
        context=state.context,
        timestamp=datetime.now().isoformat()
    )

@router.post("/state", response_model=StateResponse, summary="Update QDPI state")
async def update_state(request: StateRequest):
    """
    Update the QDPI operational state
    
    - **mode**: New mode (read, ask, index, receive)
    - **flip_orientation**: Whether to flip orientation (normal/upside)
    """
    try:
        # Update mode if provided
        if request.mode:
            try:
                mode = QDPIMode(request.mode.lower())
                qdpi_engine.set_mode(mode)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid mode: {request.mode}")
        
        # Flip orientation if requested
        if request.flip_orientation:
            qdpi_engine.flip_orientation()
        
        # Return updated state
        state = qdpi_engine.current_state
        return StateResponse(
            mode=state.mode.value,
            orientation=state.orientation.value,
            active_symbols=[s.to_dict() for s in state.active_symbols],
            context=state.context,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        log.error(f"Error updating state: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=SemanticSearchResponse, summary="Semantic symbol search")
async def semantic_search(request: SemanticSearchRequest):
    """
    Search for symbols semantically similar to a query using SREC embeddings
    
    - **query**: Text query to search for
    - **limit**: Maximum number of results to return
    """
    try:
        result = qdpi_engine.semantic_search(request.query, request.limit)
        
        return SemanticSearchResponse(
            query=result["query"],
            matches=result["matches"],
            count=result["count"]
        )
        
    except Exception as e:
        log.error(f"Error in semantic search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/function", response_model=SymbolFunctionResponse, summary="Execute symbol function")
async def execute_symbol_function(request: SymbolFunctionRequest):
    """
    Execute the function mapped to a specific symbol
    
    - **symbol_name**: Name of the symbol to execute
    - **context**: Optional context data for the function
    """
    try:
        result = qdpi_engine.execute_symbol_function(request.symbol_name, request.context)
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return SymbolFunctionResponse(
            symbol=result["symbol"],
            function=result["function"],
            description=result["description"],
            domain=result["domain"],
            result=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error executing symbol function: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/flows/execute", summary="Execute QDPI flows for symbol")
async def execute_symbol_flows(request: SymbolFunctionRequest):
    """
    Execute all QDPI flows associated with a symbol
    
    - **symbol_name**: Name of the symbol to execute flows for
    - **context**: Optional context data for the flows
    """
    try:
        # Get the symbol
        symbol = qdpi_engine.codex.get_symbol_by_name(request.symbol_name)
        if not symbol:
            raise HTTPException(status_code=404, detail=f"Symbol not found: {request.symbol_name}")
        
        # Execute flows
        result = await qdpi_flows.execute_symbol_flow(symbol, request.context)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error executing symbol flows: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class SymbolSequenceRequest(BaseModel):
    glyph_ids: List[int]
    context: Optional[Dict[str, Any]] = None

@router.post("/flows/sequence", summary="Execute QDPI flows for symbol sequence")
async def execute_symbol_sequence_flows(request: SymbolSequenceRequest):
    """
    Execute QDPI flows for a sequence of symbols
    
    - **glyph_ids**: List of glyph IDs to execute flows for
    - **context**: Optional context data for the flows
    """
    try:
        # Get symbols from glyph IDs
        symbols = []
        for glyph_id in request.glyph_ids:
            symbol = qdpi_engine.codex.get_symbol_by_id(glyph_id)
            if symbol:
                symbols.append(symbol)
            else:
                raise HTTPException(status_code=400, detail=f"Invalid glyph ID: {glyph_id}")
        
        # Execute flows for the sequence
        result = await qdpi_flows.execute_symbol_sequence(symbols, request.context)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error executing symbol sequence flows: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/symbols", summary="List all QDPI symbols")
async def list_symbols(limit: Optional[int] = None):
    """
    List all available QDPI symbols with their properties
    
    - **limit**: Optional limit on number of symbols to return
    """
    try:
        symbols = qdpi_engine.codex.list_symbols()
        
        if limit:
            symbols = symbols[:limit]
        
        return {
            "symbols": [s.to_dict() for s in symbols],
            "count": len(symbols),
            "total_available": len(qdpi_engine.codex.symbols)
        }
        
    except Exception as e:
        log.error(f"Error listing symbols: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/symbols/{symbol_name}", summary="Get specific symbol details")
async def get_symbol(symbol_name: str):
    """
    Get detailed information about a specific symbol
    
    - **symbol_name**: Name of the symbol to retrieve
    """
    try:
        symbol = qdpi_engine.codex.get_symbol_by_name(symbol_name)
        
        if not symbol:
            raise HTTPException(status_code=404, detail=f"Symbol not found: {symbol_name}")
        
        # Get function mapping if available
        func_info = qdpi_engine.symbol_functions.get(symbol_name, {})
        
        return {
            "symbol": symbol.to_dict(),
            "function": func_info.get("function"),
            "description": func_info.get("description"),
            "domain": func_info.get("domain"),
            "recommended_mode": func_info.get("mode", {}).value if func_info.get("mode") else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error getting symbol: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/functions", summary="List all symbol functions")
async def list_symbol_functions():
    """List all available symbol-to-function mappings"""
    try:
        functions = {}
        for symbol_name, func_info in qdpi_engine.symbol_functions.items():
            functions[symbol_name] = {
                "function": func_info["function"],
                "description": func_info["description"],
                "domain": func_info["domain"],
                "recommended_mode": func_info["mode"].value
            }
        
        return {
            "functions": functions,
            "count": len(functions),
            "domains": list(set(f["domain"] for f in functions.values()))
        }
        
    except Exception as e:
        log.error(f"Error listing functions: {e}")
        raise HTTPException(status_code=500, detail=str(e))