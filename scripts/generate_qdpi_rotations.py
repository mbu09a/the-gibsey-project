#!/usr/bin/env python3
"""
QDPI-256 Rotation Generator
Generates rotational variants (90°, 180°, 270°) for all base symbols
to complete the 256-glyph alphabet.

Creates: 64 base symbols × 4 rotations = 256 total glyphs
"""

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import logging
from typing import List, Tuple, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

class QDPIRotationGenerator:
    """Generate rotational variants of QDPI symbols"""
    
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.rotations = [0, 90, 180, 270]
        self.generated_count = 0
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Track symbol ID assignments
        self.symbol_id_map: Dict[str, int] = {}
        self.glyph_id_map: Dict[Tuple[str, int], int] = {}
        
    def get_svg_files(self) -> List[Path]:
        """Get all SVG files from input directory"""
        svg_files = list(self.input_dir.glob("*.svg"))
        svg_files.sort()  # Ensure consistent ordering
        log.info(f"Found {len(svg_files)} SVG files in {self.input_dir}")
        return svg_files
    
    def assign_symbol_ids(self, svg_files: List[Path]) -> None:
        """Assign symbol IDs (0-63) to base symbols"""
        # Character symbols get IDs 0-15
        character_symbols = []
        hidden_symbols = []
        
        for svg_file in svg_files:
            name = svg_file.stem
            if name.startswith('hidden_symbol_'):
                hidden_symbols.append(name)
            else:
                character_symbols.append(name)
        
        # Sort for consistent assignment
        character_symbols.sort()
        hidden_symbols.sort()
        
        # Assign IDs
        symbol_id = 0
        
        # Character symbols: IDs 0-15
        for symbol in character_symbols:
            self.symbol_id_map[symbol] = symbol_id
            symbol_id += 1
        
        # Hidden symbols: IDs 16-63
        for symbol in hidden_symbols:
            self.symbol_id_map[symbol] = symbol_id
            symbol_id += 1
        
        log.info(f"Assigned {len(character_symbols)} character symbols (IDs 0-{len(character_symbols)-1})")
        log.info(f"Assigned {len(hidden_symbols)} hidden symbols (IDs {len(character_symbols)}-{symbol_id-1})")
    
    def calculate_glyph_id(self, symbol_name: str, rotation: int) -> int:
        """Calculate unique glyph ID (0-255) for symbol+rotation combination"""
        symbol_id = self.symbol_id_map[symbol_name]
        rotation_index = self.rotations.index(rotation)
        glyph_id = symbol_id * 4 + rotation_index
        return glyph_id
    
    def extract_drawing_elements(self, element) -> List[str]:
        """Recursively extract drawing elements from XML element or group"""
        drawing_elements = []
        
        if element.tag.endswith('line'):
            # Extract line attributes
            x1 = element.get('x1', '0')
            y1 = element.get('y1', '0') 
            x2 = element.get('x2', '0')
            y2 = element.get('y2', '0')
            stroke = element.get('stroke', '#000')
            stroke_width = element.get('stroke-width', '60')
            stroke_linecap = element.get('stroke-linecap', 'square')
            
            line_element = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{stroke_width}" stroke-linecap="{stroke_linecap}"/>'
            drawing_elements.append(line_element)
            
        elif element.tag.endswith('path'):
            # Extract path
            d = element.get('d', '')
            stroke = element.get('stroke', '#000')
            stroke_width = element.get('stroke-width', '60')
            fill = element.get('fill', 'none')
            
            path_element = f'<path d="{d}" stroke="{stroke}" stroke-width="{stroke_width}" fill="{fill}"/>'
            drawing_elements.append(path_element)
            
        elif element.tag.endswith('g'):
            # Recursively process group contents, ignoring any transforms
            for child in element:
                drawing_elements.extend(self.extract_drawing_elements(child))
        
        return drawing_elements

    def create_rotated_svg(self, input_file: Path, rotation: int) -> str:
        """Create rotated version of SVG content"""
        try:
            # Read and parse the original SVG
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if rotation == 0:
                # No rotation needed, return original content
                return content
            
            # Parse the SVG
            tree = ET.parse(input_file)
            root = tree.getroot()
            
            # Check if this is a "u" oriented symbol (has existing rotate(180) transform)
            has_base_180_transform = False
            for child in root:
                if child.tag.endswith('g') and 'transform' in child.attrib:
                    transform = child.get('transform', '')
                    if 'rotate(180' in transform:
                        has_base_180_transform = True
                        break
            
            # Extract all drawing elements, handling nested groups and existing transforms
            drawing_elements = []
            for child in root:
                # Skip background rectangles
                if child.tag.endswith('rect') and child.get('fill') == '#fff':
                    continue
                else:
                    # Extract drawing elements recursively
                    drawing_elements.extend(self.extract_drawing_elements(child))
            
            # Calculate effective rotation
            # For "u" symbols with existing 180° transform:
            # - 90° rotation = 90° - 180° = -90° (or 270°)
            # - 180° rotation = 180° - 180° = 0° (no transform needed)
            # - 270° rotation = 270° - 180° = 90°
            if has_base_180_transform:
                effective_rotation = (rotation - 180) % 360
            else:
                effective_rotation = rotation
            
            center_x = center_y = 500  # Standard center for 1000x1000 viewBox
            
            if effective_rotation == 0:
                # No rotation transform needed
                new_svg = f'''<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
    <rect width="1000" height="1000" fill="#fff"/>'''
                
                # Add drawing elements directly (no group)
                for element in drawing_elements:
                    new_svg += f'\n    {element}'
                
                new_svg += '\n</svg>'
            else:
                # Apply rotation transform
                new_svg = f'''<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
    <rect width="1000" height="1000" fill="#fff"/>
    <g transform="rotate({effective_rotation} {center_x} {center_y})">'''
                
                # Add drawing elements
                for element in drawing_elements:
                    new_svg += f'\n        {element}'
                
                new_svg += '\n    </g>\n</svg>'
            
            return new_svg
            
        except Exception as e:
            log.error(f"Error rotating {input_file}: {e}")
            return None
    
    def generate_rotation_variants(self, svg_file: Path) -> None:
        """Generate all 4 rotation variants for a symbol"""
        symbol_name = svg_file.stem
        
        log.info(f"Generating rotations for {symbol_name}")
        
        for rotation in self.rotations:
            # Calculate glyph ID
            glyph_id = self.calculate_glyph_id(symbol_name, rotation)
            self.glyph_id_map[(symbol_name, rotation)] = glyph_id
            
            # Generate output filename
            if rotation == 0:
                output_name = f"{symbol_name}.svg"
            else:
                output_name = f"{symbol_name}_{rotation}.svg"
            
            output_path = self.output_dir / output_name
            
            # Create rotated SVG content
            rotated_content = self.create_rotated_svg(svg_file, rotation)
            
            if rotated_content:
                # Add QDPI metadata as comment
                metadata_comment = f"<!-- QDPI Glyph: {symbol_name}, Rotation: {rotation}°, Glyph ID: {glyph_id} -->\n"
                
                # Write to output file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(metadata_comment)
                    f.write(rotated_content)
                
                self.generated_count += 1
                log.debug(f"Generated {output_name} (Glyph ID: {glyph_id})")
            else:
                log.error(f"Failed to generate rotation {rotation}° for {symbol_name}")
    
    def generate_glyph_manifest(self) -> None:
        """Generate a manifest file with all glyph mappings"""
        manifest_path = self.output_dir / "qdpi_glyph_manifest.json"
        
        import json
        
        manifest = {
            "version": "1.0",
            "total_glyphs": len(self.glyph_id_map),
            "base_symbols": len(self.symbol_id_map),
            "rotations": self.rotations,
            "symbol_id_map": self.symbol_id_map,
            "glyph_mappings": {}
        }
        
        # Create detailed glyph mappings
        for (symbol_name, rotation), glyph_id in self.glyph_id_map.items():
            symbol_id = self.symbol_id_map[symbol_name]
            
            manifest["glyph_mappings"][str(glyph_id)] = {
                "symbol_name": symbol_name,
                "symbol_id": symbol_id,
                "rotation": rotation,
                "glyph_id": glyph_id,
                "filename": f"{symbol_name}_{rotation}.svg" if rotation != 0 else f"{symbol_name}.svg",
                "byte_value": glyph_id,
                "binary": format(glyph_id, '08b'),
                "hex": format(glyph_id, '02x')
            }
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, sort_keys=True)
        
        log.info(f"Generated glyph manifest: {manifest_path}")
    
    def generate_validation_report(self) -> None:
        """Generate validation report for the generated glyphs"""
        report_path = self.output_dir / "qdpi_validation_report.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("QDPI-256 Glyph Generation Validation Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total base symbols: {len(self.symbol_id_map)}\n")
            f.write(f"Rotations per symbol: {len(self.rotations)}\n")
            f.write(f"Total glyphs generated: {len(self.glyph_id_map)}\n")
            f.write(f"Expected glyphs: {len(self.symbol_id_map) * len(self.rotations)}\n\n")
            
            # Check for complete coverage
            expected_ids = set(range(256))
            actual_ids = set(self.glyph_id_map.values())
            
            if expected_ids == actual_ids:
                f.write("✅ COMPLETE: All 256 glyph IDs generated (0-255)\n\n")
            else:
                missing_ids = expected_ids - actual_ids
                extra_ids = actual_ids - expected_ids
                f.write(f"❌ INCOMPLETE: Missing {len(missing_ids)} IDs, {len(extra_ids)} extra IDs\n")
                if missing_ids:
                    f.write(f"Missing: {sorted(missing_ids)}\n")
                if extra_ids:
                    f.write(f"Extra: {sorted(extra_ids)}\n")
                f.write("\n")
            
            # Character vs Hidden symbol breakdown
            character_count = sum(1 for name in self.symbol_id_map.keys() if not name.startswith('hidden_'))
            hidden_count = sum(1 for name in self.symbol_id_map.keys() if name.startswith('hidden_'))
            
            f.write(f"Character symbols: {character_count} ({character_count * 4} glyphs)\n")
            f.write(f"Hidden symbols: {hidden_count} ({hidden_count * 4} glyphs)\n\n")
            
            # Symbol ID assignments
            f.write("Symbol ID Assignments:\n")
            f.write("-" * 30 + "\n")
            for symbol_name, symbol_id in sorted(self.symbol_id_map.items(), key=lambda x: x[1]):
                symbol_type = "CHARACTER" if not symbol_name.startswith('hidden_') else "HIDDEN"
                f.write(f"{symbol_id:2d}: {symbol_name} ({symbol_type})\n")
        
        log.info(f"Generated validation report: {report_path}")
    
    def run(self) -> bool:
        """Run the complete rotation generation process"""
        log.info("Starting QDPI-256 rotation generation...")
        
        # Get input files
        svg_files = self.get_svg_files()
        if not svg_files:
            log.error("No SVG files found in input directory")
            return False
        
        # Assign symbol IDs
        self.assign_symbol_ids(svg_files)
        
        # Generate rotations for each symbol
        for svg_file in svg_files:
            self.generate_rotation_variants(svg_file)
        
        # Generate manifest and validation
        self.generate_glyph_manifest()
        self.generate_validation_report()
        
        log.info(f"✅ Generation complete: {self.generated_count} glyphs created")
        log.info(f"📂 Output directory: {self.output_dir}")
        
        return True

def main():
    """Main entry point"""
    if len(sys.argv) != 3:
        print("Usage: python generate_qdpi_rotations.py <input_dir> <output_dir>")
        print("Example: python generate_qdpi_rotations.py ../public/corpus-symbols ./qdpi-256-glyphs")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist")
        sys.exit(1)
    
    generator = QDPIRotationGenerator(input_dir, output_dir)
    
    try:
        success = generator.run()
        if success:
            print("\n🎉 QDPI-256 rotation generation completed successfully!")
            print(f"📁 Check output directory: {output_dir}")
            print("📋 Review qdpi_validation_report.txt for details")
        else:
            print("\n❌ Generation failed")
            sys.exit(1)
    except Exception as e:
        log.error(f"Generation failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()