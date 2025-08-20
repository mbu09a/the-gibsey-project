#!/usr/bin/env python3
"""Build QDPI glyph manifest from SVG files or create stub for development"""

import sys
import json
import argparse
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.qdpi_manifest import create_stub_manifest

def build_manifest_from_svgs(glyph_dir: str, output_path: str):
    """Build manifest by scanning actual SVG files (TODO: implement when real glyphs available)"""
    # TODO: This would scan qdpi-256-glyphs/ and map to symbols
    # For now, just create stub
    print(f"WARNING: Real SVG scanning not implemented yet, creating stub manifest")
    return create_stub_manifest(output_path)

def main():
    parser = argparse.ArgumentParser(description="Build QDPI glyph manifest")
    parser.add_argument("--glyph-dir", default="qdpi-256-glyphs", 
                       help="Directory containing SVG glyphs")
    parser.add_argument("--output", default="public/qdpi_glyph_manifest.json",
                       help="Output manifest file")
    parser.add_argument("--stub", action="store_true",
                       help="Create stub manifest for development")
    
    args = parser.parse_args()
    
    if args.stub:
        print("Creating stub manifest for development...")
        manifest = create_stub_manifest(args.output)
    else:
        print(f"Building manifest from {args.glyph_dir}...")
        manifest = build_manifest_from_svgs(args.glyph_dir, args.output)
    
    print(f"✅ Manifest created: {args.output}")
    print(f"   Version: {manifest.version}")
    print(f"   Glyphs: {manifest.count}")
    print(f"   Timestamp: {manifest.timestamp}")
    
    # Validate by reloading
    from app.qdpi_manifest import load_manifest
    try:
        reloaded = load_manifest(args.output)
        print(f"✅ Validation passed: {len(reloaded.glyphs)} glyphs loaded")
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()