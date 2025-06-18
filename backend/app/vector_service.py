"""
Vector embedding service for semantic search in the Gibsey Mycelial Network
Supports both Sentence Transformers (SBERT) and OpenAI embeddings
"""

import asyncio
import logging
import os
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
import numpy as np
from sentence_transformers import SentenceTransformer
import openai
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

@dataclass
class EmbeddingResult:
    """Result of an embedding operation"""
    content_id: str
    content_type: str
    embedding: List[float]
    model: str
    dimensions: int
    metadata: Dict[str, Any]

class VectorEmbeddingService:
    """Service for generating and managing vector embeddings"""
    
    def __init__(self, 
                 default_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 openai_api_key: Optional[str] = None):
        """
        Initialize the vector embedding service
        
        Args:
            default_model: Default model to use (SBERT model name or 'openai')
            openai_api_key: OpenAI API key (if using OpenAI embeddings)
        """
        self.default_model = default_model
        self.sbert_model = None
        self.openai_client = None
        
        # Initialize OpenAI if API key provided
        if openai_api_key:
            self.openai_client = openai.OpenAI(api_key=openai_api_key)
        elif os.getenv('OPENAI_API_KEY'):
            self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Model dimensions mapping
        self.model_dimensions = {
            "sentence-transformers/all-MiniLM-L6-v2": 384,
            "sentence-transformers/all-mpnet-base-v2": 768,
            "text-embedding-ada-002": 1536,
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072
        }
    
    def _initialize_sbert_model(self, model_name: str = None) -> SentenceTransformer:
        """Initialize or get SBERT model"""
        model_name = model_name or self.default_model
        
        if self.sbert_model is None or getattr(self.sbert_model, '_model_name', None) != model_name:
            try:
                logger.info(f"Loading SBERT model: {model_name}")
                self.sbert_model = SentenceTransformer(model_name)
                self.sbert_model._model_name = model_name
                logger.info(f"SBERT model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load SBERT model {model_name}: {e}")
                raise
        
        return self.sbert_model
    
    async def embed_text(self, 
                        text: str, 
                        content_id: str,
                        content_type: str,
                        model: str = None,
                        metadata: Dict[str, Any] = None) -> EmbeddingResult:
        """
        Generate embedding for a single text
        
        Args:
            text: Text to embed
            content_id: Unique identifier for the content
            content_type: Type of content (page, prompt, etc.)
            model: Model to use (defaults to default_model)
            metadata: Additional metadata to store
            
        Returns:
            EmbeddingResult with embedding and metadata
        """
        model = model or self.default_model
        metadata = metadata or {}
        
        try:
            if model.startswith('text-embedding-') and self.openai_client:
                # OpenAI embedding
                embedding = await self._embed_openai(text, model)
            else:
                # SBERT embedding
                embedding = await self._embed_sbert(text, model)
            
            return EmbeddingResult(
                content_id=content_id,
                content_type=content_type,
                embedding=embedding,
                model=model,
                dimensions=len(embedding),
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Failed to embed text for {content_id}: {e}")
            raise
    
    async def _embed_sbert(self, text: str, model: str) -> List[float]:
        """Generate SBERT embedding"""
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        
        def _encode():
            sbert_model = self._initialize_sbert_model(model)
            embedding = sbert_model.encode(text, convert_to_tensor=False)
            return embedding.tolist()
        
        return await loop.run_in_executor(None, _encode)
    
    async def _embed_openai(self, text: str, model: str) -> List[float]:
        """Generate OpenAI embedding"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        try:
            response = await asyncio.to_thread(
                self.openai_client.embeddings.create,
                input=text,
                model=model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"OpenAI embedding failed: {e}")
            raise
    
    async def embed_batch(self, 
                         texts: List[Tuple[str, str, str]], 
                         model: str = None,
                         metadata_list: List[Dict[str, Any]] = None) -> List[EmbeddingResult]:
        """
        Generate embeddings for multiple texts in batch
        
        Args:
            texts: List of (text, content_id, content_type) tuples
            model: Model to use
            metadata_list: List of metadata dicts for each text
            
        Returns:
            List of EmbeddingResult objects
        """
        model = model or self.default_model
        metadata_list = metadata_list or [{}] * len(texts)
        
        if model.startswith('text-embedding-') and self.openai_client:
            return await self._embed_batch_openai(texts, model, metadata_list)
        else:
            return await self._embed_batch_sbert(texts, model, metadata_list)
    
    async def _embed_batch_sbert(self, 
                                texts: List[Tuple[str, str, str]], 
                                model: str,
                                metadata_list: List[Dict[str, Any]]) -> List[EmbeddingResult]:
        """Generate SBERT embeddings in batch"""
        loop = asyncio.get_event_loop()
        
        def _encode_batch():
            sbert_model = self._initialize_sbert_model(model)
            text_list = [text for text, _, _ in texts]
            embeddings = sbert_model.encode(text_list, convert_to_tensor=False)
            return [embedding.tolist() for embedding in embeddings]
        
        embeddings = await loop.run_in_executor(None, _encode_batch)
        
        results = []
        for i, ((text, content_id, content_type), embedding) in enumerate(zip(texts, embeddings)):
            results.append(EmbeddingResult(
                content_id=content_id,
                content_type=content_type,
                embedding=embedding,
                model=model,
                dimensions=len(embedding),
                metadata=metadata_list[i]
            ))
        
        return results
    
    async def _embed_batch_openai(self, 
                                 texts: List[Tuple[str, str, str]], 
                                 model: str,
                                 metadata_list: List[Dict[str, Any]]) -> List[EmbeddingResult]:
        """Generate OpenAI embeddings in batch"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        text_list = [text for text, _, _ in texts]
        
        try:
            response = await asyncio.to_thread(
                self.openai_client.embeddings.create,
                input=text_list,
                model=model
            )
            
            results = []
            for i, ((text, content_id, content_type), embedding_data) in enumerate(zip(texts, response.data)):
                results.append(EmbeddingResult(
                    content_id=content_id,
                    content_type=content_type,
                    embedding=embedding_data.embedding,
                    model=model,
                    dimensions=len(embedding_data.embedding),
                    metadata=metadata_list[i]
                ))
            
            return results
            
        except Exception as e:
            logger.error(f"OpenAI batch embedding failed: {e}")
            raise
    
    def calculate_similarity(self, 
                           embedding1: List[float], 
                           embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            # Convert to numpy arrays
            vec1 = np.array(embedding1).reshape(1, -1)
            vec2 = np.array(embedding2).reshape(1, -1)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(vec1, vec2)[0][0]
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Similarity calculation failed: {e}")
            return 0.0
    
    def find_most_similar(self, 
                         query_embedding: List[float], 
                         candidate_embeddings: List[Tuple[str, List[float]]], 
                         top_k: int = 10) -> List[Tuple[str, float]]:
        """
        Find most similar embeddings to a query embedding
        
        Args:
            query_embedding: The query vector
            candidate_embeddings: List of (id, embedding) tuples
            top_k: Number of top results to return
            
        Returns:
            List of (id, similarity_score) tuples, sorted by similarity desc
        """
        try:
            if not candidate_embeddings:
                return []
            
            # Calculate similarities
            similarities = []
            for content_id, embedding in candidate_embeddings:
                similarity = self.calculate_similarity(query_embedding, embedding)
                similarities.append((content_id, similarity))
            
            # Sort by similarity descending
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Return top k
            return similarities[:top_k]
            
        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
            return []
    
    async def embed_story_page(self, page_data: Dict[str, Any]) -> EmbeddingResult:
        """
        Generate embedding for a story page
        Combines title, text, and metadata for rich embedding
        """
        # Combine relevant text fields
        text_parts = []
        
        if page_data.get('title'):
            text_parts.append(f"Title: {page_data['title']}")
        
        if page_data.get('text'):
            text_parts.append(page_data['text'])
        
        if page_data.get('symbol_id'):
            text_parts.append(f"Character: {page_data['symbol_id'].replace('-', ' ').title()}")
        
        if page_data.get('section'):
            text_parts.append(f"Section: {page_data['section']}")
        
        combined_text = " | ".join(text_parts)
        
        metadata = {
            'symbol_id': page_data.get('symbol_id'),
            'page_type': page_data.get('page_type'),
            'section': page_data.get('section'),
            'author': page_data.get('author')
        }
        
        return await self.embed_text(
            text=combined_text,
            content_id=page_data['id'],
            content_type='page',
            metadata=metadata
        )
    
    async def embed_prompt(self, prompt_data: Dict[str, Any]) -> EmbeddingResult:
        """Generate embedding for a prompt"""
        # Combine prompt text with context
        text_parts = []
        
        if prompt_data.get('text'):
            text_parts.append(prompt_data['text'])
        
        if prompt_data.get('description'):
            text_parts.append(f"Description: {prompt_data['description']}")
        
        if prompt_data.get('target_symbol_id'):
            text_parts.append(f"Target: {prompt_data['target_symbol_id'].replace('-', ' ').title()}")
        
        if prompt_data.get('prompt_type'):
            text_parts.append(f"Type: {prompt_data['prompt_type']}")
        
        combined_text = " | ".join(text_parts)
        
        metadata = {
            'target_symbol_id': prompt_data.get('target_symbol_id'),
            'prompt_type': prompt_data.get('prompt_type')
        }
        
        return await self.embed_text(
            text=combined_text,
            content_id=prompt_data['id'],
            content_type='prompt',
            metadata=metadata
        )

# Global vector service instance
_vector_service = None

def get_vector_service() -> VectorEmbeddingService:
    """Get or create global vector service instance"""
    global _vector_service
    if _vector_service is None:
        _vector_service = VectorEmbeddingService()
    return _vector_service

async def initialize_vector_service(model: str = None, openai_key: str = None):
    """Initialize the global vector service"""
    global _vector_service
    _vector_service = VectorEmbeddingService(
        default_model=model or "sentence-transformers/all-MiniLM-L6-v2",
        openai_api_key=openai_key
    )
    logger.info("Vector embedding service initialized")