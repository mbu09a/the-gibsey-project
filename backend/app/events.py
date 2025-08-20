"""Event bus for real-time QDPI events with WebSocket and SSE support"""

import asyncio
import json
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Set, Optional, AsyncIterator
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Event:
    """Structured event for the QDPI system"""
    event_id: str
    type: str
    timestamp: str
    session_id: str
    payload: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "type": self.type,
            "ts": self.timestamp,
            "session_id": self.session_id,
            "payload": self.payload
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())

class EventBus:
    """In-memory event bus with session filtering and broadcast capabilities"""
    
    def __init__(self, max_queue_size: int = 1024):
        self._queues: Set[asyncio.Queue] = set()
        self._session_queues: Dict[str, Set[asyncio.Queue]] = {}
        self._max_queue_size = max_queue_size
        self._event_count = 0
        
    def subscribe(self, session_id: Optional[str] = None) -> asyncio.Queue:
        """Subscribe to events, optionally filtered by session_id"""
        queue = asyncio.Queue(maxsize=self._max_queue_size)
        
        # Add to global queue list
        self._queues.add(queue)
        
        # Add to session-specific queue list if session_id provided
        if session_id:
            if session_id not in self._session_queues:
                self._session_queues[session_id] = set()
            self._session_queues[session_id].add(queue)
            
        logger.debug(f"Client subscribed to events (session: {session_id or 'all'})")
        return queue
    
    def unsubscribe(self, queue: asyncio.Queue, session_id: Optional[str] = None):
        """Unsubscribe from events"""
        self._queues.discard(queue)
        
        if session_id and session_id in self._session_queues:
            self._session_queues[session_id].discard(queue)
            if not self._session_queues[session_id]:
                del self._session_queues[session_id]
                
        logger.debug(f"Client unsubscribed from events (session: {session_id or 'all'})")
    
    async def publish(self, event: Event):
        """Publish event to all relevant subscribers"""
        self._event_count += 1
        
        # Get all queues that should receive this event
        target_queues = set()
        
        # Session-specific queues
        if event.session_id in self._session_queues:
            target_queues.update(self._session_queues[event.session_id])
        
        # Broadcast to all queues (they can filter client-side if needed)
        target_queues.update(self._queues)
        
        # Publish to all target queues
        successful = 0
        dropped = 0
        
        for queue in list(target_queues):  # Convert to list to avoid modification during iteration
            try:
                queue.put_nowait(event)
                successful += 1
            except asyncio.QueueFull:
                # Drop events for slow consumers
                dropped += 1
                logger.warning(f"Dropped event {event.event_id} for slow consumer")
            except Exception as e:
                logger.error(f"Error publishing event {event.event_id}: {e}")
                
        logger.info(f"Published event {event.type} to {successful} clients, dropped {dropped}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get bus statistics"""
        return {
            "total_subscribers": len(self._queues),
            "session_count": len(self._session_queues),
            "events_published": self._event_count,
            "active_sessions": list(self._session_queues.keys())
        }

# Global event bus instance
BUS = EventBus()

def make_event(event_type: str, session_id: str, payload: Dict[str, Any]) -> Event:
    """Create a structured event"""
    return Event(
        event_id=str(uuid.uuid4()),
        type=event_type,
        timestamp=datetime.utcnow().isoformat() + "Z",
        session_id=session_id,
        payload=payload
    )

async def publish_page_generated(session_id: str, page_data: Dict[str, Any]):
    """Publish a page generation completion event"""
    event = make_event("gibsey.generate.page.done", session_id, page_data)
    await BUS.publish(event)

async def publish_symbol_interaction(session_id: str, symbol_code: int, action: str):
    """Publish a symbol interaction event"""
    payload = {
        "symbol_code": symbol_code,
        "action": action,
        "char_hex": (symbol_code >> 4) & 0xF,
        "behavior": symbol_code & 0xF
    }
    event = make_event("gibsey.ui.symbol", session_id, payload)
    await BUS.publish(event)

async def publish_pipeline_error(session_id: str, error: str, symbol_code: Optional[int] = None):
    """Publish a pipeline error event"""
    payload = {
        "error": error,
        "symbol_code": symbol_code
    }
    event = make_event("gibsey.pipeline.error", session_id, payload)
    await BUS.publish(event)