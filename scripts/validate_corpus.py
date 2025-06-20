#!/usr/bin/env python3
"""
Corpus validation script for CI.
Validates consistency between pages, metadata, and character data.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict

def load_json_file(filepath: Path) -> Dict:
    """Load and parse a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"✗ Error loading {filepath}: {e}")
        sys.exit(1)

def validate_pages_metadata() -> List[str]:
    """Validate pages metadata consistency."""
    errors = []
    
    # Load metadata
    metadata_path = Path('gibsey-canon/corpus/metadata/pages.json')
    if not metadata_path.exists():
        errors.append("Missing pages.json metadata file")
        return errors
    
    metadata = load_json_file(metadata_path)
    pages_dir = Path('gibsey-canon/corpus/pages')
    
    # Check that each metadata entry has a corresponding page file
    for page in metadata:
        page_index = page.get('pageIndex', 0)
        filename = page.get('filename', '')
        
        if not filename:
            errors.append(f"Page {page_index} missing filename in metadata")
            continue
            
        page_file = pages_dir / filename
        if not page_file.exists():
            errors.append(f"Missing page file: {filename} (referenced in metadata)")
    
    # Check that each page file has metadata
    if pages_dir.exists():
        page_files = list(pages_dir.glob('*.md'))
        metadata_filenames = {page.get('filename') for page in metadata}
        
        for page_file in page_files:
            if page_file.name not in metadata_filenames:
                errors.append(f"Page file {page_file.name} has no metadata entry")
    
    return errors

def validate_index_consistency() -> List[str]:
    """Validate index.json consistency."""
    errors = []
    
    # Load index
    index_path = Path('gibsey-canon/corpus/index.json')
    if not index_path.exists():
        errors.append("Missing index.json file")
        return errors
    
    index = load_json_file(index_path)
    symbols = index.get('symbols', {})
    
    # Load pages metadata for cross-reference
    metadata_path = Path('gibsey-canon/corpus/metadata/pages.json')
    if metadata_path.exists():
        metadata = load_json_file(metadata_path)
        
        # Check that all symbolIds in metadata exist in index
        metadata_symbols = {page.get('symbolId') for page in metadata if page.get('symbolId')}
        index_symbols = set(symbols.keys())
        
        missing_from_index = metadata_symbols - index_symbols
        missing_from_metadata = index_symbols - metadata_symbols
        
        for symbol in missing_from_index:
            errors.append(f"Symbol '{symbol}' found in pages but missing from index")
        
        for symbol in missing_from_metadata:
            errors.append(f"Symbol '{symbol}' in index but not found in any pages")
    
    # Validate character directories exist
    characters_dir = Path('gibsey-canon/corpus/characters')
    for symbol_id, symbol_data in symbols.items():
        char_dir = characters_dir / symbol_id
        if not char_dir.exists():
            errors.append(f"Character directory missing: {symbol_id}")
    
    return errors

def validate_character_structures() -> List[str]:
    """Validate character folder structures."""
    errors = []
    
    characters_dir = Path('gibsey-canon/corpus/characters')
    if not characters_dir.exists():
        errors.append("Missing characters directory")
        return errors
    
    # Load index to get expected characters
    index_path = Path('gibsey-canon/corpus/index.json')
    if index_path.exists():
        index = load_json_file(index_path)
        expected_chars = set(index.get('symbols', {}).keys())
    else:
        expected_chars = set()
    
    # Check each character directory
    for char_dir in characters_dir.iterdir():
        if not char_dir.is_dir():
            continue
            
        symbol_id = char_dir.name
        
        # Check required files
        required_files = ['symbol.svg', 'info.json']
        for req_file in required_files:
            file_path = char_dir / req_file
            if not file_path.exists():
                errors.append(f"Missing {req_file} for character {symbol_id}")
        
        # Validate info.json structure
        info_path = char_dir / 'info.json'
        if info_path.exists():
            try:
                info = load_json_file(info_path)
                required_fields = ['symbolId', 'color']
                for field in required_fields:
                    if field not in info:
                        errors.append(f"Missing '{field}' in info.json for {symbol_id}")
                        
                # Check symbolId matches directory name
                if info.get('symbolId') != symbol_id:
                    errors.append(f"symbolId mismatch in {symbol_id}/info.json")
                        
            except Exception as e:
                errors.append(f"Invalid JSON in {symbol_id}/info.json: {e}")
    
    return errors

def main():
    """Run all validation checks."""
    print("🔍 Validating Gibsey corpus structure...")
    
    all_errors = []
    
    # Run validation checks
    print("Checking pages metadata...")
    all_errors.extend(validate_pages_metadata())
    
    print("Checking index consistency...")
    all_errors.extend(validate_index_consistency())
    
    print("Checking character structures...")
    all_errors.extend(validate_character_structures())
    
    # Report results
    if all_errors:
        print("\n❌ Validation failed with errors:")
        for error in all_errors:
            print(f"  ✗ {error}")
        sys.exit(1)
    else:
        print("\n✅ All validation checks passed!")
        print("📊 Corpus structure is valid and consistent.")

if __name__ == '__main__':
    main()