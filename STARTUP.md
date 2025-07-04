# Gibsey Project Startup Instructions

## Quick Start (Recommended)

### 1. Start Cassandra
```bash
# Start standalone Cassandra container
docker run -d --name gibsey-cassandra \
  -p 9042:9042 \
  -e CASSANDRA_CLUSTER_NAME=gibsey-cluster \
  -e CASSANDRA_DC=datacenter1 \
  -e CASSANDRA_RACK=rack1 \
  cassandra:3.11

# Wait for Cassandra to be ready (30-60 seconds)
docker logs -f gibsey-cassandra
# Wait until you see "Starting listening for CQL clients"
```

### 2. Initialize Database
```bash
cd backend
python scripts/init_cassandra.py
```

### 3. Seed the Corpus (710 pages)
```bash
cd backend
python scripts/seed_embeddings.py
```

### 4. Start Backend
```bash
cd backend
python main.py
```

### 5. Start Frontend
```bash
cd src
npm run dev
```

## Verification

Test the complete pipeline:
```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What can you tell me about Glyph Marrow?", "character": "jacklyn-variance"}'
```

Should return a D.A.D.D.Y.S-H.A.R.D format response with story context.

## Troubleshooting

- If Cassandra fails to start, try: `docker rm -f gibsey-cassandra` then restart
- If backend fails, check Ollama is running: `ollama serve`
- Make sure llama3:8b model is pulled: `ollama pull llama3:8b`