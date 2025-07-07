#!/usr/bin/env python3
"""
QDPI-256 Symbol System Test
Validates the symbolic language using actual SVG corpus
"""

import os
import json
from pathlib import Path
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional

class QDPIRotation(Enum):
    READ = 0      # public→public, user-facing "in"
    WRITE = 1     # private→private, unpublished "out"
    REMEMBER = 2  # private→public, human curation
    DREAM = 3     # AI generative content

class QDPISymbol:
    def __init__(self, base_symbol: str, rotation: QDPIRotation, sequence_pos: int = 0):
        self.base_symbol = base_symbol
        self.rotation = rotation
        self.sequence_pos = sequence_pos
        self.timestamp = datetime.now().isoformat()
    
    @property
    def symbol_id(self) -> int:
        """Convert to 0-255 range"""
        base_id = self._get_base_id()
        return (base_id * 4) + self.rotation.value
    
    def _get_base_id(self) -> int:
        """Map symbol name to 0-63 base ID"""
        # Character symbols (0-15)
        characters = [
            "an_author", "london_fox", "glyph_marrow", "phillip_bafflemint",
            "manny_valentinas", "judy_s_cargot", "jacklyn_variance", "oren_progresso",
            "old_natalie_weissman", "princhetta", "cop_e_right", "new_natalie_weissman",
            "arieol_owlist", "jack_parlance", "shamrock_stillman", "the_author"
        ]
        
        if self.base_symbol in characters:
            return characters.index(self.base_symbol)
        
        # Hidden symbols (16-63)
        if self.base_symbol.startswith("hidden_symbol_"):
            hidden_num = int(self.base_symbol.split("_")[-1])
            return 15 + hidden_num  # 16-63 range
        
        raise ValueError(f"Unknown symbol: {self.base_symbol}")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "base_symbol": self.base_symbol,
            "rotation": self.rotation.name,
            "sequence_pos": self.sequence_pos,
            "symbol_id": self.symbol_id,
            "timestamp": self.timestamp,
            "svg_path": f"public/corpus-symbols/{self.base_symbol}.svg"
        }

class QDPISequence:
    """Track sequences of symbolic events"""
    
    def __init__(self, sequence_id: str):
        self.sequence_id = sequence_id
        self.symbols: List[QDPISymbol] = []
        self.created_at = datetime.now().isoformat()
    
    def add_symbol(self, base_symbol: str, rotation: QDPIRotation) -> QDPISymbol:
        """Add symbol to sequence"""
        symbol = QDPISymbol(
            base_symbol=base_symbol,
            rotation=rotation,
            sequence_pos=len(self.symbols)
        )
        self.symbols.append(symbol)
        return symbol
    
    def get_page_number(self, character: str) -> int:
        """Count sequential character symbols for page tracking"""
        count = 0
        for symbol in self.symbols:
            if symbol.base_symbol == character:
                count += 1
            else:
                break  # Stop at first non-matching symbol
        return count
    
    def to_ledger_entry(self) -> Dict[str, Any]:
        """Convert to ledger format"""
        return {
            "sequence_id": self.sequence_id,
            "created_at": self.created_at,
            "symbol_count": len(self.symbols),
            "symbols": [s.to_dict() for s in self.symbols],
            "privacy_map": self._analyze_privacy(),
            "character_presence": self._analyze_characters()
        }
    
    def _analyze_privacy(self) -> Dict[str, int]:
        """Analyze privacy distribution"""
        privacy_counts = {rot.name: 0 for rot in QDPIRotation}
        for symbol in self.symbols:
            privacy_counts[symbol.rotation.name] += 1
        return privacy_counts
    
    def _analyze_characters(self) -> Dict[str, int]:
        """Count character appearances"""
        char_counts = {}
        for symbol in self.symbols:
            char_counts[symbol.base_symbol] = char_counts.get(symbol.base_symbol, 0) + 1
        return char_counts

class QDPILedger:
    """System-wide symbolic event ledger"""
    
    def __init__(self, corpus_path: str = "public/corpus-symbols"):
        self.corpus_path = Path(corpus_path)
        self.sequences: Dict[str, QDPISequence] = {}
        self.validation_results = {}
        self.validate_corpus()
    
    def validate_corpus(self):
        """Verify all 64 base symbols exist"""
        missing_symbols = []
        found_symbols = []
        
        # Check 16 character symbols
        characters = [
            "an_author", "london_fox", "glyph_marrow", "phillip_bafflemint",
            "manny_valentinas", "judy_s_cargot", "jacklyn_variance", "oren_progresso",
            "old_natalie_weissman", "princhetta", "cop_e_right", "new_natalie_weissman",
            "arieol_owlist", "jack_parlance", "shamrock_stillman", "the_author"
        ]
        
        print(f"🔍 Validating corpus at: {self.corpus_path}")
        print(f"📁 Directory exists: {self.corpus_path.exists()}")
        
        if not self.corpus_path.exists():
            print(f"❌ Corpus directory not found!")
            return
        
        for char in characters:
            svg_path = self.corpus_path / f"{char}.svg"
            if not svg_path.exists():
                missing_symbols.append(f"{char}.svg")
            else:
                found_symbols.append(f"{char}.svg")
        
        # Check 48 hidden symbols
        for i in range(1, 49):
            svg_path = self.corpus_path / f"hidden_symbol_{i}.svg"
            if not svg_path.exists():
                missing_symbols.append(f"hidden_symbol_{i}.svg")
            else:
                found_symbols.append(f"hidden_symbol_{i}.svg")
        
        self.validation_results = {
            "total_expected": 64,
            "found_count": len(found_symbols),
            "missing_count": len(missing_symbols),
            "found_symbols": found_symbols,
            "missing_symbols": missing_symbols,
            "validation_status": "PASS" if len(missing_symbols) == 0 else "FAIL"
        }
        
        if missing_symbols:
            print(f"⚠️  Missing {len(missing_symbols)} symbols: {missing_symbols[:5]}{'...' if len(missing_symbols) > 5 else ''}")
        else:
            print("✅ All 64 base symbols validated")
    
    def create_sequence(self, sequence_id: str) -> QDPISequence:
        """Create new symbolic sequence"""
        sequence = QDPISequence(sequence_id)
        self.sequences[sequence_id] = sequence
        return sequence
    
    def export_ledger(self, filename: str = "test_qdpi_ledger.json"):
        """Export complete ledger"""
        ledger_data = {
            "ledger_metadata": {
                "created_at": datetime.now().isoformat(),
                "total_sequences": len(self.sequences),
                "total_symbols": sum(len(seq.symbols) for seq in self.sequences.values()),
                "corpus_path": str(self.corpus_path),
                "validation_results": self.validation_results
            },
            "sequences": {
                seq_id: seq.to_ledger_entry() 
                for seq_id, seq in self.sequences.items()
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(ledger_data, f, indent=2)
        
        print(f"📊 Ledger exported to {filename}")
        return ledger_data

def test_symbolic_interactions():
    """Test symbolic event tracking"""
    
    print("🧪 Testing QDPI-256 Symbolic Language System")
    print("=" * 50)
    
    # Initialize ledger
    ledger = QDPILedger()
    
    # Test 1: User reading an_author content (page tracking)
    print("\n📖 Test 1: User reading an_author content")
    read_sequence = ledger.create_sequence("user_read_session_001")
    
    # Three sequential an_author symbols = page 3
    read_sequence.add_symbol("an_author", QDPIRotation.READ)
    read_sequence.add_symbol("an_author", QDPIRotation.READ) 
    read_sequence.add_symbol("an_author", QDPIRotation.READ)
    
    page_num = read_sequence.get_page_number("an_author")
    print(f"   Page reached: {page_num}")
    print(f"   Symbol IDs: {[s.symbol_id for s in read_sequence.symbols]}")
    
    # Test 2: AI generating content (Dream mode)
    print("\n🤖 Test 2: AI generating london_fox analysis")
    ai_sequence = ledger.create_sequence("ai_generation_001")
    
    ai_sequence.add_symbol("london_fox", QDPIRotation.DREAM)  # AI analyzing consciousness
    ai_sequence.add_symbol("hidden_symbol_1", QDPIRotation.DREAM)  # AI processing
    ai_sequence.add_symbol("london_fox", QDPIRotation.WRITE)  # Private output
    
    print(f"   AI sequence: {[s.base_symbol for s in ai_sequence.symbols]}")
    print(f"   Privacy flow: {[s.rotation.name for s in ai_sequence.symbols]}")
    print(f"   Symbol IDs: {[s.symbol_id for s in ai_sequence.symbols]}")
    
    # Test 3: Mixed interaction sequence
    print("\n🔄 Test 3: Complex user-AI interaction")
    mixed_sequence = ledger.create_sequence("mixed_interaction_001")
    
    # User reads glyph_marrow
    mixed_sequence.add_symbol("glyph_marrow", QDPIRotation.READ)
    # User saves to memory
    mixed_sequence.add_symbol("glyph_marrow", QDPIRotation.REMEMBER)
    # AI processes in private
    mixed_sequence.add_symbol("hidden_symbol_2", QDPIRotation.WRITE)
    # AI generates public response
    mixed_sequence.add_symbol("princhetta", QDPIRotation.DREAM)
    
    privacy_analysis = mixed_sequence._analyze_privacy()
    print(f"   Privacy distribution: {privacy_analysis}")
    print(f"   Symbol IDs: {[s.symbol_id for s in mixed_sequence.symbols]}")
    
    # Test 4: Symbol ID range validation
    print("\n🎯 Test 4: Symbol ID Range Validation")
    
    # Test first character (an_author) all rotations
    an_author_ids = []
    for rot in QDPIRotation:
        symbol = QDPISymbol("an_author", rot)
        an_author_ids.append(symbol.symbol_id)
    print(f"   an_author rotations (0-3): {an_author_ids}")
    
    # Test last character (the_author) all rotations
    the_author_ids = []
    for rot in QDPIRotation:
        symbol = QDPISymbol("the_author", rot)
        the_author_ids.append(symbol.symbol_id)
    print(f"   the_author rotations (60-63): {the_author_ids}")
    
    # Test hidden symbols
    hidden_1_ids = []
    for rot in QDPIRotation:
        symbol = QDPISymbol("hidden_symbol_1", rot)
        hidden_1_ids.append(symbol.symbol_id)
    print(f"   hidden_symbol_1 rotations (64-67): {hidden_1_ids}")
    
    hidden_48_ids = []
    for rot in QDPIRotation:
        symbol = QDPISymbol("hidden_symbol_48", rot)
        hidden_48_ids.append(symbol.symbol_id)
    print(f"   hidden_symbol_48 rotations (252-255): {hidden_48_ids}")
    
    # Export ledger
    ledger_data = ledger.export_ledger("test_qdpi_ledger.json")
    
    print("\n📋 Validation Summary:")
    print(f"   Status: {ledger.validation_results['validation_status']}")
    print(f"   Found symbols: {ledger.validation_results['found_count']}/64")
    print(f"   Missing symbols: {ledger.validation_results['missing_count']}")
    
    print("\n✅ Symbolic language system test complete")
    return ledger, ledger_data

if __name__ == "__main__":
    test_ledger, results = test_symbolic_interactions()