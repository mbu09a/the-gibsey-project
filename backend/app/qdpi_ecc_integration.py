#!/usr/bin/env python3
"""
QDPI Error Correction Integration
Integrates the complete ECC system with the existing QDPI backend

This module bridges our new error correction capabilities with the 
production QDPI system, enabling bulletproof narrative preservation.
"""

import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from qdpi_complete_ecc import QDPICompleteECC
from backend.app.qdpi import QDPICodex, QDPISymbol
from typing import List, Dict, Any, Tuple, Optional
import json
import time
from dataclasses import dataclass, asdict

@dataclass
class ProtectedQDPIMessage:
    """A QDPI message with error correction protection"""
    original_symbols: List[Dict[str, Any]]  # Original symbol sequence with metadata
    protected_data: bytes                   # ECC-protected byte sequence
    block_id: int                          # Block identifier
    encoding_timestamp: float             # When protection was applied
    protection_metadata: Dict[str, Any]    # ECC statistics and info
    
class QDPIECCBackend:
    """Production QDPI backend with integrated error correction"""
    
    def __init__(self):
        self.qdpi_codex = QDPICodex()
        self.ecc_system = QDPICompleteECC()
        self.protected_messages = {}  # In production, this would be persistent storage
        self.message_counter = 0
        
    def encode_narrative_with_protection(self, narrative_description: str, 
                                       symbol_sequence: List[Tuple[str, int]]) -> ProtectedQDPIMessage:
        """Encode a narrative sequence with complete error protection"""
        
        start_time = time.time()
        
        # Step 1: Convert symbol sequence to QDPI symbols with metadata
        qdpi_symbols = []
        glyph_ids = []
        
        for symbol_name, rotation in symbol_sequence:
            # Get symbol ID and create simplified symbol representation
            symbol_id = self._get_symbol_id_from_canon(symbol_name)
            
            # Create simplified symbol dict (we don't need full QDPISymbol for ECC testing)
            qdpi_symbol = {
                'name': symbol_name,
                'id': symbol_id,
                'orientation': 'u' if any(symbol_name == char for char in 
                    ['cop-e-right', 'new_natalie_weissman', 'arieol_owlist', 'jack_parlance',
                     'manny_valentinas', 'shamrock_stillman', 'todd_fishbone', 'The_Author']) else 'n',
                'rotation': rotation
            }
            
            # Calculate glyph ID using our Canon mapping
            symbol_id = self._get_symbol_id_from_canon(symbol_name)
            rotation_index = rotation // 90
            glyph_id = symbol_id * 4 + rotation_index
            
            qdpi_symbols.append({
                'symbol': qdpi_symbol,
                'glyph_id': glyph_id,
                'canon_meaning': self._get_canon_meaning(symbol_name, rotation),
                'narrative_description': narrative_description
            })
            glyph_ids.append(glyph_id)
        
        # Step 2: Apply error correction protection
        byte_sequence = bytes(glyph_ids)
        protected_sequence = self.ecc_system.encode_with_protection(byte_sequence, self.message_counter)
        
        # Step 3: Create protected message
        protection_metadata = {
            'original_length': len(glyph_ids),
            'protected_length': len(protected_sequence.reed_solomon_block.encoded),
            'overhead_bytes': protected_sequence.total_overhead_bytes,
            'overhead_percent': (protected_sequence.total_overhead_bytes / len(glyph_ids)) * 100,
            'encoding_time_ms': (time.time() - start_time) * 1000,
            'protection_level': protected_sequence.protection_level,
            'narrative_description': narrative_description
        }
        
        protected_message = ProtectedQDPIMessage(
            original_symbols=qdpi_symbols,
            protected_data=protected_sequence.reed_solomon_block.encoded,
            block_id=self.message_counter,
            encoding_timestamp=time.time(),
            protection_metadata=protection_metadata
        )
        
        # Store for later retrieval
        self.protected_messages[self.message_counter] = protected_message
        self.message_counter += 1
        
        return protected_message
    
    def decode_protected_narrative(self, protected_data: bytes, 
                                 original_length: int, 
                                 block_id: Optional[int] = None) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Decode and error-correct a protected QDPI narrative"""
        
        start_time = time.time()
        
        # Step 1: Apply error correction
        recovered_bytes, ecc_stats = self.ecc_system.decode_with_correction(protected_data, original_length)
        
        # Step 2: Convert back to QDPI symbols
        recovered_symbols = []
        
        for i, glyph_id in enumerate(recovered_bytes):
            symbol_id = glyph_id // 4
            rotation = (glyph_id % 4) * 90
            
            # Look up symbol name from Canon
            symbol_name = self._get_symbol_name_from_id(symbol_id)
            canon_meaning = self._get_canon_meaning(symbol_name, rotation)
            
            recovered_symbols.append({
                'position': i,
                'symbol_name': symbol_name,
                'rotation': rotation,
                'glyph_id': glyph_id,
                'canon_meaning': canon_meaning
            })
        
        # Step 3: Compile decoding statistics
        decode_stats = {
            'decode_time_ms': (time.time() - start_time) * 1000,
            'recovery_successful': ecc_stats['protection_successful'],
            'meets_performance_target': ecc_stats['meets_4ms_target'],
            'error_correction': ecc_stats,
            'recovered_symbols_count': len(recovered_symbols),
            'block_id': block_id
        }
        
        return recovered_symbols, decode_stats
    
    def simulate_transmission_and_recovery(self, protected_message: ProtectedQDPIMessage, 
                                         error_rate: float = 0.01) -> Dict[str, Any]:
        """Simulate transmission errors and test recovery"""
        
        # Create a fake block object for simulation
        from dataclasses import dataclass
        
        @dataclass
        class FakeBlock:
            encoded: bytes
            
        fake_block = FakeBlock(encoded=protected_message.protected_data)
        
        # Simulate transmission corruption
        corrupted_data = self.ecc_system.reed_solomon.simulate_transmission_errors(
            fake_block, error_rate
        )
        
        # Attempt recovery
        recovered_symbols, decode_stats = self.decode_protected_narrative(
            corrupted_data, 
            protected_message.protection_metadata['original_length'],
            protected_message.block_id
        )
        
        # Compare original vs recovered
        original_glyph_ids = [sym['glyph_id'] for sym in protected_message.original_symbols]
        recovered_glyph_ids = [sym['glyph_id'] for sym in recovered_symbols]
        
        narrative_preserved = original_glyph_ids == recovered_glyph_ids
        
        # Reconstruct narrative meaning
        original_narrative = " → ".join([sym['canon_meaning'] for sym in protected_message.original_symbols])
        recovered_narrative = " → ".join([sym['canon_meaning'] for sym in recovered_symbols])
        
        return {
            'transmission_simulation': {
                'error_rate': error_rate,
                'narrative_preserved': narrative_preserved,
                'original_narrative': original_narrative,
                'recovered_narrative': recovered_narrative,
                'original_sequence': original_glyph_ids,
                'recovered_sequence': recovered_glyph_ids
            },
            'decode_performance': decode_stats,
            'protection_effectiveness': narrative_preserved
        }
    
    def _get_symbol_id_from_canon(self, symbol_name: str) -> int:
        """Get symbol ID from QDPI Canon mapping"""
        # This maps to our canonical symbol ordering
        symbol_map = {
            'an_author': 0, 'london_fox': 1, 'glyph_marrow': 2, 'phillip_bafflemint': 3,
            'jacklyn_variance': 4, 'oren_progresso': 5, 'old_natalie_weissman': 6, 'princhetta': 7,
            'cop-e-right': 8, 'new_natalie_weissman': 9, 'arieol_owlist': 10, 'jack_parlance': 11,
            'manny_valentinas': 12, 'shamrock_stillman': 13, 'todd_fishbone': 14, 'The_Author': 15
        }
        
        # Character symbols (0-15)
        if symbol_name in symbol_map:
            return symbol_map[symbol_name]
        
        # Hidden symbols (16-63) 
        if symbol_name.startswith('hidden_symbol_'):
            symbol_num = int(symbol_name.split('_')[2])
            return 15 + symbol_num
            
        # Meta-verbs (mapped to hidden symbols 33-48)
        meta_verb_map = {
            'LINK': 48, 'MERGE': 49, 'SPLIT': 50, 'FORGET': 51, 'REMEMBER': 52,
            'GIFT': 53, 'COST': 54, 'VALIDATE': 55, 'TRANSFORM': 56, 'REPLICATE': 57,
            'OBSERVE': 58, 'INTERRUPT': 59, 'RESUME': 60, 'BRANCH': 61, 'SYNCHRONIZE': 62, 'TERMINATE': 63
        }
        
        if symbol_name in meta_verb_map:
            return meta_verb_map[symbol_name]
            
        return 0  # Default fallback
    
    def _get_symbol_name_from_id(self, symbol_id: int) -> str:
        """Get symbol name from ID using Canon mapping"""
        if symbol_id <= 15:
            symbol_names = [
                'an_author', 'london_fox', 'glyph_marrow', 'phillip_bafflemint',
                'jacklyn_variance', 'oren_progresso', 'old_natalie_weissman', 'princhetta',
                'cop-e-right', 'new_natalie_weissman', 'arieol_owlist', 'jack_parlance',
                'manny_valentinas', 'shamrock_stillman', 'todd_fishbone', 'The_Author'
            ]
            return symbol_names[symbol_id]
        elif 16 <= symbol_id <= 47:
            return f"hidden_symbol_{symbol_id - 15:02d}"
        else:
            # Meta-verbs
            meta_verbs = [
                'LINK', 'MERGE', 'SPLIT', 'FORGET', 'REMEMBER', 'GIFT', 'COST', 'VALIDATE',
                'TRANSFORM', 'REPLICATE', 'OBSERVE', 'INTERRUPT', 'RESUME', 'BRANCH', 'SYNCHRONIZE', 'TERMINATE'
            ]
            verb_index = symbol_id - 48
            if 0 <= verb_index < len(meta_verbs):
                return meta_verbs[verb_index]
        
        return f"unknown_symbol_{symbol_id}"
    
    def _get_canon_meaning(self, symbol_name: str, rotation: int) -> str:
        """Get canonical meaning for symbol at rotation"""
        rotation_verbs = {0: "READ", 90: "ASK", 180: "INDEX", 270: "RECEIVE"}
        rotation_verb = rotation_verbs.get(rotation, "UNKNOWN")
        
        # Character symbols - use system component
        character_systems = {
            'an_author': 'Content Management', 'london_fox': 'Graph Engine', 
            'glyph_marrow': 'QDPI Protocol', 'phillip_bafflemint': 'Interface Management',
            'jacklyn_variance': 'Core Database', 'oren_progresso': 'Orchestration Engine',
            'old_natalie_weissman': 'Memory Management', 'princhetta': 'AI Coordination',
            'cop-e-right': 'Security & Permissions', 'new_natalie_weissman': 'Research & Development',
            'arieol_owlist': 'Event Streaming', 'jack_parlance': 'Network Communications',
            'manny_valentinas': 'Resource Allocation', 'shamrock_stillman': 'Testing & Validation',
            'todd_fishbone': 'Deployment Pipeline', 'The_Author': 'System Bootstrap'
        }
        
        if symbol_name in character_systems:
            return f"{rotation_verb} {character_systems[symbol_name]}"
        elif symbol_name.startswith('hidden_symbol_'):
            return f"{rotation_verb} {symbol_name.replace('_', ' ').title()}"
        else:
            # Meta-verbs
            return f"{rotation_verb} {symbol_name} operation"

def test_production_integration():
    """Test the complete production integration"""
    
    print("🏭 QDPI Production Error Correction Integration Test")
    print("=" * 60)
    
    backend = QDPIECCBackend()
    
    # Test real production scenarios
    production_scenarios = [
        {
            'name': 'User Authentication Flow',
            'description': 'Critical user login sequence with security validation',
            'sequence': [
                ('cop-e-right', 90),      # ASK Security System
                ('VALIDATE', 270),        # Validation completes
                ('phillip_bafflemint', 270), # Interface receives
                ('london_fox', 180)       # Index user connection
            ]
        },
        {
            'name': 'AI-Human Collaboration',
            'description': 'Complex AI collaboration workflow with content generation',
            'sequence': [
                ('princhetta', 90),       # ASK AI Orchestrator
                ('an_author', 270),       # Content Management receives
                ('MERGE', 270),           # Merge operation completes
                ('glyph_marrow', 180),    # Index in QDPI Protocol
                ('phillip_bafflemint', 0) # Read Interface state
            ]
        },
        {
            'name': 'System Health Check',
            'description': 'Comprehensive system monitoring and status verification',
            'sequence': [
                ('oren_progresso', 90),   # ASK Orchestration Engine
                ('OBSERVE', 0),           # Read observation state
                ('shamrock_stillman', 270), # Testing receives
                ('VALIDATE', 270),        # Validation completes
                ('todd_fishbone', 180)    # Index deployment state
            ]
        }
    ]
    
    for i, scenario in enumerate(production_scenarios, 1):
        print(f"\n## Production Test {i}: {scenario['name']}")
        print(f"**Scenario**: {scenario['description']}")
        
        # Encode with protection
        protected_msg = backend.encode_narrative_with_protection(
            scenario['description'], 
            scenario['sequence']
        )
        
        print(f"**Original Narrative**: {protected_msg.protection_metadata['narrative_description']}")
        
        # Show symbol sequence
        symbol_sequence = []
        for sym_data in protected_msg.original_symbols:
            symbol_sequence.append(f"{sym_data['symbol']['name']}@{sym_data['symbol']['rotation']}°")
        print(f"**Symbol Sequence**: {' → '.join(symbol_sequence)}")
        
        # Show canonical meaning
        narrative_meaning = " → ".join([sym['canon_meaning'] for sym in protected_msg.original_symbols])
        print(f"**Narrative Meaning**: {narrative_meaning}")
        
        print(f"**Protection Applied**: {protected_msg.protection_metadata['protection_level']}")
        print(f"**Encoding Time**: {protected_msg.protection_metadata['encoding_time_ms']:.2f}ms")
        
        # Test transmission scenarios
        error_rates = [0.005, 0.01, 0.02]  # 0.5%, 1.0%, 2.0%
        
        for error_rate in error_rates:
            print(f"\n### Transmission Test: {error_rate*100}% Error Rate")
            
            result = backend.simulate_transmission_and_recovery(protected_msg, error_rate)
            
            status = "✅ NARRATIVE PRESERVED" if result['protection_effectiveness'] else "❌ NARRATIVE CORRUPTED"
            print(f"   **Result**: {status}")
            print(f"   **Decode Time**: {result['decode_performance']['decode_time_ms']:.2f}ms")
            print(f"   **Performance Target**: {'✅ <4ms' if result['decode_performance']['meets_performance_target'] else '❌ >4ms'}")
            
            if result['protection_effectiveness']:
                print(f"   **Preserved Meaning**: {result['transmission_simulation']['recovered_narrative']}")
            else:
                print(f"   **Original**: {result['transmission_simulation']['original_narrative']}")
                print(f"   **Corrupted**: {result['transmission_simulation']['recovered_narrative']}")
                print("   **Impact**: Critical system operation would fail!")

def test_narrative_coherence():
    """Test narrative coherence preservation under extreme conditions"""
    
    print(f"\n{'='*60}")
    print("📚 Narrative Coherence Preservation Test")
    print(f"{'='*60}")
    
    backend = QDPIECCBackend()
    
    # Complex multi-step narrative
    complex_narrative = [
        ('The_Author', 90),           # ASK System Bootstrap
        ('SYNCHRONIZE', 270),         # Sync completes
        ('oren_progresso', 270),      # Orchestration receives
        ('arieol_owlist', 90),        # ASK Event Streaming
        ('OBSERVE', 0),               # Read observation
        ('princhetta', 90),           # ASK AI Orchestrator
        ('TRANSFORM', 270),           # Transform completes
        ('phillip_bafflemint', 270),  # Interface receives
        ('LINK', 180),                # Index connection
        ('london_fox', 0)             # Read Graph state
    ]
    
    description = "Complete system startup with AI coordination and user interface activation"
    
    print(f"**Complex Narrative**: {description}")
    print(f"**Sequence Length**: {len(complex_narrative)} symbols")
    
    # Encode with protection
    protected = backend.encode_narrative_with_protection(description, complex_narrative)
    
    # Show full narrative
    full_narrative = " → ".join([sym['canon_meaning'] for sym in protected.original_symbols])
    print(f"**Full Narrative**: {full_narrative}")
    
    # Test extreme corruption scenarios
    extreme_tests = [
        {'name': 'Light Corruption', 'error_rate': 0.005},
        {'name': 'Moderate Corruption', 'error_rate': 0.015}, 
        {'name': 'Heavy Corruption', 'error_rate': 0.025},
        {'name': 'Extreme Corruption', 'error_rate': 0.05}
    ]
    
    print(f"\n**Extreme Corruption Testing**:")
    
    for test in extreme_tests:
        result = backend.simulate_transmission_and_recovery(protected, test['error_rate'])
        
        coherence_preserved = result['protection_effectiveness']
        status = "✅ COHERENT" if coherence_preserved else "❌ CORRUPTED"
        
        print(f"   **{test['name']} ({test['error_rate']*100}%)**: {status}")
        if coherence_preserved:
            print(f"      Complete {len(complex_narrative)}-step narrative preserved")
        else:
            print(f"      Narrative broken - system startup would fail")

if __name__ == "__main__":
    test_production_integration()
    test_narrative_coherence()