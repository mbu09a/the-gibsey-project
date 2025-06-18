"""
Vector search API endpoints for semantic similarity and content discovery
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from app.database import get_database
from app.models import StoryPage
from app.cassandra_database_v2 import ProductionCassandraDatabase

router = APIRouter(prefix="/api/v1/search", tags=["Vector Search"])

class SearchQuery(BaseModel):
    """Request model for semantic search"""
    query: str
    limit: int = 10
    content_type: str = "page"
    filters: Optional[Dict[str, Any]] = None

class SearchResult(BaseModel):
    """Search result with similarity score"""
    page: StoryPage
    similarity_score: float
    
class RelatedContentRequest(BaseModel):
    """Request for finding related content"""
    page_id: str
    limit: int = 5

@router.post("/semantic", response_model=List[SearchResult])
async def semantic_search(
    search_query: SearchQuery,
    db = Depends(get_database)
):
    """
    Perform semantic search using vector embeddings
    
    Find pages similar to the query text using vector similarity.
    Requires Cassandra database with vector embeddings.
    """
    # Check if we're using the production database with vector search
    if not isinstance(db, ProductionCassandraDatabase):
        raise HTTPException(
            status_code=501, 
            detail="Vector search requires Cassandra database. Set DATABASE_URL=cassandra://localhost:9042"
        )
    
    try:
        # Perform vector search
        results = await db.search_similar_pages(
            query_text=search_query.query,
            limit=search_query.limit,
            content_type=search_query.content_type
        )
        
        # Convert to response format
        search_results = [
            SearchResult(page=page, similarity_score=score)
            for page, score in results
        ]
        
        return search_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/similar/{page_id}", response_model=List[SearchResult])
async def get_similar_pages(
    page_id: str,
    limit: int = Query(5, ge=1, le=20),
    db = Depends(get_database)
):
    """
    Find pages similar to a specific page using vector embeddings
    
    Returns pages that are semantically similar to the given page.
    """
    if not isinstance(db, ProductionCassandraDatabase):
        raise HTTPException(
            status_code=501, 
            detail="Vector search requires Cassandra database"
        )
    
    try:
        # Get the page first to ensure it exists
        page = await db.get_page(page_id)
        if not page:
            raise HTTPException(status_code=404, detail="Page not found")
        
        # Find related pages
        results = await db.get_related_pages(page_id, limit=limit)
        
        # Filter out the original page if it appears in results
        filtered_results = [
            (page, score) for page, score in results 
            if page.id != page_id
        ][:limit]
        
        search_results = [
            SearchResult(page=page, similarity_score=score)
            for page, score in filtered_results
        ]
        
        return search_results
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Related pages search failed: {str(e)}")

@router.get("/by-character/{symbol_id}", response_model=List[SearchResult])
async def search_by_character_semantic(
    symbol_id: str,
    query: str = Query(..., description="Search query within character's content"),
    limit: int = Query(10, ge=1, le=50),
    db = Depends(get_database)
):
    """
    Semantic search within a specific character's pages
    
    Combines character filtering with semantic search for precise results.
    """
    if not isinstance(db, ProductionCassandraDatabase):
        raise HTTPException(
            status_code=501, 
            detail="Vector search requires Cassandra database"
        )
    
    try:
        # First get pages by character (fast path)
        character_pages = await db.get_pages_by_symbol(symbol_id, limit=100)
        
        if not character_pages:
            return []
        
        # Perform semantic search on the query
        all_results = await db.search_similar_pages(
            query_text=query,
            limit=limit * 3,  # Get more to filter
            content_type='page'
        )
        
        # Filter results to only include the specified character
        character_page_ids = {page.id for page in character_pages}
        filtered_results = [
            (page, score) for page, score in all_results
            if page.id in character_page_ids
        ][:limit]
        
        search_results = [
            SearchResult(page=page, similarity_score=score)
            for page, score in filtered_results
        ]
        
        return search_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Character semantic search failed: {str(e)}")

@router.post("/recommend", response_model=List[SearchResult])
async def get_recommendations(
    recommendation_request: RelatedContentRequest,
    db = Depends(get_database)
):
    """
    Get content recommendations based on a page
    
    Uses vector similarity to recommend related content that users might find interesting.
    """
    if not isinstance(db, ProductionCassandraDatabase):
        raise HTTPException(
            status_code=501, 
            detail="Recommendations require Cassandra database"
        )
    
    try:
        # Get recommendations (same as similar pages but with different semantics)
        results = await db.get_related_pages(
            recommendation_request.page_id, 
            limit=recommendation_request.limit
        )
        
        # Filter out the original page
        filtered_results = [
            (page, score) for page, score in results 
            if page.id != recommendation_request.page_id
        ][:recommendation_request.limit]
        
        recommendations = [
            SearchResult(page=page, similarity_score=score)
            for page, score in filtered_results
        ]
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendations failed: {str(e)}")

@router.get("/explore", response_model=List[SearchResult])
async def explore_content(
    themes: List[str] = Query([], description="Themes to explore (e.g., 'consciousness', 'mystery')"),
    character: Optional[str] = Query(None, description="Specific character to focus on"),
    limit: int = Query(10, ge=1, le=20),
    db = Depends(get_database)
):
    """
    Explore content by themes and concepts
    
    Discover content related to specific themes, concepts, or philosophical ideas.
    """
    if not isinstance(db, ProductionCassandraDatabase):
        raise HTTPException(
            status_code=501, 
            detail="Content exploration requires Cassandra database"
        )
    
    try:
        if not themes:
            # Default exploration query
            query = "consciousness mystery philosophy narrative meaning"
        else:
            # Combine themes into search query
            query = " ".join(themes)
        
        # Add character context if specified
        if character:
            query += f" character:{character.replace('-', ' ')}"
        
        # Perform semantic search
        results = await db.search_similar_pages(
            query_text=query,
            limit=limit,
            content_type='page'
        )
        
        # If character filter specified, apply post-filtering
        if character:
            filtered_results = [
                (page, score) for page, score in results
                if page.symbol_id == character
            ][:limit]
        else:
            filtered_results = results
        
        search_results = [
            SearchResult(page=page, similarity_score=score)
            for page, score in filtered_results
        ]
        
        return search_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content exploration failed: {str(e)}")

@router.get("/status")
async def get_search_status(db = Depends(get_database)):
    """
    Get the status of vector search capabilities
    
    Returns information about vector search availability and configuration.
    """
    if isinstance(db, ProductionCassandraDatabase):
        try:
            # Test if vector service is working
            from app.vector_service import get_vector_service
            vector_service = get_vector_service()
            
            # Get some basic info
            status = {
                "available": True,
                "database_type": "cassandra",
                "vector_service": "enabled",
                "default_model": getattr(vector_service, 'default_model', 'unknown'),
                "features": [
                    "semantic_search",
                    "similarity_matching", 
                    "content_recommendations",
                    "theme_exploration"
                ]
            }
            
            return status
            
        except Exception as e:
            return {
                "available": False,
                "database_type": "cassandra",
                "vector_service": "error",
                "error": str(e)
            }
    else:
        return {
            "available": False,
            "database_type": "mock",
            "vector_service": "disabled",
            "message": "Vector search requires Cassandra database. Set DATABASE_URL=cassandra://localhost:9042"
        }