"""
WebSocket manager for real-time updates in the Gibsey Mycelial Network
Handles streaming AI responses, vault updates, and cluster events
"""

from typing import Dict, List, Any, Optional
from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio
from datetime import datetime
import uuid
import logging

from app.models import WebSocketMessage

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        # Active connections by session/user
        self.active_connections: Dict[str, WebSocket] = {}
        # Connection metadata
        self.connection_metadata: Dict[str, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str, user_id: Optional[str] = None):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        self.connection_metadata[session_id] = {
            "user_id": user_id,
            "connected_at": datetime.utcnow(),
            "last_activity": datetime.utcnow()
        }
        
        # Send welcome message
        await self.send_personal_message({
            "type": "connection_established",
            "data": {
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        }, session_id)
    
    def disconnect(self, session_id: str):
        """Remove a WebSocket connection"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        if session_id in self.connection_metadata:
            del self.connection_metadata[session_id]
    
    async def send_personal_message(self, message: Dict[str, Any], session_id: str):
        """Send a message to a specific session"""
        if session_id in self.active_connections:
            try:
                websocket = self.active_connections[session_id]
                await websocket.send_text(json.dumps(message))
                
                # Update last activity
                if session_id in self.connection_metadata:
                    self.connection_metadata[session_id]["last_activity"] = datetime.utcnow()
            except Exception as e:
                print(f"Error sending message to {session_id}: {e}")
                # Connection might be dead, remove it
                self.disconnect(session_id)
    
    async def broadcast(self, message: Dict[str, Any]):
        """Send a message to all connected sessions"""
        if not self.active_connections:
            return
        
        disconnected_sessions = []
        for session_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                print(f"Error broadcasting to {session_id}: {e}")
                disconnected_sessions.append(session_id)
        
        # Clean up disconnected sessions
        for session_id in disconnected_sessions:
            self.disconnect(session_id)
    
    async def broadcast_to_users(self, message: Dict[str, Any], user_ids: List[str]):
        """Send a message to specific users (all their sessions)"""
        target_sessions = [
            session_id for session_id, metadata in self.connection_metadata.items()
            if metadata.get("user_id") in user_ids
        ]
        
        for session_id in target_sessions:
            await self.send_personal_message(message, session_id)
    
    # Event-specific message methods
    async def send_page_update(self, page_id: str, page_data: Dict[str, Any], session_id: Optional[str] = None):
        """Send page update notification"""
        message = {
            "type": "page_update",
            "data": {
                "page_id": page_id,
                "page_data": page_data,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        if session_id:
            await self.send_personal_message(message, session_id)
        else:
            await self.broadcast(message)
    
    async def send_vault_update(self, vault_data: Dict[str, Any], session_id: Optional[str] = None):
        """Send vault state update"""
        message = {
            "type": "vault_update",
            "data": {
                "vault_data": vault_data,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        if session_id:
            await self.send_personal_message(message, session_id)
        else:
            await self.broadcast(message)
    
    async def stream_ai_response(self, session_id: str, response_id: str, token: str, is_complete: bool = False):
        """Stream AI response tokens in real-time"""
        message = {
            "type": "ai_response_stream",
            "data": {
                "response_id": response_id,
                "token": token,
                "is_complete": is_complete,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        await self.send_personal_message(message, session_id)
    
    async def send_cluster_event(self, event_type: str, event_data: Dict[str, Any]):
        """Send cluster/infrastructure event"""
        message = {
            "type": "cluster_event",
            "data": {
                "event_type": event_type,
                "event_data": event_data,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        await self.broadcast(message)
    
    async def send_error(self, session_id: str, error_message: str, error_code: Optional[str] = None):
        """Send error message to specific session"""
        message = {
            "type": "error",
            "data": {
                "message": error_message,
                "code": error_code,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        await self.send_personal_message(message, session_id)
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get statistics about current connections"""
        return {
            "total_connections": len(self.active_connections),
            "connections": [
                {
                    "session_id": session_id,
                    "user_id": metadata.get("user_id"),
                    "connected_at": metadata.get("connected_at").isoformat() if metadata.get("connected_at") else None,
                    "last_activity": metadata.get("last_activity").isoformat() if metadata.get("last_activity") else None
                }
                for session_id, metadata in self.connection_metadata.items()
            ]
        }

# Global connection manager instance
manager = ConnectionManager()

# Real AI streaming functions (Phase 3)
async def stream_character_response(session_id: str, prompt: str, character_id: str, current_page_id: str = None):
    """
    Stream character response using appropriate service
    Uses specialized Jacklyn service for jacklyn-variance, RAG service for others
    """
    response_id = str(uuid.uuid4())
    
    try:
        logger.info(f"Streaming response for {character_id}: {prompt[:100]}...")
        logger.info(f"Character ID match check: '{character_id}' == 'jacklyn-variance': {character_id == 'jacklyn-variance'}")
        
        # Use specialized Jacklyn service for jacklyn-variance
        if character_id == "jacklyn-variance":
            from .jacklyn_service import get_jacklyn_service
            
            jacklyn_service = get_jacklyn_service()
            
            # Get conversation history from connection metadata if available
            conversation_history = []  # TODO: Implement conversation history storage
            
            # Stream response from Jacklyn service (includes full pipeline)
            async for token in jacklyn_service.generate_response(
                user_query=prompt,
                conversation_history=conversation_history,
                current_page_id=current_page_id,
                session_id=session_id
            ):
                # Stream token to user
                await manager.stream_ai_response(
                    session_id=session_id,
                    response_id=response_id,
                    token=token.token,
                    is_complete=token.is_complete
                )
                
                # Log completion metadata
                if token.is_complete and token.metadata:
                    logger.info(f"Jacklyn response completed: {token.metadata}")
                    break
        
        else:
            # Use standard RAG service for other characters
            from .rag_service import get_rag_service
            from .llm_service import ChatMessage
            from .moderation import get_moderator
            
            rag_service = get_rag_service()
            moderator = get_moderator()
            
            # Moderate user input first
            moderation_result = moderator.moderate_input(prompt, user_id=session_id)
            if not moderation_result.is_safe:
                logger.warning(f"Blocked unsafe input from {session_id}: {moderation_result.reason}")
                await manager.stream_ai_response(
                    session_id=session_id,
                    response_id=response_id,
                    token=f"I'm sorry, but I cannot process that request. ({moderation_result.reason})",
                    is_complete=True
                )
                return
            
            # Get conversation history from connection metadata if available
            conversation_history = []  # TODO: Implement conversation history storage
            
            # Collect full response for output moderation
            full_response = ""
            
            # Stream response from RAG service
            async for token in rag_service.get_character_response(
                character_id=character_id,
                user_query=prompt,
                conversation_history=conversation_history,
                current_page_id=current_page_id,
                stream=True
            ):
                # Accumulate response for moderation
                full_response += token.token
                
                # Stream token to user (before output moderation for responsiveness)
                await manager.stream_ai_response(
                    session_id=session_id,
                    response_id=response_id,
                    token=token.token,
                    is_complete=token.is_complete
                )
                
                # Break if response is complete
                if token.is_complete:
                    # Moderate the complete output (log only, don't block)
                    output_moderation = moderator.moderate_output(full_response, character_id=character_id)
                    if output_moderation.flagged_content:
                        logger.info(f"AI output from {character_id} flagged: {output_moderation.flagged_content}")
                    break
    
    except Exception as e:
        logger.error(f"Error in character response streaming: {e}")
        # Send error message
        await manager.stream_ai_response(
            session_id=session_id,
            response_id=response_id,
            token=f"I apologize, but I'm having trouble responding right now. ({str(e)[:50]})",
            is_complete=True
        )

# Keep mock function for fallback
async def mock_stream_ai_response(session_id: str, prompt: str, character_id: str):
    """Mock streaming AI response for development/fallback"""
    response_id = str(uuid.uuid4())
    
    # Mock response based on character
    responses = {
        "london-fox": "I must analyze this through my Synchromy-M.Y.S.S.T.E.R.Y framework...",
        "glyph-marrow": "The words... they taste like... waiting in queues...",
        "phillip-bafflemint": "Filing this under: requires further investigation.",
        "default": "Interesting perspective. Let me consider this..."
    }
    
    response_text = responses.get(character_id, responses["default"])
    words = response_text.split()
    
    # Stream word by word
    for i, word in enumerate(words):
        await manager.stream_ai_response(
            session_id=session_id,
            response_id=response_id,
            token=word + " ",
            is_complete=False
        )
        await asyncio.sleep(0.1)  # Simulate streaming delay
    
    # Send completion signal
    await manager.stream_ai_response(
        session_id=session_id,
        response_id=response_id,
        token="",
        is_complete=True
    )