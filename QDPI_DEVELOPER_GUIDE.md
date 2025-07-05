# QDPI Developer & Agent Integration Guide

## Overview

QDPI-256 (Quaternary Data Protocol Interface) is a symbolic machine language that transforms data into meaningful symbol sequences. This guide shows how developers and agents can programmatically interact with the QDPI system.

## API Endpoints

### Base URLs
- **Production**: `https://your-domain.com/api/v1/qdpi`
- **Development**: `http://localhost:8000/api/v1/qdpi`
- **WebSocket**: `ws://localhost:8000/ws/{session_id}`

### Authentication
Currently no authentication required for development. Session-based state management.

## Core API Operations

### 1. Session Management

#### Get Current QDPI State
```bash
curl -X GET "http://localhost:8000/api/v1/qdpi/mode/{session_id}"
```

#### Set QDPI Mode and Orientation
```bash
curl -X POST "http://localhost:8000/api/v1/qdpi/mode/{session_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "ask",
    "orientation": "u",
    "context": {"purpose": "seeking wisdom"}
  }'
```

**Available Modes:**
- `read` - Consuming & analyzing existing content
- `ask` - Querying & requesting information  
- `index` - Creating & cataloging new content
- `receive` - Accepting & processing incoming data

**Available Orientations:**
- `n` - Normal orientation
- `u` - Upside-down orientation

### 2. Data Encoding & Decoding

#### Encode Data into QDPI Symbols
```bash
curl -X POST "http://localhost:8000/api/v1/qdpi/encode/{session_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "data": "Hello Gibsey world!",
    "mode": "index",
    "execute_flows": true
  }'
```

#### Decode QDPI Symbols to Data
```bash
curl -X POST "http://localhost:8000/api/v1/qdpi/decode/{session_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol_names": ["london_fox", "an_author", "jacklyn_variance"]
  }'
```

### 3. Symbol Search & Discovery

#### Semantic Symbol Search
```bash
curl -X POST "http://localhost:8000/api/v1/qdpi/search/{session_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "wisdom and knowledge",
    "limit": 10,
    "mode_filter": "ask",
    "flow_type_filter": "narrative"
  }'
```

### 4. Flow Execution

#### Execute Symbol Flows
```bash
curl -X POST "http://localhost:8000/api/v1/qdpi/execute/{session_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol_name": "london_fox",
    "context": {
      "query": "search for patterns",
      "depth": "deep"
    },
    "save_to_history": true
  }'
```

### 5. History & Analytics

#### Get Session History
```bash
curl -X GET "http://localhost:8000/api/v1/qdpi/history/{session_id}?history_type=all&limit=50"
```

#### List Active Sessions
```bash
curl -X GET "http://localhost:8000/api/v1/qdpi/sessions?user_id=agent_001&limit=20"
```

## WebSocket Integration

### Real-Time QDPI Events

Connect to WebSocket and subscribe to QDPI events:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/my-session-id');

// Subscribe to QDPI events
ws.send(JSON.stringify({
  type: 'qdpi_subscribe',
  data: {
    events: {
      mode_changes: true,
      orientation_flips: true,
      symbol_activations: true,
      flow_executions: true,
      search_results: true
    }
  }
}));

// Handle QDPI events
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  
  switch (message.type) {
    case 'qdpi_mode_changed':
      console.log(`Mode changed: ${message.data.old_mode} → ${message.data.new_mode}`);
      break;
      
    case 'qdpi_orientation_flipped':
      console.log(`Orientation flipped: ${message.data.old_orientation} → ${message.data.new_orientation}`);
      break;
      
    case 'qdpi_symbol_activated':
      console.log(`Symbol activated: ${message.data.symbol.name}`);
      break;
      
    case 'qdpi_flow_executed':
      console.log(`Flows executed for: ${message.data.symbol_name}`);
      break;
  }
};
```

### Triggering QDPI Actions via WebSocket

```javascript
// Change mode
ws.send(JSON.stringify({
  type: 'qdpi_mode_change',
  data: { mode: 'ask', orientation: 'u' }
}));

// Execute symbol
ws.send(JSON.stringify({
  type: 'qdpi_symbol_execute',
  data: { 
    symbol_name: 'london_fox',
    context: { query: 'find patterns' }
  }
}));

// Search symbols
ws.send(JSON.stringify({
  type: 'qdpi_search',
  data: { query: 'wisdom', limit: 5 }
}));
```

## Example Scripts

### Python Agent Script

```python
#!/usr/bin/env python3
"""
QDPI Agent Integration Example
"""

import requests
import json
import asyncio
import websockets
import uuid

class QDPIAgent:
    def __init__(self, base_url="http://localhost:8000/api/v1/qdpi"):
        self.base_url = base_url
        self.session_id = f"agent-{uuid.uuid4().hex[:8]}"
        
    def set_mode(self, mode, orientation=None, context=None):
        """Set QDPI mode and orientation"""
        data = {"mode": mode}
        if orientation:
            data["orientation"] = orientation
        if context:
            data["context"] = context
            
        response = requests.post(
            f"{self.base_url}/mode/{self.session_id}",
            json=data
        )
        return response.json()
    
    def encode_data(self, data, execute_flows=False):
        """Encode data into QDPI symbols"""
        response = requests.post(
            f"{self.base_url}/encode/{self.session_id}",
            json={
                "data": data,
                "execute_flows": execute_flows
            }
        )
        return response.json()
    
    def search_symbols(self, query, limit=5):
        """Search for symbols semantically"""
        response = requests.post(
            f"{self.base_url}/search/{self.session_id}",
            json={
                "query": query,
                "limit": limit
            }
        )
        return response.json()
    
    def execute_symbol(self, symbol_name, context=None):
        """Execute flows for a symbol"""
        response = requests.post(
            f"{self.base_url}/execute/{self.session_id}",
            json={
                "symbol_name": symbol_name,
                "context": context or {}
            }
        )
        return response.json()

# Example usage
if __name__ == "__main__":
    agent = QDPIAgent()
    
    # Set mode to ASK
    print("Setting mode to ASK...")
    state = agent.set_mode("ask")
    print(f"Current mode: {state['mode']}")
    
    # Search for wisdom symbols
    print("\nSearching for wisdom symbols...")
    search_results = agent.search_symbols("wisdom and knowledge")
    for match in search_results['matches']:
        print(f"- {match['symbol']['name']}: {match['similarity']:.2f}")
    
    # Encode a question
    print("\nEncoding question...")
    encoded = agent.encode_data("What is the meaning of life?", execute_flows=True)
    print(f"Encoded into {len(encoded['encoded_symbols'])} symbols")
    
    # Execute specific symbol
    print("\nExecuting london_fox symbol...")
    result = agent.execute_symbol("london_fox", {"query": "search for meaning"})
    print(f"Executed {len(result['execution_result']['flows'])} flows")
```

### Node.js Agent Script

```javascript
// qdpi-agent.js
const axios = require('axios');
const WebSocket = require('ws');
const { v4: uuidv4 } = require('uuid');

class QDPIAgent {
    constructor(baseUrl = 'http://localhost:8000/api/v1/qdpi') {
        this.baseUrl = baseUrl;
        this.sessionId = `agent-${uuidv4().slice(0, 8)}`;
        this.ws = null;
    }
    
    async connectWebSocket() {
        return new Promise((resolve, reject) => {
            this.ws = new WebSocket(`ws://localhost:8000/ws/${this.sessionId}`);
            
            this.ws.on('open', () => {
                // Subscribe to QDPI events
                this.ws.send(JSON.stringify({
                    type: 'qdpi_subscribe',
                    data: { events: { mode_changes: true, flow_executions: true } }
                }));
                resolve();
            });
            
            this.ws.on('message', (data) => {
                const message = JSON.parse(data);
                if (message.type.startsWith('qdpi_')) {
                    console.log(`[WS] ${message.type}:`, message.data);
                }
            });
            
            this.ws.on('error', reject);
        });
    }
    
    async setMode(mode, orientation = null, context = null) {
        const data = { mode };
        if (orientation) data.orientation = orientation;
        if (context) data.context = context;
        
        const response = await axios.post(`${this.baseUrl}/mode/${this.sessionId}`, data);
        return response.data;
    }
    
    async encodeData(data, executeFlows = false) {
        const response = await axios.post(`${this.baseUrl}/encode/${this.sessionId}`, {
            data,
            execute_flows: executeFlows
        });
        return response.data;
    }
    
    async searchSymbols(query, limit = 5) {
        const response = await axios.post(`${this.baseUrl}/search/${this.sessionId}`, {
            query,
            limit
        });
        return response.data;
    }
    
    async executeSymbol(symbolName, context = {}) {
        const response = await axios.post(`${this.baseUrl}/execute/${this.sessionId}`, {
            symbol_name: symbolName,
            context
        });
        return response.data;
    }
}

// Example usage
async function main() {
    const agent = new QDPIAgent();
    
    // Connect WebSocket
    await agent.connectWebSocket();
    console.log('Connected to QDPI WebSocket');
    
    // Set mode to INDEX
    const state = await agent.setMode('index');
    console.log(`Mode set to: ${state.mode}`);
    
    // Search for narrative symbols
    const search = await agent.searchSymbols('story and narrative');
    console.log(`Found ${search.count} narrative symbols`);
    
    // Encode creative content
    const encoded = await agent.encodeData('Once upon a time in Gibsey...', true);
    console.log(`Encoded story into ${encoded.encoded_symbols.length} symbols`);
    
    // Execute author symbol
    const result = await agent.executeSymbol('an_author', { 
        story_type: 'fantasy', 
        mood: 'mysterious' 
    });
    console.log('Author flows executed:', result.execution_result.flows.length);
}

main().catch(console.error);
```

### Bash/cURL Integration Script

```bash
#!/bin/bash
# qdpi-agent.sh

BASE_URL="http://localhost:8000/api/v1/qdpi"
SESSION_ID="bash-agent-$(date +%s)"

echo "🤖 QDPI Bash Agent - Session: $SESSION_ID"

# Set mode to READ
echo "📖 Setting mode to READ..."
curl -s -X POST "$BASE_URL/mode/$SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{"mode": "read", "context": {"agent": "bash_script"}}' | jq '.mode'

# Search for analysis symbols  
echo "🔍 Searching for analysis symbols..."
curl -s -X POST "$BASE_URL/search/$SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{"query": "analysis and patterns", "limit": 3}' | jq '.matches[].symbol.name'

# Encode system status
echo "📝 Encoding system status..."
SYSTEM_STATUS="System operational, all services running"
curl -s -X POST "$BASE_URL/encode/$SESSION_ID" \
  -H "Content-Type: application/json" \
  -d "{\"data\": \"$SYSTEM_STATUS\", \"execute_flows\": true}" | jq '.encoded_symbols | length'

# Execute variance analysis
echo "📊 Executing variance analysis..."
curl -s -X POST "$BASE_URL/execute/$SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{"symbol_name": "jacklyn_variance", "context": {"data_source": "system_metrics"}}' | jq '.execution_result.flows[0].action'

echo "✅ Agent script completed"
```

## Symbol Reference

### Core Character Symbols

| Symbol | Function | Mode | Description |
|--------|----------|------|-------------|
| `an_author` | `narrative_create` | index | Create new narrative content |
| `london_fox` | `data_query` | ask | Query and search existing data |
| `jacklyn_variance` | `variance_analysis` | read | Analyze patterns and variance |
| `The_Author` | `meta_control` | index | Meta-level narrative control |
| `princhetta` | `system_control` | index | Full system orchestration |
| `arieol_owlist` | `wisdom_quest` | ask | Seek wisdom and knowledge |
| `todd_fishbone` | `pattern_detect` | read | Detect patterns in data |
| `cop-e-right` | `rights_manage` | receive | Manage rights and permissions |

### Flow Types

- **narrative** - Story creation and development
- **data** - Information processing and analysis  
- **character** - Character-specific interactions
- **system** - System-level operations
- **automation** - Automated process flows
- **ui** - User interface interactions

## Best Practices

### 1. Session Management
- Use descriptive session IDs: `agent-{purpose}-{timestamp}`
- Clean up sessions when done: `DELETE /session/{session_id}`
- Monitor session history for debugging

### 2. Mode Transitions
- Always check current mode before operations
- Use appropriate modes for different tasks:
  - `read` for analysis and understanding
  - `ask` for queries and requests
  - `index` for creation and cataloging
  - `receive` for processing inputs

### 3. Error Handling
- Check HTTP status codes (200 = success)
- Handle WebSocket connection drops gracefully
- Retry failed operations with exponential backoff

### 4. Performance
- Batch symbol operations when possible
- Use WebSocket for real-time updates
- Limit search results appropriately (5-20 items)
- Cache frequently used symbol data

### 5. Context Management
- Pass relevant context with each operation
- Use context to maintain state across operations
- Include agent identification in context

## Integration Examples

### CI/CD Integration
```yaml
# .github/workflows/qdpi-analysis.yml
name: QDPI Code Analysis
on: [push]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: QDPI Analysis
        run: |
          # Encode commit message into QDPI
          curl -X POST "$QDPI_URL/encode/ci-$GITHUB_RUN_ID" \
            -d "{\"data\": \"$GITHUB_COMMIT_MESSAGE\"}"
          
          # Execute pattern analysis
          curl -X POST "$QDPI_URL/execute/ci-$GITHUB_RUN_ID" \
            -d "{\"symbol_name\": \"todd_fishbone\"}"
```

### Monitoring Integration
```python
# monitoring/qdpi_monitor.py
def monitor_system_health():
    agent = QDPIAgent()
    
    # Set monitoring mode
    agent.set_mode("read", context={"purpose": "monitoring"})
    
    # Encode system metrics
    metrics = get_system_metrics()
    encoded = agent.encode_data(json.dumps(metrics))
    
    # Analyze with variance detection
    analysis = agent.execute_symbol("jacklyn_variance", {
        "metrics": metrics,
        "threshold": 0.8
    })
    
    return analysis
```

This completes the developer integration guide for QDPI-256. Agents and external systems can now programmatically interact with the symbolic machine language through REST APIs and WebSocket events.