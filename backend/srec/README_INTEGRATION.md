# Symbol Embedding Workflow

This document describes the complete SREC (Symbol-Rotation Embedding Compiler) integration for the Gibsey project.

## Overview

SREC processes SVG symbol files to create CLIP embeddings for each symbol at 4 rotations (0°, 90°, 180°, 270°), storing them in ChromaDB for vector similarity search.

## Installation

### 1. System Dependencies

**macOS:**
```bash
brew install imagemagick
```

**Ubuntu/Debian:**
```bash
apt-get install imagemagick libmagickwand-dev
```

**Docker:** Already included in Dockerfile

### 2. Python Dependencies

```bash
pip install Wand watchdog
```

Or use the included requirements.txt:
```bash
pip install -r backend/requirements.txt
```

### 3. ChromaDB Setup

**Docker (Recommended):**
```bash
docker run -d --name chromadb -p 8001:8000 -e ALLOW_ALL=TRUE ghcr.io/chroma-core/chroma:latest
```

**Docker Compose:**
```bash
cd backend
docker-compose up -d chromadb
```

## Usage

### Manual Compilation

Process all SVGs in a directory:
```bash
cd backend/srec
python compiler.py /path/to/corpus-symbols
```

### API Upload

**Single file:**
```bash
curl -X POST http://localhost:8000/api/v1/symbols/upload \
  -F "file=@new_symbol.svg"
```

**Multiple files:**
```bash
curl -X POST http://localhost:8000/api/v1/symbols/upload-batch \
  -F "files=@symbol1.svg" \
  -F "files=@symbol2.svg"
```

**Check status:**
```bash
curl http://localhost:8000/api/v1/symbols/status
```

### Automatic Processing

**File Watcher:**
```bash
cd backend/srec
python watcher.py ../../public/corpus-symbols
```

**Startup Script:**
```bash
cd backend/srec
python startup.py
```

**Git Hook Installation:**
```bash
cd your-repo
ln -s backend/srec/git-hooks/pre-commit .git/hooks/pre-commit
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CHROMA_HOST` | `localhost` | ChromaDB host |
| `CHROMA_PORT` | `8001` | ChromaDB port |
| `SREC_COLLECTION` | `corpus_symbols` | Collection name in ChromaDB |
| `SREC_EMBED_MODEL` | `sentence-transformers/clip-ViT-B-32` | CLIP model to use |
| `SREC_ENV` | `development` | Set to `production` to enforce Wand |
| `CORPUS_SYMBOLS_DIR` | `../public/corpus-symbols` | Default symbols directory |

## API Endpoints

### Upload Symbol
`POST /api/v1/symbols/upload`
- Upload single SVG file
- Returns embedding IDs and metadata

### Batch Upload
`POST /api/v1/symbols/upload-batch`
- Upload multiple SVG files (max 100)
- Large batches processed in background

### Status Check
`GET /api/v1/symbols/status`
- Get total symbols and embeddings
- List all embedded symbols

### Reprocess All
`POST /api/v1/symbols/reprocess-all`
- Reprocess all symbols in corpus directory
- Runs in background

## Verification

### Check ChromaDB is running:
```bash
curl http://localhost:8001/api/v1/heartbeat
```

### Count embeddings:
```bash
curl http://localhost:8001/api/v1/collections/corpus_symbols/count
```

### Verify via API:
```bash
curl http://localhost:8000/api/v1/symbols/status
```

## Troubleshooting

### "Wand not available" Error
- **Development:** Creates placeholder embeddings (acceptable)
- **Production:** Install Wand: `pip install Wand`
- **Docker:** Rebuild image after updating Dockerfile

### ChromaDB Connection Error
- Ensure ChromaDB is running on port 8001
- Check Docker: `docker ps | grep chroma`
- Start if needed: `docker start chromadb`

### SVG Processing Fails
- Verify SVG files are valid (open in browser)
- Check ImageMagick: `convert -version`
- Install if missing: `brew install imagemagick`

### Missing Embeddings
- Run startup script: `python srec/startup.py`
- Check logs for errors
- Verify ChromaDB collection exists

## Integration with Backend

### FastAPI Startup
Add to your `main.py`:
```python
from srec.startup import ensure_all_symbols_compiled

@app.on_event("startup")
async def startup_event():
    # Ensure all symbols are embedded
    ensure_all_symbols_compiled()
```

### Docker Compose
The full stack includes ChromaDB:
```bash
docker-compose up -d
```

### Production Deployment
1. Set `SREC_ENV=production` in environment
2. Ensure ImageMagick is in Docker image
3. Mount persistent volume for ChromaDB data
4. Run startup script on container start

## Search Integration

Example search endpoint:
```python
from chromadb import HttpClient

@router.get("/api/v1/symbols/search")
async def search_symbols(query_embedding: List[float], n_results: int = 5):
    client = HttpClient(host="localhost", port=8001)
    collection = client.get_collection("corpus_symbols")
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    return results
```

## Monitoring

### Logs
- SREC logs to console with emojis for status
- Failed embeddings logged with error details
- Progress bars show processing status

### Metrics
- Total embeddings: Check via `/api/v1/symbols/status`
- Processing time: ~1-2 seconds per symbol
- Storage: ~1KB per embedding in ChromaDB

## Best Practices

1. **Always run ChromaDB** before processing symbols
2. **Use production mode** (`SREC_ENV=production`) in production
3. **Backup ChromaDB data** regularly
4. **Monitor disk space** - embeddings accumulate
5. **Test SVGs** before bulk processing
6. **Use batch API** for multiple uploads
7. **Enable file watcher** for automatic processing

## Known Issues

1. PIL cannot read SVGs directly (use Wand)
2. Large SVGs (>5MB) may timeout
3. ChromaDB requires explicit allow-all in Docker
4. First run downloads CLIP model (~340MB)

## Support

- Check logs for detailed error messages
- Verify all dependencies installed
- Test with single SVG first
- Use development mode for debugging