#!/usr/bin/env python3
"""
Script to freeze and restructure the Gibsey corpus from monolithic JSON to modular files.
Reads src/assets/texts.json and outputs:
- Individual markdown files for each page
- Metadata JSON files
- Master index linking pages to symbols/characters
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any

def slugify(text: str) -> str:
    """Convert text to filename-safe slug."""
    # Remove special characters and convert to lowercase
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    # Replace spaces with hyphens
    slug = re.sub(r'[-\s]+', '-', slug)
    # Remove leading/trailing hyphens
    return slug.strip('-')

def load_texts_json(filepath: str) -> List[Dict]:
    """Load the texts.json file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_page_as_markdown(page: Dict, output_dir: Path, file_counter: int) -> str:
    """
    Save a single page's text content as a markdown file.
    Returns the filename created.
    """
    # Use the file counter to ensure unique filenames, not pageIndex which has duplicates
    page_id = page.get('id', f'page_{file_counter}')
    title = page.get('title', 'Untitled')
    slug = slugify(title)[:50]  # Limit slug length
    
    # Use file counter (sequential position in array) for unique numbering
    filename = f"{file_counter:03d}-{slug}.md"
    filepath = output_dir / filename
    
    # Extract just the text content
    text_content = page.get('text', '')
    
    # Write the markdown file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text_content)
    
    return filename

def extract_metadata(page: Dict, filename: str) -> Dict:
    """Extract all non-text fields from a page for metadata."""
    metadata = {}
    
    # Copy all fields except 'text'
    for key, value in page.items():
        if key != 'text':
            metadata[key] = value
    
    # Add the filename reference
    metadata['filename'] = filename
    
    return metadata

def build_symbol_index(pages_metadata: List[Dict]) -> Dict:
    """Build an index mapping symbols to their pages and characteristics."""
    symbols = {}
    
    for page in pages_metadata:
        symbol_id = page.get('symbolId')
        if not symbol_id:
            continue
            
        if symbol_id not in symbols:
            symbols[symbol_id] = {
                'title': '',  # Will be set from first page or character data
                'color': page.get('color', '#FFFFFF'),
                'characterDir': f"characters/{symbol_id}",
                'pages': []
            }
        
        # Add page to symbol's page list
        page_index = page.get('pageIndex', 0)
        symbols[symbol_id]['pages'].append(page_index)
        
        # Set title from section name if available
        if not symbols[symbol_id]['title'] and page.get('section'):
            symbols[symbol_id]['title'] = page.get('section')
    
    # Sort page lists
    for symbol in symbols.values():
        symbol['pages'].sort()
    
    return {'symbols': symbols}

def main():
    """Main execution function."""
    # Setup paths
    project_root = Path('/Users/ghostradongus/the-gibsey-project')
    texts_json_path = project_root / 'src' / 'assets' / 'texts.json'
    canon_dir = project_root / 'gibsey-canon' / 'corpus'
    pages_dir = canon_dir / 'pages'
    metadata_dir = canon_dir / 'metadata'
    
    # Create directories if they don't exist
    pages_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)
    
    print("Loading texts.json...")
    pages = load_texts_json(texts_json_path)
    print(f"Found {len(pages)} pages to process")
    
    # Process each page
    pages_metadata = []
    for i, page in enumerate(pages):
        # Save page content as markdown (use i+1 for 1-based numbering)
        filename = save_page_as_markdown(page, pages_dir, i + 1)
        
        # Extract metadata
        metadata = extract_metadata(page, filename)
        pages_metadata.append(metadata)
        
        if (i + 1) % 50 == 0:
            print(f"Processed {i + 1} pages...")
    
    print(f"\nCreated {len(pages_metadata)} markdown files in {pages_dir}")
    
    # Save pages metadata
    pages_json_path = metadata_dir / 'pages.json'
    with open(pages_json_path, 'w', encoding='utf-8') as f:
        json.dump(pages_metadata, f, indent=2, ensure_ascii=False)
    print(f"Saved metadata to {pages_json_path}")
    
    # Build and save symbol index
    symbol_index = build_symbol_index(pages_metadata)
    index_path = canon_dir / 'index.json'
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(symbol_index, f, indent=2, ensure_ascii=False)
    print(f"Created symbol index at {index_path}")
    
    # Print summary
    print("\nSummary:")
    print(f"- Pages processed: {len(pages_metadata)}")
    print(f"- Symbols found: {len(symbol_index['symbols'])}")
    print("\nSymbols:")
    for symbol_id, data in sorted(symbol_index['symbols'].items()):
        print(f"  - {symbol_id}: {len(data['pages'])} pages")

if __name__ == '__main__':
    main()