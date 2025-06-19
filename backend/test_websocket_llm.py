#!/usr/bin/env python3
"""
Test WebSocket LLM integration
Tests the full end-to-end streaming functionality
"""

import asyncio
import json
import websockets
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_websocket_llm():
    """Test WebSocket with real LLM streaming"""
    
    logger.info("🧪 Testing WebSocket LLM integration...")
    
    try:
        # Connect to WebSocket
        uri = "ws://localhost:8000/ws/test-session-llm"
        
        async with websockets.connect(uri) as websocket:
            logger.info("✅ Connected to WebSocket")
            
            # Wait for connection message
            connection_msg = await websocket.recv()
            logger.info(f"📨 Connection: {json.loads(connection_msg)['type']}")
            
            # Send AI chat request
            test_message = {
                "type": "ai_chat_request",
                "data": {
                    "prompt": "Hello London Fox, what makes consciousness unique?",
                    "character_id": "london-fox"
                }
            }
            
            await websocket.send(json.dumps(test_message))
            logger.info("📤 Sent AI chat request")
            
            # Receive streaming response
            token_count = 0
            full_response = ""
            
            while True:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                    data = json.loads(response)
                    
                    if data["type"] == "ai_response_stream":
                        token_count += 1
                        token = data["data"]["token"]
                        is_complete = data["data"]["is_complete"]
                        
                        full_response += token
                        
                        # Log first few tokens
                        if token_count <= 5:
                            logger.info(f"🤖 Token {token_count}: '{token}' (complete: {is_complete})")
                        
                        if is_complete:
                            logger.info(f"✅ Streaming complete! Received {token_count} tokens")
                            logger.info(f"📝 Response preview: {full_response[:100]}...")
                            break
                            
                except asyncio.TimeoutError:
                    logger.error("❌ Timeout waiting for response")
                    return False
                    
        return True
        
    except Exception as e:
        logger.error(f"❌ WebSocket test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run WebSocket test"""
    
    logger.info("🚀 Starting WebSocket LLM test...")
    
    # Test WebSocket integration
    success = await test_websocket_llm()
    
    if success:
        logger.info("🎉 WebSocket LLM integration test passed!")
        return True
    else:
        logger.error("❌ WebSocket LLM integration test failed")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)