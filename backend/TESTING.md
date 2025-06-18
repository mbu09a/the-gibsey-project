# 🧪 Testing Guide for Gibsey Cassandra Integration

## Quick Start Testing

### 1. Start Services

**Option A: Development Mode (Mock Database - Fast)**
```bash
cd backend
DATABASE_URL=mock://localhost docker-compose up --build api redis
```

**Option B: Production Mode (Cassandra - Full Features)**
```bash
cd backend
docker-compose up --build
# Wait 2-3 minutes for Cassandra initialization
```

### 2. Run Automated Tests

**Basic Shell Tests:**
```bash
./test_cassandra.sh
```

**Comprehensive Python Tests:**
```bash
# Install dependencies if needed
pip install requests websockets

# Run all tests
python test_api.py

# Or run specific test
python test_api.py health
python test_api.py create_page
python test_api.py websocket
```

### 3. Manual Browser Testing

1. **API Documentation**: http://localhost:8000/api/docs
   - Try out endpoints directly in the browser
   - Test CRUD operations interactively

2. **Health Check**: http://localhost:8000/health
   - Should show database type and connection status

3. **WebSocket Test Page**: http://localhost:8000/test
   - Send messages and see streaming responses

## What to Look For

### ✅ Success Indicators

**Mock Database Mode:**
- Health check shows `"type": "mock"`
- Pages load from JSON data
- All CRUD operations work
- Data resets on restart

**Cassandra Mode:**
- Health check shows `"type": "cassandra"`
- Data persists between restarts
- Can create and retrieve pages
- WebSocket streaming works

### ❌ Common Issues

**Issue: Services not responding**
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs cassandra
docker-compose logs stargate
docker-compose logs api
```

**Issue: Cassandra not ready**
- Wait 2-3 minutes after `docker-compose up`
- Check health: `docker-compose ps` (should show "healthy")

**Issue: Connection refused**
- Ensure ports 8000, 8082, 9042 are not in use
- Check firewall settings

## Detailed Test Scenarios

### 1. Database Connection Test
```bash
curl http://localhost:8000/health | jq .
```

Expected (Cassandra):
```json
{
  "status": "healthy",
  "database": {
    "type": "cassandra",
    "status": "connected"
  }
}
```

### 2. Page Creation and Retrieval
```bash
# Create a page
curl -X POST http://localhost:8000/api/v1/pages/ \
  -H "Content-Type: application/json" \
  -d '{
    "symbol_id": "london-fox",
    "text": "Test page from London Fox",
    "page_type": "ai_response",
    "rotation": 90
  }'

# Get all pages
curl http://localhost:8000/api/v1/pages/ | jq .
```

### 3. WebSocket Streaming Test
```javascript
// In browser console at http://localhost:8000/test
const ws = new WebSocket('ws://localhost:8000/ws/test-session');
ws.onmessage = (event) => console.log(JSON.parse(event.data));
ws.send(JSON.stringify({
  type: 'ai_chat_request',
  data: {
    prompt: 'Hello',
    character_id: 'london-fox'
  }
}));
```

### 4. Performance Check
```bash
# Time fetching 100 pages
time curl -s http://localhost:8000/api/v1/pages/?limit=100 > /dev/null
```

Expected:
- Mock DB: < 50ms
- Cassandra: < 200ms (after warm-up)

## Monitoring

### View Container Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f cassandra
docker-compose logs -f stargate
docker-compose logs -f api
```

### Check Cassandra Data
```bash
# Connect to Cassandra
docker exec -it gibsey-cassandra cqlsh

# In CQL shell
USE gibsey_network;
SELECT COUNT(*) FROM story_pages;
SELECT * FROM story_pages LIMIT 5;
```

### Check Stargate Health
```bash
curl http://localhost:8082/health
curl http://localhost:8082/v1/health
```

## Troubleshooting

### Reset Everything
```bash
# Stop all containers
docker-compose down -v

# Remove data volumes
docker volume rm backend_cassandra_data

# Rebuild from scratch
docker-compose up --build
```

### Test Cassandra Connection Directly
```python
from cassandra.cluster import Cluster

cluster = Cluster(['localhost'])
session = cluster.connect()
print("Connected to Cassandra!")
session.shutdown()
cluster.shutdown()
```

## Next Steps

Once all tests pass:

1. ✅ Mock database working → Development ready
2. ✅ Cassandra database working → Production ready
3. ✅ WebSocket streaming working → Real-time features ready
4. ✅ All tests passing → Ready for Phase 2 (Authentication/AI)

---

**Need help?** Check the logs first, then the troubleshooting section!