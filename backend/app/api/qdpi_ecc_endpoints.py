#!/usr/bin/env python3
"""
QDPI Error Correction API Endpoints
Production-ready FastAPI endpoints for QDPI error correction system

Provides REST API access to the complete two-tier error correction system
for bulletproof narrative preservation in production environments.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Tuple
import time
import json
import logging

# Import our ECC integration
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.qdpi_ecc_integration import QDPIECCBackend, ProtectedQDPIMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

router = APIRouter(prefix="/qdpi/ecc", tags=["QDPI Error Correction"])

# Global backend instance (in production, this would be dependency-injected)
ecc_backend = QDPIECCBackend()

# Pydantic models for API
class SymbolSequenceItem(BaseModel):
    """Single symbol in a QDPI sequence"""
    symbol_name: str = Field(..., description="Symbol name from QDPI Canon")
    rotation: int = Field(..., ge=0, le=270, description="Rotation in degrees (0, 90, 180, 270)")

class NarrativeEncodeRequest(BaseModel):
    """Request to encode a narrative with error protection"""
    description: str = Field(..., description="Human-readable narrative description")
    symbol_sequence: List[SymbolSequenceItem] = Field(..., description="Sequence of QDPI symbols")
    protection_level: Optional[str] = Field("standard", description="Protection level (standard, enhanced)")

class NarrativeDecodeRequest(BaseModel):
    """Request to decode and error-correct a protected narrative"""
    protected_data: str = Field(..., description="Base64-encoded protected data")
    original_length: int = Field(..., description="Original sequence length")
    block_id: Optional[int] = Field(None, description="Block identifier for tracking")

class TransmissionTestRequest(BaseModel):
    """Request to test transmission error simulation"""
    block_id: int = Field(..., description="Block ID to test")
    error_rate: float = Field(0.01, ge=0.0, le=0.1, description="Bit error rate (0.0-0.1)")

class ProtectedNarrativeResponse(BaseModel):
    """Response containing a protected narrative"""
    block_id: int
    original_symbols: List[Dict[str, Any]]
    narrative_meaning: str
    symbol_sequence: str
    protection_metadata: Dict[str, Any]
    encoding_time_ms: float
    protected_data_base64: str

class DecodedNarrativeResponse(BaseModel):
    """Response containing a decoded narrative"""
    recovered_symbols: List[Dict[str, Any]]
    narrative_meaning: str
    decode_statistics: Dict[str, Any]
    recovery_successful: bool
    performance_target_met: bool

class TransmissionTestResponse(BaseModel):
    """Response containing transmission test results"""
    test_successful: bool
    narrative_preserved: bool
    original_narrative: str
    recovered_narrative: str
    error_correction_stats: Dict[str, Any]
    performance_metrics: Dict[str, Any]

@router.post("/encode", response_model=ProtectedNarrativeResponse)
async def encode_narrative_with_protection(
    request: NarrativeEncodeRequest,
    background_tasks: BackgroundTasks
) -> ProtectedNarrativeResponse:
    """
    Encode a QDPI narrative sequence with complete error correction protection.
    
    This endpoint:
    1. Validates the symbol sequence against QDPI Canon
    2. Applies two-tier error correction (Reed-Solomon + mini-syndrome)
    3. Returns protected data with metadata for transmission/storage
    """
    try:
        # Convert Pydantic models to tuples
        symbol_sequence = [(item.symbol_name, item.rotation) for item in request.symbol_sequence]
        
        # Encode with protection
        protected_msg = ecc_backend.encode_narrative_with_protection(
            request.description, 
            symbol_sequence
        )
        
        # Generate response
        symbol_sequence_str = []
        for sym_data in protected_msg.original_symbols:
            symbol_sequence_str.append(f"{sym_data['symbol']['name']}@{sym_data['symbol']['rotation']}°")
        
        narrative_meaning = " → ".join([sym['canon_meaning'] for sym in protected_msg.original_symbols])
        
        # Encode protected data as base64 for JSON transport
        import base64
        protected_data_b64 = base64.b64encode(protected_msg.protected_data).decode('utf-8')
        
        # Log the encoding for monitoring
        background_tasks.add_task(
            log_narrative_encoding,
            protected_msg.block_id,
            len(symbol_sequence),
            protected_msg.protection_metadata['encoding_time_ms']
        )
        
        return ProtectedNarrativeResponse(
            block_id=protected_msg.block_id,
            original_symbols=protected_msg.original_symbols,
            narrative_meaning=narrative_meaning,
            symbol_sequence=" → ".join(symbol_sequence_str),
            protection_metadata=protected_msg.protection_metadata,
            encoding_time_ms=protected_msg.protection_metadata['encoding_time_ms'],
            protected_data_base64=protected_data_b64
        )
        
    except Exception as e:
        log.error(f"Error encoding narrative: {e}")
        raise HTTPException(status_code=400, detail=f"Encoding failed: {str(e)}")

@router.post("/decode", response_model=DecodedNarrativeResponse)
async def decode_protected_narrative(
    request: NarrativeDecodeRequest,
    background_tasks: BackgroundTasks
) -> DecodedNarrativeResponse:
    """
    Decode and error-correct a protected QDPI narrative sequence.
    
    This endpoint:
    1. Decodes base64 protected data
    2. Applies complete error correction (Reed-Solomon + mini-syndrome)
    3. Returns recovered narrative with correction statistics
    """
    try:
        # Decode base64 data
        import base64
        protected_data = base64.b64decode(request.protected_data.encode('utf-8'))
        
        # Decode with error correction
        recovered_symbols, decode_stats = ecc_backend.decode_protected_narrative(
            protected_data,
            request.original_length,
            request.block_id
        )
        
        # Generate narrative meaning
        narrative_meaning = " → ".join([sym['canon_meaning'] for sym in recovered_symbols])
        
        # Log the decoding for monitoring
        background_tasks.add_task(
            log_narrative_decoding,
            request.block_id or 0,
            decode_stats['decode_time_ms'],
            decode_stats['recovery_successful']
        )
        
        return DecodedNarrativeResponse(
            recovered_symbols=recovered_symbols,
            narrative_meaning=narrative_meaning,
            decode_statistics=decode_stats,
            recovery_successful=decode_stats['recovery_successful'],
            performance_target_met=decode_stats['meets_performance_target']
        )
        
    except Exception as e:
        log.error(f"Error decoding narrative: {e}")
        raise HTTPException(status_code=400, detail=f"Decoding failed: {str(e)}")

@router.post("/test-transmission", response_model=TransmissionTestResponse)
async def test_transmission_errors(
    request: TransmissionTestRequest
) -> TransmissionTestResponse:
    """
    Test transmission error recovery for a protected narrative.
    
    This endpoint:
    1. Retrieves a protected message by block_id
    2. Simulates transmission errors at specified rate
    3. Tests recovery and reports narrative preservation
    """
    try:
        # Get protected message
        if request.block_id not in ecc_backend.protected_messages:
            raise HTTPException(status_code=404, detail=f"Block {request.block_id} not found")
        
        protected_msg = ecc_backend.protected_messages[request.block_id]
        
        # Simulate transmission and recovery
        result = ecc_backend.simulate_transmission_and_recovery(
            protected_msg, 
            request.error_rate
        )
        
        return TransmissionTestResponse(
            test_successful=True,
            narrative_preserved=result['protection_effectiveness'],
            original_narrative=result['transmission_simulation']['original_narrative'],
            recovered_narrative=result['transmission_simulation']['recovered_narrative'],
            error_correction_stats=result['decode_performance']['error_correction'],
            performance_metrics={
                'decode_time_ms': result['decode_performance']['decode_time_ms'],
                'meets_4ms_target': result['decode_performance']['meets_performance_target'],
                'error_rate_tested': request.error_rate
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error in transmission test: {e}")
        raise HTTPException(status_code=500, detail=f"Transmission test failed: {str(e)}")

@router.get("/performance")
async def get_performance_summary() -> Dict[str, Any]:
    """
    Get comprehensive performance summary of the error correction system.
    """
    try:
        perf_summary = ecc_backend.ecc_system.get_performance_summary()
        
        return {
            "system_status": "operational",
            "performance_summary": perf_summary,
            "total_messages_processed": ecc_backend.message_counter,
            "meets_specifications": {
                "decode_time_target": perf_summary['combined_performance']['meets_4ms_target'],
                "error_correction_capacity": "16 byte errors per 255-byte block",
                "protection_overhead": "~38% as specified"
            }
        }
        
    except Exception as e:
        log.error(f"Error getting performance summary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get performance summary: {str(e)}")

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint for error correction system.
    """
    try:
        # Test basic encoding/decoding
        test_sequence = [("glyph_marrow", 0), ("VALIDATE", 270)]
        test_protected = ecc_backend.encode_narrative_with_protection(
            "Health check test", 
            test_sequence
        )
        
        # Test decoding
        recovered, _ = ecc_backend.decode_protected_narrative(
            test_protected.protected_data,
            len(test_sequence)
        )
        
        if len(recovered) == len(test_sequence):
            return {"status": "healthy", "error_correction": "operational"}
        else:
            return {"status": "degraded", "error_correction": "partial"}
            
    except Exception as e:
        log.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}

@router.get("/canon/validate/{symbol_name}")
async def validate_symbol_against_canon(symbol_name: str) -> Dict[str, Any]:
    """
    Validate a symbol name against the QDPI Canon.
    """
    try:
        symbol_id = ecc_backend._get_symbol_id_from_canon(symbol_name)
        
        if symbol_id == 0 and symbol_name != "an_author":
            return {
                "valid": False,
                "symbol_name": symbol_name,
                "error": "Symbol not found in QDPI Canon"
            }
        
        # Get symbol type and meaning
        if symbol_id <= 15:
            symbol_type = "character"
        elif 16 <= symbol_id <= 47:
            symbol_type = "hidden_symbol" 
        else:
            symbol_type = "meta_verb"
            
        return {
            "valid": True,
            "symbol_name": symbol_name,
            "symbol_id": symbol_id,
            "symbol_type": symbol_type,
            "available_rotations": [0, 90, 180, 270],
            "canonical_meanings": {
                0: ecc_backend._get_canon_meaning(symbol_name, 0),
                90: ecc_backend._get_canon_meaning(symbol_name, 90),
                180: ecc_backend._get_canon_meaning(symbol_name, 180),
                270: ecc_backend._get_canon_meaning(symbol_name, 270)
            }
        }
        
    except Exception as e:
        log.error(f"Error validating symbol {symbol_name}: {e}")
        raise HTTPException(status_code=400, detail=f"Validation failed: {str(e)}")

# Background task functions
async def log_narrative_encoding(block_id: int, sequence_length: int, encoding_time_ms: float):
    """Log narrative encoding for monitoring"""
    log.info(f"Encoded narrative block {block_id}: {sequence_length} symbols in {encoding_time_ms:.2f}ms")

async def log_narrative_decoding(block_id: int, decode_time_ms: float, success: bool):
    """Log narrative decoding for monitoring"""
    status = "SUCCESS" if success else "FAILED"
    log.info(f"Decoded narrative block {block_id}: {decode_time_ms:.2f}ms - {status}")