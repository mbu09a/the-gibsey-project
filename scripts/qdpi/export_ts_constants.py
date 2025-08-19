#!/usr/bin/env python3
"""
Export TypeScript constants and index JSON from the QDPI glyph manifest.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST = ROOT / "public/qdpi/qdpi_glyph_manifest.json"
TS_OUT = ROOT / "public/qdpi/manifest.d.ts"
INDEX_OUT = ROOT / "public/qdpi/manifest.index.json"

def main():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    # Export index of filenames
    with INDEX_OUT.open("w", encoding="utf-8") as f:
        json.dump([row["filename"] for row in data], f, indent=2)
    # Export TS module
    content = []
    content.append("// Generated file; do not edit.")
    content.append("import manifest from './qdpi_glyph_manifest.json';")
    content.append("\nexport default manifest;\n")
    with TS_OUT.open("w", encoding="utf-8") as f:
        f.write("\n".join(content))
    print(f"Wrote TypeScript constants to {TS_OUT} and {INDEX_OUT}")

if __name__ == '__main__':
    main()