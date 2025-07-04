"""Symbol search API using ChromaDB vector similarity."""
import os
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
from PIL import Image
import io

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/symbol-search", tags=["symbol-search"])

# Global clients
_client = None
_collection = None
_model = None

def get_chromadb_client():
    """Get or create ChromaDB client."""
    global _client, _collection
    if _client is None:
        _client = chromadb.HttpClient(
            host=os.getenv("CHROMA_HOST", "localhost"),
            port=int(os.getenv("CHROMA_PORT", "8001"))
        )
        _collection = _client.get_collection(
            os.getenv("SREC_COLLECTION", "corpus_symbols")
        )
    return _client, _collection

def get_embedding_model():
    """Get or create embedding model."""
    global _model
    if _model is None:
        model_name = os.getenv("SREC_EMBED_MODEL", "sentence-transformers/clip-ViT-B-32")
        _model = SentenceTransformer(model_name)
    return _model

class SymbolSearchRequest(BaseModel):
    """Request for symbol search by embedding."""
    query_embedding: List[float]
    n_results: int = 5
    filter_rotation: Optional[int] = None  # Filter by specific rotation (0, 90, 180, 270)

class SymbolSearchResponse(BaseModel):
    """Response for symbol search."""
    results: List[Dict[str, Any]]
    distances: List[float]
    total_results: int

class TextSearchRequest(BaseModel):
    """Request for text-based symbol search."""
    query_text: str
    n_results: int = 5

@router.post("/by-embedding", response_model=SymbolSearchResponse)
async def search_symbols_by_embedding(request: SymbolSearchRequest) -> SymbolSearchResponse:
    """
    Search for similar symbols using a query embedding.
    
    This is useful when you already have an embedding vector.
    """
    try:
        _, collection = get_chromadb_client()
        
        # Build filter if rotation specified
        where = None
        if request.filter_rotation is not None:
            where = {"rot": request.filter_rotation}
        
        # Query ChromaDB
        results = collection.query(
            query_embeddings=[request.query_embedding],
            n_results=request.n_results,
            where=where,
            include=["metadatas", "distances", "documents"]
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['ids'][0])):
            formatted_results.append({
                "id": results['ids'][0][i],
                "symbol": results['metadatas'][0][i].get('symbol'),
                "rotation": results['metadatas'][0][i].get('rot'),
                "distance": results['distances'][0][i],
                "metadata": results['metadatas'][0][i]
            })
        
        return SymbolSearchResponse(
            results=formatted_results,
            distances=results['distances'][0],
            total_results=len(results['ids'][0])
        )
        
    except Exception as e:
        logger.error(f"Symbol search failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )

@router.post("/by-text", response_model=SymbolSearchResponse)
async def search_symbols_by_text(request: TextSearchRequest) -> SymbolSearchResponse:
    """
    Search for symbols using a text query.
    
    The text is converted to an embedding using CLIP.
    """
    try:
        model = get_embedding_model()
        _, collection = get_chromadb_client()
        
        # Convert text to embedding
        query_embedding = model.encode(request.query_text).tolist()
        
        # Query ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=request.n_results,
            include=["metadatas", "distances", "documents"]
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['ids'][0])):
            formatted_results.append({
                "id": results['ids'][0][i],
                "symbol": results['metadatas'][0][i].get('symbol'),
                "rotation": results['metadatas'][0][i].get('rot'),
                "distance": results['distances'][0][i],
                "metadata": results['metadatas'][0][i]
            })
        
        return SymbolSearchResponse(
            results=formatted_results,
            distances=results['distances'][0],
            total_results=len(results['ids'][0])
        )
        
    except Exception as e:
        logger.error(f"Text search failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )

@router.post("/by-image", response_model=SymbolSearchResponse)
async def search_symbols_by_image(
    file: UploadFile = File(...),
    n_results: int = Query(5, ge=1, le=50)
) -> SymbolSearchResponse:
    """
    Search for similar symbols by uploading an image.
    
    The image is converted to an embedding using CLIP.
    """
    try:
        # Validate file type
        if not file.content_type or 'image' not in file.content_type:
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )
        
        # Read and process image
        content = await file.read()
        img = Image.open(io.BytesIO(content))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get embedding
        model = get_embedding_model()
        query_embedding = model.encode(img).tolist()
        
        # Query ChromaDB
        _, collection = get_chromadb_client()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["metadatas", "distances", "documents"]
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['ids'][0])):
            formatted_results.append({
                "id": results['ids'][0][i],
                "symbol": results['metadatas'][0][i].get('symbol'),
                "rotation": results['metadatas'][0][i].get('rot'),
                "distance": results['distances'][0][i],
                "metadata": results['metadatas'][0][i]
            })
        
        return SymbolSearchResponse(
            results=formatted_results,
            distances=results['distances'][0],
            total_results=len(results['ids'][0])
        )
        
    except Exception as e:
        logger.error(f"Image search failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )

@router.get("/symbol/{symbol_id}", response_model=Dict[str, Any])
async def get_symbol_embeddings(symbol_id: str) -> Dict[str, Any]:
    """
    Get all embeddings for a specific symbol (all rotations).
    """
    try:
        _, collection = get_chromadb_client()
        
        # Query for all rotations of this symbol
        results = collection.get(
            where={"symbol": symbol_id},
            include=["embeddings", "metadatas", "documents"]
        )
        
        if not results['ids']:
            raise HTTPException(
                status_code=404,
                detail=f"Symbol '{symbol_id}' not found"
            )
        
        # Organize by rotation
        rotations = {}
        for i in range(len(results['ids'])):
            rot = results['metadatas'][i].get('rot', 0)
            rotations[f"rotation_{rot}"] = {
                "id": results['ids'][i],
                "embedding": results['embeddings'][i] if results['embeddings'] else None,
                "metadata": results['metadatas'][i]
            }
        
        return {
            "symbol_id": symbol_id,
            "rotations": rotations,
            "total_embeddings": len(results['ids'])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get symbol embeddings: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve symbol: {str(e)}"
        )

@router.get("/stats", response_model=Dict[str, Any])
async def get_search_stats() -> Dict[str, Any]:
    """Get statistics about the symbol collection."""
    try:
        _, collection = get_chromadb_client()
        
        # Get total count
        total_embeddings = collection.count()
        
        # Get sample to analyze
        sample = collection.get(
            limit=1000,
            include=["metadatas"]
        )
        
        # Count unique symbols and rotations
        symbols = set()
        rotation_counts = {0: 0, 90: 0, 180: 0, 270: 0}
        
        for meta in sample['metadatas']:
            if meta:
                symbols.add(meta.get('symbol'))
                rot = meta.get('rot', 0)
                if rot in rotation_counts:
                    rotation_counts[rot] += 1
        
        return {
            "total_embeddings": total_embeddings,
            "unique_symbols": len(symbols),
            "rotation_distribution": rotation_counts,
            "collection_name": os.getenv("SREC_COLLECTION", "corpus_symbols"),
            "embedding_model": os.getenv("SREC_EMBED_MODEL", "sentence-transformers/clip-ViT-B-32"),
            "sample_size": len(sample['ids'])
        }
        
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get statistics: {str(e)}"
        )