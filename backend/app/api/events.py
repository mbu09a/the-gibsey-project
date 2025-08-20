"""Event streaming API endpoints (WebSocket + SSE)"""

import json
import logging
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import Optional

from ..events import BUS, Event

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["events"])

@router.get("/events/stream")
async def event_stream(
    request: Request,
    session_id: str = Query(..., description="Session ID to filter events")
):
    """
    Server-Sent Events (SSE) stream for real-time QDPI events.
    
    Streams events filtered by session_id to avoid cross-session leakage.
    """
    logger.info(f"SSE client connecting for session: {session_id}")
    
    # Subscribe to events for this session
    queue = BUS.subscribe(session_id)
    
    async def event_generator():
        try:
            # Send initial connection event
            yield f"data: {json.dumps({'type': 'connection', 'session_id': session_id})}\n\n"
            
            while True:
                # Check if client disconnected
                if await request.is_disconnected():
                    logger.info(f"SSE client disconnected: {session_id}")
                    break
                
                # Wait for next event
                try:
                    event: Event = await queue.get()
                    
                    # Only send events for this session
                    if event.session_id == session_id:
                        # Format as SSE
                        event_data = event.to_json()
                        yield f"data: {event_data}\n\n"
                        
                except Exception as e:
                    logger.error(f"Error in SSE stream for {session_id}: {e}")
                    break
                    
        except Exception as e:
            logger.error(f"SSE stream error for {session_id}: {e}")
        finally:
            # Clean up subscription
            BUS.unsubscribe(queue, session_id)
            logger.info(f"SSE stream closed for session: {session_id}")
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    )

@router.websocket("/ws/events")
async def websocket_events(
    websocket: WebSocket,
    session_id: str = Query(..., description="Session ID to filter events")
):
    """
    WebSocket endpoint for real-time QDPI events.
    
    Provides same event stream as SSE but over WebSocket protocol.
    """
    await websocket.accept()
    logger.info(f"WebSocket client connected for session: {session_id}")
    
    # Subscribe to events for this session
    queue = BUS.subscribe(session_id)
    
    try:
        # Send initial connection event
        await websocket.send_json({
            "type": "connection",
            "session_id": session_id,
            "status": "connected"
        })
        
        while True:
            # Wait for next event
            event: Event = await queue.get()
            
            # Only send events for this session
            if event.session_id == session_id:
                await websocket.send_json(event.to_dict())
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error for {session_id}: {e}")
        try:
            await websocket.close(code=1011, reason=f"Server error: {str(e)}")
        except:
            pass
    finally:
        # Clean up subscription
        BUS.unsubscribe(queue, session_id)
        logger.info(f"WebSocket closed for session: {session_id}")

@router.get("/events/stats")
async def get_event_stats():
    """
    Get event bus statistics for monitoring.
    
    Returns subscriber counts and other bus metrics.
    """
    try:
        stats = BUS.get_stats()
        return {
            "status": "healthy",
            "bus_stats": stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get event stats: {str(e)}"
        )

@router.post("/events/test")
async def test_event(
    session_id: str,
    event_type: str = "test.event",
    payload: dict = None
):
    """
    Send a test event for development/debugging.
    
    Useful for testing event streams without triggering full pipeline.
    """
    from ..events import make_event
    
    if payload is None:
        payload = {"message": "test event", "timestamp": "now"}
    
    event = make_event(event_type, session_id, payload)
    await BUS.publish(event)
    
    return {
        "status": "sent",
        "event_id": event.event_id,
        "type": event_type,
        "session_id": session_id
    }