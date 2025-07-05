"""
Main FastAPI application for the Gibsey Mycelial Network
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import json
from typing import Optional
import uuid

from app.api import pages, prompts, users, vector_search, retrieval, ask, symbols, symbol_search, qdpi, qdpi_ux, glyph_marrow_api
from app.websocket import manager, mock_stream_ai_response, stream_character_response
from app.qdpi_websocket import QDPI_WS_HANDLERS
from app.database import get_database, close_database
from app.models import WebSocketMessage
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Gibsey Mycelial Network API",
    description="Backend API for the AI-powered narrative OS",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "http://localhost:8080",  # Alternative dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(pages.router)
app.include_router(prompts.router)
app.include_router(users.router)
app.include_router(vector_search.router)
app.include_router(retrieval.router)
app.include_router(ask.router)
app.include_router(symbols.router)
app.include_router(symbol_search.router)
app.include_router(qdpi.router)
app.include_router(qdpi_ux.router)
app.include_router(glyph_marrow_api.router)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Gibsey Mycelial Network API",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "docs": "/api/docs",
            "websocket": "/ws/{session_id}",
            "pages": "/api/v1/pages",
            "prompts": "/api/v1/prompts", 
            "users": "/api/v1/users",
            "search": "/api/v1/search",
            "retrieval": "/api/v1/retrieval",
            "ask": "/api/v1/ask",
            "qdpi": "/qdpi",
            "qdpi_ux": "/api/v1/qdpi",
            "glyph_marrow": "/api/glyph-marrow"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint with real database status"""
    database_status = "unknown"
    database_type = "unknown"
    
    try:
        db = await get_database()
        database_url = os.getenv('DATABASE_URL', 'mock://localhost')
        
        if database_url.startswith('cassandra://'):
            database_type = "cassandra"
            # Try a simple operation to test connection
            await db.get_pages(skip=0, limit=1)
            database_status = "connected"
        else:
            database_type = "mock"
            database_status = "connected"
            
    except Exception as e:
        database_status = f"error: {str(e)}"
    
    return {
        "status": "healthy" if database_status == "connected" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "database": {
            "type": database_type,
            "status": database_status
        },
        "websocket_connections": len(manager.active_connections)
    }

@app.get("/api/v1/stats")
async def get_api_stats(db = Depends(get_database)):
    """Get API and database statistics"""
    # Get database stats (method varies by database type)
    database_stats = {}
    try:
        database_url = os.getenv('DATABASE_URL', 'mock://localhost')
        
        if database_url.startswith('cassandra://'):
            # For Cassandra, we'd need to query each table for counts
            # For now, return basic info
            pages = await db.get_pages(skip=0, limit=1000)
            database_stats = {
                "type": "cassandra",
                "pages": len(pages),
                "prompts": "N/A",  # TODO: Implement count queries
                "users": "N/A",
                "sessions": "N/A",
                "branches": "N/A",
                "motifs": "N/A"
            }
        else:
            # Mock database
            database_stats = {
                "type": "mock",
                "pages": len(db.pages),
                "prompts": len(db.prompts),
                "users": len(db.users),
                "sessions": len(db.sessions),
                "branches": len(db.branches),
                "motifs": len(db.motifs)
            }
    except Exception as e:
        database_stats = {"error": str(e)}
    
    return {
        "database": database_stats,
        "websocket": manager.get_connection_stats(),
        "version": "1.0.0"
    }

# WebSocket endpoint for real-time communication
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    session_id: str,
    user_id: Optional[str] = None
):
    """
    WebSocket endpoint for real-time updates
    Handles streaming AI responses, vault updates, and cluster events
    """
    await manager.connect(websocket, session_id, user_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            message_type = message.get("type")
            message_data = message.get("data", {})
            
            # Handle different message types
            if message_type == "ping":
                # Respond to ping with pong
                await manager.send_personal_message({
                    "type": "pong",
                    "data": {"timestamp": message_data.get("timestamp")}
                }, session_id)
            
            elif message_type == "ai_chat_request":
                # Handle AI chat request with streaming response
                prompt = message_data.get("prompt", "")
                character_id = message_data.get("character_id", "london-fox")
                current_page_id = message_data.get("current_page_id")
                
                # Use real LLM streaming with RAG
                await stream_character_response(session_id, prompt, character_id, current_page_id)
            
            elif message_type == "page_navigation":
                # Handle page navigation updates
                page_index = message_data.get("page_index", 0)
                await manager.send_vault_update({
                    "current_page_index": page_index,
                    "session_id": session_id
                }, session_id)
            
            elif message_type == "prompt_selection":
                # Handle prompt selection
                prompt_id = message_data.get("prompt_id")
                await manager.send_personal_message({
                    "type": "prompt_selected",
                    "data": {"prompt_id": prompt_id}
                }, session_id)
            
            elif message_type in QDPI_WS_HANDLERS:
                # Handle QDPI WebSocket messages
                handler = QDPI_WS_HANDLERS[message_type]
                await handler(session_id, message_data)
            
            else:
                # Unknown message type
                await manager.send_error(
                    session_id, 
                    f"Unknown message type: {message_type}",
                    "UNKNOWN_MESSAGE_TYPE"
                )
    
    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        print(f"WebSocket error for session {session_id}: {e}")
        await manager.send_error(session_id, str(e), "WEBSOCKET_ERROR")
        manager.disconnect(session_id)

# Simple test page for WebSocket
@app.get("/test-llm-debug") 
async def test_llm_debug():
    """Debug LLM service in server context"""
    try:
        from app.llm_service import get_llm_service, ChatMessage
        
        llm_service = get_llm_service()
        available = await llm_service.get_available_providers()
        
        # Test simple message
        messages = [ChatMessage(role="user", content="Hello")]
        response_tokens = []
        
        async for token in llm_service.chat_stream(messages):
            response_tokens.append(token.token)
            if len(response_tokens) >= 5 or token.is_complete:
                break
        
        return {
            "status": "success",
            "available_providers": available,
            "test_response": "".join(response_tokens),
            "token_count": len(response_tokens)
        }
    except Exception as e:
        import traceback
        return {
            "status": "error", 
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@app.get("/test")
async def get_test_page():
    """Simple test page for WebSocket functionality"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gibsey WebSocket Test</title>
    </head>
    <body>
        <h1>Gibsey Mycelial Network WebSocket Test</h1>
        <div id="messages"></div>
        <input type="text" id="messageInput" placeholder="Type a message...">
        <button onclick="sendMessage()">Send</button>
        <button onclick="connect()">Connect</button>
        <button onclick="disconnect()">Disconnect</button>
        
        <script>
            let ws = null;
            const messages = document.getElementById('messages');
            const sessionId = 'test-session-' + Math.random().toString(36).substr(2, 9);
            
            function connect() {
                ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);
                
                ws.onopen = function(event) {
                    addMessage('Connected to WebSocket');
                };
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    addMessage(`Received: ${JSON.stringify(data, null, 2)}`);
                };
                
                ws.onclose = function(event) {
                    addMessage('WebSocket connection closed');
                };
                
                ws.onerror = function(error) {
                    addMessage(`WebSocket error: ${error}`);
                };
            }
            
            function disconnect() {
                if (ws) {
                    ws.close();
                    ws = null;
                }
            }
            
            function sendMessage() {
                const input = document.getElementById('messageInput');
                if (ws && input.value) {
                    const message = {
                        type: 'ai_chat_request',
                        data: {
                            prompt: input.value,
                            character_id: 'london-fox'
                        }
                    };
                    ws.send(JSON.stringify(message));
                    addMessage(`Sent: ${input.value}`);
                    input.value = '';
                }
            }
            
            function addMessage(message) {
                const div = document.createElement('div');
                div.innerHTML = `<pre>${message}</pre>`;
                messages.appendChild(div);
                messages.scrollTop = messages.scrollHeight;
            }
            
            // Auto-connect on page load
            connect();
        </script>
    </body>
    </html>
    """)

# Event handlers for startup/shutdown
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("🚀 Gibsey Mycelial Network API starting up...")
    print("📊 Database: Mock (in-memory)")
    print("🔌 WebSocket: Ready for connections")
    print("📡 API Docs: http://localhost:8000/api/docs")
    print("🧪 Test Page: http://localhost:8000/test")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Gibsey Mycelial Network API shutting down...")
    
    # Close database connections
    try:
        await close_database()
        print("✅ Database connections closed")
    except Exception as e:
        print(f"⚠️ Error closing database: {e}")
    
    # TODO: Add cleanup for Kafka, etc.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)