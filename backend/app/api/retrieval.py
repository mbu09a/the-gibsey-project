"""
Retrieval API endpoints for corpus page retrieval and semantic search
"""

import os
import time
import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

# Import retrieval functionality from retrieval_api module
from ..retrieval_api import (
    SearchQuery, SearchResponse, PageResponse,
    cassandra_session, get_embedding, truncate_to_tokens,
    tokenizer_service
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/retrieval", tags=["Retrieval"])

@router.post("/read/{page_id}", response_model=PageResponse)
async def read_page(page_id: str):
    """
    Retrieve a specific page by ID.
    
    Args:
        page_id: The unique identifier of the page (e.g., "001-an-authors-preface")
    
    Returns:
        PageResponse with title, content, symbol_id, tokens, and page_index
    """
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

@router.post("/index", response_model=SearchResponse)
async def semantic_search(query: SearchQuery):
    """
    Perform semantic search over the corpus.
    
    Args:
        query: SearchQuery object containing:
            - q: Query string for semantic search
            - top_k: Number of results to return (default 5, max 50)
            - symbol_id: Optional filter by character symbol ID
    
    Returns:
        SearchResponse with results, query, total_results, and processing_time_ms
    """
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
            
            search_results.append({
                "page_id": row.page_id,
                "title": row.title,
                "preview": preview,
                "symbol_id": row.symbol_id,
                "score": float(row.score),
                "page_index": row.page_index
            })
        
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

@router.get("/corpus-stats")
async def get_corpus_stats():
    """
    Get statistics about the corpus.
    
    Returns:
        Dictionary with total_pages, total_tokens, pages_by_character, and model info
    """
    if not cassandra_session:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        # Count total pages
        total_pages_result = cassandra_session.execute("SELECT COUNT(*) FROM pages")
        total_pages = total_pages_result.one().count
        
        # Count pages by character (Note: This query might be slow without proper indexing)
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
            "embedding_model": os.getenv("EMBED_MODEL", "text-embedding-3-small"),
            "tokenizer_available": tokenizer_service is not None
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")