#!/usr/bin/env python3
"""
Gibsey Project Retrieval API

FastAPI endpoints for semantic search and page retrieval using Cassandra vector store.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

import numpy as np
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import DCAwareRoundRobinPolicy
import openai
from sentence_transformers import SentenceTransformer

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from backend.app.tokenizer_service import get_tokenizer_service
    TOKENIZER_AVAILABLE = True
except ImportError:
    TOKENIZER_AVAILABLE = False
    print("⚠️ Warning: Tokenizer service not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for services
cassandra_session = None
embedding_model = None
tokenizer_service = None

# Configuration from environment
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "localhost")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", "9042"))
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "gibsey")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")

# API Models
class SearchQuery(BaseModel):
    q: str = Field(..., description="Query string for semantic search")
    top_k: int = Field(default=5, ge=1, le=50, description="Number of results to return")
    symbol_id: Optional[str] = Field(None, description="Filter by character symbol ID")

class PageResponse(BaseModel):
    page_id: str
    title: str
    content: str
    symbol_id: Optional[str]
    tokens: int
    page_index: int

class SearchResult(BaseModel):
    page_id: str
    title: str
    preview: str
    symbol_id: Optional[str]
    score: float
    page_index: int

class SearchResponse(BaseModel):
    results: List[SearchResult]
    query: str
    total_results: int
    processing_time_ms: float

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup and cleanup on shutdown."""
    global cassandra_session, embedding_model, tokenizer_service
    
    try:
        # Initialize Cassandra connection
        logger.info(f"Connecting to Cassandra at {CASSANDRA_HOST}:{CASSANDRA_PORT}")
        cluster = Cluster(
            [CASSANDRA_HOST],
            port=CASSANDRA_PORT,
            load_balancing_policy=DCAwareRoundRobinPolicy()
        )
        cassandra_session = cluster.connect(CASSANDRA_KEYSPACE)
        logger.info("✓ Cassandra connection established")
        
        # Initialize embedding model
        if OPENAI_API_KEY:
            openai.api_key = OPENAI_API_KEY
            embedding_model = "openai"
            logger.info(f"✓ OpenAI embedding model configured: {EMBED_MODEL}")
        else:
            # Fallback to local model
            logger.info("Loading local sentence transformer model...")
            embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✓ Local sentence transformer loaded")
        
        # Initialize tokenizer service
        if TOKENIZER_AVAILABLE:
            tokenizer_service = get_tokenizer_service()
            logger.info("✓ Gibsey tokenizer service loaded")
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise
    finally:
        # Cleanup
        if cassandra_session:
            cassandra_session.shutdown()
        logger.info("Services shut down")

# Create FastAPI app
app = FastAPI(
    title="Gibsey Retrieval API",
    description="Semantic search and page retrieval for the Gibsey corpus",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_embedding(text: str) -> List[float]:
    """Generate embedding for text using configured model."""
    if embedding_model == "openai":
        response = openai.embeddings.create(
            model=EMBED_MODEL,
            input=text
        )
        return response.data[0].embedding
    else:
        # Use local sentence transformer
        embedding = embedding_model.encode(text)
        return embedding.tolist()

def truncate_to_tokens(text: str, max_tokens: int = 300) -> str:
    """Truncate text to maximum number of tokens for preview."""
    if tokenizer_service:
        return tokenizer_service.truncate_to_tokens(text, max_tokens)
    else:
        # Fallback: approximate by characters
        approx_chars = max_tokens * 4  # Rough estimate
        return text[:approx_chars] + ("..." if len(text) > approx_chars else "")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "services": {
            "cassandra": cassandra_session is not None,
            "embedding_model": embedding_model is not None,
            "tokenizer": tokenizer_service is not None
        }
    }

@app.post("/read/{page_id}", response_model=PageResponse)
async def read_page(page_id: str):
    """Retrieve a specific page by ID."""
    if not cassandra_session:
        raise HTTPException(status_code=503, detail="Database not available")
    
    # Query page by primary key
    query = """
    SELECT page_id, title, content, symbol_id, tokens, page_index
    FROM pages 
    WHERE page_id = ?
    """
    
    try:
        result = cassandra_session.execute(query, [page_id])
        row = result.one()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Page {page_id} not found")
        
        return PageResponse(
            page_id=row.page_id,
            title=row.title,
            content=row.content,
            symbol_id=row.symbol_id,
            tokens=row.tokens,
            page_index=row.page_index
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (like 404) without modification
        raise
    except Exception as e:
        logger.error(f"Error reading page {page_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve page")

@app.post("/index", response_model=SearchResponse)
async def semantic_search(query: SearchQuery):
    """Perform semantic search over the corpus."""
    import time
    start_time = time.time()
    
    if not cassandra_session:
        raise HTTPException(status_code=503, detail="Database not available")
    
    # Validate query length
    if tokenizer_service:
        query_tokens = tokenizer_service.count_tokens(query.q)
        if query_tokens > 200:
            raise HTTPException(
                status_code=400, 
                detail=f"Query too long: {query_tokens} tokens (max 200)"
            )
    
    try:
        # Generate embedding for query
        query_embedding = get_embedding(query.q)
        
        # Prepare CQL query with vector search
        if query.symbol_id:
            # Filter by character symbol
            cql_query = """
            SELECT page_id, title, content, symbol_id, page_index, 
                   similarity_cosine(embedding, ?) as score
            FROM pages 
            WHERE symbol_id = ? AND embedding ANN OF ? LIMIT ?
            """
            params = [query_embedding, query.symbol_id, query_embedding, query.top_k]
        else:
            # Search all pages
            cql_query = """
            SELECT page_id, title, content, symbol_id, page_index,
                   similarity_cosine(embedding, ?) as score
            FROM pages 
            WHERE embedding ANN OF ? LIMIT ?
            """
            params = [query_embedding, query_embedding, query.top_k]
        
        # Execute search
        result = cassandra_session.execute(cql_query, params)
        
        # Process results
        search_results = []
        for row in result:
            preview = truncate_to_tokens(row.content, 300)
            
            search_results.append(SearchResult(
                page_id=row.page_id,
                title=row.title,
                preview=preview,
                symbol_id=row.symbol_id,
                score=float(row.score),
                page_index=row.page_index
            ))
        
        processing_time = (time.time() - start_time) * 1000
        
        return SearchResponse(
            results=search_results,
            query=query.q,
            total_results=len(search_results),
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error in semantic search: {e}")
        raise HTTPException(status_code=500, detail="Search failed")

@app.get("/stats")
async def get_corpus_stats():
    """Get statistics about the corpus."""
    if not cassandra_session:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        # Count total pages
        total_pages_result = cassandra_session.execute("SELECT COUNT(*) FROM pages")
        total_pages = total_pages_result.one().count
        
        # Count pages by character
        symbol_counts_result = cassandra_session.execute("""
            SELECT symbol_id, COUNT(*) as count 
            FROM pages 
            GROUP BY symbol_id 
            ALLOW FILTERING
        """)
        
        symbol_counts = {}
        for row in symbol_counts_result:
            if row.symbol_id:
                symbol_counts[row.symbol_id] = row.count
        
        # Get total token count
        token_sum_result = cassandra_session.execute("SELECT SUM(tokens) FROM pages")
        total_tokens = token_sum_result.one().system_sum_tokens or 0
        
        return {
            "total_pages": total_pages,
            "total_tokens": total_tokens,
            "pages_by_character": symbol_counts,
            "embedding_model": EMBED_MODEL if embedding_model == "openai" else "local",
            "tokenizer_available": tokenizer_service is not None
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)