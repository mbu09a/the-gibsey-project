#!/usr/bin/env python3
"""
Script to consolidate character symbols, colors, and first principles documents
into the gibsey-canon character folders structure.
"""

import json
import shutil
from pathlib import Path
import re

def load_colors_map():
    """Extract colors from the TypeScript colors file."""
    colors_path = Path('/Users/ghostradongus/the-gibsey-project/src/assets/colors.ts')
    colors = {}
    
    if colors_path.exists():
        with open(colors_path, 'r') as f:
            content = f.read()
        
        # Parse the symbolColors object using regex
        symbol_colors_match = re.search(r'export const symbolColors[^{]*{([^}]+)}', content, re.DOTALL)
        if symbol_colors_match:
            colors_content = symbol_colors_match.group(1)
            
            # Extract key-value pairs
            for line in colors_content.split(','):
                line = line.strip()
                if ':' in line:
                    # Parse "symbol-id": "#color" format
                    parts = line.split(':')
                    if len(parts) >= 2:
                        key = parts[0].strip().strip('"\'')
                        value = parts[1].strip().strip('"\'').rstrip(',')
                        colors[key] = value
    
    return colors

def find_character_docs():
    """Find all first principles documents."""
    docs_dir = Path('/Users/ghostradongus/the-gibsey-project/docs/characters')
    docs = {}
    
    if docs_dir.exists():
        for doc_file in docs_dir.glob('*.md'):
            # Extract character name from filename
            # Convert london_fox_first_principles.md -> london-fox
            name = doc_file.stem
            name = re.sub(r'_first_principles$', '', name)
            name = name.replace('_', '-')
            docs[name] = doc_file
    
    return docs

def copy_svg_symbols():
    """Copy SVG symbols to character folders."""
    svg_dir = Path('/Users/ghostradongus/the-gibsey-project/public/corpus-symbols')
    characters_dir = Path('/Users/ghostradongus/the-gibsey-project/gibsey-canon/corpus/characters')
    
    svg_mapping = {}
    
    if svg_dir.exists():
        for svg_file in svg_dir.glob('*.svg'):
            # Map SVG filenames to symbol IDs
            # Many SVGs may need manual mapping, but let's try common patterns
            filename = svg_file.stem.lower()
            
            # Common mappings
            symbol_mappings = {
                'london_fox': 'london-fox',
                'jacklyn_variance': 'jacklyn-variance',
                'cop_e_right': 'cop-e-right',
                'todd_fishbone': 'todd-fishbone',
                'jack_parlance': 'jack-parlance',
                'shamrock_stillman': 'shamrock-stillman',
                'arieol_owlist': 'arieol-owlist',
                'oren_progresso': 'oren-progresso',
                'phillip_bafflemint': 'phillip-bafflemint',
                'manny_valentinas': 'manny-valentinas',
                'glyph_marrow': 'glyph-marrow',
                'new_natalie': 'new-natalie',
                'old_natalie': 'old-natalie',
                'the_author': 'the-author',
                'an_author': 'an-author',
                'princhetta': 'princhetta'
            }
            
            symbol_id = symbol_mappings.get(filename, filename.replace('_', '-'))
            
            # Create character directory
            char_dir = characters_dir / symbol_id
            char_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy SVG file
            dest_svg = char_dir / 'symbol.svg'
            shutil.copy2(svg_file, dest_svg)
            
            svg_mapping[symbol_id] = svg_file.name
            print(f"Copied {svg_file.name} -> {symbol_id}/symbol.svg")
    
    return svg_mapping

def consolidate_character_info():
    """Main function to consolidate all character information."""
    # Load existing data
    colors = load_colors_map()
    docs = find_character_docs()
    
    # Copy SVG symbols
    svg_mapping = copy_svg_symbols()
    
    # Load symbol index to get all character IDs
    index_path = Path('/Users/ghostradongus/the-gibsey-project/gibsey-canon/corpus/index.json')
    if index_path.exists():
        with open(index_path, 'r') as f:
            index = json.load(f)
        symbols = index.get('symbols', {})
    else:
        symbols = {}
    
    characters_dir = Path('/Users/ghostradongus/the-gibsey-project/gibsey-canon/corpus/characters')
    
    # Process each symbol/character
    for symbol_id in symbols.keys():
        char_dir = characters_dir / symbol_id
        char_dir.mkdir(parents=True, exist_ok=True)
        
        # Create info.json with character metadata
        info = {
            'symbolId': symbol_id,
            'color': colors.get(symbol_id, '#FFFFFF'),
            'pages': len(symbols[symbol_id].get('pages', [])),
            'svgFile': svg_mapping.get(symbol_id, ''),
            'hasFirstPrinciples': symbol_id in docs
        }
        
        info_path = char_dir / 'info.json'
        with open(info_path, 'w') as f:
            json.dump(info, f, indent=2)
        
        # Copy first principles document if it exists
        if symbol_id in docs:
            dest_doc = char_dir / 'first_principles.md'
            shutil.copy2(docs[symbol_id], dest_doc)
            print(f"Copied first principles for {symbol_id}")
        else:
            print(f"No first principles found for {symbol_id}")
    
    print(f"\nConsolidated {len(symbols)} characters")
    print(f"Colors mapped: {len(colors)}")
    print(f"Docs found: {len(docs)}")
    print(f"SVGs copied: {len(svg_mapping)}")

def consolidate_documentation():
    """Copy high-level documentation to gibsey-canon."""
    docs_source = Path('/Users/ghostradongus/the-gibsey-project/docs')
    docs_dest = Path('/Users/ghostradongus/the-gibsey-project/gibsey-canon/documentation')
    
    # Files to copy
    docs_to_copy = [
        'architecture.md',
        'gibsey_first_principles.md',
        'README.md'
    ]
    
    for doc_name in docs_to_copy:
        source_file = docs_source / doc_name
        if source_file.exists():
            dest_file = docs_dest / doc_name
            shutil.copy2(source_file, dest_file)
            print(f"Copied {doc_name} to documentation/")

if __name__ == '__main__':
    print("Consolidating character information...")
    consolidate_character_info()
    
    print("\nConsolidating documentation...")
    consolidate_documentation()
    
    print("\nCharacter consolidation complete!")