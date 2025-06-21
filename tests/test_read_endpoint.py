#!/usr/bin/env python3
"""
Unit tests for the /read/{page_id} endpoint.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient

# Mock Cassandra and other dependencies before importing the app
sys.modules['cassandra.cluster'] = Mock()
sys.modules['cassandra.auth'] = Mock()
sys.modules['cassandra.policies'] = Mock()
sys.modules['openai'] = Mock()
sys.modules['sentence_transformers'] = Mock()

class MockCassandraRow:
    """Mock Cassandra row object."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class TestReadEndpoint(unittest.TestCase):
    """Test the /read/{page_id} endpoint."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Import after mocking dependencies
        from backend.app.retrieval_api import app
        self.client = TestClient(app)
        
        # Mock cassandra session
        self.mock_session = Mock()
        
        # Patch the global session in the app
        with patch('backend.app.retrieval_api.cassandra_session', self.mock_session):
            pass
    
    @patch('backend.app.retrieval_api.cassandra_session')
    def test_read_existing_page(self, mock_session):
        """Test reading an existing page."""
        # Mock successful database response
        mock_row = MockCassandraRow(
            page_id="001-test-page",
            title="Test Page",
            content="This is a test page content.",
            symbol_id="london-fox",
            tokens=42,
            page_index=1
        )
        
        mock_result = Mock()
        mock_result.one.return_value = mock_row
        mock_session.execute.return_value = mock_result
        
        # Make request
        response = self.client.post("/read/001-test-page")
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data["page_id"], "001-test-page")
        self.assertEqual(data["title"], "Test Page")
        self.assertEqual(data["content"], "This is a test page content.")
        self.assertEqual(data["symbol_id"], "london-fox")
        self.assertEqual(data["tokens"], 42)
        self.assertEqual(data["page_index"], 1)
    
    @patch('backend.app.retrieval_api.cassandra_session')
    def test_read_nonexistent_page(self, mock_session):
        """Test reading a page that doesn't exist."""
        # Mock database returning no results
        mock_result = Mock()
        mock_result.one.return_value = None
        mock_session.execute.return_value = mock_result
        
        # Make request
        response = self.client.post("/read/nonexistent-page")
        
        # Assert 404 response
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("not found", data["detail"])
    
    @patch('backend.app.retrieval_api.cassandra_session', None)
    def test_read_page_no_database(self):
        """Test reading when database is not available."""
        response = self.client.post("/read/test-page")
        
        # Assert 503 service unavailable
        self.assertEqual(response.status_code, 503)
        data = response.json()
        self.assertIn("Database not available", data["detail"])
    
    @patch('backend.app.retrieval_api.cassandra_session')
    def test_read_page_database_error(self, mock_session):
        """Test handling database errors."""
        # Mock database raising an exception
        mock_session.execute.side_effect = Exception("Database connection error")
        
        # Make request
        response = self.client.post("/read/test-page")
        
        # Assert 500 internal server error
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to retrieve page", data["detail"])
    
    def test_health_check(self):
        """Test the health check endpoint."""
        with patch('backend.app.retrieval_api.cassandra_session', Mock()):
            with patch('backend.app.retrieval_api.embedding_model', Mock()):
                with patch('backend.app.retrieval_api.tokenizer_service', Mock()):
                    response = self.client.get("/health")
                    
                    self.assertEqual(response.status_code, 200)
                    data = response.json()
                    
                    self.assertEqual(data["status"], "healthy")
                    self.assertIn("services", data)
                    self.assertTrue(data["services"]["cassandra"])

if __name__ == "__main__":
    unittest.main()