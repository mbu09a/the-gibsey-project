#!/usr/bin/env python3
"""
Validate the QDPI-256 glyph manifest for coverage, duplicates,
and consistency with asset filenames.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST = ROOT / "public/qdpi/qdpi_glyph_manifest.json"
GLYPH_DIR = ROOT / "public/qdpi-256-glyphs"

def main():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert len(data) == 256, f"Expected 256 entries, got {len(data)}"
    ids = sorted(r["glyph_id"] for r in data)
    assert ids == list(range(256)), "glyph_id coverage must be 0..255"
    # Check per-character grouping
    from collections import Counter
    cnt = Counter(r["char_slug"] for r in data)
    errors = []
    for slug, num in cnt.items():
        if num != 16:
            errors.append(f"{slug} has {num} entries (expected 16)")
    assert not errors, "Per-character counts invalid: " + "; ".join(errors)
    # Check file presence
    missing = [r["filename"] for r in data if not (GLYPH_DIR / r["filename"]).exists()]
    assert not missing, f"Missing files: {missing[:5]}{'...' if len(missing)>5 else ''}"
    print("Manifest validation passed: 256 glyphs, filenames exist, distribution correct.")

if __name__ == '__main__':
    main()