#!/usr/bin/env python3
"""
Ingest all pages from The Entrance Way (texts.json) into Jacklyn's memory.
Each page becomes a "novel-recollection" memory entry.
"""

import json
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.ai.memory.embedding_store import EmbeddingStore

def load_texts_json():
    """Load the texts.json file containing all 710 pages"""
    texts_path = Path(__file__).parent.parent.parent / "assets" / "texts.json"
    with open(texts_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def page_already_exists(store, page_num):
    """Check if a page is already in memory to enable resumability"""
    # Search for exact page number match
    existing = store.search(
        f"page {page_num}", 
        k=1000,  # Search through many results
        filters={"page_num": page_num, "author": "jacklyn-variance"}
    )
    return len(existing) > 0

def ingest_entrance_way():
    """Main ingestion function"""
    print("🧠 Starting ingestion of The Entrance Way into Jacklyn's memory...")
    
    # Initialize the embedding store
    store = EmbeddingStore()
    
    # Load all pages
    pages = load_texts_json()
    total_pages = len(pages)
    print(f"📚 Found {total_pages} pages to process")
    
    # Track progress
    imported = 0
    skipped = 0
    
    for idx, page in enumerate(pages):
        page_num = idx + 1  # 1-indexed
        
        # Check if already imported (for resumability)
        if page_already_exists(store, page_num):
            skipped += 1
            continue
        
        # Extract page content
        content = page.get("text", "")
        if not content:
            print(f"⚠️  Skipping page {page_num} - no content")
            continue
        
        # Build metadata
        meta = {
            "author": "jacklyn-variance",
            "source": "the-entrance-way",
            "memory_type": "novel-recollection",
            "page_num": page_num,
            "title": page.get("title", ""),
            "section": page.get("section", ""),
            "symbol": page.get("symbolId", ""),
            "tags": ["novel", "memory", "the-entrance-way"],
            "comment": "Jacklyn is recalling a passage from The Entrance Way",
            # Additional useful fields
            "chapter": page.get("chapter", ""),
            "part": page.get("part", ""),
            "corpus": page.get("symbolId", "unknown"),  # Which character's section
            "word_count": len(content.split()),
            "char_count": len(content)
        }
        
        # Remove empty string values from metadata
        meta = {k: v for k, v in meta.items() if v != ""}
        
        # Add to memory
        try:
            store.add(content, meta)
            imported += 1
            
            # Progress update every 25 pages
            if imported % 25 == 0:
                print(f"📝 Imported {imported}/{total_pages} pages...")
                
        except Exception as e:
            print(f"❌ Error importing page {page_num}: {e}")
            continue
    
    # Final summary
    print(f"\n✅ Import complete!")
    print(f"   - Imported: {imported} pages")
    print(f"   - Skipped (already exists): {skipped} pages")
    print(f"   - Total in memory: {len(store.entries)} entries")
    
    # Quick verification - search for a sample
    print(f"\n🔍 Quick verification - searching for 'Jacklyn'...")
    results = store.search("Jacklyn", k=3, filters={"author": "jacklyn-variance"})
    print(f"   Found {len(results)} relevant memories")
    if results:
        print(f"   Top match: {results[0][1]:.3f} similarity")

if __name__ == "__main__":
    ingest_entrance_way()