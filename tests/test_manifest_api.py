"""Tests for QDPI manifest API endpoints"""

import pytest
import json
from fastapi.testclient import TestClient
import tempfile
import os
from pathlib import Path

# Add backend to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.api.qdpi_manifest import router
from app.qdpi_manifest import create_stub_manifest, load_manifest
from fastapi import FastAPI

# Create test app
app = FastAPI()
app.include_router(router)
client = TestClient(app)

class TestManifestAPI:
    """Test manifest API endpoints"""
    
    def test_manifest_endpoint_with_stub(self):
        """Test manifest endpoint returns valid stub data"""
        # Create a temporary manifest file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            manifest = create_stub_manifest(f.name)
            
        # Set environment variable to point to temp file
        os.environ["QDPI_GLYPH_MANIFEST_PATH"] = f.name
        
        try:
            response = client.get("/api/v1/qdpi/manifest")
            assert response.status_code == 200
            
            data = response.json()
            assert data["version"] == "v1.0"
            assert data["count"] == 256
            assert len(data["glyphs"]) == 256
            
            # Check ETag header
            assert "ETag" in response.headers
            assert response.headers["Cache-Control"] == "public, max-age=300"
            
            # Verify first glyph structure
            first_glyph = data["glyphs"][0]
            assert first_glyph["glyph_id"] == 0
            assert first_glyph["hex"] == "0x00"
            assert first_glyph["char_hex"] == 0
            assert first_glyph["behavior"] == 0
            assert first_glyph["behavior_name"] == "XC"
            
        finally:
            # Clean up
            os.unlink(f.name)
            if "QDPI_GLYPH_MANIFEST_PATH" in os.environ:
                del os.environ["QDPI_GLYPH_MANIFEST_PATH"]
    
    def test_manifest_missing_file(self):
        """Test manifest endpoint when file is missing"""
        # Set to non-existent file
        os.environ["QDPI_GLYPH_MANIFEST_PATH"] = "nonexistent.json"
        
        try:
            response = client.get("/api/v1/qdpi/manifest")
            # Should auto-create stub manifest
            assert response.status_code == 200
            assert "X-Manifest-Type" in response.headers
            assert response.headers["X-Manifest-Type"] == "stub"
            
        finally:
            # Clean up auto-created file
            if os.path.exists("nonexistent.json"):
                os.unlink("nonexistent.json")
            del os.environ["QDPI_GLYPH_MANIFEST_PATH"]
    
    def test_characters_endpoint(self):
        """Test characters metadata endpoint"""
        response = client.get("/api/v1/qdpi/characters")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 16
        
        # Check first character
        first_char = data[0]
        assert first_char["char_hex"] == 0
        assert first_char["name"] == "an author"
        assert first_char["glyph_count"] == 16
        assert first_char["color"].startswith("#")
        assert len(first_char["color"]) == 7  # #RRGGBB format
    
    def test_validate_manifest_endpoint(self):
        """Test manifest validation endpoint"""
        # Create a temporary manifest file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            create_stub_manifest(f.name)
            
        os.environ["QDPI_GLYPH_MANIFEST_PATH"] = f.name
        
        try:
            response = client.get("/api/v1/qdpi/manifest/validate")
            assert response.status_code == 200
            
            data = response.json()
            assert data["status"] == "valid"
            assert data["glyph_count"] == 256
            assert data["validation_passed"] == True
            assert "character_distribution" in data
            assert "behavior_distribution" in data
            
        finally:
            os.unlink(f.name)
            del os.environ["QDPI_GLYPH_MANIFEST_PATH"]

class TestManifestValidation:
    """Test manifest validation logic"""
    
    def test_stub_manifest_creation(self):
        """Test creating and validating stub manifest"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            manifest = create_stub_manifest(f.name)
            
        try:
            # Manifest should be valid
            assert manifest.count == 256
            assert len(manifest.glyphs) == 256
            assert manifest.version == "v1.0"
            
            # All glyph IDs should be unique and cover 0-255
            glyph_ids = [g.glyph_id for g in manifest.glyphs]
            assert set(glyph_ids) == set(range(256))
            
            # Each character should have exactly 16 behaviors
            char_counts = {}
            for glyph in manifest.glyphs:
                char_counts[glyph.char_hex] = char_counts.get(glyph.char_hex, 0) + 1
            
            for char_hex in range(16):
                assert char_counts[char_hex] == 16
                
        finally:
            os.unlink(f.name)
    
    def test_manifest_loader_validation(self):
        """Test that manifest loader validates correctly"""
        # Test valid manifest loads
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            create_stub_manifest(f.name)
            
        try:
            loaded = load_manifest(f.name)
            assert loaded.count == 256
            assert len(loaded.glyphs) == 256
            
        finally:
            os.unlink(f.name)
        
        # Test invalid manifest fails
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            invalid_data = {
                "version": "v1.0",
                "count": 1,  # Wrong count
                "timestamp": "2025-01-01T00:00:00Z",
                "glyphs": [
                    {
                        "glyph_id": 0,
                        "hex": "0x00",
                        "char_hex": 0,
                        "char_name": "test",
                        "behavior": 0,
                        "behavior_name": "XC",
                        "rotation": 0,
                        "filename": "test.svg",
                        "url": "/test.svg"
                    }
                ]
            }
            json.dump(invalid_data, f)
            
        try:
            with pytest.raises(Exception):  # Will be ValidationError from Pydantic
                load_manifest(f.name)
                
        finally:
            os.unlink(f.name)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])