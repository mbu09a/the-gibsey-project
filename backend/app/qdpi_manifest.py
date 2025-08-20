"""QDPI Glyph Manifest loader and validation"""

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import List, Dict, Any
from pydantic import BaseModel, Field, validator

# 16 behaviors: 4 orientations × 4 provenances
BEHAVIOR_NAMES = [
    "XC", "XP", "XU", "XS",  # Read: Canon, Parallel, User, System
    "YC", "YP", "YU", "YS",  # Index: Canon, Parallel, User, System  
    "AC", "AP", "AU", "AS",  # Ask: Canon, Parallel, User, System
    "ZC", "ZP", "ZU", "ZS"   # Receive: Canon, Parallel, User, System
]

# Character colors for UI (16 distinct colors)
CHARACTER_COLORS = [
    "#FF6B6B",  # an author - red
    "#4ECDC4",  # london-fox - teal
    "#45B7D1",  # glyph-marrow - blue
    "#96CEB4",  # phillip-bafflemint - mint
    "#FFEAA7",  # jacklyn-variance - yellow
    "#DDA0DD",  # oren-progresso - plum
    "#98D8C8",  # old-natalie-weissman - seafoam
    "#F7DC6F",  # princhetta - gold
    "#BB8FCE",  # cop-e-right - lavender
    "#85C1E9",  # new-natalie-weissman - sky blue
    "#F8C471",  # arieol-owlist - orange
    "#82E0AA",  # jack-parlance - light green
    "#F1948A",  # manny-valentinas - salmon
    "#AED6F1",  # shamrock-stillman - powder blue
    "#D2B4DE",  # todd-fishbone - lilac
    "#A569BD"   # the-author - purple
]

class Glyph(BaseModel):
    """Single glyph entry in the manifest"""
    glyph_id: int = Field(ge=0, le=255, description="Symbol code (0-255)")
    hex: str = Field(pattern=r"^0x[0-9A-F]{2}$", description="Hex representation")
    char_hex: int = Field(ge=0, le=15, description="Character index (0-15)")
    char_name: str = Field(min_length=1, description="Character name")
    behavior: int = Field(ge=0, le=15, description="Behavior index (0-15)")
    behavior_name: str = Field(pattern=r"^[XYAZ][CPUS]$", description="Behavior notation")
    rotation: int = Field(ge=0, le=270, description="SVG rotation degrees")
    filename: str = Field(min_length=1, description="SVG filename")
    url: str = Field(min_length=1, description="Relative URL to SVG")
    
    @validator("hex")
    def hex_matches_id(cls, v, values):
        if "glyph_id" in values:
            expected = f"0x{values['glyph_id']:02X}"
            assert v == expected, f"Hex {v} doesn't match glyph_id {values['glyph_id']}"
        return v
    
    @validator("behavior_name")
    def behavior_name_matches_index(cls, v, values):
        if "behavior" in values:
            expected = BEHAVIOR_NAMES[values["behavior"]]
            assert v == expected, f"Behavior name {v} doesn't match index {values['behavior']}"
        return v

class Character(BaseModel):
    """Character metadata for UI"""
    char_hex: int = Field(ge=0, le=15)
    name: str
    color: str = Field(pattern=r"^#[0-9A-F]{6}$")
    glyph_count: int = Field(ge=16, le=16)  # Each character has exactly 16 behaviors

class Manifest(BaseModel):
    """Complete QDPI glyph manifest"""
    version: str = "v1.0"
    count: int = Field(ge=256, le=256)
    timestamp: str = Field(description="Generation timestamp")
    glyphs: List[Glyph] = Field(min_items=256, max_items=256)
    
    @validator("glyphs")
    def validate_complete_coverage(cls, v):
        """Ensure we have exactly 256 unique glyphs covering all symbol codes"""
        if len(v) != 256:
            raise ValueError(f"Must have exactly 256 glyphs, got {len(v)}")
            
        ids = [g.glyph_id for g in v]
        if len(set(ids)) != 256:
            raise ValueError("Glyph IDs must be unique")
            
        if set(ids) != set(range(256)):
            missing = set(range(256)) - set(ids)
            raise ValueError(f"Missing glyph IDs: {sorted(missing)[:10]}...")
            
        # Validate character/behavior distribution
        char_behavior_pairs = set()
        for g in v:
            pair = (g.char_hex, g.behavior)
            if pair in char_behavior_pairs:
                raise ValueError(f"Duplicate char_hex/behavior pair: {pair}")
            char_behavior_pairs.add(pair)
            
        # Should have 16 chars × 16 behaviors = 256 combinations
        expected_pairs = {(c, b) for c in range(16) for b in range(16)}
        if char_behavior_pairs != expected_pairs:
            raise ValueError("Incomplete character/behavior coverage")
            
        return v

def get_character_metadata() -> List[Character]:
    """Get metadata for all 16 characters"""
    from qdpi.symbols import CHARACTER_MAP
    
    characters = []
    for char_hex in range(16):
        characters.append(Character(
            char_hex=char_hex,
            name=CHARACTER_MAP[char_hex],
            color=CHARACTER_COLORS[char_hex],
            glyph_count=16
        ))
    
    return characters

@lru_cache(maxsize=1)
def load_manifest(manifest_path: str) -> Manifest:
    """Load and validate the QDPI glyph manifest"""
    path = Path(manifest_path)
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return Manifest(**data)

def create_stub_manifest(output_path: str = "public/qdpi_glyph_manifest.json") -> Manifest:
    """Create a stub manifest for development (when real glyphs aren't available)"""
    from datetime import datetime
    from qdpi.symbols import CHARACTER_MAP
    
    glyphs = []
    
    for glyph_id in range(256):
        char_hex = (glyph_id >> 4) & 0xF
        behavior = glyph_id & 0xF
        
        char_name = CHARACTER_MAP[char_hex].replace(" ", "_").replace("-", "_")
        behavior_name = BEHAVIOR_NAMES[behavior]
        
        # Map behavior to rotation (simplified)
        rotation_map = {"X": 0, "Y": 90, "A": 180, "Z": 270}
        orientation = behavior_name[0]
        rotation = rotation_map[orientation]
        
        # Generate filename
        if rotation == 0:
            filename = f"{char_name}.svg"
        else:
            filename = f"{char_name}_{rotation}.svg"
            
        glyph = Glyph(
            glyph_id=glyph_id,
            hex=f"0x{glyph_id:02X}",
            char_hex=char_hex,
            char_name=CHARACTER_MAP[char_hex],
            behavior=behavior,
            behavior_name=behavior_name,
            rotation=rotation,
            filename=filename,
            url=f"/qdpi-256-glyphs/{filename}"
        )
        glyphs.append(glyph)
    
    manifest = Manifest(
        count=256,
        timestamp=datetime.utcnow().isoformat() + "Z",
        glyphs=glyphs
    )
    
    # Save to file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(manifest.dict(), f, indent=2)
    
    return manifest