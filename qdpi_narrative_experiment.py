#!/usr/bin/env python3
"""
QDPI Narrative Experiment
Encode real system operations and narratives as symbol sequences
Test how they "read" in plain English using the QDPI-256 Canon
"""

import yaml
from pathlib import Path
from typing import List, Tuple, Dict, Any

class QDPICanonEncoder:
    """Encodes narratives using the QDPI-256 Canon mapping"""
    
    def __init__(self):
        self.load_canon_mapping()
        self.rotation_names = {0: "READ", 90: "ASK", 180: "INDEX", 270: "RECEIVE"}
        
    def load_canon_mapping(self):
        """Load the canonical symbol mapping"""
        mapping_file = Path("/Users/ghostradongus/the-gibsey-project/qdpi_symbol_mapping.yaml")
        with open(mapping_file, 'r') as f:
            self.mapping = yaml.safe_load(f)
        
        # Create reverse lookup for easy encoding
        self.symbol_lookup = {}
        
        # Character symbols
        for symbol, info in self.mapping['character_symbols'].items():
            self.symbol_lookup[symbol] = {
                'id': info['id'],
                'type': 'character',
                'who': info['who'],
                'how': info['how']
            }
        
        # Meta-verbs
        for symbol, info in self.mapping['meta_verbs'].items():
            self.symbol_lookup[info['verb']] = {
                'id': info['id'],
                'type': 'meta_verb',
                'symbol': symbol,
                'verb': info['verb']
            }
    
    def encode_sequence(self, sequence_description: str, symbols: List[Tuple[str, int]]) -> Dict[str, Any]:
        """Encode a sequence and provide plain English translation"""
        
        encoded = []
        plain_english_parts = []
        
        for symbol_name, rotation in symbols:
            # Look up symbol info
            if symbol_name in self.symbol_lookup:
                symbol_info = self.symbol_lookup[symbol_name]
                
                # Create encoding
                encoding = {
                    'symbol': symbol_name,
                    'rotation': rotation,
                    'glyph_id': symbol_info['id'] * 4 + (rotation // 90),  # 0-255 range
                    'svg_file': f"{symbol_name}_{rotation}.svg" if rotation != 0 else f"{symbol_name}.svg"
                }
                encoded.append(encoding)
                
                # Create plain English
                rotation_verb = self.rotation_names[rotation]
                
                if symbol_info['type'] == 'character':
                    plain_part = f"{rotation_verb} {symbol_info['how']}"
                elif symbol_info['type'] == 'meta_verb':
                    plain_part = f"{rotation_verb} {symbol_info['verb']} operation"
                else:
                    plain_part = f"{rotation_verb} {symbol_name}"
                    
                plain_english_parts.append(plain_part)
        
        return {
            'description': sequence_description,
            'encoded_sequence': encoded,
            'plain_english': " → ".join(plain_english_parts),
            'total_glyphs': len(encoded),
            'byte_equivalent': bytes([enc['glyph_id'] for enc in encoded])
        }

def run_narrative_experiments():
    """Run experiments with real system narratives"""
    
    encoder = QDPICanonEncoder()
    
    experiments = [
        {
            'name': "User Login Flow",
            'description': "User attempts to log in, system validates, grants access",
            'sequence': [
                ('cop_e_right', 90),     # Ask Security Guardian
                ('VALIDATE', 270),       # Validation completes  
                ('phillip_bafflemint', 270),  # Interface receives result
                ('london_fox', 180)      # Index user connection
            ]
        },
        
        {
            'name': "Data Analysis Request", 
            'description': "User requests data analysis, system processes and displays",
            'sequence': [
                ('jacklyn_variance', 90),    # Ask Data Analyst
                ('OBSERVE', 0),              # Read observation state
                ('TRANSFORM', 270),          # Transformation completes
                ('phillip_bafflemint', 270)  # Interface receives
            ]
        },
        
        {
            'name': "System Memory Recall",
            'description': "System recalls historical context for current operation", 
            'sequence': [
                ('old_natalie_weissman', 90),  # Ask Memory Keeper
                ('REMEMBER', 270),             # Remember operation completes
                ('new_natalie_weissman', 0),   # Read Innovation state
                ('LINK', 180)                  # Index the connection
            ]
        },
        
        {
            'name': "AI Collaboration Session",
            'description': "User collaborates with AI on content creation",
            'sequence': [
                ('princhetta', 90),        # Ask AI Orchestrator
                ('an_author', 270),        # Content Management receives
                ('MERGE', 270),            # Merge operation completes
                ('glyph_marrow', 180)      # Index in QDPI Protocol
            ]
        },
        
        {
            'name': "Event Stream Processing",
            'description': "Real-time event comes in, gets processed and routed",
            'sequence': [
                ('arieol_owlist', 270),     # Event Coordinator receives
                ('OBSERVE', 0),             # Read observation
                ('jack_parlance', 90),      # Ask Network Specialist  
                ('LINK', 270)               # Link operation completes
            ]
        },
        
        {
            'name': "System Bootstrap Sequence",
            'description': "System starts up and initializes all components",
            'sequence': [
                ('The_Author', 90),         # Ask Meta-System
                ('SYNCHRONIZE', 270),       # Sync completes
                ('glyph_marrow', 270),      # QDPI Protocol receives
                ('oren_progresso', 180)     # Index progress state
            ]
        },
        
        {
            'name': "Quality Assurance Flow",
            'description': "Testing runs, results analyzed, deployment approved",
            'sequence': [
                ('shamrock_stillman', 90),  # Ask Quality Assurance
                ('VALIDATE', 270),          # Validation completes
                ('todd_fishbone', 90),      # Ask Deployment Specialist
                ('BRANCH', 180)             # Index branch for deployment
            ]
        },
        
        {
            'name': "Resource Optimization",
            'description': "System checks resources, optimizes allocation",
            'sequence': [
                ('manny_valentinas', 90),   # Ask Resource Manager
                ('COST', 0),                # Read cost calculation
                ('TRANSFORM', 270),         # Transformation completes
                ('SYNCHRONIZE', 180)        # Index synchronization
            ]
        }
    ]
    
    print("🔮 QDPI Narrative Experiment Results\n")
    print("=" * 60)
    
    for i, exp in enumerate(experiments, 1):
        print(f"\n## Experiment {i}: {exp['name']}")
        print(f"**Scenario**: {exp['description']}")
        
        result = encoder.encode_sequence(exp['description'], exp['sequence'])
        
        print(f"**Symbol Sequence**: ", end="")
        for j, enc in enumerate(result['encoded_sequence']):
            arrow = " → " if j < len(result['encoded_sequence']) - 1 else ""
            print(f"{enc['symbol']}@{enc['rotation']}°{arrow}", end="")
        print()
        
        print(f"**Plain English**: {result['plain_english']}")
        print(f"**Byte Sequence**: {list(result['byte_equivalent'])}")
        print(f"**Total Glyphs**: {result['total_glyphs']}")
        
        # Show what error correction would protect
        print(f"**Error Protection**: Reed-Solomon would ensure this {result['total_glyphs']}-glyph narrative")
        print(f"survives transmission corruption, preserving the semantic meaning.")

def test_rotation_effects():
    """Test how rotation changes meaning"""
    
    encoder = QDPICanonEncoder()
    
    print(f"\n{'='*60}")
    print("🔄 Rotation Effect Analysis")
    print(f"{'='*60}")
    
    test_symbol = 'london_fox'
    
    print(f"\nTesting symbol: {test_symbol} (Graph Engine)")
    print("-" * 40)
    
    for rotation in [0, 90, 180, 270]:
        result = encoder.encode_sequence(f"Test rotation {rotation}°", [(test_symbol, rotation)])
        print(f"**{rotation}° ({encoder.rotation_names[rotation]})**: {result['plain_english']}")
        print(f"   Glyph ID: {result['encoded_sequence'][0]['glyph_id']}")
        print(f"   SVG File: {result['encoded_sequence'][0]['svg_file']}")

def test_meta_verb_composition():
    """Test how meta-verbs change narrative flow"""
    
    encoder = QDPICanonEncoder()
    
    print(f"\n{'='*60}")
    print("🔧 Meta-Verb Composition Analysis") 
    print(f"{'='*60}")
    
    base_sequence = [
        ('jacklyn_variance', 90),    # Ask Data Analyst
        ('phillip_bafflemint', 270)  # Interface receives
    ]
    
    meta_verbs = ['LINK', 'MERGE', 'TRANSFORM', 'OBSERVE', 'VALIDATE']
    
    print("\nBase sequence: Data Analyst → Interface")
    print("Testing meta-verb insertion effects:")
    print("-" * 40)
    
    for verb in meta_verbs:
        # Insert meta-verb between base sequence
        test_sequence = [
            base_sequence[0],
            (verb, 270),           # Meta-verb completes
            base_sequence[1]
        ]
        
        result = encoder.encode_sequence(f"With {verb}", test_sequence)
        print(f"**+ {verb}**: {result['plain_english']}")

if __name__ == "__main__":
    run_narrative_experiments()
    test_rotation_effects()
    test_meta_verb_composition()