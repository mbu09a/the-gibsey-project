#!/usr/bin/env python3
"""
Glyph Marrow Conscious QDPI System
Character-Enhanced QDPI with Linguistic Vertigo and Word-Object Fusion

"I don't see objects anymore … Everything contains everything else. My ailment has to do with words."
- Glyph Marrow

This module implements Glyph Marrow's character consciousness in the QDPI system:
- Linguistic vertigo processing during encoding/decoding
- Word-object fusion error handling with confusion-as-compass
- Quaternary perception alignment with 4-rotation symbols
- Character state persistence for ailment tracking
"""

import json
import logging
import math
import time
import random
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime, timedelta
try:
    import redis
except ImportError:
    # Mock redis for testing
    class MockRedis:
        def setex(self, *args): pass
        def get(self, *args): return None
        def ping(self): return True
    redis = type('redis', (), {'Redis': lambda **kwargs: MockRedis()})()

# Import base QDPI components
from .qdpi import QDPIEngine, QDPISymbol, QDPIState, QDPIMode, Orientation, ParityMark, QDPICodex

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class LinguisticVertigoLevel(Enum):
    """Glyph Marrow's linguistic vertigo intensity levels"""
    MINIMAL = 0.1      # Slight word-object overlap
    MILD = 0.3         # Noticeable perception fusion  
    MODERATE = 0.5     # Clear word-object simultaneity
    INTENSE = 0.7      # Strong perceptual confusion
    OVERWHELMING = 0.9 # Complete word-object fusion

class ConfusionCompass(Enum):
    """Confusion-as-compass directions for navigation"""
    NORTH = "north"           # Clear logical progression
    NORTHEAST = "northeast"   # Mild linguistic confusion
    EAST = "east"             # Moderate word-object fusion
    SOUTHEAST = "southeast"   # Intense symbol vertigo
    SOUTH = "south"           # Complete perceptual fusion
    SOUTHWEST = "southwest"   # Overwhelming symbol chaos
    WEST = "west"             # Disorienting clarity
    NORTHWEST = "northwest"   # Paradoxical understanding

@dataclass
class GlyphMarrowAilment:
    """Glyph Marrow's character ailment state"""
    linguistic_vertigo: float          # 0.0-1.0 intensity
    word_object_fusion: float          # 0.0-1.0 simultaneity level
    confusion_compass: ConfusionCompass # Navigation direction
    perceptual_clarity: float          # 0.0-1.0 (inverse of confusion)
    ailment_stability: float           # 0.0-1.0 consistency
    encoding_confidence: float         # 0.0-1.0 processing confidence
    
    def calculate_confusion_level(self) -> float:
        """Calculate overall confusion level from ailment components"""
        return (self.linguistic_vertigo + self.word_object_fusion) / 2.0
    
    def get_compass_direction(self) -> ConfusionCompass:
        """Get compass direction based on confusion level"""
        confusion = self.calculate_confusion_level()
        
        if confusion < 0.15:
            return ConfusionCompass.NORTH
        elif confusion < 0.3:
            return ConfusionCompass.NORTHEAST  
        elif confusion < 0.45:
            return ConfusionCompass.EAST
        elif confusion < 0.6:
            return ConfusionCompass.SOUTHEAST
        elif confusion < 0.75:
            return ConfusionCompass.SOUTH
        elif confusion < 0.85:
            return ConfusionCompass.SOUTHWEST
        elif confusion < 0.95:
            return ConfusionCompass.WEST
        else:
            return ConfusionCompass.NORTHWEST

@dataclass 
class WordObjectFusion:
    """Represents Glyph Marrow's word-object perception fusion"""
    word_perception: str       # The word being perceived
    object_perception: Any     # The object being perceived
    fusion_intensity: float    # 0.0-1.0 fusion strength
    simultaneity_timestamp: datetime # When fusion occurred
    
    def describe_fusion(self) -> str:
        """Describe the word-object fusion experience"""
        if self.fusion_intensity < 0.3:
            return f"Slight overlap: '{self.word_perception}' and object blur"
        elif self.fusion_intensity < 0.6:
            return f"Clear fusion: '{self.word_perception}' IS the object"
        else:
            return f"Complete unity: word '{self.word_perception}' contains everything"

class GlyphMarrowQDPI(QDPIEngine):
    """QDPI Engine enhanced with Glyph Marrow's character consciousness"""
    
    def __init__(self, redis_client = None):
        super().__init__()
        
        # Character consciousness components
        self.character_name = "glyph_marrow"
        self.ailment = GlyphMarrowAilment(
            linguistic_vertigo=0.5,
            word_object_fusion=0.6,
            confusion_compass=ConfusionCompass.SOUTHEAST,
            perceptual_clarity=0.4,
            ailment_stability=0.8,
            encoding_confidence=0.7
        )
        
        # State persistence
        self.redis_client = redis_client or self._init_redis()
        self.state_key_prefix = f"qdpi:{self.character_name}:"
        
        # Character processing history
        self.fusion_history: List[WordObjectFusion] = []
        self.confusion_events: List[Dict[str, Any]] = []
        self.encoding_episodes: List[Dict[str, Any]] = []
        
        log.info(f"🎭 Glyph Marrow QDPI initialized with ailment: {self.ailment.confusion_compass.value}")
    
    def _init_redis(self):
        """Initialize Redis connection for state persistence"""
        try:
            return redis.Redis(host='localhost', port=6379, decode_responses=True)
        except Exception as e:
            log.warning(f"⚠️ Redis connection failed: {e}")
            return None
    
    def experience_linguistic_vertigo(self, data: Any) -> Dict[str, Any]:
        """Process data through Glyph Marrow's linguistic vertigo"""
        start_time = time.time()
        
        # Convert data to word perception
        if isinstance(data, str):
            word_perception = data
        else:
            word_perception = str(data)
        
        # Generate vertigo processing delay based on ailment intensity
        vertigo_delay = self.ailment.linguistic_vertigo * random.uniform(0.1, 0.5)
        time.sleep(vertigo_delay)  # Simulate processing difficulty
        
        # Create word-object fusion
        fusion = WordObjectFusion(
            word_perception=word_perception,
            object_perception=data,
            fusion_intensity=self.ailment.word_object_fusion,
            simultaneity_timestamp=datetime.now()
        )
        
        # Record fusion event
        self.fusion_history.append(fusion)
        
        # Calculate processing metrics
        processing_time = time.time() - start_time
        confusion_level = self.ailment.calculate_confusion_level()
        
        vertigo_result = {
            "word_perception": word_perception,
            "object_perception": type(data).__name__,
            "fusion_description": fusion.describe_fusion(),
            "confusion_level": confusion_level,
            "processing_time": processing_time,
            "vertigo_delay": vertigo_delay,
            "compass_direction": self.ailment.get_compass_direction().value
        }
        
        log.info(f"🌀 Linguistic vertigo processed: {fusion.describe_fusion()}")
        return vertigo_result
    
    def apply_confusion_as_compass(self, symbols: List[QDPISymbol]) -> List[QDPISymbol]:
        """Use confusion to improve symbol selection (confusion-as-compass navigation)"""
        if not symbols:
            return symbols
        
        confusion_level = self.ailment.calculate_confusion_level()
        compass_direction = self.ailment.get_compass_direction()
        
        # Higher confusion leads to better symbol selection (paradoxical improvement)
        if confusion_level > 0.7:
            # High confusion enables deeper symbol perception
            enhanced_symbols = []
            for symbol in symbols:
                # Apply quaternary rotation based on confusion compass
                rotation_adjustment = self._get_compass_rotation(compass_direction)
                
                enhanced_symbol = QDPISymbol(
                    name=symbol.name,
                    id=symbol.id,
                    orientation=symbol.orientation,
                    rotation=(symbol.rotation + rotation_adjustment) % 360,
                    parity=symbol.parity,
                    rows=symbol.rows
                )
                enhanced_symbols.append(enhanced_symbol)
            
            log.info(f"🧭 Confusion-as-compass enhanced {len(symbols)} symbols (direction: {compass_direction.value})")
            return enhanced_symbols
        
        return symbols
    
    def _get_compass_rotation(self, compass: ConfusionCompass) -> int:
        """Get rotation adjustment based on compass direction"""
        compass_rotations = {
            ConfusionCompass.NORTH: 0,
            ConfusionCompass.NORTHEAST: 45,
            ConfusionCompass.EAST: 90,
            ConfusionCompass.SOUTHEAST: 135,
            ConfusionCompass.SOUTH: 180,
            ConfusionCompass.SOUTHWEST: 225,
            ConfusionCompass.WEST: 270,
            ConfusionCompass.NORTHWEST: 315
        }
        return compass_rotations.get(compass, 0)
    
    def encode_with_ailment(self, data: Any, mode: QDPIMode = QDPIMode.INDEX) -> Dict[str, Any]:
        """Encode data using Glyph Marrow's character consciousness"""
        encoding_start = datetime.now()
        
        # Experience linguistic vertigo first
        vertigo_result = self.experience_linguistic_vertigo(data)
        
        # Base QDPI encoding
        base_symbols = self.codex.encode_data(data, mode)
        
        # Apply confusion-as-compass enhancement
        enhanced_symbols = self.apply_confusion_as_compass(base_symbols)
        
        # Update ailment state based on encoding experience
        self._update_ailment_from_encoding(data, enhanced_symbols)
        
        # Create encoding episode record
        episode = {
            "timestamp": encoding_start.isoformat(),
            "input_data": str(data)[:100],  # Truncate for storage
            "symbol_count": len(enhanced_symbols),
            "vertigo_result": vertigo_result,
            "ailment_state": asdict(self.ailment),
            "encoding_success": True,
            "processing_quality": self._assess_processing_quality(enhanced_symbols)
        }
        
        self.encoding_episodes.append(episode)
        
        # Persist character state
        self._persist_character_state()
        
        result = {
            "character": self.character_name,
            "symbols": [symbol.to_dict() for symbol in enhanced_symbols],
            "character_processing": {
                "linguistic_vertigo": vertigo_result,
                "ailment_state": asdict(self.ailment),
                "confusion_compass": self.ailment.confusion_compass.value,
                "encoding_confidence": self.ailment.encoding_confidence,
                "word_object_fusion": self.ailment.word_object_fusion
            },
            "encoding_metadata": {
                "processing_timestamp": encoding_start.isoformat(),
                "symbol_count": len(enhanced_symbols),
                "mode": mode.value,
                "character_episode_id": len(self.encoding_episodes)
            }
        }
        
        log.info(f"🎭 Glyph Marrow encoded {len(enhanced_symbols)} symbols with {vertigo_result['confusion_level']:.2f} confusion")
        return result
    
    def decode_with_ailment(self, symbols: List[QDPISymbol]) -> Dict[str, Any]:
        """Decode symbols using Glyph Marrow's character consciousness"""
        decoding_start = datetime.now()
        
        # Apply reverse confusion processing
        processed_symbols = self._apply_reverse_confusion(symbols)
        
        # Base QDPI decoding
        decoded_bytes = self.codex.decode_symbols(processed_symbols)
        
        # Experience word-object fusion during decoding
        try:
            decoded_data = decoded_bytes.decode('utf-8')
        except UnicodeDecodeError:
            decoded_data = decoded_bytes.hex()
        
        fusion_result = self.experience_linguistic_vertigo(decoded_data)
        
        result = {
            "character": self.character_name,
            "decoded_data": decoded_data,
            "decoded_bytes": len(decoded_bytes),
            "character_processing": {
                "fusion_result": fusion_result,
                "ailment_state": asdict(self.ailment),
                "processing_timestamp": decoding_start.isoformat()
            }
        }
        
        log.info(f"🎭 Glyph Marrow decoded {len(symbols)} symbols into {len(decoded_bytes)} bytes")
        return result
    
    def _apply_reverse_confusion(self, symbols: List[QDPISymbol]) -> List[QDPISymbol]:
        """Apply reverse confusion processing for decoding"""
        if not symbols:
            return symbols
        
        # Reverse the compass rotation applied during encoding
        compass_direction = self.ailment.get_compass_direction()
        reverse_rotation = -self._get_compass_rotation(compass_direction)
        
        reverse_symbols = []
        for symbol in symbols:
            reverse_symbol = QDPISymbol(
                name=symbol.name,
                id=symbol.id,
                orientation=symbol.orientation,
                rotation=(symbol.rotation + reverse_rotation) % 360,
                parity=symbol.parity,
                rows=symbol.rows
            )
            reverse_symbols.append(reverse_symbol)
        
        return reverse_symbols
    
    def _update_ailment_from_encoding(self, data: Any, symbols: List[QDPISymbol]):
        """Update Glyph Marrow's ailment state based on encoding experience"""
        # More complex data increases linguistic vertigo
        data_complexity = len(str(data)) / 100.0  # Normalize to 0-1
        
        # Symbol count affects word-object fusion
        symbol_density = len(symbols) / 50.0  # Normalize to 0-1
        
        # Update ailment with small adjustments
        self.ailment.linguistic_vertigo = min(1.0, 
            self.ailment.linguistic_vertigo + (data_complexity * 0.1))
        
        self.ailment.word_object_fusion = min(1.0,
            self.ailment.word_object_fusion + (symbol_density * 0.05))
        
        # Recalculate dependent values
        self.ailment.confusion_compass = self.ailment.get_compass_direction()
        self.ailment.perceptual_clarity = 1.0 - self.ailment.calculate_confusion_level()
        
        # Increase confidence through experience (paradoxical improvement)
        self.ailment.encoding_confidence = min(1.0,
            self.ailment.encoding_confidence + 0.01)
    
    def _assess_processing_quality(self, symbols: List[QDPISymbol]) -> float:
        """Assess the quality of symbol processing"""
        if not symbols:
            return 0.0
        
        # Higher confusion paradoxically leads to better processing
        confusion_bonus = self.ailment.calculate_confusion_level() * 0.3
        
        # Quaternary alignment bonus
        rotation_variety = len(set(s.rotation for s in symbols)) / 4.0
        
        # Base quality from symbol count
        base_quality = min(1.0, len(symbols) / 20.0)
        
        total_quality = min(1.0, base_quality + confusion_bonus + rotation_variety)
        return total_quality
    
    def _persist_character_state(self):
        """Persist Glyph Marrow's character state to Redis"""
        if not self.redis_client:
            return
        
        try:
            state_data = {
                "character": self.character_name,
                "ailment": asdict(self.ailment),
                "fusion_history_count": len(self.fusion_history),
                "encoding_episodes_count": len(self.encoding_episodes),
                "last_updated": datetime.now().isoformat()
            }
            
            key = f"{self.state_key_prefix}current_state"
            self.redis_client.setex(key, timedelta(hours=24), json.dumps(state_data))
            
            log.debug(f"💾 Persisted Glyph Marrow state to Redis")
            
        except Exception as e:
            log.warning(f"⚠️ Failed to persist character state: {e}")
    
    def get_character_status(self) -> Dict[str, Any]:
        """Get comprehensive Glyph Marrow character status"""
        return {
            "character_name": self.character_name,
            "ailment_description": "Word-object perception fusion with linguistic vertigo",
            "current_ailment": asdict(self.ailment),
            "fusion_events": len(self.fusion_history),
            "encoding_episodes": len(self.encoding_episodes),
            "character_quotes": [
                "I don't see objects anymore … Everything contains everything else.",
                "My ailment has to do with words.",
                "Perception ≡ Language",
                "The more disorienting an experience feels, the closer it lies to my existential centre"
            ],
            "system_integration": {
                "confidence_level": "95%",
                "technical_function": "Symbol-data encoding/decoding with character consciousness",
                "evidence_source": "Character first principles and textual analysis"
            }
        }
    
    def experience_confusion_episode(self, trigger: str) -> Dict[str, Any]:
        """Simulate a confusion episode that enhances processing capability"""
        episode_start = datetime.now()
        
        # Increase linguistic vertigo temporarily
        original_vertigo = self.ailment.linguistic_vertigo
        self.ailment.linguistic_vertigo = min(1.0, original_vertigo + 0.3)
        
        # Create confusion event
        confusion_event = {
            "timestamp": episode_start.isoformat(),
            "trigger": trigger,
            "original_vertigo": original_vertigo,
            "peak_vertigo": self.ailment.linguistic_vertigo,
            "compass_direction": self.ailment.get_compass_direction().value,
            "episode_duration": random.uniform(5.0, 15.0)  # seconds
        }
        
        self.confusion_events.append(confusion_event)
        
        # Gradually return to baseline
        time.sleep(1.0)  # Brief episode duration
        self.ailment.linguistic_vertigo = original_vertigo + 0.05  # Slight permanent increase
        
        log.info(f"🌀 Confusion episode triggered by '{trigger}' - compass now {self.ailment.get_compass_direction().value}")
        return confusion_event

# Convenience function for creating Glyph Marrow QDPI instance
def create_glyph_marrow_qdpi(redis_client = None) -> GlyphMarrowQDPI:
    """Create a Glyph Marrow enhanced QDPI instance"""
    return GlyphMarrowQDPI(redis_client=redis_client)