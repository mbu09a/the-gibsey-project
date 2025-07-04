"""
Context retrieval service for providing <X_READ> context to prompts.

Connects to the retrieval API to fetch relevant corpus snippets for a given query.
"""

import logging
import os
from typing import List, Optional, Dict
import httpx
from dataclasses import dataclass

# Direct Cassandra imports
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import openai
from sentence_transformers import SentenceTransformer

from .tokenizer_service import get_tokenizer_service

logger = logging.getLogger(__name__)


@dataclass
class RetrievedContext:
    """Container for retrieved context information."""
    snippets: List[str]
    page_ids: List[str]
    total_tokens: int
    character_symbols: List[str]


class ContextRetrievalService:
    """Service for retrieving relevant context from the corpus."""
    
    def __init__(self, max_context_tokens: int = 1500):
        """
        Initialize the context retrieval service.
        
        Args:
            max_context_tokens: Maximum tokens to include in context
        """
        self.max_context_tokens = max_context_tokens
        self.tokenizer = get_tokenizer_service()
        self.cassandra_session = None
        self.embedding_model = None
        
        # Load environment configuration
        self.cassandra_host = os.getenv("CASSANDRA_HOST", "localhost")
        self.cassandra_port = int(os.getenv("CASSANDRA_PORT", "9042"))
        self.cassandra_keyspace = os.getenv("CASSANDRA_KEYSPACE", "gibsey_network")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.embed_model = os.getenv("EMBED_MODEL", "text-embedding-3-small")
        
    def _ensure_connections(self):
        """Ensure Cassandra and embedding model connections are ready."""
        if self.cassandra_session is None:
            try:
                logger.info(f"Connecting to Cassandra at {self.cassandra_host}:{self.cassandra_port}")
                cluster = Cluster([self.cassandra_host], port=self.cassandra_port)
                self.cassandra_session = cluster.connect(self.cassandra_keyspace)
                logger.info("✓ Cassandra connection established for context retrieval")
            except Exception as e:
                logger.error(f"Failed to connect to Cassandra: {e}")
                return False
        
        if self.embedding_model is None:
            try:
                if self.openai_api_key:
                    openai.api_key = self.openai_api_key
                    self.embedding_model = "openai"
                    logger.info("✓ OpenAI embedding model configured for context retrieval")
                else:
                    logger.info("Loading local sentence transformer for context retrieval...")
                    self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                    logger.info("✓ Local sentence transformer loaded for context retrieval")
            except Exception as e:
                logger.error(f"Failed to initialize embedding model: {e}")
                return False
        
        return True
    
    def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text."""
        if self.embedding_model == "openai":
            try:
                response = openai.embeddings.create(
                    model=self.embed_model,
                    input=text[:8000]  # OpenAI has input limits
                )
                return response.data[0].embedding
            except Exception as e:
                logger.error(f"OpenAI embedding failed: {e}")
                raise
        else:
            # Use local sentence transformer
            embedding = self.embedding_model.encode(text[:512])  # Local model limits
            return embedding.tolist()
    
    async def retrieve_context(
        self, 
        query: str,
        character_id: Optional[str] = None,
        top_k: int = 5
    ) -> RetrievedContext:
        """
        Retrieve relevant context snippets for a query.
        
        Args:
            query: The user's query
            character_id: Optional character to filter by
            top_k: Number of top results to consider
            
        Returns:
            RetrievedContext with snippets and metadata
        """
        # Ensure connections are ready
        if not self._ensure_connections():
            logger.error("Failed to establish connections for context retrieval")
            return RetrievedContext(snippets=[], page_ids=[], total_tokens=0, character_symbols=[])
        
        try:
            # Generate embedding for the query
            query_embedding = self._get_embedding(query)
            
            # Use keyword-based search since vector search extensions aren't available
            query_terms = query.lower().split()
            
            if character_id:
                # Search pages by character with keyword matching
                cql_query = """
                SELECT page_id, title, content, symbol_id, page_index, embedding
                FROM pages 
                WHERE symbol_id = %s ALLOW FILTERING
                """
                params = (character_id,)
            else:
                # Get all pages for manual filtering
                cql_query = """
                SELECT page_id, title, content, symbol_id, page_index, embedding
                FROM pages
                """
                params = ()
            
            # Execute search
            result = self.cassandra_session.execute(cql_query, params)
            
            # Collect all pages and calculate similarity manually
            page_scores = []
            for row in result:
                # Calculate text-based relevance score
                content_lower = row.content.lower()
                title_lower = row.title.lower()
                
                # Simple keyword matching score
                content_score = sum(1 for term in query_terms if term in content_lower)
                title_score = sum(2 for term in query_terms if term in title_lower)  # Title matches worth more
                text_score = content_score + title_score
                
                # Add semantic similarity if embeddings available
                if row.embedding and query_embedding:
                    try:
                        # Calculate cosine similarity
                        import numpy as np
                        row_embedding = np.array(row.embedding)
                        query_embedding_np = np.array(query_embedding)
                        
                        dot_product = np.dot(row_embedding, query_embedding_np)
                        norm_row = np.linalg.norm(row_embedding)
                        norm_query = np.linalg.norm(query_embedding_np)
                        
                        if norm_row > 0 and norm_query > 0:
                            semantic_score = dot_product / (norm_row * norm_query)
                        else:
                            semantic_score = 0.0
                    except:
                        semantic_score = 0.0
                else:
                    semantic_score = 0.0
                
                # Combined score (text + semantic)
                total_score = text_score + (semantic_score * 5)  # Weight semantic similarity
                
                if total_score > 0:  # Only include relevant pages
                    page_scores.append((row, total_score))
            
            # Sort by score and take top results
            page_scores.sort(key=lambda x: x[1], reverse=True)
            result = [row for row, score in page_scores[:top_k]]
            
            # Process results and collect snippets
            snippets = []
            page_ids = []
            character_symbols = set()
            total_tokens = 0
            
            for row in result:
                # Extract a relevant snippet from the content
                snippet = self._extract_relevant_snippet(row.content, query)
                
                # Check if adding this snippet would exceed token limit
                snippet_tokens = self.tokenizer.count_tokens(snippet) if self.tokenizer else len(snippet.split())
                
                if total_tokens + snippet_tokens > self.max_context_tokens:
                    # Try to get a shorter snippet
                    snippet = self._truncate_snippet(snippet, self.max_context_tokens - total_tokens)
                    snippet_tokens = self.tokenizer.count_tokens(snippet) if self.tokenizer else len(snippet.split())
                    
                    if snippet_tokens == 0:
                        break
                
                # Add to results
                snippets.append(f"[{row.title}]: {snippet}")
                page_ids.append(row.page_id)
                if row.symbol_id:
                    character_symbols.add(row.symbol_id)
                total_tokens += snippet_tokens
                
                # Stop if we've reached token limit
                if total_tokens >= self.max_context_tokens:
                    break
            
            return RetrievedContext(
                snippets=snippets,
                page_ids=page_ids,
                total_tokens=total_tokens,
                character_symbols=list(character_symbols)
            )
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return RetrievedContext(snippets=[], page_ids=[], total_tokens=0, character_symbols=[])
    
    def _extract_relevant_snippet(self, content: str, query: str, context_window: int = 300) -> str:
        """
        Extract the most relevant snippet from content based on query.
        
        Args:
            content: Full page content
            query: User query
            context_window: Characters to include around match
            
        Returns:
            Relevant snippet
        """
        # Simple approach: find query terms in content
        query_terms = query.lower().split()
        content_lower = content.lower()
        
        # Find best matching position
        best_pos = 0
        best_score = 0
        
        # Sliding window to find densest area of query terms
        window_size = min(len(content), context_window * 2)
        for i in range(0, len(content) - window_size, 50):
            window = content_lower[i:i + window_size]
            score = sum(1 for term in query_terms if term in window)
            if score > best_score:
                best_score = score
                best_pos = i
        
        # Extract snippet around best position
        start = max(0, best_pos)
        end = min(len(content), best_pos + context_window * 2)
        
        snippet = content[start:end].strip()
        
        # Add ellipsis if truncated
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."
            
        return snippet
    
    def _truncate_snippet(self, snippet: str, max_tokens: int) -> str:
        """
        Truncate snippet to fit within token limit.
        
        Args:
            snippet: Text to truncate
            max_tokens: Maximum tokens allowed
            
        Returns:
            Truncated snippet
        """
        if not self.tokenizer or max_tokens <= 0:
            return ""
        
        # Use tokenizer to truncate precisely
        return self.tokenizer.truncate_to_tokens(snippet, max_tokens)
    
    def format_context_for_prompt(self, context: RetrievedContext) -> str:
        """
        Format retrieved context for inclusion in prompt.
        
        Args:
            context: Retrieved context object
            
        Returns:
            Formatted string with <X_READ> marker
        """
        if not context.snippets:
            return ""
        
        formatted = "<X_READ>\n"
        for snippet in context.snippets:
            formatted += f"{snippet}\n\n"
        
        return formatted.strip()


# Singleton instance
_context_service: Optional[ContextRetrievalService] = None


def get_context_retrieval_service() -> ContextRetrievalService:
    """Get or create the singleton context retrieval service."""
    global _context_service
    if _context_service is None:
        _context_service = ContextRetrievalService()
    return _context_service