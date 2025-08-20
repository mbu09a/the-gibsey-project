"""Tests for pipeline symbol execution with event emission"""

import pytest
import asyncio
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.api.pipeline import router
from app.events import BUS, make_event
from fastapi import FastAPI

# Create test app
app = FastAPI()
app.include_router(router)
client = TestClient(app)

class TestRunSymbolWithEvents:
    """Test pipeline execution with event emission"""
    
    def test_run_symbol_basic(self):
        """Test basic symbol execution returns expected response"""
        response = client.post(
            "/api/v1/pipeline/run/symbol/0x00",
            json={"session_id": "test-session", "user_intent": "test"}
        )
        
        assert response.status_code == 200
        
        data = response.json()
        
        # Check response structure
        required_fields = [
            "page_id", "session_id", "symbol", "page_text", 
            "edges", "validation", "trajectory", "index_signals"
        ]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
        
        # Verify session_id is preserved
        assert data["session_id"] == "test-session"
        
        # Verify page_id format
        assert data["page_id"].startswith("P00-00-")
        
        # Verify symbol info
        symbol = data["symbol"]
        assert symbol["code"] == 0
        assert symbol["character"] == "an author"
        assert symbol["orientation"] == "X"
        assert symbol["provenance"] == "C"
    
    def test_run_symbol_auto_session_id(self):
        """Test that session_id is auto-generated if not provided"""
        response = client.post(
            "/api/v1/pipeline/run/symbol/0x10",
            json={"user_intent": "test without session"}
        )
        
        assert response.status_code == 200
        
        data = response.json()
        assert "session_id" in data
        assert data["session_id"].startswith("session-")
        assert len(data["session_id"]) > 10  # Should be generated UUID-based
    
    def test_run_symbol_different_codes(self):
        """Test symbol execution with different codes"""
        test_codes = ["0x00", "0x10", "0x4C", "255"]
        
        for code in test_codes:
            response = client.post(
                f"/api/v1/pipeline/run/symbol/{code}",
                json={"session_id": f"test-{code}", "user_intent": "test"}
            )
            
            assert response.status_code == 200
            
            data = response.json()
            expected_code = int(code, 0)
            assert data["symbol"]["code"] == expected_code
    
    def test_run_symbol_invalid_codes(self):
        """Test symbol execution with invalid codes"""
        invalid_codes = ["-1", "256", "abc", "0xGG"]
        
        for code in invalid_codes:
            response = client.post(
                f"/api/v1/pipeline/run/symbol/{code}",
                json={"session_id": "test-invalid"}
            )
            
            assert response.status_code == 400
            assert "Invalid symbol code" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_run_symbol_emits_event(self):
        """Test that symbol execution emits page generation event"""
        # Subscribe to events
        event_queue = BUS.subscribe("test-event-session")
        
        try:
            # Execute symbol in background to avoid blocking
            import asyncio
            from httpx import AsyncClient
            
            app_for_async = FastAPI()
            app_for_async.include_router(router)
            
            async def run_symbol():
                async with AsyncClient(app=app_for_async, base_url="http://test") as client:
                    return await client.post(
                        "/api/v1/pipeline/run/symbol/0x2A",
                        json={"session_id": "test-event-session", "user_intent": "event test"}
                    )
            
            # Run symbol execution
            response = await run_symbol()
            assert response.status_code == 200
            
            # Should receive a page generation event
            event = await asyncio.wait_for(event_queue.get(), timeout=2.0)
            
            assert event.type == "gibsey.generate.page.done"
            assert event.session_id == "test-event-session"
            
            payload = event.payload
            assert "page_id" in payload
            assert "symbol_code" in payload
            assert payload["symbol_code"] == 0x2A  # glyph-marrow
            assert "char_hex" in payload
            assert payload["char_hex"] == 2
            assert "behavior" in payload
            assert payload["behavior"] == 10  # AU
            assert "trajectory" in payload
            assert "character" in payload
            assert payload["character"] == "glyph-marrow"
            
        finally:
            # Clean up subscription
            BUS.unsubscribe(event_queue, "test-event-session")
    
    @pytest.mark.asyncio
    async def test_run_symbol_error_emits_error_event(self):
        """Test that pipeline errors emit error events"""
        # Subscribe to events  
        event_queue = BUS.subscribe("test-error-session")
        
        try:
            # Try to execute invalid symbol
            response = client.post(
                "/api/v1/pipeline/run/symbol/999",  # Invalid code
                json={"session_id": "test-error-session"}
            )
            
            assert response.status_code == 400
            
            # Should receive an error event
            event = await asyncio.wait_for(event_queue.get(), timeout=2.0)
            
            assert event.type == "gibsey.pipeline.error"
            assert event.session_id == "test-error-session"
            
            payload = event.payload
            assert "error" in payload
            assert "Invalid symbol code" in payload["error"]
            
        finally:
            BUS.unsubscribe(event_queue, "test-error-session")
    
    def test_run_symbol_response_structure(self):
        """Test detailed response structure validation"""
        response = client.post(
            "/api/v1/pipeline/run/symbol/0x4C",  # jacklyn-variance:ZC
            json={
                "session_id": "structure-test",
                "user_intent": "detailed test",
                "current_page_id": "canon-05-236"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate symbol structure
        symbol = data["symbol"]
        expected_symbol_fields = ["code", "character", "char_hex", "behavior", "orientation", "provenance", "notation"]
        for field in expected_symbol_fields:
            assert field in symbol
        
        # Validate edges structure
        edges = data["edges"]
        assert isinstance(edges, dict)
        
        # Validate validation structure
        validation = data["validation"]
        assert isinstance(validation, dict)
        
        # Validate index_signals structure
        index_signals = data["index_signals"]
        assert isinstance(index_signals, dict)
        expected_signals = ["entities", "motifs", "novelty", "coherence"]
        for signal in expected_signals:
            assert signal in index_signals

class TestPipelineHealthAndStats:
    """Test pipeline health and utility endpoints"""
    
    def test_pipeline_health(self):
        """Test pipeline health endpoint"""
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
        
        # Check symbol structure
        symbols = data["symbols"]
        assert len(symbols) == 256
        
        first_symbol = symbols[0]
        expected_fields = ["code", "hex", "character", "char_hex", "behavior", "orientation", "provenance", "notation"]
        for field in expected_fields:
            assert field in first_symbol
    
    def test_create_branch_stub(self):
        """Test branch creation endpoint (stub implementation)"""
        response = client.post(
            "/api/v1/pipeline/branch/canon-01-001",
            json="T1"
        )
        
        assert response.status_code == 200
        
        data = response.json()
        assert data["source_page"] == "canon-01-001"
        assert data["trajectory"] == "T1"
        assert "branch_id" in data
        assert data["status"] == "created"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])