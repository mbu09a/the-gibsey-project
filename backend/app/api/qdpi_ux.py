#!/usr/bin/env python3
"""
QDPI User Experience API Endpoints
Session-aware QDPI state management and user-friendly interfaces
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
import uuid
from datetime import datetime, timedelta

from ..qdpi import qdpi_engine, QDPIMode, Orientation, QDPISymbol
from ..qdpi_flows import qdpi_flows

# Configure logging
log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/qdpi", tags=["QDPI UX"])

# Session state storage (in production, use Redis or database)
session_states: Dict[str, Dict[str, Any]] = {}

# Pydantic models for UX-focused API
class QDPISessionState(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    mode: str
    orientation: str
    active_symbol: Optional[Dict[str, Any]] = None
    symbol_history: List[Dict[str, Any]] = Field(default_factory=list)
    flow_history: List[Dict[str, Any]] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    created_at: str
    updated_at: str

class ModeRequest(BaseModel):
    mode: str = Field(..., description="QDPI mode: read, ask, index, receive")
    orientation: Optional[str] = Field(None, description="Symbol orientation: n (normal) or u (upside)")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")

class EncodeRequest(BaseModel):
    data: Any = Field(..., description="Data to encode into QDPI symbols")
    mode: Optional[str] = Field(None, description="Override current mode for encoding")
    execute_flows: bool = Field(False, description="Execute symbol flows after encoding")

class DecodeRequest(BaseModel):
    symbol_names: Optional[List[str]] = Field(None, description="Symbol names to decode")
    glyph_ids: Optional[List[int]] = Field(None, description="Glyph IDs to decode")

class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query for semantic symbol matching")
    limit: int = Field(5, ge=1, le=20, description="Maximum results to return")
    mode_filter: Optional[str] = Field(None, description="Filter by recommended mode")
    flow_type_filter: Optional[str] = Field(None, description="Filter by flow type")

class FlowExecuteRequest(BaseModel):
    symbol_name: str = Field(..., description="Symbol to execute flows for")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Execution context")
    save_to_history: bool = Field(True, description="Save execution to flow history")

def get_or_create_session(session_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
    """Get or create a QDPI session state"""
    if session_id not in session_states:
        session_states[session_id] = {
            "session_id": session_id,
            "user_id": user_id,
            "mode": QDPIMode.READ.value,
            "orientation": Orientation.NORMAL.value,
            "active_symbol": None,
            "symbol_history": [],
            "flow_history": [],
            "context": {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    else:
        session_states[session_id]["updated_at"] = datetime.now().isoformat()
    
    return session_states[session_id]

def update_session_state(session_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update session state with new data"""
    session = get_or_create_session(session_id)
    session.update(updates)
    session["updated_at"] = datetime.now().isoformat()
    return session

@router.get("/mode/{session_id}", 
           response_model=QDPISessionState, 
           summary="Get current QDPI mode and state")
async def get_qdpi_mode(
    session_id: str,
    user_id: Optional[str] = Query(None, description="User ID for the session")
):
    """
    Get the current QDPI mode and state for a user session
    
    - **session_id**: Unique session identifier
    - **user_id**: Optional user identifier
    """
    try:
        session = get_or_create_session(session_id, user_id)
        return QDPISessionState(**session)
        
    except Exception as e:
        log.error(f"Error getting QDPI mode for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mode/{session_id}", 
            response_model=QDPISessionState, 
            summary="Set QDPI mode and state")
async def set_qdpi_mode(
    session_id: str,
    request: ModeRequest,
    user_id: Optional[str] = Query(None, description="User ID for the session")
):
    """
    Set the QDPI mode and state for a user session
    
    - **session_id**: Unique session identifier
    - **mode**: QDPI mode (read, ask, index, receive)
    - **orientation**: Symbol orientation (n=normal, u=upside)
    - **context**: Additional context data
    """
    try:
        # Validate mode
        try:
            mode = QDPIMode(request.mode.lower())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid mode: {request.mode}")
        
        # Validate orientation if provided
        orientation = None
        if request.orientation:
            try:
                orientation = Orientation(request.orientation.lower())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid orientation: {request.orientation}")
        
        # Update global QDPI engine state
        qdpi_engine.set_mode(mode)
        if orientation:
            if qdpi_engine.current_state.orientation != orientation:
                qdpi_engine.flip_orientation()
        
        # Update session state
        updates = {
            "mode": mode.value,
            "context": {**request.context} if request.context else {}
        }
        if orientation:
            updates["orientation"] = orientation.value
        
        session = update_session_state(session_id, updates)
        
        log.info(f"✅ Set QDPI mode to {mode.value} for session {session_id}")
        return QDPISessionState(**session)
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error setting QDPI mode for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/encode/{session_id}", summary="Encode data into QDPI symbols")
async def encode_data(
    session_id: str,
    request: EncodeRequest,
    user_id: Optional[str] = Query(None, description="User ID for the session")
):
    """
    Encode data into QDPI symbol sequences for a user session
    
    - **session_id**: Unique session identifier
    - **data**: Data to encode (string, dict, list, etc.)
    - **mode**: Override current mode for encoding
    - **execute_flows**: Whether to execute symbol flows after encoding
    """
    try:
        session = get_or_create_session(session_id, user_id)
        
        # Use provided mode or current session mode
        mode = None
        if request.mode:
            try:
                mode = QDPIMode(request.mode.lower())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid mode: {request.mode}")
        else:
            mode = QDPIMode(session["mode"])
        
        # Encode the data
        result = qdpi_engine.encode_message(str(request.data), mode)
        
        # Execute flows if requested
        flow_results = []
        if request.execute_flows:
            symbols = [qdpi_engine.codex.get_symbol_by_id(s["glyph_id"]) 
                      for s in result["encoded_symbols"]]
            symbols = [s for s in symbols if s is not None]
            
            if symbols:
                flow_result = await qdpi_flows.execute_symbol_sequence(symbols, session["context"])
                flow_results = flow_result["sequence_results"]
                
                # Update session with flow history
                session["flow_history"].append({
                    "timestamp": datetime.now().isoformat(),
                    "symbols": [s.name for s in symbols],
                    "flows": flow_results,
                    "context": session["context"]
                })
        
        # Update session with symbol history
        session["symbol_history"].extend([
            {
                "timestamp": datetime.now().isoformat(),
                "symbol": s["name"],
                "glyph_id": s["glyph_id"],
                "action": "encoded"
            } for s in result["encoded_symbols"]
        ])
        
        # Set active symbol to the first encoded symbol
        if result["encoded_symbols"]:
            session["active_symbol"] = result["encoded_symbols"][0]
        
        update_session_state(session_id, session)
        
        return {
            "session_id": session_id,
            "original_data": request.data,
            "encoded_symbols": result["encoded_symbols"],
            "execution_results": result["execution_results"],
            "flow_results": flow_results,
            "state": {
                "mode": session["mode"],
                "orientation": session["orientation"],
                "active_symbol": session["active_symbol"]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error encoding data for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/decode/{session_id}", summary="Decode QDPI symbols to data")
async def decode_symbols(
    session_id: str,
    request: DecodeRequest,
    user_id: Optional[str] = Query(None, description="User ID for the session")
):
    """
    Decode QDPI symbols back to original data for a user session
    
    - **session_id**: Unique session identifier
    - **symbol_names**: List of symbol names to decode
    - **glyph_ids**: List of glyph IDs to decode (alternative to symbol_names)
    """
    try:
        session = get_or_create_session(session_id, user_id)
        
        # Get symbols from names or glyph IDs
        symbols = []
        if request.symbol_names:
            for name in request.symbol_names:
                symbol = qdpi_engine.codex.get_symbol_by_name(name)
                if symbol:
                    symbols.append(symbol)
                else:
                    raise HTTPException(status_code=400, detail=f"Symbol not found: {name}")
        elif request.glyph_ids:
            for glyph_id in request.glyph_ids:
                symbol = qdpi_engine.codex.get_symbol_by_id(glyph_id)
                if symbol:
                    symbols.append(symbol)
                else:
                    raise HTTPException(status_code=400, detail=f"Invalid glyph ID: {glyph_id}")
        else:
            raise HTTPException(status_code=400, detail="Must provide either symbol_names or glyph_ids")
        
        # Decode symbols
        decoded_bytes = qdpi_engine.codex.decode_symbols(symbols)
        decoded_data = decoded_bytes.decode('utf-8', errors='ignore')
        
        # Update session with symbol history
        session["symbol_history"].extend([
            {
                "timestamp": datetime.now().isoformat(),
                "symbol": s.name,
                "glyph_id": s.glyph_id,
                "action": "decoded"
            } for s in symbols
        ])
        
        update_session_state(session_id, session)
        
        return {
            "session_id": session_id,
            "decoded_data": decoded_data,
            "symbols": [s.to_dict() for s in symbols],
            "symbol_count": len(symbols)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error decoding symbols for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search/{session_id}", summary="Search for relevant QDPI symbols")
async def search_symbols(
    session_id: str,
    request: SearchRequest,
    user_id: Optional[str] = Query(None, description="User ID for the session")
):
    """
    Search for symbols by semantic similarity, mode, or flow type
    
    - **session_id**: Unique session identifier
    - **query**: Search query for semantic matching
    - **limit**: Maximum results to return
    - **mode_filter**: Filter by recommended mode
    - **flow_type_filter**: Filter by flow type
    """
    try:
        session = get_or_create_session(session_id, user_id)
        
        # Perform semantic search
        search_results = qdpi_engine.semantic_search(request.query, request.limit)
        matches = search_results["matches"]
        
        # Apply filters
        if request.mode_filter:
            try:
                filter_mode = QDPIMode(request.mode_filter.lower())
                matches = [m for m in matches if m.get("function") and 
                          qdpi_engine.symbol_functions.get(m["symbol"]["name"], {}).get("mode") == filter_mode]
            except ValueError:
                pass  # Invalid mode filter, ignore
        
        if request.flow_type_filter:
            matches = [m for m in matches if m.get("domain") == request.flow_type_filter.lower()]
        
        # Update session with search history
        session["context"]["last_search"] = {
            "query": request.query,
            "results_count": len(matches),
            "timestamp": datetime.now().isoformat()
        }
        
        update_session_state(session_id, session)
        
        return {
            "session_id": session_id,
            "query": request.query,
            "matches": matches,
            "count": len(matches),
            "filters_applied": {
                "mode": request.mode_filter,
                "flow_type": request.flow_type_filter
            }
        }
        
    except Exception as e:
        log.error(f"Error searching symbols for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute/{session_id}", summary="Execute symbol flows")
async def execute_symbol_flows(
    session_id: str,
    request: FlowExecuteRequest,
    user_id: Optional[str] = Query(None, description="User ID for the session")
):
    """
    Execute flows for a specific symbol in a user session
    
    - **session_id**: Unique session identifier
    - **symbol_name**: Name of symbol to execute flows for
    - **context**: Additional context for execution
    - **save_to_history**: Whether to save execution to flow history
    """
    try:
        session = get_or_create_session(session_id, user_id)
        
        # Get the symbol
        symbol = qdpi_engine.codex.get_symbol_by_name(request.symbol_name)
        if not symbol:
            raise HTTPException(status_code=404, detail=f"Symbol not found: {request.symbol_name}")
        
        # Merge session context with request context
        execution_context = {**session["context"], **request.context}
        
        # Execute flows
        result = await qdpi_flows.execute_symbol_flow(symbol, execution_context)
        
        # Update session state
        session["active_symbol"] = symbol.to_dict()
        session["context"].update(execution_context)
        
        if request.save_to_history:
            session["flow_history"].append({
                "timestamp": datetime.now().isoformat(),
                "symbol": request.symbol_name,
                "flows": result["flows"],
                "context": execution_context
            })
        
        session["symbol_history"].append({
            "timestamp": datetime.now().isoformat(),
            "symbol": request.symbol_name,
            "glyph_id": symbol.glyph_id,
            "action": "executed"
        })
        
        update_session_state(session_id, session)
        
        return {
            "session_id": session_id,
            "symbol": request.symbol_name,
            "execution_result": result,
            "updated_context": execution_context,
            "state": {
                "mode": session["mode"],
                "orientation": session["orientation"],
                "active_symbol": session["active_symbol"]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error executing symbol flows for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}", summary="Get session history")
async def get_session_history(
    session_id: str,
    history_type: str = Query("all", description="Type of history: all, symbols, flows"),
    limit: int = Query(50, ge=1, le=200, description="Maximum items to return"),
    user_id: Optional[str] = Query(None, description="User ID for the session")
):
    """
    Get session history (symbols, flows, or both)
    
    - **session_id**: Unique session identifier
    - **history_type**: Type of history to retrieve (all, symbols, flows)
    - **limit**: Maximum items to return
    """
    try:
        session = get_or_create_session(session_id, user_id)
        
        result = {
            "session_id": session_id,
            "history_type": history_type,
            "limit": limit
        }
        
        if history_type in ["all", "symbols"]:
            result["symbol_history"] = session["symbol_history"][-limit:]
        
        if history_type in ["all", "flows"]:
            result["flow_history"] = session["flow_history"][-limit:]
        
        if history_type == "all":
            result["session_info"] = {
                "created_at": session["created_at"],
                "updated_at": session["updated_at"],
                "current_mode": session["mode"],
                "current_orientation": session["orientation"],
                "active_symbol": session["active_symbol"],
                "context": session["context"]
            }
        
        return result
        
    except Exception as e:
        log.error(f"Error getting session history for {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/session/{session_id}", summary="Clear session state")
async def clear_session(
    session_id: str,
    user_id: Optional[str] = Query(None, description="User ID for the session")
):
    """
    Clear session state and history
    
    - **session_id**: Unique session identifier
    """
    try:
        if session_id in session_states:
            del session_states[session_id]
            log.info(f"✅ Cleared session {session_id}")
        
        return {
            "session_id": session_id,
            "status": "cleared",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        log.error(f"Error clearing session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions", summary="List active sessions")
async def list_sessions(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    limit: int = Query(50, ge=1, le=200, description="Maximum sessions to return")
):
    """
    List active QDPI sessions
    
    - **user_id**: Optional filter by user ID
    - **limit**: Maximum sessions to return
    """
    try:
        sessions = list(session_states.values())
        
        # Filter by user_id if provided
        if user_id:
            sessions = [s for s in sessions if s.get("user_id") == user_id]
        
        # Sort by updated_at and limit
        sessions.sort(key=lambda s: s["updated_at"], reverse=True)
        sessions = sessions[:limit]
        
        return {
            "sessions": sessions,
            "total_count": len(sessions),
            "limit": limit,
            "filtered_by_user": user_id
        }
        
    except Exception as e:
        log.error(f"Error listing sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))