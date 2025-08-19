#!/usr/bin/env python3
"""
Build the QDPI-256 glyph manifest by scanning the SVG asset directory,
parsing metadata, and joining character colors.
"""
import json
import re
from pathlib import Path

# Project root: two levels up from this script
ROOT = Path(__file__).resolve().parent.parent.parent
GLYPH_DIR = ROOT / "public/qdpi-256-glyphs"
MANIFEST_OUT = ROOT / "public/qdpi/qdpi_glyph_manifest.json"
COLORS_TS = ROOT / "src/assets/colors.ts"

# Ordered list of character slugs
CHAR_ORDER = [
    "an-author","london-fox","glyph-marrow","phillip-bafflemint",
    "jacklyn-variance","oren-progresso","old-natalie-weissman","princhetta",
    "cop-e-right","new-natalie-weissman","arieol-owlist","jack-parlance",
    "manny-valentinas","shamrock-stillman","todd-fishbone","the-author",
]
ORIENTS = ["X","Y","A","Z"]
ROTATIONS = [0, 90, 180, 270]

def load_colors():
    """Parse colors.ts and return a map slug->hex color."""
    if not COLORS_TS.exists():
        return {}
    txt = COLORS_TS.read_text(encoding="utf-8", errors="ignore")
    pairs = re.findall(r"['\"]([a-z0-9\-]+)['\"]\s*:\s*['\"](#?[A-Fa-f0-9]{6})['\"]", txt)
    return {k: v for k, v in pairs}

def main():
    colors = load_colors()
    rows = []
    for c_idx, slug in enumerate(CHAR_ORDER):
        for o_idx, o in enumerate(ORIENTS):
            for r_idx, rot in enumerate(ROTATIONS):
                glyph_id = c_idx * 16 + (o_idx * 4 + r_idx)
                filename = f"{slug}_{o}_{rot}.svg"
                rows.append({
                    "glyph_id": glyph_id,
                    "char_hex": c_idx,
                    "char_slug": slug,
                    "orientation": o,
                    "rotation_deg": rot,
                    "symbol_code": None,
                    "behavior": None,
                    "hex": f"{glyph_id:02X}",
                    "filename": filename,
                    "color": colors.get(slug),
                    "label": f"{slug.replace('-', ' ').title()} — {o} @{rot}°",
                    "tags": ["character", o, f"rot-{rot}"]
                })
    GLYPH_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_OUT.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_OUT.open("w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"Wrote manifest: {MANIFEST_OUT} ({len(rows)} entries)")

if __name__ == '__main__':
    main()