#!/usr/bin/env python3
"""
QDPI-256 Symbol System Test V2
Enhanced with character-system architecture mapping
"""

import os
import json
from pathlib import Path
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple

class QDPIRotation(Enum):
    READ = 0      # public→public, user-facing "in"
    WRITE = 1     # private→private, unpublished "out"
    REMEMBER = 2  # private→public, human curation
    DREAM = 3     # AI generative content

class QDPISystem(Enum):
    """16 core systems mapped to characters"""
    USER_AUTH = 1              # an_author
    GRAPH_ENGINE = 2           # london_fox
    QDPI_PROTOCOL = 3          # glyph_marrow
    WORKFLOW_AUTOMATION = 4    # phillip_bafflemint
    CORE_DATABASE = 5          # jacklyn_variance
    ORCHESTRATION = 6          # oren_progresso
    SEMANTIC_SEARCH = 7        # old_natalie_weissman
    AI_ORCHESTRATION = 8       # princhetta
    LOCAL_AI = 9               # cop_e_right
    REAL_TIME_DATA = 10        # new_natalie_weissman
    EVENT_STREAMING = 11       # arieol_owlist
    REAL_TIME_COMM = 12        # jack_parlance
    KNOWLEDGE_BASE = 13        # manny_valentinas
    SECURITY_CDN = 14          # shamrock_stillman
    NLU = 15                   # judy_s_cargot
    P2P_NETWORK = 16           # the_author

# Character to System mapping with confidence scores
CHARACTER_SYSTEM_MAP = {
    # High confidence mappings
    "glyph_marrow": (QDPISystem.QDPI_PROTOCOL, 0.95),
    "london_fox": (QDPISystem.GRAPH_ENGINE, 0.92),
    "jacklyn_variance": (QDPISystem.CORE_DATABASE, 0.90),
    "oren_progresso": (QDPISystem.ORCHESTRATION, 0.88),
    "princhetta": (QDPISystem.AI_ORCHESTRATION, 0.87),
    "arieol_owlist": (QDPISystem.EVENT_STREAMING, 0.85),
    "phillip_bafflemint": (QDPISystem.WORKFLOW_AUTOMATION, 0.83),
    "shamrock_stillman": (QDPISystem.SECURITY_CDN, 0.82),
    
    # Medium confidence mappings
    "an_author": (QDPISystem.USER_AUTH, 0.75),
    "jack_parlance": (QDPISystem.REAL_TIME_COMM, 0.72),
    "old_natalie_weissman": (QDPISystem.SEMANTIC_SEARCH, 0.70),
    "new_natalie_weissman": (QDPISystem.REAL_TIME_DATA, 0.68),
    "cop_e_right": (QDPISystem.LOCAL_AI, 0.65),
    "the_author": (QDPISystem.P2P_NETWORK, 0.62),
    
    # Lower confidence / needs assignment
    "manny_valentinas": (QDPISystem.KNOWLEDGE_BASE, 0.50),
    "judy_s_cargot": (QDPISystem.NLU, 0.55),
}

class QDPISymbol:
    def __init__(self, base_symbol: str, rotation: QDPIRotation, system: Optional[QDPISystem] = None, sequence_pos: int = 0):
        self.base_symbol = base_symbol
        self.rotation = rotation
        self.sequence_pos = sequence_pos
        self.timestamp = datetime.now().isoformat()
        
        # Auto-detect system from character mapping
        if system is None and base_symbol in CHARACTER_SYSTEM_MAP:
            self.system, self.confidence = CHARACTER_SYSTEM_MAP[base_symbol]
        else:
            self.system = system
            self.confidence = 1.0 if system else 0.0
    
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
        
        # Handle case variations
        normalized_symbol = self.base_symbol.lower().replace("-", "_")
        
        if normalized_symbol in characters:
            return characters.index(normalized_symbol)
        
        # Hidden symbols (16-63) - handle both formats
        if normalized_symbol.startswith("hidden_symbol_"):
            hidden_str = normalized_symbol.replace("hidden_symbol_", "")
            # Handle both "01" and "1" formats
            hidden_num = int(hidden_str.lstrip("0") or "0")
            return 15 + hidden_num  # 16-63 range
        
        raise ValueError(f"Unknown symbol: {self.base_symbol}")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "base_symbol": self.base_symbol,
            "rotation": self.rotation.name,
            "rotation_value": self.rotation.value,
            "sequence_pos": self.sequence_pos,
            "symbol_id": self.symbol_id,
            "system": self.system.name if self.system else None,
            "system_id": self.system.value if self.system else None,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "svg_path": f"public/corpus-symbols/{self.base_symbol}.svg"
        }

class QDPISequence:
    """Track sequences of symbolic events with system context"""
    
    def __init__(self, sequence_id: str, originating_system: QDPISystem):
        self.sequence_id = sequence_id
        self.originating_system = originating_system
        self.symbols: List[QDPISymbol] = []
        self.created_at = datetime.now().isoformat()
    
    def add_symbol(self, base_symbol: str, rotation: QDPIRotation, system: Optional[QDPISystem] = None) -> QDPISymbol:
        """Add symbol to sequence"""
        symbol = QDPISymbol(
            base_symbol=base_symbol,
            rotation=rotation,
            system=system,
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
                break
        return count
    
    def analyze_system_flow(self) -> Dict[str, Any]:
        """Analyze how data flows between systems"""
        system_transitions = []
        for i in range(1, len(self.symbols)):
            prev_system = self.symbols[i-1].system
            curr_system = self.symbols[i].system
            if prev_system and curr_system:
                system_transitions.append({
                    "from": prev_system.name,
                    "to": curr_system.name,
                    "privacy_shift": f"{self.symbols[i-1].rotation.name}→{self.symbols[i].rotation.name}"
                })
        return {
            "originating_system": self.originating_system.name,
            "systems_involved": list(set(s.system.name for s in self.symbols if s.system)),
            "system_transitions": system_transitions
        }
    
    def to_ledger_entry(self) -> Dict[str, Any]:
        """Convert to ledger format with system context"""
        return {
            "sequence_id": self.sequence_id,
            "created_at": self.created_at,
            "originating_system": self.originating_system.name,
            "symbol_count": len(self.symbols),
            "symbols": [s.to_dict() for s in self.symbols],
            "privacy_map": self._analyze_privacy(),
            "character_presence": self._analyze_characters(),
            "system_flow": self.analyze_system_flow()
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
    """System-wide symbolic event ledger with architecture awareness"""
    
    def __init__(self, corpus_path: str = "public/corpus-symbols"):
        self.corpus_path = Path(corpus_path)
        self.sequences: Dict[str, QDPISequence] = {}
        self.validation_results = {}
        self.validate_corpus()
    
    def validate_corpus(self):
        """Verify all 64 base symbols exist"""
        missing_symbols = []
        found_symbols = []
        naming_issues = []
        
        # Expected character symbols
        expected_characters = [
            "an_author", "london_fox", "glyph_marrow", "phillip_bafflemint",
            "manny_valentinas", "judy_s_cargot", "jacklyn_variance", "oren_progresso",
            "old_natalie_weissman", "princhetta", "cop_e_right", "new_natalie_weissman",
            "arieol_owlist", "jack_parlance", "shamrock_stillman", "the_author"
        ]
        
        print(f"🔍 Validating corpus at: {self.corpus_path}")
        
        if not self.corpus_path.exists():
            print(f"❌ Corpus directory not found!")
            return
        
        # Get all SVG files
        all_svgs = list(self.corpus_path.glob("*.svg"))
        svg_names = [svg.stem for svg in all_svgs]
        
        # Check character symbols with flexible matching
        for expected_char in expected_characters:
            found = False
            # Try exact match
            if expected_char in svg_names:
                found_symbols.append(f"{expected_char}.svg")
                found = True
            else:
                # Try variations
                variations = [
                    expected_char.replace("_", "-"),
                    expected_char.replace("_", " "),
                    expected_char.replace("_", ""),
                    expected_char.title().replace("_", ""),
                ]
                for variant in variations:
                    if variant in svg_names or variant.lower() in [s.lower() for s in svg_names]:
                        found_symbols.append(f"{variant}.svg")
                        naming_issues.append(f"Expected '{expected_char}' but found variant")
                        found = True
                        break
            
            if not found:
                missing_symbols.append(f"{expected_char}.svg")
        
        # Check hidden symbols (both 01 and 1 formats)
        for i in range(1, 49):
            # Try both formats
            formats = [f"hidden_symbol_{i}", f"hidden_symbol_{i:02d}"]
            found = False
            for fmt in formats:
                if fmt in svg_names:
                    found_symbols.append(f"{fmt}.svg")
                    found = True
                    break
            if not found:
                missing_symbols.append(f"hidden_symbol_{i}.svg")
        
        self.validation_results = {
            "total_expected": 64,
            "found_count": len(found_symbols),
            "missing_count": len(missing_symbols),
            "naming_issues": naming_issues,
            "found_symbols": found_symbols,
            "missing_symbols": missing_symbols,
            "validation_status": "PASS" if len(missing_symbols) == 0 else "PARTIAL"
        }
        
        print(f"✅ Found {len(found_symbols)}/64 symbols")
        if naming_issues:
            print(f"⚠️  {len(naming_issues)} naming inconsistencies detected")
        if missing_symbols:
            print(f"⚠️  Missing {len(missing_symbols)} symbols")
    
    def create_sequence(self, sequence_id: str, originating_system: QDPISystem) -> QDPISequence:
        """Create new symbolic sequence with system context"""
        sequence = QDPISequence(sequence_id, originating_system)
        self.sequences[sequence_id] = sequence
        return sequence

def test_system_integrated_flows():
    """Test symbolic flows with system architecture integration"""
    
    print("🧪 Testing QDPI-256 with System Architecture Integration")
    print("=" * 60)
    
    ledger = QDPILedger()
    
    # Test 1: User Authentication Flow
    print("\n🔐 Test 1: User Authentication Flow")
    auth_sequence = ledger.create_sequence("auth_flow_001", QDPISystem.USER_AUTH)
    
    # User initiates auth (an_author system)
    auth_sequence.add_symbol("an_author", QDPIRotation.READ)
    # Security validates (shamrock_stillman)
    auth_sequence.add_symbol("shamrock_stillman", QDPIRotation.WRITE)
    # Database stores (jacklyn_variance)
    auth_sequence.add_symbol("jacklyn_variance", QDPIRotation.REMEMBER)
    
    flow_analysis = auth_sequence.analyze_system_flow()
    print(f"   Systems: {' → '.join(flow_analysis['systems_involved'])}")
    print(f"   Symbol IDs: {[s.symbol_id for s in auth_sequence.symbols]}")
    
    # Test 2: AI Processing Pipeline
    print("\n🤖 Test 2: AI Processing Pipeline")
    ai_sequence = ledger.create_sequence("ai_pipeline_001", QDPISystem.AI_ORCHESTRATION)
    
    # User input (glyph_marrow QDPI encoding)
    ai_sequence.add_symbol("glyph_marrow", QDPIRotation.READ)
    # AI orchestration (princhetta)
    ai_sequence.add_symbol("princhetta", QDPIRotation.DREAM)
    # Local AI processing (cop_e_right)
    ai_sequence.add_symbol("cop_e_right", QDPIRotation.WRITE)
    # Graph relationships (london_fox)
    ai_sequence.add_symbol("london_fox", QDPIRotation.REMEMBER)
    
    ai_flow = ai_sequence.analyze_system_flow()
    print(f"   Pipeline: {' → '.join(s['from'] + '(' + s['privacy_shift'] + ')' for s in ai_flow['system_transitions'])}")
    
    # Test 3: Real-time Event Flow
    print("\n⚡ Test 3: Real-time Event Processing")
    event_sequence = ledger.create_sequence("realtime_001", QDPISystem.EVENT_STREAMING)
    
    # Event triggered (arieol_owlist)
    event_sequence.add_symbol("arieol_owlist", QDPIRotation.READ)
    # Workflow automation (phillip_bafflemint)
    event_sequence.add_symbol("phillip_bafflemint", QDPIRotation.WRITE)
    # Real-time data update (new_natalie)
    event_sequence.add_symbol("new_natalie_weissman", QDPIRotation.DREAM)
    # Orchestration monitoring (oren_progresso)
    event_sequence.add_symbol("oren_progresso", QDPIRotation.REMEMBER)
    
    print(f"   Event flow confidence: {[f'{s.confidence:.2f}' for s in event_sequence.symbols]}")
    
    # Test 4: Cross-System Integration
    print("\n🔄 Test 4: Full System Integration Test")
    
    # Map all 16 systems
    system_coverage = set()
    integration_sequence = ledger.create_sequence("full_integration_001", QDPISystem.ORCHESTRATION)
    
    for char, (system, confidence) in CHARACTER_SYSTEM_MAP.items():
        integration_sequence.add_symbol(char, QDPIRotation(len(system_coverage) % 4))
        system_coverage.add(system)
    
    print(f"   Systems covered: {len(system_coverage)}/16")
    print(f"   Average confidence: {sum(s.confidence for s in integration_sequence.symbols) / len(integration_sequence.symbols):.2f}")
    
    # Export enhanced ledger
    ledger_data = {
        "ledger_metadata": {
            "created_at": datetime.now().isoformat(),
            "total_sequences": len(ledger.sequences),
            "corpus_validation": ledger.validation_results,
            "system_architecture_version": "2.0"
        },
        "sequences": {
            seq_id: seq.to_ledger_entry()
            for seq_id, seq in ledger.sequences.items()
        },
        "system_mappings": {
            char: {"system": sys.name, "confidence": conf}
            for char, (sys, conf) in CHARACTER_SYSTEM_MAP.items()
        }
    }
    
    with open("test_qdpi_system_ledger.json", "w") as f:
        json.dump(ledger_data, f, indent=2)
    
    print(f"\n📊 Enhanced ledger exported with system integration")
    print(f"✅ QDPI-256 + System Architecture test complete")
    
    return ledger, ledger_data

if __name__ == "__main__":
    ledger, results = test_system_integrated_flows()