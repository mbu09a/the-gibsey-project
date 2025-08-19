#!/usr/bin/env python3
"""
Generate the 256 QDPI glyph SVGs by duplicating and rotating
the base character symbols from public/corpus-symbols.
"""
import xml.etree.ElementTree as ET
from pathlib import Path

ET.register_namespace('', 'http://www.w3.org/2000/svg')

ROOT = Path(__file__).resolve().parent.parent.parent
SRC_DIR = ROOT / 'public/corpus-symbols'
DST_DIR = ROOT / 'public/qdpi-256-glyphs'

CHAR_ORDER = [
    'an-author','london-fox','glyph-marrow','phillip-bafflemint',
    'jacklyn-variance','oren-progresso','old-natalie-weissman','princhetta',
    'cop-e-right','new-natalie-weissman','arieol-owlist','jack-parlance',
    'manny-valentinas','shamrock-stillman','todd-fishbone','the-author',
]
ORIENTS = ['X','Y','A','Z']
ROTATIONS = [0, 90, 180, 270]

def find_base_svgs():
    mapping = {}
    for p in SRC_DIR.glob('*.svg'):
        key = p.stem.lower()
        mapping[key] = p
    return mapping

def rotate_and_write(tree, rot, center, out_path):
    root = tree.getroot()
    # Remove metadata nodes
    for md in root.findall('.//{http://www.w3.org/2000/svg}metadata'):
        root.remove(md)
    children = list(root)
    # clear existing children
    for ch in children:
        root.remove(ch)
    # wrap in group if rotation needed
    if rot != 0:
        cx, cy = center
        g = ET.Element('g', {'transform': f'translate({cx},{cy}) rotate({rot}) translate({-cx},{-cy})'})
        for ch in children:
            g.append(ch)
        root.append(g)
    else:
        for ch in children:
            root.append(ch)
    # write
    tree.write(out_path, encoding='utf-8', xml_declaration=True)

def main():
    mapping = find_base_svgs()
    DST_DIR.mkdir(parents=True, exist_ok=True)
    for slug in CHAR_ORDER:
        key_dash = slug
        key_underscore = slug.replace('-', '_')
        base_file = mapping.get(key_dash) or mapping.get(key_underscore)
        if base_file is None:
            print(f"[WARN] no base SVG for '{slug}' in {SRC_DIR}")
            continue
        tree = ET.parse(base_file)
        root = tree.getroot()
        vb = root.attrib.get('viewBox', '0 0 100 100').split()
        minx, miny, w, h = map(float, vb)
        center = (minx + w/2, miny + h/2)
        for o in ORIENTS:
            for rot in ROTATIONS:
                fname = f'{slug}_{o}_{rot}.svg'
                out = DST_DIR / fname
                rotate_and_write(tree, rot, center, out)
    print(f"Generated glyphs in {DST_DIR}")

if __name__ == '__main__':
    main()