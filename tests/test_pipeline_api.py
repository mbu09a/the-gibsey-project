"""Test the FastAPI pipeline endpoints"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.api.pipeline import router
from fastapi import FastAPI

# Create test app
app = FastAPI()
app.include_router(router)

client = TestClient(app)

class TestPipelineAPI:
    """Test pipeline API endpoints"""
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/api/v1/pipeline/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "pipeline" in data
        assert "version" in data
    
    def test_list_symbols(self):
        """Test symbols listing endpoint"""
        response = client.get("/api/v1/pipeline/symbols")
        assert response.status_code == 200
        
        data = response.json()
        assert "symbols" in data
        assert "total" in data
        assert data["total"] == 256
        
        # Check first symbol
        first_symbol = data["symbols"][0]
        assert first_symbol["code"] == 0
        assert first_symbol["hex"] == "0x00"
        assert first_symbol["character"] == "an author"
        assert first_symbol["orientation"] == "X"
        assert first_symbol["provenance"] == "C"
    
    def test_run_symbol_hex(self):
        """Test running symbol with hex code"""
        response = client.post(
            "/api/v1/pipeline/run/symbol/0x00",
            json={"user_intent": "continue"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "symbol" in data
        assert "page_text" in data
        assert "edges" in data
        assert "validation" in data
        assert "trajectory" in data
        
        # Check symbol info
        assert data["symbol"]["code"] == 0
        assert data["symbol"]["character"] == "an author"
    
    def test_run_symbol_decimal(self):
        """Test running symbol with decimal code"""
        response = client.post(
            "/api/v1/pipeline/run/symbol/76",  # 0x4C
            json={"user_intent": "observe"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["symbol"]["code"] == 76
        assert data["symbol"]["character"] == "jacklyn-variance"
    
    def test_run_symbol_no_body(self):
        """Test running symbol without request body"""
        response = client.post("/api/v1/pipeline/run/symbol/0")
        assert response.status_code == 200
        
        data = response.json()
        assert "page_text" in data
    
    def test_run_symbol_invalid_code(self):
        """Test running symbol with invalid code"""
        # Test negative code
        response = client.post(
            "/api/v1/pipeline/run/symbol/-1",
            json={}
        )
        assert response.status_code == 400
        
        # Test too large code
        response = client.post(
            "/api/v1/pipeline/run/symbol/256",
            json={}
        )
        assert response.status_code == 400
        
        # Test invalid hex
        response = client.post(
            "/api/v1/pipeline/run/symbol/0xGG",
            json={}
        )
        assert response.status_code == 400
    
    def test_create_branch(self):
        """Test branch creation endpoint"""
        response = client.post(
            "/api/v1/pipeline/branch/canon-01-001",
            json="T1"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["source_page"] == "canon-01-001"
        assert data["trajectory"] == "T1"
        assert "branch_id" in data
    
    def test_run_symbol_with_context(self):
        """Test running symbol with current page context"""
        response = client.post(
            "/api/v1/pipeline/run/symbol/0x10",
            json={
                "user_intent": "continue reading",
                "current_page_id": "canon-02-009"
            }
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["symbol"]["character"] == "london-fox"
        assert "page_text" in data

def test_response_schema():
    """Test that response matches expected schema"""
    response = client.post(
        "/api/v1/pipeline/run/symbol/0x00",
        json={"user_intent": "test"}
    )
    
    data = response.json()
    
    # Required fields
    required_fields = [
        "symbol", "page_text", "edges", 
        "validation", "trajectory", "index_signals"
    ]
    
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    # Symbol structure
    symbol = data["symbol"]
    symbol_fields = [
        "code", "character", "orientation", 
        "provenance", "notation"
    ]
    
    for field in symbol_fields:
        assert field in symbol, f"Missing symbol field: {field}"
    
    # Edges structure
    edges = data["edges"]
    assert isinstance(edges, dict)
    
    # Index signals structure
    signals = data["index_signals"]
    assert isinstance(signals, dict)
    assert "entities" in signals
    assert "motifs" in signals
    assert "novelty" in signals
    assert "coherence" in signals

if __name__ == "__main__":
    pytest.main([__file__, "-v"])