#!/usr/bin/env python3
"""
Generate all 64 QDPI symbols from the codex.
Creates SVG files based on the systematic encoding pattern.
"""
import os
from pathlib import Path

# Complete codex with all 64 symbols
SYMBOL_CODEX = [
    # Name, ID, Orientation, Row1, Row2, Row3, Row4
    ("an_author", 1, "n", "o/o", "o/o", "o/o", "x/x"),
    ("london_fox", 2, "n", "o/o", "o/o", "x/x", "x/x"),
    ("glyph_marrow", 3, "n", "o/o", "x/x", "o/o", "x/x"),
    ("phillip_bafflemint", 4, "n", "x/x", "o/o", "o/o", "x/x"),
    ("jacklyn_variance", 5, "n", "o/o", "x/x", "x/x", "x/x"),
    ("oren_progresso", 6, "n", "x/x", "o/o", "x/x", "x/x"),
    ("old_natalie_weissman", 7, "n", "x/x", "x/x", "o/o", "x/x"),
    ("princhetta", 8, "n", "x/x", "x/x", "x/x", "x/x"),
    ("cop-e-right", 9, "u", "x/x", "x/x", "x/x", "x/x"),
    ("new_natalie_weissman", 10, "u", "x/x", "o/o", "x/x", "x/x"),
    ("arieol_owlist", 11, "u", "x/x", "x/x", "o/o", "x/x"),
    ("jack_parlance", 12, "u", "x/x", "x/x", "x/x", "o/o"),
    ("manny_valentinas", 13, "u", "x/x", "o/o", "o/o", "x/x"),
    ("shamrock_stillman", 14, "u", "x/x", "o/o", "x/x", "o/o"),
    ("todd_fishbone", 15, "u", "x/x", "x/x", "o/o", "o/o"),
    ("The_Author", 16, "u", "x/x", "o/o", "o/o", "o/o"),
    ("hidden_symbol_01", 17, "n", "o/o", "o/o", "x/o", "x/x"),
    ("hidden_symbol_02", 18, "n", "o/o", "o/o", "o/x", "x/x"),
    ("hidden_symbol_03", 19, "n", "o/o", "x/o", "o/o", "x/x"),
    ("hidden_symbol_04", 20, "n", "o/o", "o/x", "o/o", "x/x"),
    ("hidden_symbol_05", 21, "n", "x/o", "o/o", "o/o", "x/x"),
    ("hidden_symbol_06", 22, "n", "o/x", "o/o", "o/o", "x/x"),
    ("hidden_symbol_07", 23, "n", "o/o", "x/o", "x/x", "x/x"),
    ("hidden_symbol_08", 24, "n", "o/o", "o/x", "x/x", "x/x"),
    ("hidden_symbol_09", 25, "n", "x/o", "o/o", "x/x", "x/x"),
    ("hidden_symbol_10", 26, "n", "o/x", "o/o", "x/x", "x/x"),
    ("hidden_symbol_11", 27, "n", "o/o", "x/x", "x/o", "x/x"),  # Note: codex had missing orientation, assuming 'n'
    ("hidden_symbol_12", 28, "n", "o/o", "x/x", "o/x", "x/x"),
    ("hidden_symbol_13", 29, "n", "x/o", "x/x", "o/x", "x/x"),
    ("hidden_symbol_14", 30, "n", "o/x", "x/x", "o/x", "x/x"),
    ("hidden_symbol_15", 31, "n", "x/x", "x/x", "x/o", "x/x"),
    ("hidden_symbol_16", 32, "n", "x/x", "x/x", "o/x", "x/x"),
    ("hidden_symbol_17", 33, "n", "x/x", "o/x", "x/x", "x/x"),
    ("hidden_symbol_18", 34, "n", "x/x", "x/o", "x/x", "x/x"),
    ("hidden_symbol_19", 35, "n", "o/x", "x/x", "x/x", "x/x"),
    ("hidden_symbol_20", 36, "n", "x/o", "x/x", "x/x", "x/x"),
    ("hidden_symbol_21", 37, "n", "o/x", "x/x", "x/o", "x/x"),
    ("hidden_symbol_22", 38, "n", "x/o", "x/x", "x/o", "x/x"),
    ("hidden_symbol_23", 39, "n", "o/x", "x/o", "o/o", "x/x"),
    ("hidden_symbol_24", 40, "n", "x/o", "o/x", "o/o", "x/x"),
    ("hidden_symbol_25", 41, "u", "x/x", "x/o", "o/o", "o/o"),
    ("hidden_symbol_26", 42, "u", "x/x", "o/x", "o/o", "o/o"),
    ("hidden_symbol_27", 43, "u", "x/x", "o/o", "x/o", "o/o"),
    ("hidden_symbol_28", 44, "u", "x/x", "o/o", "o/x", "o/o"),
    ("hidden_symbol_29", 45, "u", "x/x", "o/o", "o/o", "x/o"),
    ("hidden_symbol_30", 46, "u", "x/x", "o/o", "o/o", "o/x"),
    ("hidden_symbol_31", 47, "u", "x/x", "x/x", "x/o", "o/o"),
    ("hidden_symbol_32", 48, "u", "x/x", "x/x", "o/x", "o/o"),
    ("hidden_symbol_33", 49, "u", "x/x", "x/x", "o/o", "x/o"),
    ("hidden_symbol_34", 50, "u", "x/x", "x/x", "o/o", "o/x"),
    ("hidden_symbol_35", 51, "u", "x/x", "x/o", "x/x", "o/o"),
    ("hidden_symbol_36", 52, "u", "x/x", "o/x", "x/x", "o/o"),
    ("hidden_symbol_37", 53, "u", "x/x", "o/x", "x/x", "x/o"),
    ("hidden_symbol_38", 54, "u", "x/x", "o/x", "x/x", "o/x"),
    ("hidden_symbol_39", 55, "u", "x/x", "x/o", "x/x", "x/x"),
    ("hidden_symbol_40", 56, "u", "x/x", "o/x", "x/x", "x/x"),
    ("hidden_symbol_41", 57, "u", "x/x", "x/x", "o/x", "x/x"),
    ("hidden_symbol_42", 58, "u", "x/x", "x/x", "x/o", "x/x"),
    ("hidden_symbol_43", 59, "u", "x/x", "x/x", "x/x", "x/o"),
    ("hidden_symbol_44", 60, "u", "x/x", "x/x", "x/x", "o/x"),
    ("hidden_symbol_45", 61, "u", "x/x", "x/o", "x/x", "o/x"),
    ("hidden_symbol_46", 62, "u", "x/x", "x/o", "x/x", "x/o"),
    ("hidden_symbol_47", 63, "u", "x/x", "o/o", "x/o", "o/x"),
    ("hidden_symbol_48", 64, "u", "x/x", "o/o", "o/x", "o/x"),
]

def generate_svg_lines(row_pattern, y_position, is_upside_down=False):
    """Generate SVG line elements for a given row pattern."""
    lines = []
    left, right = row_pattern.split('/')
    
    if is_upside_down:
        # For upside-down symbols, we extend outward from the frame
        if left == 'x':
            lines.append(f'    <line x1="200" y1="{y_position}" x2="0" y2="{y_position}" stroke="#000" stroke-width="60" stroke-linecap="square"/>')
        if right == 'x':
            lines.append(f'    <line x1="800" y1="{y_position}" x2="1000" y2="{y_position}" stroke="#000" stroke-width="60" stroke-linecap="square"/>')
    else:
        # For normal symbols, we extend inward from the frame
        if left == 'x':
            lines.append(f'    <line x1="200" y1="{y_position}" x2="400" y2="{y_position}" stroke="#000" stroke-width="60" stroke-linecap="square"/>')
        if right == 'x':
            lines.append(f'    <line x1="800" y1="{y_position}" x2="600" y2="{y_position}" stroke="#000" stroke-width="60" stroke-linecap="square"/>')
    
    return lines

def generate_svg(name, orientation, row1, row2, row3, row4):
    """Generate complete SVG content for a symbol."""
    is_upside_down = (orientation == 'u')
    
    # Base SVG structure
    svg_lines = ['<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">']
    
    if is_upside_down:
        svg_lines.append('  <g transform="rotate(180 500 500)">')
        svg_lines.append('    <rect width="1000" height="1000" fill="#fff"/>')
    else:
        svg_lines.append('    <rect width="1000" height="1000" fill="#fff"/>')
    
    # Main frame (U-shape)
    svg_lines.append('    <line x1="200" y1="200" x2="800" y2="200" stroke="#000" stroke-width="60" stroke-linecap="square"/>')
    svg_lines.append('    <line x1="200" y1="200" x2="200" y2="800" stroke="#000" stroke-width="60" stroke-linecap="square"/>')
    svg_lines.append('    <line x1="800" y1="200" x2="800" y2="800" stroke="#000" stroke-width="60" stroke-linecap="square"/>')
    
    # Add row extensions
    # Row positions from bottom to top: 800, 700, 600, 500
    svg_lines.extend(generate_svg_lines(row4, 800, is_upside_down))
    svg_lines.extend(generate_svg_lines(row3, 700, is_upside_down))
    svg_lines.extend(generate_svg_lines(row2, 600, is_upside_down))
    svg_lines.extend(generate_svg_lines(row1, 500, is_upside_down))
    
    if is_upside_down:
        svg_lines.append('  </g>')
    
    svg_lines.append('</svg>')
    
    return '\n'.join(svg_lines)

def main():
    """Generate all 64 QDPI symbols."""
    # Create output directory
    output_dir = Path("/Users/ghostradongus/the-gibsey-project/public/corpus-symbols")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🎨 Generating 64 QDPI symbols to {output_dir}")
    
    generated = 0
    skipped = 0
    
    for symbol in SYMBOL_CODEX:
        name, symbol_id, orientation, row1, row2, row3, row4 = symbol
        filename = f"{name}.svg"
        filepath = output_dir / filename
        
        # Check if file already exists (for the 16 existing symbols)
        if filepath.exists() and symbol_id <= 16:
            print(f"✓ Skipping existing symbol {symbol_id}: {name}")
            skipped += 1
            continue
        
        # Generate SVG content
        svg_content = generate_svg(name, orientation, row1, row2, row3, row4)
        
        # Write SVG file
        with open(filepath, 'w') as f:
            f.write(svg_content)
        
        print(f"✅ Generated symbol {symbol_id}: {name}")
        generated += 1
    
    print(f"\n📊 Summary:")
    print(f"   Generated: {generated} new symbols")
    print(f"   Skipped: {skipped} existing symbols")
    print(f"   Total: {len(SYMBOL_CODEX)} symbols in corpus")
    
    # Verify all files exist
    svg_files = list(output_dir.glob("*.svg"))
    print(f"\n✨ Verification: Found {len(svg_files)} SVG files in {output_dir}")

if __name__ == "__main__":
    main()