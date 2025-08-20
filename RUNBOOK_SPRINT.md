# QDPI Backend Sprint Runbook

Commands and endpoints for the manifest + events handshake delivered in this sprint.

## Quick Start

### 1. Environment Setup
```bash
# Ensure manifest exists
export QDPI_GLYPH_MANIFEST_PATH=public/qdpi_glyph_manifest.json
export KAFKA_ENABLED=false

# Generate stub manifest if needed
python scripts/build_qdpi_manifest.py --stub
```

### 2. Start Backend
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Test Integration
```bash
# Test all new endpoints
python test_integration.py

# Individual tests
python -m pytest tests/test_manifest_api.py -v
python -m pytest tests/test_run_symbol_events.py::TestRunSymbolWithEvents::test_run_symbol_basic -v
```

## New API Endpoints

### Manifest & Characters
```bash
# Get 256-glyph manifest with validation
curl http://localhost:8000/api/v1/qdpi/manifest

# Get 16 characters with colors
curl http://localhost:8000/api/v1/qdpi/characters

# Validate current manifest
curl http://localhost:8000/api/v1/qdpi/manifest/validate
```

### Pipeline with Events
```bash
# Execute symbol with session tracking
curl -X POST "http://localhost:8000/api/v1/pipeline/run/symbol/0x00" \
  -H "Content-Type: application/json" \
  -d '{"session_id":"ui-session","user_intent":"test"}'

# Response includes page_id and emits real-time event
```

### Event Streaming
```bash
# Server-Sent Events (SSE)
curl -N "http://localhost:8000/api/v1/events/stream?session_id=ui-session"

# WebSocket endpoint
ws://localhost:8000/api/v1/ws/events?session_id=ui-session

# Event bus stats
curl http://localhost:8000/api/v1/events/stats

# Send test event
curl -X POST "http://localhost:8000/api/v1/events/test?session_id=ui-session&event_type=test"
```

## Event Schema

All events follow this JSON structure:
```json
{
  "event_id": "uuid",
  "type": "gibsey.generate.page.done",
  "ts": "2025-08-19T02:17:59Z",
  "session_id": "ui-session",
  "payload": {
    "page_id": "P00-00-a1b2c3d4",
    "symbol_code": 0,
    "char_hex": 0,
    "behavior": 0,
    "trajectory": "T0",
    "character": "an author",
    "notation": "an author:XC",
    "edges": {"next_within": "page-001-next"},
    "text_excerpt": "First 140 characters of generated page...",
    "validation": {"character_consistency": true},
    "index_signals": {"novelty": 0.7, "coherence": 0.8}
  }
}
```

## UI Integration Guide

### 1. Fetch Manifest
```javascript
// Get 256 glyphs with colors
const manifest = await fetch('/api/v1/qdpi/manifest').then(r => r.json());
const characters = await fetch('/api/v1/qdpi/characters').then(r => r.json());

// Use manifest.glyphs for symbol grid
// Use characters for color mapping
```

### 2. Open Event Stream
```javascript
// SSE connection
const eventSource = new EventSource(`/api/v1/events/stream?session_id=${sessionId}`);
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'gibsey.generate.page.done') {
    displayGeneratedPage(data.payload);
  }
};

// OR WebSocket connection
const ws = new WebSocket(`ws://localhost:8000/api/v1/ws/events?session_id=${sessionId}`);
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  handleRealtimeEvent(data);
};
```

### 3. Execute Symbol
```javascript
// Click symbol → generate page → receive event
const response = await fetch(`/api/v1/pipeline/run/symbol/0x${code.toString(16).padStart(2, '0')}`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    session_id: sessionId,
    user_intent: 'continue reading'
  })
});

const result = await response.json();
// HTTP response AND real-time event will both contain page data
```

## Kafka Configuration

### Enable Kafka (Optional)
```bash
# Set environment variables
export KAFKA_ENABLED=true
export KAFKA_BROKERS=localhost:9092

# Topics will be auto-used:
# - gibsey.ui.symbol
# - gibsey.generate.page.request  
# - gibsey.generate.page.done

# Same event payload schema for Kafka and in-memory bus
```

## Static Assets

### Glyph Files
- Backend serves: `/qdpi-256-glyphs/` (if directory exists)
- Manifest URLs point to: `/qdpi-256-glyphs/an_author.svg`
- Fallback: Frontend can serve these from `public/`

### CORS Headers
- Vite dev server: `http://localhost:5173` ✅
- React dev server: `http://localhost:3000` ✅ 
- Expose headers: `ETag`, `X-Manifest-Type`

## Testing

### Unit Tests
```bash
# Manifest validation
python -m pytest tests/test_manifest_api.py -v

# Event bus & streaming
python -m pytest tests/test_events_stream.py -v

# Pipeline with events
python -m pytest tests/test_run_symbol_events.py -v
```

### Integration Test
```bash
# Full end-to-end test
python test_integration.py
```

### Manual Testing
```bash
# 1. Start backend
uvicorn backend.main:app --reload

# 2. Open SSE stream (terminal 1)
curl -N "http://localhost:8000/api/v1/events/stream?session_id=test"

# 3. Execute symbol (terminal 2)
curl -X POST "http://localhost:8000/api/v1/pipeline/run/symbol/0x4C" \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test","user_intent":"test"}'

# 4. Observe event in terminal 1:
# data: {"event_id":"...","type":"gibsey.generate.page.done",...}
```

## Definition of Done ✅

All deliverables completed:

- ✅ `GET /api/v1/qdpi/manifest` returns validated 256-entry manifest (+ETag)
- ✅ `GET /api/v1/qdpi/characters` returns 16 characters with colors  
- ✅ `GET /api/v1/events/stream?session_id=…` (SSE) streams events
- ✅ `WS /api/v1/ws/events?session_id=…` mirrors same event feed
- ✅ `POST /api/v1/pipeline/run/symbol/{code}` accepts `{session_id,...}` and emits events
- ✅ Kafka bridge works with same payload schema (toggleable)
- ✅ CORS allows Vite dev origin; static assets served
- ✅ Tests cover manifest validation, SSE/WS handshake, pipeline→event emission

## Next Phase Handoff

**Ready for Gemini UI Development:**
1. Manifest API provides all 256 symbol mappings with colors
2. Event streams deliver real-time page generation notifications  
3. Pipeline API accepts symbol clicks and returns structured responses
4. CORS configured for local development
5. Test coverage validates all integration points

The backend now provides a **stable manifest + events handshake** that the UI can consume reliably. 🚀