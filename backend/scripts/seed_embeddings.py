#!/usr/bin/env python3
"""
Gibsey Embeddings Seeder

Reads all corpus pages and populates Cassandra vector store with embeddings.
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
import re

import numpy as np
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import openai
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from backend.app.tokenizer_service import get_tokenizer_service
    TOKENIZER_AVAILABLE = True
except ImportError:
    TOKENIZER_AVAILABLE = False
    print("⚠️ Warning: Tokenizer service not available, using fallback")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "localhost")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", "9042"))
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "gibsey_network")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")

class EmbeddingsSeeder:
    """Seed Cassandra vector store with corpus embeddings."""
    
    def __init__(self):
        """Initialize the seeder with required services."""
        self.session = None
        self.embedding_model = None
        self.tokenizer_service = None
        self.corpus_path = None
        self.processed_count = 0
        self.skipped_count = 0
        self.error_count = 0
        
    def connect_cassandra(self):
        """Connect to Cassandra cluster."""
        logger.info(f"Connecting to Cassandra at {CASSANDRA_HOST}:{CASSANDRA_PORT}")
        
        cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
        self.session = cluster.connect(CASSANDRA_KEYSPACE)
        
        logger.info("✓ Connected to Cassandra")
        
    def initialize_embedding_model(self):
        """Initialize the embedding model (OpenAI or local)."""
        if OPENAI_API_KEY:
            openai.api_key = OPENAI_API_KEY
            self.embedding_model = "openai"
            logger.info(f"✓ Using OpenAI embedding model: {EMBED_MODEL}")
        else:
            logger.info("Loading local sentence transformer model...")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✓ Loaded local sentence transformer")
    
    def initialize_tokenizer(self):
        """Initialize the Gibsey tokenizer service."""
        if TOKENIZER_AVAILABLE:
            self.tokenizer_service = get_tokenizer_service()
            logger.info("✓ Gibsey tokenizer service loaded")
        else:
            logger.warning("⚠️ Tokenizer service not available")
    
    def find_corpus_path(self) -> Path:
        """Find the corpus pages directory."""
        project_root = Path(__file__).parent.parent
        
        # Try different possible locations
        possible_paths = [
            project_root / "gibsey-canon" / "corpus" / "pages",
            project_root / "corpus" / "pages",
            project_root / "src" / "assets" / "pages"
        ]
        
        for path in possible_paths:
            if path.exists() and path.is_dir():
                logger.info(f"✓ Found corpus at: {path}")
                return path
                
        raise FileNotFoundError("Could not find corpus pages directory")
    
    def extract_metadata_from_filename(self, filename: str) -> Dict[str, Any]:
        """Extract metadata from page filename."""
        # Expected format: 001-page-title-slug.md
        match = re.match(r'(\d+)-(.+)\.md$', filename)
        if match:
            page_index = int(match.group(1))
            title_slug = match.group(2).replace('-', ' ').title()
            return {
                "page_index": page_index,
                "title": title_slug,
                "page_id": filename.replace('.md', '')
            }
        else:
            # Fallback for non-standard filenames
            return {
                "page_index": 0,
                "title": filename.replace('.md', '').replace('-', ' ').title(),
                "page_id": filename.replace('.md', '')
            }
    
    def extract_character_symbol(self, content: str) -> Optional[str]:
        """Extract character symbol ID from page content."""
        # Look for character mentions in the text
        character_patterns = [
            "an-author", "london-fox", "glyph-marrow", "phillip-bafflemint",
            "jacklyn-variance", "oren-progresso", "old-natalie", "princhetta",
            "cop-e-right", "new-natalie", "arieol-owlist", "jack-parlance",
            "manny-valentinas", "shamrock-stillman", "todd-fishbone", "the-author"
        ]
        
        content_lower = content.lower()
        for pattern in character_patterns:
            # Look for character name patterns (allowing for variations)
            name_variant = pattern.replace('-', ' ')
            if pattern in content_lower or name_variant in content_lower:
                return pattern
                
        return None
    
    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text."""
        if self.embedding_model == "openai":
            try:
                response = openai.embeddings.create(
                    model=EMBED_MODEL,
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
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text using Gibsey tokenizer or fallback."""
        if self.tokenizer_service:
            return self.tokenizer_service.count_tokens(text)
        else:
            # Fallback: rough estimate
            return len(text.split()) * 1.3  # Approximate subword factor
    
    def page_exists(self, page_id: str) -> bool:
        """Check if page already exists in database."""
        query = "SELECT page_id FROM pages WHERE page_id = %s"
        result = self.session.execute(query, (page_id,))
        return result.one() is not None
    
    def process_page(self, page_path: Path) -> bool:
        """Process a single page file and insert into database."""
        try:
            # Read page content
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                logger.warning(f"Empty page: {page_path.name}")
                return False
            
            # Extract metadata
            metadata = self.extract_metadata_from_filename(page_path.name)
            page_id = metadata["page_id"]
            
            # Check if already processed
            if self.page_exists(page_id):
                logger.debug(f"Skipping existing page: {page_id}")
                self.skipped_count += 1
                return True
            
            # Extract character symbol
            symbol_id = self.extract_character_symbol(content)
            
            # Count tokens
            token_count = int(self.count_tokens(content))
            
            # Generate embedding
            logger.debug(f"Generating embedding for: {page_id}")
            embedding = self.get_embedding(content)
            
            # Insert into database
            insert_query = """
            INSERT INTO pages (page_id, symbol_id, title, page_index, tokens, content, embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            self.session.execute(insert_query, (
                page_id,
                symbol_id,
                metadata["title"],
                metadata["page_index"],
                token_count,
                content,
                embedding
            ))
            
            self.processed_count += 1
            logger.info(f"✓ Processed page {self.processed_count}: {page_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing {page_path.name}: {e}")
            self.error_count += 1
            return False
    
    def run(self, incremental: bool = True):
        """Run the seeding process."""
        logger.info("Starting Gibsey embeddings seeding process")
        
        try:
            # Initialize services
            self.connect_cassandra()
            self.initialize_embedding_model()
            self.initialize_tokenizer()
            
            # Find corpus
            corpus_path = self.find_corpus_path()
            
            # Get all markdown files
            md_files = list(corpus_path.glob("*.md"))
            logger.info(f"Found {len(md_files)} markdown files to process")
            
            if not md_files:
                logger.error("No markdown files found in corpus directory")
                return False
            
            # Process files
            start_time = time.time()
            
            for i, page_path in enumerate(sorted(md_files), 1):
                logger.debug(f"Processing {i}/{len(md_files)}: {page_path.name}")
                
                success = self.process_page(page_path)
                
                # Rate limiting for OpenAI API
                if self.embedding_model == "openai" and success:
                    time.sleep(0.1)  # 10 requests per second max
                
                # Progress logging
                if i % 50 == 0:
                    elapsed = time.time() - start_time
                    rate = i / elapsed
                    remaining = (len(md_files) - i) / rate if rate > 0 else 0
                    logger.info(f"Progress: {i}/{len(md_files)} ({i/len(md_files)*100:.1f}%) "
                              f"- {rate:.1f} pages/sec - ETA: {remaining/60:.1f} min")
            
            # Final statistics
            elapsed = time.time() - start_time
            logger.info("=" * 60)
            logger.info("SEEDING COMPLETE")
            logger.info(f"Total time: {elapsed/60:.1f} minutes")
            logger.info(f"Pages processed: {self.processed_count}")
            logger.info(f"Pages skipped: {self.skipped_count}")
            logger.info(f"Errors: {self.error_count}")
            logger.info(f"Processing rate: {len(md_files)/elapsed:.1f} pages/sec")
            
            return self.error_count == 0
            
        except Exception as e:
            logger.error(f"Fatal error in seeding process: {e}")
            return False
        finally:
            if self.session:
                self.session.shutdown()

def main():
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Seed Gibsey corpus embeddings into Cassandra")
    parser.add_argument("--full", action="store_true", 
                       help="Full reseed (ignore existing pages)")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug logging")
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    seeder = EmbeddingsSeeder()
    success = seeder.run(incremental=not args.full)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()