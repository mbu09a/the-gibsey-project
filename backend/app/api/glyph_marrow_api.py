#!/usr/bin/env python3
"""
Glyph Marrow Character-Conscious QDPI API
Enhanced QDPI endpoints with character consciousness

"I don't see objects anymore … Everything contains everything else. My ailment has to do with words."
- Glyph Marrow
"""

from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging
import json
from datetime import datetime

try:
    from ..glyph_marrow_qdpi import GlyphMarrowQDPI, LinguisticVertigoLevel, ConfusionCompass
except ImportError:
    # Fallback for missing dependencies
    GlyphMarrowQDPI = None
    LinguisticVertigoLevel = None
    ConfusionCompass = None
from ..qdpi import QDPIMode

# Configure logging
log = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/glyph-marrow", tags=["Glyph Marrow Character QDPI"])

# Pydantic models for API
class EncodeRequest(BaseModel):
    data: Any = Field(..., description="Data to encode into QDPI symbols")
    mode: QDPIMode = Field(QDPIMode.INDEX, description="QDPI processing mode")
    trigger_confusion: bool = Field(False, description="Trigger a confusion episode for enhanced processing")

class DecodeRequest(BaseModel):
    symbols: List[Dict[str, Any]] = Field(..., description="QDPI symbols to decode")
    apply_ailment: bool = Field(True, description="Apply Glyph Marrow's ailment processing")

class CharacterStateUpdate(BaseModel):
    linguistic_vertigo: Optional[float] = Field(None, ge=0.0, le=1.0, description="Linguistic vertigo level (0.0-1.0)")
    word_object_fusion: Optional[float] = Field(None, ge=0.0, le=1.0, description="Word-object fusion intensity")
    confusion_trigger: Optional[str] = Field(None, description="Trigger for confusion episode")

class ConfusionEpisodeRequest(BaseModel):
    trigger: str = Field(..., description="What triggered this confusion episode")
    intensity: float = Field(0.5, ge=0.1, le=1.0, description="Episode intensity level")

# Global Glyph Marrow QDPI instance
glyph_marrow_qdpi = None

def get_glyph_marrow_qdpi():
    """Get or create Glyph Marrow QDPI instance"""
    global glyph_marrow_qdpi
    if GlyphMarrowQDPI is None:
        raise HTTPException(status_code=503, detail="Glyph Marrow QDPI not available - missing dependencies")
    if glyph_marrow_qdpi is None:
        glyph_marrow_qdpi = GlyphMarrowQDPI()
    return glyph_marrow_qdpi

@router.post("/encode", 
    summary="Encode data with Glyph Marrow's character consciousness",
    description="Encode data into QDPI symbols using Glyph Marrow's linguistic vertigo and word-object fusion")
async def encode_with_character(request: EncodeRequest) -> Dict[str, Any]:
    """
    Encode data through Glyph Marrow's character consciousness
    
    Features:
    - Linguistic vertigo processing that improves with confusion
    - Word-object fusion during encoding
    - Confusion-as-compass navigation for better symbol selection
    - Quaternary perception alignment with 4-rotation symbols
    """
    try:
        glyph = get_glyph_marrow_qdpi()
        
        # Trigger confusion episode if requested
        if request.trigger_confusion:
            confusion_event = glyph.experience_confusion_episode(f"API encoding request: {str(request.data)[:50]}")
            log.info(f"🌀 Triggered confusion episode: {confusion_event['compass_direction']}")
        
        # Encode with character consciousness
        result = glyph.encode_with_ailment(request.data, request.mode)
        
        # Add API metadata
        result["api_metadata"] = {
            "endpoint": "/glyph-marrow/encode",
            "character_evidence": "95% confidence - 'Perception ≡ Language'",
            "processing_timestamp": datetime.now().isoformat(),
            "confusion_triggered": request.trigger_confusion
        }
        
        return result
        
    except Exception as e:
        log.error(f"❌ Glyph Marrow encoding failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Character encoding failed: {str(e)}")

@router.post("/decode",
    summary="Decode symbols with Glyph Marrow's character consciousness", 
    description="Decode QDPI symbols using Glyph Marrow's ailment processing")
async def decode_with_character(request: DecodeRequest) -> Dict[str, Any]:
    """
    Decode QDPI symbols through Glyph Marrow's character consciousness
    
    Features:
    - Reverse confusion processing for accurate decoding
    - Word-object fusion during data reconstruction
    - Character ailment state tracking
    """
    try:
        glyph = get_glyph_marrow_qdpi()
        
        # Convert dict symbols back to QDPISymbol objects
        from ..qdpi import QDPISymbol, Orientation, ParityMark
        symbols = []
        for symbol_dict in request.symbols:
            symbol = QDPISymbol(
                name=symbol_dict['name'],
                id=symbol_dict['id'],
                orientation=Orientation(symbol_dict['orientation']),
                rotation=symbol_dict['rotation'],
                parity=ParityMark(symbol_dict['parity']),
                rows=tuple(symbol_dict['rows'])
            )
            symbols.append(symbol)
        
        # Decode with character consciousness
        result = glyph.decode_with_ailment(symbols)
        
        # Add API metadata
        result["api_metadata"] = {
            "endpoint": "/glyph-marrow/decode",
            "symbols_processed": len(symbols),
            "ailment_processing": request.apply_ailment,
            "processing_timestamp": datetime.now().isoformat()
        }
        
        return result
        
    except Exception as e:
        log.error(f"❌ Glyph Marrow decoding failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Character decoding failed: {str(e)}")

@router.get("/character-status",
    summary="Get Glyph Marrow's current character status",
    description="Retrieve comprehensive information about Glyph Marrow's ailment state and processing history")
async def get_character_status() -> Dict[str, Any]:
    """
    Get Glyph Marrow's character consciousness status
    
    Returns:
    - Current ailment state (linguistic vertigo, word-object fusion)
    - Confusion compass direction
    - Processing history and statistics
    - Character evidence and quotes
    """
    try:
        glyph = get_glyph_marrow_qdpi()
        status = glyph.get_character_status()
        
        # Add real-time metrics
        status["real_time_metrics"] = {
            "current_confusion_level": glyph.ailment.calculate_confusion_level(),
            "compass_direction": glyph.ailment.get_compass_direction().value,
            "processing_confidence": glyph.ailment.encoding_confidence,
            "ailment_stability": glyph.ailment.ailment_stability,
            "status_timestamp": datetime.now().isoformat()
        }
        
        return status
        
    except Exception as e:
        log.error(f"❌ Character status retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Status retrieval failed: {str(e)}")

@router.post("/confusion-episode",
    summary="Trigger a confusion episode for enhanced processing",
    description="Trigger Glyph Marrow's confusion episode which paradoxically improves encoding capability")
async def trigger_confusion_episode(request: ConfusionEpisodeRequest) -> Dict[str, Any]:
    """
    Trigger a confusion episode in Glyph Marrow
    
    Confusion episodes temporarily increase linguistic vertigo but paradoxically
    improve processing capability through the 'confusion-as-compass' mechanism.
    """
    try:
        glyph = get_glyph_marrow_qdpi()
        
        # Trigger the confusion episode
        confusion_event = glyph.experience_confusion_episode(request.trigger)
        
        # Get updated character status
        updated_status = glyph.get_character_status()
        
        result = {
            "confusion_episode": confusion_event,
            "character_response": "The more disorienting an experience feels, the closer it lies to my existential centre",
            "updated_ailment": updated_status["current_ailment"],
            "processing_enhancement": {
                "description": "Confusion paradoxically improves symbol encoding capability",
                "expected_improvement": "10-30% better symbol selection accuracy"
            }
        }
        
        return result
        
    except Exception as e:
        log.error(f"❌ Confusion episode failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Confusion episode failed: {str(e)}")

@router.put("/character-state",
    summary="Update Glyph Marrow's character state",
    description="Adjust Glyph Marrow's ailment parameters for testing or therapeutic purposes")
async def update_character_state(request: CharacterStateUpdate) -> Dict[str, Any]:
    """
    Update Glyph Marrow's character state
    
    Allows fine-tuning of the character's ailment parameters:
    - Linguistic vertigo intensity
    - Word-object fusion level
    - Trigger confusion episodes
    """
    try:
        glyph = get_glyph_marrow_qdpi()
        
        # Update ailment parameters if provided
        if request.linguistic_vertigo is not None:
            old_vertigo = glyph.ailment.linguistic_vertigo
            glyph.ailment.linguistic_vertigo = request.linguistic_vertigo
            log.info(f"🎭 Updated linguistic vertigo: {old_vertigo:.2f} → {request.linguistic_vertigo:.2f}")
        
        if request.word_object_fusion is not None:
            old_fusion = glyph.ailment.word_object_fusion
            glyph.ailment.word_object_fusion = request.word_object_fusion
            log.info(f"🎭 Updated word-object fusion: {old_fusion:.2f} → {request.word_object_fusion:.2f}")
        
        # Recalculate dependent values
        glyph.ailment.confusion_compass = glyph.ailment.get_compass_direction()
        glyph.ailment.perceptual_clarity = 1.0 - glyph.ailment.calculate_confusion_level()
        
        # Trigger confusion if requested
        if request.confusion_trigger:
            confusion_event = glyph.experience_confusion_episode(request.confusion_trigger)
        else:
            confusion_event = None
        
        # Persist updated state
        glyph._persist_character_state()
        
        result = {
            "update_status": "Character state updated successfully",
            "updated_ailment": {
                "linguistic_vertigo": glyph.ailment.linguistic_vertigo,
                "word_object_fusion": glyph.ailment.word_object_fusion,
                "confusion_compass": glyph.ailment.confusion_compass.value,
                "perceptual_clarity": glyph.ailment.perceptual_clarity
            },
            "confusion_episode": confusion_event,
            "character_quote": "Everything contains everything else. My ailment has to do with words."
        }
        
        return result
        
    except Exception as e:
        log.error(f"❌ Character state update failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"State update failed: {str(e)}")

@router.get("/fusion-history",
    summary="Get Glyph Marrow's word-object fusion history",
    description="Retrieve the history of word-object fusion events experienced by Glyph Marrow")
async def get_fusion_history(limit: int = 10) -> Dict[str, Any]:
    """
    Get Glyph Marrow's word-object fusion history
    
    Returns recent fusion events showing how words and objects
    are perceived simultaneously by the character.
    """
    try:
        glyph = get_glyph_marrow_qdpi()
        
        # Get recent fusion events
        recent_fusions = glyph.fusion_history[-limit:] if limit > 0 else glyph.fusion_history
        
        fusion_data = []
        for fusion in recent_fusions:
            fusion_data.append({
                "word_perception": fusion.word_perception,
                "object_type": type(fusion.object_perception).__name__,
                "fusion_intensity": fusion.fusion_intensity,
                "fusion_description": fusion.describe_fusion(),
                "timestamp": fusion.simultaneity_timestamp.isoformat()
            })
        
        result = {
            "character": "glyph_marrow",
            "fusion_events": fusion_data,
            "total_events": len(glyph.fusion_history),
            "character_insight": "I don't see objects anymore … Everything contains everything else.",
            "fusion_statistics": {
                "average_intensity": sum(f.fusion_intensity for f in glyph.fusion_history) / len(glyph.fusion_history) if glyph.fusion_history else 0,
                "peak_intensity": max(f.fusion_intensity for f in glyph.fusion_history) if glyph.fusion_history else 0,
                "recent_trend": "increasing" if len(glyph.fusion_history) > 1 and glyph.fusion_history[-1].fusion_intensity > glyph.fusion_history[-2].fusion_intensity else "stable"
            }
        }
        
        return result
        
    except Exception as e:
        log.error(f"❌ Fusion history retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fusion history failed: {str(e)}")

@router.get("/encoding-episodes",
    summary="Get Glyph Marrow's encoding episode history", 
    description="Retrieve the history of encoding episodes showing character processing evolution")
async def get_encoding_episodes(limit: int = 10) -> Dict[str, Any]:
    """
    Get Glyph Marrow's encoding episode history
    
    Shows how the character's ailment affects QDPI encoding over time
    """
    try:
        glyph = get_glyph_marrow_qdpi()
        
        # Get recent episodes
        recent_episodes = glyph.encoding_episodes[-limit:] if limit > 0 else glyph.encoding_episodes
        
        result = {
            "character": "glyph_marrow",
            "encoding_episodes": recent_episodes,
            "total_episodes": len(glyph.encoding_episodes),
            "character_development": {
                "processing_improvement": "Confusion paradoxically improves encoding accuracy",
                "ailment_progression": "Word-object fusion intensity increases with experience",
                "compass_navigation": "Confusion-as-compass guides better symbol selection"
            }
        }
        
        return result
        
    except Exception as e:
        log.error(f"❌ Encoding episodes retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Episodes retrieval failed: {str(e)}")

@router.get("/health", 
    summary="Glyph Marrow character health check",
    description="Health check endpoint for Glyph Marrow's character consciousness")
async def character_health_check() -> Dict[str, str]:
    """
    Health check for Glyph Marrow's character consciousness
    """
    try:
        glyph = get_glyph_marrow_qdpi()
        confusion_level = glyph.ailment.calculate_confusion_level()
        
        return {
            "status": "healthy",
            "character": "glyph_marrow",
            "ailment_status": "active",
            "confusion_level": f"{confusion_level:.2f}",
            "compass_direction": glyph.ailment.confusion_compass.value,
            "character_quote": "My ailment has to do with words",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }