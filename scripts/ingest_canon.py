#!/usr/bin/env python3
"""Ingest canonical Gibsey pages into Cassandra"""

import os
import sys
import json
import uuid
from pathlib import Path
from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from dotenv import load_dotenv

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from qdpi import encode_symbol, CHARACTER_MAP

# Load environment variables
load_dotenv(Path(__file__).parent.parent / "backend" / ".env")

def load_table_of_contents():
    """Load the table of contents to map pages to sections"""
    toc_path = Path(__file__).parent.parent / "gibsey-canon" / "corpus" / "metadata" / "table_of_contents.json"
    with open(toc_path, 'r') as f:
        return json.load(f)

def load_corpus_pages():
    """Load all pages from the corpus"""
    pages_dir = Path(__file__).parent.parent / "gibsey-canon" / "corpus" / "pages"
    pages = []
    
    for page_file in sorted(pages_dir.glob("*.md")):
        page_num = int(page_file.stem.split("-")[0])
        
        with open(page_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract title from filename
        title_parts = page_file.stem.split("-")[1:]
        title = " ".join(title_parts).replace("-", " ")
        
        pages.append({
            "page_num": page_num,
            "filename": page_file.name,
            "title": title,
            "text": content
        })
    
    return pages

def map_page_to_section(page_num, toc):
    """Map a page number to its section based on TOC"""
    for section in toc["sections"]:
        # Parse page range
        if "-" in section["pages"]:
            start, end = section["pages"].split("-")
            start, end = int(start), int(end)
            if start <= page_num <= end:
                return section["section_number"], section.get("connected_character", "unknown")
    return 1, "an author"  # Default

def get_character_hex(character_name):
    """Get character hex from name"""
    # Normalize character name
    char_map = {
        "an author": 0,
        "London Fox": 1,
        "Glyph Marrow": 2,
        "Phillip Bafflemint": 3,
        "Jacklyn Variance": 4,
        "Oren Progresso": 5,
        "Old Natalie Weissman": 6,
        "Princhetta": 7,
        "Cop E. Right": 8,
        "New Natalie Weissman": 9,
        "Arieol Owlist": 10,
        "Jack Parlance": 11,
        "Manny Valentinas": 12,
        "Shamrock Stillman": 13,
        "Todd Fishbone": 14,
        "The Author": 15
    }
    
    return char_map.get(character_name, 0)

def ingest_canon(dry_run=False):
    """Ingest canonical pages into Cassandra"""
    
    # Load data
    print("Loading corpus data...")
    toc = load_table_of_contents()
    pages = load_corpus_pages()
    print(f"Found {len(pages)} pages to ingest")
    
    if dry_run:
        print("\n[DRY RUN MODE - Not connecting to database]")
        # Just show what would be inserted
        for i, page in enumerate(pages[:5]):  # Show first 5
            section, character = map_page_to_section(page["page_num"], toc)
            char_hex = get_character_hex(character)
            symbol_code = encode_symbol(char_hex, 0)  # XC for canon
            page_id = f"canon-{section:02d}-{page['page_num']:03d}"
            
            print(f"\nPage {page['page_num']}:")
            print(f"  ID: {page_id}")
            print(f"  Section: {section}")
            print(f"  Character: {character} (hex: {char_hex})")
            print(f"  Symbol: {symbol_code} (0x{symbol_code:02X})")
            print(f"  Title: {page['title']}")
            print(f"  Text preview: {page['text'][:100]}...")
        
        print(f"\n... and {len(pages) - 5} more pages")
        return
    
    # Connect to Cassandra
    hosts = os.getenv("CASSANDRA_HOSTS", "localhost:9042").split(",")
    hosts = [h.split(":")[0] for h in hosts]
    keyspace = os.getenv("CASSANDRA_KEYSPACE", "gibsey")
    
    try:
        print(f"Connecting to Cassandra at {hosts}...")
        cluster = Cluster(hosts)
        session = cluster.connect()
        session.execute(f"USE {keyspace}")
        
        # Prepare statements
        insert_page = session.prepare("""
            INSERT INTO pages (
                page_id, char_hex, behavior, symbol_code, section, page_num,
                provenance, orientation, trajectory, text, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """)
        
        insert_edge = session.prepare("""
            INSERT INTO page_edges (page_id, edge_type, target_id, created_at)
            VALUES (?, ?, ?, ?)
        """)
        
        # Insert pages
        print("Inserting pages...")
        page_ids = []
        
        for i, page in enumerate(pages):
            section, character = map_page_to_section(page["page_num"], toc)
            char_hex = get_character_hex(character)
            symbol_code = encode_symbol(char_hex, 0)  # behavior=0 (XC)
            
            page_id = f"canon-{section:02d}-{page['page_num']:03d}"
            page_ids.append(page_id)
            
            # Insert page
            session.execute(insert_page, (
                page_id,
                char_hex,
                0,  # behavior (XC)
                symbol_code,
                section,
                page["page_num"],
                "C",  # provenance (Canon)
                "X",  # orientation (Read)
                "T0", # trajectory (Continue)
                page["text"],
                datetime.utcnow()
            ))
            
            if (i + 1) % 50 == 0:
                print(f"  Inserted {i + 1}/{len(pages)} pages...")
        
        # Create NEXT edges
        print("Creating NEXT edge ring...")
        for i in range(len(page_ids)):
            next_idx = (i + 1) % len(page_ids)  # Wrap around to create ring
            
            session.execute(insert_edge, (
                page_ids[i],
                "NEXT",
                page_ids[next_idx],
                uuid.uuid1()
            ))
        
        print(f"\n✅ Successfully ingested {len(pages)} canon pages!")
        print(f"First page: {page_ids[0]}")
        print(f"Last page: {page_ids[-1]}")
        print("Ring closed: Last page links to first")
        
        cluster.shutdown()
        
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ingest Gibsey canon into Cassandra")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be ingested without connecting to DB")
    parser.add_argument("--from", dest="source", choices=["corpus", "json"], default="corpus",
                       help="Source to ingest from (corpus folder or texts.json)")
    
    args = parser.parse_args()
    ingest_canon(dry_run=args.dry_run)