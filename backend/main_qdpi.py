#!/usr/bin/env python3
"""
QDPI Integration Server
FastAPI server with QDPI endpoints and WebSocket support
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import json
import asyncio
from typing import Dict, List
import uvicorn

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Import QDPI APIs
from app.api.qdpi_ecc_endpoints import router as qdpi_ecc_router
from app.api.qdpi import router as qdpi_router
from app.api.qdpi_ux import router as qdpi_ux_router

# Create FastAPI app
app = FastAPI(
    title="QDPI Integration Server",
    description="Quaternary Data Protocol Interface with ECC and WebSocket support",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include QDPI routers
app.include_router(qdpi_ecc_router, prefix="/api/qdpi")
app.include_router(qdpi_router, prefix="/api/qdpi")
app.include_router(qdpi_ux_router, prefix="/api/qdpi")

# WebSocket connection manager
class QDPIConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_data: Dict[WebSocket, dict] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_data[websocket] = {
            "session_id": session_id,
            "subscriptions": {
                "mode_changes": True,
                "orientation_flips": True,
                "symbol_activations": True,
                "flow_executions": True,
                "search_results": True,
                "ecc_status": True
            }
        }

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.connection_data:
            del self.connection_data[websocket]

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_text(json.dumps(message))
        except:
            self.disconnect(websocket)

    async def broadcast(self, message: dict):
        if self.active_connections:
            disconnected = []
            for connection in self.active_connections:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    disconnected.append(connection)
            
            # Clean up disconnected clients
            for connection in disconnected:
                self.disconnect(connection)

    async def broadcast_qdpi_event(self, event_type: str, data: dict):
        message = {
            "type": f"qdpi_{event_type}",
            "data": data,
            "timestamp": data.get("timestamp") or asyncio.get_event_loop().time()
        }
        await self.broadcast(message)

manager = QDPIConnectionManager()

@app.websocket("/ws/qdpi/{session_id}")
async def qdpi_websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    
    # Send initial confirmation
    await manager.send_personal_message({
        "type": "qdpi_connection_established",
        "data": {
            "session_id": session_id,
            "timestamp": asyncio.get_event_loop().time()
        }
    }, websocket)
    
    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "qdpi_subscribe":
                # Update subscription preferences
                subscriptions = message.get("data", {}).get("events", {})
                if websocket in manager.connection_data:
                    manager.connection_data[websocket]["subscriptions"].update(subscriptions)
                
                await manager.send_personal_message({
                    "type": "qdpi_subscription_confirmed",
                    "data": {
                        "subscriptions": manager.connection_data[websocket]["subscriptions"],
                        "session_id": session_id
                    }
                }, websocket)
            
            elif message.get("type") == "qdpi_encode_request":
                # Handle encoding request
                content = message.get("data", {}).get("content", "")
                
                # Broadcast encoding event
                await manager.broadcast_qdpi_event("encoding_started", {
                    "content": content,
                    "session_id": session_id
                })
                
                # Simulate encoding process (in real implementation, call QDPI encoder)
                await asyncio.sleep(0.1)  # Simulate processing time
                
                # Broadcast encoded result
                await manager.broadcast_qdpi_event("content_encoded", {
                    "original_content": content,
                    "glyph_sequence": f"QDPI_{len(content)}_GLYPHS",
                    "session_id": session_id,
                    "ecc_status": "clean"
                })
            
            elif message.get("type") == "qdpi_symbol_clicked":
                # Handle symbol click
                symbol_data = message.get("data", {})
                
                await manager.broadcast_qdpi_event("symbol_activated", {
                    "symbol": symbol_data,
                    "session_id": session_id
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "QDPI Integration Server",
        "version": "1.0.0", 
        "status": "online",
        "endpoints": {
            "docs": "/api/docs",
            "qdpi_ecc": "/api/qdpi/",
            "websocket": "/ws/qdpi/{session_id}"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "websocket_connections": len(manager.active_connections),
        "qdpi_available": True
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)