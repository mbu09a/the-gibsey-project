#!/usr/bin/env python3
"""
Fix character folder mapping issues - some SVGs were copied to wrong folders.
"""

import shutil
from pathlib import Path

def fix_character_mappings():
    """Fix the character folder mappings."""
    characters_dir = Path('/Users/ghostradongus/the-gibsey-project/gibsey-canon/corpus/characters')
    
    # Mappings that need to be corrected
    corrections = [
        # Remove incorrectly named folders and fix symbol IDs
        ('new-natalie-weissman', 'new-natalie'),
        ('old-natalie-weissman', 'old-natalie'),
    ]
    
    for old_name, new_name in corrections:
        old_dir = characters_dir / old_name
        new_dir = characters_dir / new_name
        
        if old_dir.exists():
            if new_dir.exists():
                # Merge contents
                for item in old_dir.iterdir():
                    dest = new_dir / item.name
                    if item.is_file():
                        shutil.copy2(item, dest)
                        print(f"Moved {item.name} from {old_name} to {new_name}")
                
                # Remove old directory
                shutil.rmtree(old_dir)
                print(f"Removed incorrect directory: {old_name}")
            else:
                # Simple rename
                old_dir.rename(new_dir)
                print(f"Renamed {old_name} to {new_name}")

if __name__ == '__main__':
    fix_character_mappings()
    print("Character mapping fixes complete!")