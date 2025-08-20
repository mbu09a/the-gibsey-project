"""QDPI Manifest API endpoints"""

import os
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import List

from ..qdpi_manifest import load_manifest, get_character_metadata, create_stub_manifest, Manifest, Character

router = APIRouter(prefix="/api/v1/qdpi", tags=["qdpi-manifest"])

@router.get("/manifest", response_model=Manifest)
async def get_manifest() -> JSONResponse:
    """
    Get the complete QDPI glyph manifest with all 256 symbols.
    
    Returns validated manifest with ETag for caching.
    """
    manifest_path = os.getenv("QDPI_GLYPH_MANIFEST_PATH", "public/qdpi_glyph_manifest.json")
    
    try:
        manifest = load_manifest(manifest_path)
        
        # Generate ETag for client caching
        etag = f'W/"{manifest.count}-{manifest.version}-{hash(manifest.timestamp) & 0xFFFFFF:06x}"'
        
        return JSONResponse(
            content=manifest.dict(),
            headers={
                "ETag": etag,
                "Cache-Control": "public, max-age=300"  # 5 minutes
            }
        )
        
    except FileNotFoundError:
        # Try to create a stub manifest for development
        try:
            manifest = create_stub_manifest(manifest_path)
            return JSONResponse(
                content=manifest.dict(),
                headers={
                    "ETag": f'W/stub-{manifest.count}',
                    "Cache-Control": "no-cache",
                    "X-Manifest-Type": "stub"
                }
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Could not load or create manifest: {str(e)}"
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Manifest validation failed: {str(e)}"
        )

@router.get("/characters", response_model=List[Character])
async def get_characters() -> List[Character]:
    """
    Get metadata for all 16 characters including colors for UI.
    
    Returns character info with hex codes, names, and assigned colors.
    """
    try:
        return get_character_metadata()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load character metadata: {str(e)}"
        )

@router.get("/manifest/validate")
async def validate_manifest():
    """
    Validate the current manifest and return health info.
    
    Useful for debugging and health checks.
    """
    manifest_path = os.getenv("QDPI_GLYPH_MANIFEST_PATH", "public/qdpi_glyph_manifest.json")
    
    try:
        manifest = load_manifest(manifest_path)
        
        # Additional validation stats
        char_counts = {}
        behavior_counts = {}
        
        for glyph in manifest.glyphs:
            char_counts[glyph.char_hex] = char_counts.get(glyph.char_hex, 0) + 1
            behavior_counts[glyph.behavior] = behavior_counts.get(glyph.behavior, 0) + 1
        
        return {
            "status": "valid",
            "manifest_path": manifest_path,
            "version": manifest.version,
            "glyph_count": len(manifest.glyphs),
            "character_distribution": char_counts,
            "behavior_distribution": behavior_counts,
            "expected_per_character": 16,
            "expected_per_behavior": 16,
            "validation_passed": all(count == 16 for count in char_counts.values()),
            "timestamp": manifest.timestamp
        }
        
    except FileNotFoundError:
        return {
            "status": "missing",
            "manifest_path": manifest_path,
            "error": "Manifest file not found"
        }
    except Exception as e:
        return {
            "status": "invalid", 
            "manifest_path": manifest_path,
            "error": str(e)
        }