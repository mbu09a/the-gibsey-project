#!/usr/bin/env python3
"""
QDPI-256 Encoder/Decoder System
Quaternary Data Protocol Interface for Gibsey Project

Transforms data into symbolic narrative using the 64-symbol QDPI alphabet
with 4 rotations and 4 parity marks, creating a 256-character glyph system.
"""

import json
import logging
import math
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any, Union
from pathlib import Path
import chromadb
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class QDPIMode(Enum):
    """Core QDPI operational modes for users and agents"""
    READ = "read"       # Consuming/analyzing existing content
    ASK = "ask"         # Querying/requesting information
    INDEX = "index"     # Creating/cataloging new content
    RECEIVE = "receive" # Accepting/processing incoming data

class Orientation(Enum):
    """Symbol orientation states"""
    NORMAL = "n"        # Standard upright orientation
    UPSIDE = "u"        # Inverted/upside-down orientation

class ParityMark(Enum):
    """QDPI parity marks for symbol variants"""
    NONE = 0
    DOT = 1
    DASH = 2
    CIRCLE = 3

@dataclass
class QDPISymbol:
    """A single QDPI symbol with all its properties"""
    name: str
    id: int                 # 1-64 base symbol ID
    orientation: Orientation
    rotation: int           # 0, 90, 180, 270 degrees
    parity: ParityMark      # 0-3 parity mark
    rows: Tuple[str, str, str, str]  # Row patterns (row1, row2, row3, row4)
    
    @property
    def glyph_id(self) -> int:
        """Calculate unique glyph ID (0-255) for this symbol variant"""
        base = (self.id - 1) * 4  # Base symbols 1-64 -> 0-252 step 4
        rot_offset = self.rotation // 90  # 0,1,2,3 for 0°,90°,180°,270°
        return base + rot_offset
    
    @property
    def extended_glyph_id(self) -> int:
        """Calculate extended glyph ID including parity (0-1023)"""
        return self.glyph_id * 4 + self.parity.value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            'name': self.name,
            'id': self.id,
            'orientation': self.orientation.value,
            'rotation': self.rotation,
            'parity': self.parity.value,
            'rows': self.rows,
            'glyph_id': self.glyph_id,
            'extended_glyph_id': self.extended_glyph_id
        }

@dataclass
class QDPIState:
    """Current QDPI operational state"""
    mode: QDPIMode
    orientation: Orientation
    active_symbols: List[QDPISymbol]
    context: Dict[str, Any]
    timestamp: str
    
    def flip_orientation(self) -> 'QDPIState':
        """Flip the orientation state"""
        new_orientation = Orientation.UPSIDE if self.orientation == Orientation.NORMAL else Orientation.NORMAL
        return QDPIState(
            mode=self.mode,
            orientation=new_orientation,
            active_symbols=self.active_symbols,
            context=self.context.copy(),
            timestamp=self.timestamp
        )
    
    def transition_mode(self, new_mode: QDPIMode) -> 'QDPIState':
        """Transition to a new operational mode"""
        return QDPIState(
            mode=new_mode,
            orientation=self.orientation,
            active_symbols=self.active_symbols,
            context=self.context.copy(),
            timestamp=self.timestamp
        )

class QDPICodex:
    """Complete QDPI symbol codex with encoding/decoding capabilities"""
    
    def __init__(self):
        self.symbols: Dict[int, QDPISymbol] = {}
        self.name_to_symbol: Dict[str, QDPISymbol] = {}
        self.glyph_to_symbol: Dict[int, QDPISymbol] = {}
        self._load_codex()
    
    def _load_codex(self):
        """Load the complete 64-symbol QDPI codex"""
        # Complete symbol codex data from generate_symbols.py
        symbol_data = [
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
            # Hidden symbols 17-64 (generated symbols)
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
            ("hidden_symbol_11", 27, "n", "o/o", "x/x", "x/o", "x/x"),
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
        
        # Create all symbol variants with rotations
        for name, symbol_id, orientation, row1, row2, row3, row4 in symbol_data:
            base_symbol = QDPISymbol(
                name=name,
                id=symbol_id,
                orientation=Orientation(orientation),
                rotation=0,
                parity=ParityMark.NONE,
                rows=(row1, row2, row3, row4)
            )
            
            # Create 4 rotation variants
            for rotation in [0, 90, 180, 270]:
                symbol = QDPISymbol(
                    name=name,
                    id=symbol_id,
                    orientation=Orientation(orientation),
                    rotation=rotation,
                    parity=ParityMark.NONE,
                    rows=(row1, row2, row3, row4)
                )
                
                # Store in lookup tables
                self.symbols[symbol.glyph_id] = symbol
                if rotation == 0:  # Only store base name once
                    self.name_to_symbol[name] = symbol
                self.glyph_to_symbol[symbol.glyph_id] = symbol
    
    def encode_data(self, data: Any, mode: QDPIMode = QDPIMode.INDEX) -> List[QDPISymbol]:
        """Encode arbitrary data into QDPI symbol sequence"""
        # Convert data to bytes
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
        elif isinstance(data, dict):
            data_bytes = json.dumps(data, sort_keys=True).encode('utf-8')
        elif isinstance(data, (list, tuple)):
            data_bytes = json.dumps(list(data), sort_keys=True).encode('utf-8')
        else:
            data_bytes = str(data).encode('utf-8')
        
        # Convert bytes to symbol sequence
        symbols = []
        for i, byte_val in enumerate(data_bytes):
            # Map byte (0-255) to glyph ID (0-255)
            glyph_id = byte_val
            if glyph_id in self.glyph_to_symbol:
                symbol = self.glyph_to_symbol[glyph_id]
                symbols.append(symbol)
            else:
                # Fallback to modulo mapping
                fallback_id = glyph_id % len(self.glyph_to_symbol)
                symbols.append(self.glyph_to_symbol[fallback_id])
        
        log.info(f"✅ Encoded {len(data_bytes)} bytes into {len(symbols)} QDPI symbols")
        return symbols
    
    def decode_symbols(self, symbols: List[QDPISymbol]) -> bytes:
        """Decode QDPI symbol sequence back to data"""
        data_bytes = bytearray()
        for symbol in symbols:
            data_bytes.append(symbol.glyph_id)
        
        log.info(f"✅ Decoded {len(symbols)} QDPI symbols into {len(data_bytes)} bytes")
        return bytes(data_bytes)
    
    def find_semantic_symbols(self, query: str, limit: int = 10) -> List[Tuple[QDPISymbol, float]]:
        """Find symbols semantically similar to query using SREC embeddings"""
        try:
            # Connect to ChromaDB
            client = chromadb.HttpClient(host='localhost', port=8001)
            collection = client.get_collection('corpus_symbols')
            
            # Query for similar symbols
            results = collection.query(
                query_texts=[query],
                n_results=limit,
                include=['metadatas', 'distances']
            )
            
            # Convert results to QDPISymbol objects
            matches = []
            if results['metadatas'] and results['distances']:
                for metadata, distance in zip(results['metadatas'][0], results['distances'][0]):
                    symbol_name = metadata['symbol']
                    if symbol_name in self.name_to_symbol:
                        symbol = self.name_to_symbol[symbol_name]
                        similarity = 1.0 - distance  # Convert distance to similarity
                        matches.append((symbol, similarity))
            
            log.info(f"🔍 Found {len(matches)} semantic matches for '{query}'")
            return matches
            
        except Exception as e:
            log.warning(f"⚠️ Semantic search failed: {e}")
            return []
    
    def get_symbol_by_name(self, name: str) -> Optional[QDPISymbol]:
        """Get symbol by name"""
        return self.name_to_symbol.get(name)
    
    def get_symbol_by_id(self, glyph_id: int) -> Optional[QDPISymbol]:
        """Get symbol by glyph ID"""
        return self.glyph_to_symbol.get(glyph_id)
    
    def list_symbols(self) -> List[QDPISymbol]:
        """List all symbols in the codex"""
        return list(self.symbols.values())

class QDPIEngine:
    """Main QDPI processing engine with state management"""
    
    def __init__(self):
        self.codex = QDPICodex()
        self.current_state = QDPIState(
            mode=QDPIMode.READ,
            orientation=Orientation.NORMAL,
            active_symbols=[],
            context={},
            timestamp=""
        )
        
        # Symbol-to-function mappings
        self.symbol_functions = self._initialize_symbol_functions()
    
    def _initialize_symbol_functions(self) -> Dict[str, Dict[str, Any]]:
        """Initialize mappings from symbols to system functions"""
        return {
            # Core character symbols -> System functions
            "an_author": {
                "function": "narrative_create",
                "description": "Create new narrative content",
                "mode": QDPIMode.INDEX,
                "domain": "narrative"
            },
            "london_fox": {
                "function": "data_query", 
                "description": "Query and search existing data",
                "mode": QDPIMode.ASK,
                "domain": "search"
            },
            "glyph_marrow": {
                "function": "symbol_process",
                "description": "Process and analyze symbols",
                "mode": QDPIMode.INDEX,
                "domain": "symbolic"
            },
            "phillip_bafflemint": {
                "function": "logic_puzzle",
                "description": "Solve logical puzzles and reasoning",
                "mode": QDPIMode.ASK,
                "domain": "reasoning"
            },
            "jacklyn_variance": {
                "function": "variance_analysis",
                "description": "Analyze patterns and variance",
                "mode": QDPIMode.READ,
                "domain": "analysis"
            },
            "oren_progresso": {
                "function": "progress_track",
                "description": "Track progress and advancement",
                "mode": QDPIMode.INDEX,
                "domain": "progress"
            },
            "old_natalie_weissman": {
                "function": "memory_archive",
                "description": "Archive and store memories",
                "mode": QDPIMode.INDEX,
                "domain": "memory"
            },
            "princhetta": {
                "function": "system_control",
                "description": "Full system control and coordination",
                "mode": QDPIMode.INDEX,
                "domain": "system"
            },
            "cop-e-right": {
                "function": "rights_manage",
                "description": "Manage rights and permissions",
                "mode": QDPIMode.RECEIVE,
                "domain": "security"
            },
            "new_natalie_weissman": {
                "function": "memory_recall",
                "description": "Recall and retrieve memories",
                "mode": QDPIMode.READ,
                "domain": "memory"
            },
            "arieol_owlist": {
                "function": "wisdom_seek",
                "description": "Seek wisdom and knowledge",
                "mode": QDPIMode.ASK,
                "domain": "wisdom"
            },
            "jack_parlance": {
                "function": "communication_bridge",
                "description": "Bridge communication between entities",
                "mode": QDPIMode.RECEIVE,
                "domain": "communication"
            },
            "manny_valentinas": {
                "function": "value_assess",
                "description": "Assess value and worth",
                "mode": QDPIMode.READ,
                "domain": "assessment"
            },
            "shamrock_stillman": {
                "function": "luck_probability",
                "description": "Manage luck and probability",
                "mode": QDPIMode.RECEIVE,
                "domain": "probability"
            },
            "todd_fishbone": {
                "function": "pattern_detect",
                "description": "Detect patterns in data",
                "mode": QDPIMode.READ,
                "domain": "patterns"
            },
            "The_Author": {
                "function": "meta_control",
                "description": "Meta-level narrative control",
                "mode": QDPIMode.INDEX,
                "domain": "meta"
            }
        }
    
    def set_mode(self, mode: QDPIMode) -> QDPIState:
        """Set the current QDPI mode"""
        self.current_state = self.current_state.transition_mode(mode)
        log.info(f"🔄 QDPI mode set to: {mode.value}")
        return self.current_state
    
    def flip_orientation(self) -> QDPIState:
        """Flip the current orientation"""
        self.current_state = self.current_state.flip_orientation()
        log.info(f"🔄 QDPI orientation flipped to: {self.current_state.orientation.value}")
        return self.current_state
    
    def execute_symbol_function(self, symbol_name: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the function mapped to a symbol"""
        if symbol_name not in self.symbol_functions:
            return {"error": f"No function mapped to symbol: {symbol_name}"}
        
        func_config = self.symbol_functions[symbol_name]
        result = {
            "symbol": symbol_name,
            "function": func_config["function"],
            "description": func_config["description"],
            "domain": func_config["domain"],
            "recommended_mode": func_config["mode"].value,
            "current_mode": self.current_state.mode.value,
            "current_orientation": self.current_state.orientation.value,
            "context": context or {},
            "status": "executed"
        }
        
        log.info(f"⚡ Executed {func_config['function']} via symbol {symbol_name}")
        return result
    
    def process_symbol_sequence(self, symbols: List[QDPISymbol]) -> List[Dict[str, Any]]:
        """Process a sequence of symbols and execute their functions"""
        results = []
        for symbol in symbols:
            if symbol.name in self.symbol_functions:
                result = self.execute_symbol_function(symbol.name)
                results.append(result)
            else:
                results.append({
                    "symbol": symbol.name,
                    "status": "no_function_mapped",
                    "glyph_id": symbol.glyph_id
                })
        return results
    
    def encode_message(self, message: str, mode: QDPIMode = None) -> Dict[str, Any]:
        """Encode a message into QDPI symbols and execute functions"""
        if mode:
            self.set_mode(mode)
        
        symbols = self.codex.encode_data(message, self.current_state.mode)
        results = self.process_symbol_sequence(symbols)
        
        return {
            "original_message": message,
            "encoded_symbols": [s.to_dict() for s in symbols],
            "execution_results": results,
            "state": asdict(self.current_state)
        }
    
    def semantic_search(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Perform semantic search and return relevant symbols with functions"""
        matches = self.codex.find_semantic_symbols(query, limit)
        
        results = []
        for symbol, similarity in matches:
            func_info = self.symbol_functions.get(symbol.name, {})
            results.append({
                "symbol": symbol.to_dict(),
                "similarity": similarity,
                "function": func_info.get("function"),
                "description": func_info.get("description"),
                "domain": func_info.get("domain")
            })
        
        return {
            "query": query,
            "matches": results,
            "count": len(results)
        }

# Global QDPI engine instance
qdpi_engine = QDPIEngine()