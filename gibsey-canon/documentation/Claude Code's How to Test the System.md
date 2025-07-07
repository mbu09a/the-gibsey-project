 Generated 7/7/2025 by Claude Code on how to test the current system
 
 🚀 Step 1: Start Both Servers

  Terminal 1 - Backend QDPI Server:

  cd /Users/ghostradongus/the-gibsey-project/backend
  python main_qdpi.py
  Wait for: "Uvicorn running on http://0.0.0.0:8000"

  Terminal 2 - Frontend Server:

  cd /Users/ghostradongus/the-gibsey-project
  npm run dev
  Wait for: "Local: http://localhost:5173/"

  🧪 Step 2: Basic Functionality Tests

  Test 1: API Endpoints

  # Test QDPI encoding
  curl -X POST http://localhost:8000/api/qdpi/qdpi/encode \
    -H "Content-Type: application/json" \
    -d '{"data": "Hello QDPI Integration"}'

  # Test WebSocket health
  curl http://localhost:8000/api/health

  Test 2: Main Interface

  1. Visit: http://localhost:5173/
  2. Look for:
    - Green "◯ QDPI-256" button in header
    - Green "● CLEAN" ECC signal widget (top right)
    - Story symbols in sidebar

  Test 3: QDPI Demo Interface

  1. Visit: http://localhost:5173/qdpi
  2. Expected: Full QDPI demo interface with:
    - WebSocket connection status indicator
    - Demo examples panel
    - Activity log section
    - Connection status: "connected"

  🎯 Step 3: End-to-End Integration Tests

  Test A: Symbol Click → QDPI Flow

  1. Navigate to: http://localhost:5173/ (main story)
  2. Open browser console (F12 → Console tab)
  3. Click any symbol in the left sidebar (Table of Contents)
  4. Expected console output:
  QDPI Flow Result: {success: true, data: {...}}
  QDPI Encode Result: {success: true, data: {...}}

  Test B: QDPI Demo Functionality

  1. Go to: http://localhost:5173/qdpi
  2. Check WebSocket status: Should show green dot + "connected"
  3. Click "Execute Demo" button
  4. Expected: Activity log shows timestamped events
  5. Try different demo examples from dropdown

  Test C: Error Correction Demo

  # Test Reed-Solomon correction (should show yellow status)
  curl -X POST http://localhost:8000/api/qdpi/qdpi/ecc/encode \
    -H "Content-Type: application/json" \
    -d '{"description": "Test message", "symbol_sequence": 
  [1,2,3,4,5]}'

  🔍 Step 4: Visual Verification Tests

  Test 1: ECC Signal Widget

  - Location: Top right of main interface header
  - States to verify:
    - 🟢 "● CLEAN" (normal state)
    - 🟡 "◐ RS-N" (when errors corrected)
    - 🔴 "◯ ERROR" (uncorrectable)

  Test 2: Symbol Hover Effects

  1. Hover over symbols in story interface
  2. Expected: Symbols should scale up slightly when QDPI is enabled
  3. Click symbols should trigger QDPI flows (check console)

  Test 3: WebSocket Real-Time Updates

  4. Open two browser tabs: Both at http://localhost:5173/qdpi
  5. In tab 1: Click "Execute Demo"
  6. In tab 2: Should see activity log update in real-time
  7. Expected: Live synchronization between tabs

  🐛 Step 5: Error Scenarios

  Test 1: Backend Offline

  8. Stop backend server (Ctrl+C in Terminal 1)
  9. Refresh QDPI demo page
  10. Expected: WebSocket status shows "disconnected" (red dot)

  Test 2: WebSocket Reconnection

  11. Restart backend server
  12. Wait 3 seconds
  13. Expected: WebSocket auto-reconnects (green dot returns)

  Test 3: Invalid API Calls

  # Should return error gracefully
  curl -X POST http://localhost:8000/api/qdpi/qdpi/encode \
    -H "Content-Type: application/json" \
    -d '{"invalid": "data"}'

  📊 Step 6: Performance Verification

  Test 1: Encoding Speed

  time curl -X POST http://localhost:8000/api/qdpi/qdpi/encode \
    -H "Content-Type: application/json" \
    -d '{"data": "Performance test message"}'
  Expected: <100ms response time

  Test 2: WebSocket Latency

  14. Open browser console on QDPI demo page
  15. Monitor network tab for WebSocket messages
  16. Click Execute Demo
  17. Expected: <10ms message roundtrip

  🎉 Success Criteria

  ✅ All tests pass if you see:
  - Backend API responding with encoded symbol sequences
  - Frontend displaying QDPI interface correctly
  - WebSocket showing "connected" status
  - Symbol clicks generating console output
  - ECC signal widget showing "CLEAN" status
  - Real-time activity logs updating
  - Smooth navigation between / and /qdpi routes

  🚨 Troubleshooting

  Frontend won't start:

  npm install
  npm run dev

  Backend errors:

  cd backend
  pip install fastapi uvicorn cassandra-driver aiohttp python-dotenv
  python main_qdpi.py

  WebSocket connection fails:

  - Check both servers are running
  - Verify ports 5173 and 8000 are available
  - Check browser console for CORS errors

  Ready to test? Start with Step 1 and work through each section! 🚀