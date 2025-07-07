import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/qdpi/test-session"
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket")
            
            # Subscribe to events
            await websocket.send(json.dumps({
                "type": "qdpi_subscribe", 
                "data": {"events": {"symbol_activations": True}}
            }))
            
            # Receive confirmation
            response = await websocket.recv()
            print("📨 Response:", response)
            
            # Test symbol click
            await websocket.send(json.dumps({
                "type": "qdpi_symbol_clicked",
                "data": {"symbol_id": "london-fox"}
            }))
            
            print("✅ WebSocket test complete")
            
    except Exception as e:
        print("❌ WebSocket error:", e)

asyncio.run(test_websocket())
