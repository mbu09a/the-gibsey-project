"""
Custom Gibsey BPE Tokenizer Service

Provides consistent tokenization across all backend services using the 
custom-trained BPE tokenizer with special tokens for QDPI roles and character glyphs.
"""

import logging
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import sentencepiece as spm

logger = logging.getLogger(__name__)

class GibseyTokenizerService:
    """
    Service for custom Gibsey BPE tokenization
    
    Features:
    - Consistent token counting across all services
    - Special token handling for QDPI roles and character glyphs
    - Text chunking for embeddings and context management
    - TNA (Token Network Abstraction) cost calculation
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """Initialize the tokenizer service."""
        
        # Default model path
        if model_path is None:
            project_root = Path(__file__).parent.parent.parent
            model_path = project_root / "tokenizer" / "gibsey_bpe.model"
        
        self.model_path = str(model_path)
        self.tokenizer = None
        
        # TNA cost configuration
        self.tokens_per_tna = 100  # 1 TNA = 100 tokens
        
        # Special tokens for recognition
        self.qdpi_tokens = ["<X_READ>", "<Y_INDEX>", "<A_ASK>", "<Z_RECEIVE>"]
        self.character_tokens = [
            "an-author", "london-fox", "glyph-marrow", "phillip-bafflemint",
            "jacklyn-variance", "oren-progresso", "old-natalie", "princhetta",
            "cop-e-right", "new-natalie", "arieol-owlist", "jack-parlance",
            "manny-valentinas", "shamrock-stillman", "todd-fishbone", "the-author"
        ]
        
        self._load_tokenizer()
    
    def _load_tokenizer(self):
        """Load the SentencePiece tokenizer."""
        try:
            if not os.path.exists(self.model_path):
                logger.warning(f"Gibsey tokenizer model not found at {self.model_path}")
                logger.warning("Falling back to character estimation")
                self.tokenizer = None
                return
            
            self.tokenizer = spm.SentencePieceProcessor()
            self.tokenizer.load(self.model_path)
            
            logger.info(f"Loaded Gibsey BPE tokenizer from {self.model_path}")
            logger.info(f"  Vocab size: {self.tokenizer.get_piece_size()}")
            logger.info(f"  Special tokens: {len(self.qdpi_tokens)} QDPI + {len(self.character_tokens)} characters")
            
        except Exception as e:
            logger.error(f"Failed to load Gibsey tokenizer: {e}")
            logger.warning("Falling back to character estimation")
            self.tokenizer = None
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text using the custom tokenizer."""
        if self.tokenizer:
            try:
                return len(self.tokenizer.encode(text))
            except Exception as e:
                logger.warning(f"Tokenizer encode failed: {e}, falling back to estimation")
        
        # Fallback: estimate based on characters (conservative estimate)
        return len(text) // 3  # Slightly more conservative than tiktoken's ~4 chars/token
    
    def encode(self, text: str) -> List[int]:
        """Encode text to token IDs."""
        if self.tokenizer:
            try:
                return self.tokenizer.encode(text)
            except Exception as e:
                logger.warning(f"Tokenizer encode failed: {e}")
                return []
        
        logger.warning("No tokenizer available for encoding")
        return []
    
    def decode(self, token_ids: List[int]) -> str:
        """Decode token IDs back to text."""
        if self.tokenizer:
            try:
                return self.tokenizer.decode(token_ids)
            except Exception as e:
                logger.warning(f"Tokenizer decode failed: {e}")
                return ""
        
        logger.warning("No tokenizer available for decoding")
        return ""
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into string pieces."""
        if self.tokenizer:
            try:
                return self.tokenizer.encode(text, out_type=str)
            except Exception as e:
                logger.warning(f"Tokenizer tokenize failed: {e}")
                return []
        
        # Fallback: simple whitespace + punctuation split
        import re
        return re.findall(r'\S+', text)
    
    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to maximum number of tokens."""
        if self.tokenizer:
            try:
                token_ids = self.tokenizer.encode(text)
                if len(token_ids) <= max_tokens:
                    return text
                
                truncated_ids = token_ids[:max_tokens]
                return self.tokenizer.decode(truncated_ids)
            except Exception as e:
                logger.warning(f"Tokenizer truncation failed: {e}, falling back to character truncation")
        
        # Fallback: character-based truncation
        estimated_chars = max_tokens * 3
        return text[:estimated_chars]
    
    def chunk_text(self, text: str, max_tokens_per_chunk: int, overlap_tokens: int = 0) -> List[str]:
        """
        Split text into chunks of maximum token size with optional overlap.
        
        Args:
            text: Text to chunk
            max_tokens_per_chunk: Maximum tokens per chunk
            overlap_tokens: Number of tokens to overlap between chunks
            
        Returns:
            List of text chunks
        """
        if not text.strip():
            return []
        
        if self.tokenizer:
            try:
                token_ids = self.tokenizer.encode(text)
                
                if len(token_ids) <= max_tokens_per_chunk:
                    return [text]
                
                chunks = []
                start = 0
                
                while start < len(token_ids):
                    end = min(start + max_tokens_per_chunk, len(token_ids))
                    chunk_ids = token_ids[start:end]
                    chunk_text = self.tokenizer.decode(chunk_ids)
                    chunks.append(chunk_text)
                    
                    # Move start forward, accounting for overlap
                    start = end - overlap_tokens
                    if start >= len(token_ids):
                        break
                
                return chunks
                
            except Exception as e:
                logger.warning(f"Tokenizer chunking failed: {e}, falling back to character chunking")
        
        # Fallback: character-based chunking
        estimated_chars_per_chunk = max_tokens_per_chunk * 3
        overlap_chars = overlap_tokens * 3
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + estimated_chars_per_chunk, len(text))
            chunk = text[start:end]
            chunks.append(chunk)
            
            start = end - overlap_chars
            if start >= len(text):
                break
        
        return chunks
    
    def calculate_tna_cost(self, text: str) -> float:
        """Calculate TNA (Token Network Abstraction) cost for text."""
        token_count = self.count_tokens(text)
        return token_count / self.tokens_per_tna
    
    def has_special_tokens(self, text: str) -> Dict[str, List[str]]:
        """
        Check if text contains special tokens (QDPI or character tokens).
        
        Returns:
            Dict with 'qdpi' and 'character' keys containing found tokens
        """
        found_qdpi = [token for token in self.qdpi_tokens if token in text]
        found_characters = [token for token in self.character_tokens if token in text]
        
        return {
            "qdpi": found_qdpi,
            "character": found_characters
        }
    
    def get_tokenizer_info(self) -> Dict[str, Any]:
        """Get information about the loaded tokenizer."""
        if self.tokenizer:
            return {
                "model_path": self.model_path,
                "vocab_size": self.tokenizer.get_piece_size(),
                "unk_id": self.tokenizer.unk_id(),
                "bos_id": self.tokenizer.bos_id(),
                "eos_id": self.tokenizer.eos_id(),
                "special_tokens": {
                    "qdpi": self.qdpi_tokens,
                    "characters": self.character_tokens
                },
                "tokens_per_tna": self.tokens_per_tna,
                "loaded": True
            }
        else:
            return {
                "model_path": self.model_path,
                "loaded": False,
                "fallback_mode": "character_estimation"
            }

# Global tokenizer service instance
_tokenizer_service = None

def get_tokenizer_service() -> GibseyTokenizerService:
    """Get the global tokenizer service instance."""
    global _tokenizer_service
    if _tokenizer_service is None:
        _tokenizer_service = GibseyTokenizerService()
    return _tokenizer_service

# Convenience functions for direct use
def count_tokens(text: str) -> int:
    """Count tokens using the Gibsey tokenizer."""
    return get_tokenizer_service().count_tokens(text)

def truncate_to_tokens(text: str, max_tokens: int) -> str:
    """Truncate text to max tokens using the Gibsey tokenizer."""
    return get_tokenizer_service().truncate_to_tokens(text, max_tokens)

def chunk_text(text: str, max_tokens_per_chunk: int, overlap_tokens: int = 0) -> List[str]:
    """Chunk text using the Gibsey tokenizer."""
    return get_tokenizer_service().chunk_text(text, max_tokens_per_chunk, overlap_tokens)

def calculate_tna_cost(text: str) -> float:
    """Calculate TNA cost using the Gibsey tokenizer."""
    return get_tokenizer_service().calculate_tna_cost(text)