#!/usr/bin/env python3
"""
QDPI WebSocket Integration
Real-time QDPI state changes, symbol highlighting, and flow updates
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .websocket import manager
from .qdpi import qdpi_engine, QDPIMode, Orientation
from .qdpi_flows import qdpi_flows

log = logging.getLogger(__name__)

class QDPIWebSocketManager:
    """Manages real-time QDPI WebSocket events"""
    
    def __init__(self):
        self.session_subscriptions: Dict[str, Dict[str, bool]] = {}
    
    async def subscribe_session(self, session_id: str, events: Dict[str, bool] = None):
        """Subscribe a session to QDPI WebSocket events"""
        if events is None:
            events = {
                "mode_changes": True,
                "orientation_flips": True,
                "symbol_activations": True,
                "flow_executions": True,
                "search_results": True
            }
        
        self.session_subscriptions[session_id] = events
        
        await manager.send_personal_message({
            "type": "qdpi_subscription_confirmed",
            "data": {
                "session_id": session_id,
                "events": events,
                "timestamp": datetime.now().isoformat()
            }
        }, session_id)
        
        log.info(f"✅ Session {session_id} subscribed to QDPI events")
    
    async def unsubscribe_session(self, session_id: str):
        """Unsubscribe a session from QDPI WebSocket events"""
        if session_id in self.session_subscriptions:
            del self.session_subscriptions[session_id]
        
        await manager.send_personal_message({
            "type": "qdpi_unsubscribed",
            "data": {
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }
        }, session_id)
        
        log.info(f"✅ Session {session_id} unsubscribed from QDPI events")
    
    async def broadcast_mode_change(self, session_id: str, old_mode: str, new_mode: str, orientation: str):
        """Broadcast QDPI mode change to subscribed sessions"""
        if session_id not in self.session_subscriptions:
            return
        
        if not self.session_subscriptions[session_id].get("mode_changes", False):
            return
        
        await manager.send_personal_message({
            "type": "qdpi_mode_changed",
            "data": {
                "session_id": session_id,
                "old_mode": old_mode,
                "new_mode": new_mode,
                "orientation": orientation,
                "timestamp": datetime.now().isoformat(),
                "animation": {
                    "type": "mode_transition",
                    "duration": 800,
                    "easing": "ease-in-out"
                }
            }
        }, session_id)
        
        log.info(f"📡 Broadcasted mode change {old_mode} → {new_mode} for session {session_id}")
    
    async def broadcast_orientation_flip(self, session_id: str, old_orientation: str, new_orientation: str, mode: str):
        """Broadcast orientation flip to subscribed sessions"""
        if session_id not in self.session_subscriptions:
            return
        
        if not self.session_subscriptions[session_id].get("orientation_flips", False):
            return
        
        await manager.send_personal_message({
            "type": "qdpi_orientation_flipped",
            "data": {
                "session_id": session_id,
                "old_orientation": old_orientation,
                "new_orientation": new_orientation,
                "mode": mode,
                "timestamp": datetime.now().isoformat(),
                "animation": {
                    "type": "flip_animation",
                    "duration": 600,
                    "easing": "cubic-bezier(0.175, 0.885, 0.32, 1.275)",
                    "rotation_degrees": 180
                }
            }
        }, session_id)
        
        log.info(f"🔄 Broadcasted orientation flip {old_orientation} → {new_orientation} for session {session_id}")
    
    async def broadcast_symbol_activation(self, session_id: str, symbol_data: Dict[str, Any]):
        """Broadcast symbol activation to subscribed sessions"""
        if session_id not in self.session_subscriptions:
            return
        
        if not self.session_subscriptions[session_id].get("symbol_activations", False):
            return
        
        await manager.send_personal_message({
            "type": "qdpi_symbol_activated",
            "data": {
                "session_id": session_id,
                "symbol": symbol_data,
                "timestamp": datetime.now().isoformat(),
                "animation": {
                    "type": "symbol_highlight",
                    "duration": 400,
                    "glow_color": "#00ff88",
                    "pulse_count": 2
                }
            }
        }, session_id)
        
        log.info(f"✨ Broadcasted symbol activation {symbol_data['name']} for session {session_id}")
    
    async def broadcast_flow_execution(self, session_id: str, symbol_name: str, flow_results: Dict[str, Any]):
        """Broadcast flow execution results to subscribed sessions"""
        if session_id not in self.session_subscriptions:
            return
        
        if not self.session_subscriptions[session_id].get("flow_executions", False):
            return
        
        await manager.send_personal_message({
            "type": "qdpi_flow_executed",
            "data": {
                "session_id": session_id,
                "symbol_name": symbol_name,
                "flow_results": flow_results,
                "timestamp": datetime.now().isoformat(),
                "animation": {
                    "type": "flow_cascade",
                    "duration": 1000,
                    "effect": "ripple",
                    "color": "#ff6b00"
                }
            }
        }, session_id)
        
        log.info(f"⚡ Broadcasted flow execution for {symbol_name} in session {session_id}")
    
    async def broadcast_search_results(self, session_id: str, query: str, results: Dict[str, Any]):
        """Broadcast search results to subscribed sessions"""
        if session_id not in self.session_subscriptions:
            return
        
        if not self.session_subscriptions[session_id].get("search_results", False):
            return
        
        await manager.send_personal_message({
            "type": "qdpi_search_results",
            "data": {
                "session_id": session_id,
                "query": query,
                "results": results,
                "timestamp": datetime.now().isoformat(),
                "animation": {
                    "type": "search_highlight",
                    "duration": 300,
                    "stagger_delay": 100
                }
            }
        }, session_id)
        
        log.info(f"🔍 Broadcasted search results for '{query}' in session {session_id}")
    
    async def broadcast_symbol_sequence(self, session_id: str, symbols: list, context: Dict[str, Any]):
        """Broadcast symbol sequence encoding/decoding"""
        if session_id not in self.session_subscriptions:
            return
        
        await manager.send_personal_message({
            "type": "qdpi_symbol_sequence",
            "data": {
                "session_id": session_id,
                "symbols": symbols,
                "context": context,
                "timestamp": datetime.now().isoformat(),
                "animation": {
                    "type": "sequence_flow",
                    "duration": 1200,
                    "direction": "left_to_right",
                    "stagger_delay": 150
                }
            }
        }, session_id)
        
        log.info(f"📝 Broadcasted symbol sequence ({len(symbols)} symbols) for session {session_id}")
    
    async def broadcast_context_update(self, session_id: str, context_changes: Dict[str, Any]):
        """Broadcast context updates to subscribed sessions"""
        if session_id not in self.session_subscriptions:
            return
        
        await manager.send_personal_message({
            "type": "qdpi_context_updated",
            "data": {
                "session_id": session_id,
                "context_changes": context_changes,
                "timestamp": datetime.now().isoformat()
            }
        }, session_id)
        
        log.info(f"📊 Broadcasted context update for session {session_id}")

# Global QDPI WebSocket manager instance
qdpi_ws = QDPIWebSocketManager()

# WebSocket message handlers for QDPI events
async def handle_qdpi_subscribe(session_id: str, data: Dict[str, Any]):
    """Handle QDPI subscription request"""
    events = data.get("events", {})
    await qdpi_ws.subscribe_session(session_id, events)

async def handle_qdpi_unsubscribe(session_id: str, data: Dict[str, Any]):
    """Handle QDPI unsubscription request"""
    await qdpi_ws.unsubscribe_session(session_id)

async def handle_qdpi_mode_change(session_id: str, data: Dict[str, Any]):
    """Handle QDPI mode change request"""
    try:
        mode = data.get("mode", "read").lower()
        orientation = data.get("orientation")
        
        # Get current state
        current_mode = qdpi_engine.current_state.mode.value
        current_orientation = qdpi_engine.current_state.orientation.value
        
        # Update mode
        if mode != current_mode:
            qdpi_engine.set_mode(QDPIMode(mode))
            await qdpi_ws.broadcast_mode_change(session_id, current_mode, mode, current_orientation)
        
        # Update orientation if provided
        if orientation and orientation != current_orientation:
            qdpi_engine.flip_orientation()
            new_orientation = qdpi_engine.current_state.orientation.value
            await qdpi_ws.broadcast_orientation_flip(session_id, current_orientation, new_orientation, mode)
        
    except Exception as e:
        await manager.send_error(session_id, f"QDPI mode change failed: {str(e)}", "QDPI_MODE_ERROR")

async def handle_qdpi_symbol_execute(session_id: str, data: Dict[str, Any]):
    """Handle QDPI symbol execution request"""
    try:
        symbol_name = data.get("symbol_name")
        context = data.get("context", {})
        
        if not symbol_name:
            await manager.send_error(session_id, "Symbol name required", "QDPI_SYMBOL_ERROR")
            return
        
        # Get symbol
        symbol = qdpi_engine.codex.get_symbol_by_name(symbol_name)
        if not symbol:
            await manager.send_error(session_id, f"Symbol not found: {symbol_name}", "QDPI_SYMBOL_ERROR")
            return
        
        # Broadcast symbol activation
        await qdpi_ws.broadcast_symbol_activation(session_id, symbol.to_dict())
        
        # Execute flows
        flow_results = await qdpi_flows.execute_symbol_flow(symbol, context)
        
        # Broadcast flow execution
        await qdpi_ws.broadcast_flow_execution(session_id, symbol_name, flow_results)
        
    except Exception as e:
        await manager.send_error(session_id, f"QDPI symbol execution failed: {str(e)}", "QDPI_EXECUTION_ERROR")

async def handle_qdpi_search(session_id: str, data: Dict[str, Any]):
    """Handle QDPI semantic search request"""
    try:
        query = data.get("query")
        limit = data.get("limit", 5)
        
        if not query:
            await manager.send_error(session_id, "Search query required", "QDPI_SEARCH_ERROR")
            return
        
        # Perform search
        results = qdpi_engine.semantic_search(query, limit)
        
        # Broadcast results
        await qdpi_ws.broadcast_search_results(session_id, query, results)
        
    except Exception as e:
        await manager.send_error(session_id, f"QDPI search failed: {str(e)}", "QDPI_SEARCH_ERROR")

# Register WebSocket message handlers
QDPI_WS_HANDLERS = {
    "qdpi_subscribe": handle_qdpi_subscribe,
    "qdpi_unsubscribe": handle_qdpi_unsubscribe,
    "qdpi_mode_change": handle_qdpi_mode_change,
    "qdpi_symbol_execute": handle_qdpi_symbol_execute,
    "qdpi_search": handle_qdpi_search
}