#!/bin/bash
# Comprehensive test script for Cassandra integration

echo "🧪 Testing Gibsey Cassandra Integration..."
echo "========================================"

# Base URL
BASE_URL="http://localhost:8000"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test function
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local expected_status=$4
    local test_name=$5
    
    echo -e "\n${YELLOW}Testing: $test_name${NC}"
    echo "Method: $method"
    echo "Endpoint: $endpoint"
    
    if [ "$method" == "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$BASE_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" \
            -H "Content-Type: application/json" \
            -d "$data" \
            "$BASE_URL$endpoint")
    fi
    
    # Extract status code (last line)
    status_code=$(echo "$response" | tail -n 1)
    # Extract body (everything except last line)
    body=$(echo "$response" | sed '$d')
    
    if [ "$status_code" == "$expected_status" ]; then
        echo -e "${GREEN}✅ PASSED${NC} - Status: $status_code"
        echo "Response: $(echo $body | jq . 2>/dev/null || echo $body)"
    else
        echo -e "${RED}❌ FAILED${NC} - Expected: $expected_status, Got: $status_code"
        echo "Response: $body"
    fi
}

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# 1. Test Health Check
echo -e "\n${YELLOW}=== HEALTH CHECKS ===${NC}"
test_endpoint "GET" "/health" "" "200" "Health Check"

# 2. Test API Stats
test_endpoint "GET" "/api/v1/stats" "" "200" "API Statistics"

# 3. Test Pages Endpoints
echo -e "\n${YELLOW}=== STORY PAGES ===${NC}"

# Get all pages
test_endpoint "GET" "/api/v1/pages/?skip=0&limit=5" "" "200" "Get Pages (first 5)"

# Get pages by symbol
test_endpoint "GET" "/api/v1/pages/symbol/london-fox" "" "200" "Get London Fox Pages"

# Get specific page (assuming page_0 exists)
test_endpoint "GET" "/api/v1/pages/page_0" "" "200" "Get Specific Page"

# Create a new page
new_page_data='{
    "symbol_id": "london-fox",
    "text": "Test page created via API",
    "page_type": "ai_response",
    "rotation": 90
}'
test_endpoint "POST" "/api/v1/pages/" "$new_page_data" "200" "Create New Page"

# 4. Test User/Session Endpoints
echo -e "\n${YELLOW}=== USERS & SESSIONS ===${NC}"

# Create a test user
user_data='{
    "username": "test_user_'$(date +%s)'",
    "email": "test@gibsey.network"
}'
test_endpoint "POST" "/api/v1/users/" "$user_data" "200" "Create Test User"

# Create guest session
test_endpoint "POST" "/api/v1/users/sessions/guest" "" "200" "Create Guest Session"

# 5. Test Prompts
echo -e "\n${YELLOW}=== PROMPTS ===${NC}"

# Get prompts for a page
test_endpoint "GET" "/api/v1/prompts/page/page_0" "" "200" "Get Prompts for Page"

# 6. Test WebSocket Connection
echo -e "\n${YELLOW}=== WEBSOCKET TEST ===${NC}"
echo "Testing WebSocket connection..."

# Use Python for WebSocket test
python3 -c "
import asyncio
import websockets
import json

async def test_websocket():
    uri = 'ws://localhost:8000/ws/test-session-cassandra'
    try:
        async with websockets.connect(uri) as websocket:
            # Wait for connection message
            msg = await websocket.recv()
            data = json.loads(msg)
            if data['type'] == 'connection_established':
                print('✅ WebSocket connected successfully')
                print(f'   Session ID: {data[\"data\"][\"session_id\"]}')
                
                # Send a test message
                test_msg = json.dumps({
                    'type': 'ping',
                    'data': {'timestamp': 'test'}
                })
                await websocket.send(test_msg)
                
                # Wait for pong
                response = await websocket.recv()
                pong = json.loads(response)
                if pong['type'] == 'pong':
                    print('✅ WebSocket ping/pong successful')
            else:
                print('❌ Unexpected connection message:', data)
    except Exception as e:
        print(f'❌ WebSocket test failed: {e}')

asyncio.run(test_websocket())
" 2>/dev/null || echo "❌ WebSocket test requires Python websockets library"

# 7. Performance Test
echo -e "\n${YELLOW}=== PERFORMANCE CHECK ===${NC}"
echo "Testing response times..."

start_time=$(date +%s%N)
curl -s "$BASE_URL/api/v1/pages/?limit=100" > /dev/null
end_time=$(date +%s%N)
elapsed=$((($end_time - $start_time) / 1000000))
echo "Fetching 100 pages took: ${elapsed}ms"

# Summary
echo -e "\n${YELLOW}=== TEST SUMMARY ===${NC}"
echo "Check the results above for any failures."
echo "If all tests pass, Cassandra integration is working correctly!"
echo ""
echo "💡 Tips:"
echo "- Check docker-compose logs if services aren't responding"
echo "- Ensure DATABASE_URL=cassandra://cassandra:9042 is set"
echo "- Wait 2-3 minutes after docker-compose up for initialization"