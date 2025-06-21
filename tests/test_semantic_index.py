#!/usr/bin/env python3
"""
Integration tests for the /index semantic search endpoint.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient

# Mock dependencies before importing the app
sys.modules['cassandra.cluster'] = Mock()
sys.modules['cassandra.auth'] = Mock()
sys.modules['cassandra.policies'] = Mock()
sys.modules['openai'] = Mock()
sys.modules['sentence_transformers'] = Mock()

class MockSearchRow:
    """Mock Cassandra search result row."""
    def __init__(self, page_id, title, content, symbol_id, page_index, score):
        self.page_id = page_id
        self.title = title
        self.content = content
        self.symbol_id = symbol_id
        self.page_index = page_index
        self.score = score

class TestSemanticIndex(unittest.TestCase):
    """Test the /index semantic search endpoint."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Import after mocking dependencies
        from backend.app.retrieval_api import app
        self.client = TestClient(app)
    
    @patch('backend.app.retrieval_api.cassandra_session')
    @patch('backend.app.retrieval_api.get_embedding')
    @patch('backend.app.retrieval_api.tokenizer_service')
    @patch('backend.app.retrieval_api.truncate_to_tokens')
    def test_semantic_search_basic(self, mock_truncate, mock_tokenizer, mock_embedding, mock_session):
        """Test basic semantic search functionality."""
        # Mock tokenizer service
        mock_tokenizer.count_tokens.return_value = 5
        
        # Mock text truncation
        mock_truncate.side_effect = lambda text, max_tokens: text[:100] + "..." if len(text) > 100 else text
        
        # Mock embedding generation
        mock_embedding.return_value = [0.1] * 768  # Mock 768-dim embedding
        
        # Mock search results
        mock_rows = [
            MockSearchRow(
                page_id="001-test-page",
                title="Test Page",
                content="This is a test page about london-fox character.",
                symbol_id="london-fox",
                page_index=1,
                score=0.95
            ),
            MockSearchRow(
                page_id="002-another-page",
                title="Another Page",
                content="This page mentions jacklyn-variance in the story.",
                symbol_id="jacklyn-variance",
                page_index=2,
                score=0.87
            )
        ]
        
        mock_session.execute.return_value = mock_rows
        
        # Make search request
        response = self.client.post("/index", json={
            "q": "tell me about london-fox",
            "top_k": 5
        })
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data["query"], "tell me about london-fox")
        self.assertEqual(data["total_results"], 2)
        self.assertGreater(data["processing_time_ms"], 0)
        
        # Check results
        results = data["results"]
        self.assertEqual(len(results), 2)
        
        # First result should have higher score
        self.assertEqual(results[0]["page_id"], "001-test-page")
        self.assertEqual(results[0]["score"], 0.95)
        self.assertIn("london-fox", results[0]["preview"])
        
        # Second result
        self.assertEqual(results[1]["page_id"], "002-another-page")
        self.assertEqual(results[1]["score"], 0.87)
    
    @patch('backend.app.retrieval_api.cassandra_session')
    @patch('backend.app.retrieval_api.get_embedding')
    @patch('backend.app.retrieval_api.tokenizer_service')
    @patch('backend.app.retrieval_api.truncate_to_tokens')
    def test_semantic_search_with_character_filter(self, mock_truncate, mock_tokenizer, mock_embedding, mock_session):
        """Test semantic search with character symbol filter."""
        # Mock tokenizer service
        mock_tokenizer.count_tokens.return_value = 5
        
        # Mock text truncation
        mock_truncate.side_effect = lambda text, max_tokens: text[:100] + "..." if len(text) > 100 else text
        
        # Mock embedding generation
        mock_embedding.return_value = [0.1] * 768
        
        # Mock filtered search results
        mock_rows = [
            MockSearchRow(
                page_id="003-jacklyn-page",
                title="Jacklyn's Analysis",
                content="Jacklyn variance observes the data patterns.",
                symbol_id="jacklyn-variance",
                page_index=3,
                score=0.92
            )
        ]
        
        mock_session.execute.return_value = mock_rows
        
        # Make filtered search request
        response = self.client.post("/index", json={
            "q": "data analysis",
            "top_k": 5,
            "symbol_id": "jacklyn-variance"
        })
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data["total_results"], 1)
        self.assertEqual(data["results"][0]["symbol_id"], "jacklyn-variance")
    
    @patch('backend.app.retrieval_api.cassandra_session')
    @patch('backend.app.retrieval_api.tokenizer_service')
    def test_semantic_search_query_too_long(self, mock_tokenizer, mock_session):
        """Test rejection of queries that are too long."""
        # Mock tokenizer to return large token count
        mock_tokenizer.count_tokens.return_value = 250  # Exceeds 200 token limit
        
        # Make request with long query
        response = self.client.post("/index", json={
            "q": "very long query " * 50,  # Simulate long query
            "top_k": 5
        })
        
        # Assert 400 bad request
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("Query too long", data["detail"])
    
    @patch('backend.app.retrieval_api.cassandra_session', None)
    def test_semantic_search_no_database(self):
        """Test search when database is not available."""
        response = self.client.post("/index", json={
            "q": "test query",
            "top_k": 5
        })
        
        # Assert 503 service unavailable
        self.assertEqual(response.status_code, 503)
        data = response.json()
        self.assertIn("Database not available", data["detail"])
    
    @patch('backend.app.retrieval_api.cassandra_session')
    @patch('backend.app.retrieval_api.get_embedding')
    @patch('backend.app.retrieval_api.tokenizer_service')
    def test_semantic_search_embedding_error(self, mock_tokenizer, mock_embedding, mock_session):
        """Test handling of embedding generation errors."""
        # Mock tokenizer service
        mock_tokenizer.count_tokens.return_value = 5
        
        # Mock embedding generation failure
        mock_embedding.side_effect = Exception("Embedding service unavailable")
        
        # Make search request
        response = self.client.post("/index", json={
            "q": "test query",
            "top_k": 5
        })
        
        # Assert 500 internal server error
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Search failed", data["detail"])
    
    def test_semantic_search_invalid_request(self):
        """Test validation of search request parameters."""
        # Test missing query
        response = self.client.post("/index", json={
            "top_k": 5
        })
        self.assertEqual(response.status_code, 422)  # Validation error
        
        # Test invalid top_k
        response = self.client.post("/index", json={
            "q": "test query",
            "top_k": 0  # Invalid: must be >= 1
        })
        self.assertEqual(response.status_code, 422)
        
        # Test top_k too large
        response = self.client.post("/index", json={
            "q": "test query",
            "top_k": 100  # Invalid: must be <= 50
        })
        self.assertEqual(response.status_code, 422)
    
    @patch('backend.app.retrieval_api.cassandra_session')
    @patch('backend.app.retrieval_api.get_embedding')
    @patch('backend.app.retrieval_api.tokenizer_service')
    @patch('backend.app.retrieval_api.truncate_to_tokens')
    def test_preview_truncation(self, mock_truncate, mock_tokenizer, mock_embedding, mock_session):
        """Test that long content is truncated for previews."""
        # Mock tokenizer service
        mock_tokenizer.count_tokens.return_value = 5
        
        # Mock embedding generation
        mock_embedding.return_value = [0.1] * 768
        
        # Mock truncation
        mock_truncate.return_value = "Truncated preview..."
        
        # Mock search results with long content
        long_content = "This is a very long piece of content " * 50
        mock_rows = [
            MockSearchRow(
                page_id="001-long-page",
                title="Long Page",
                content=long_content,
                symbol_id="london-fox",
                page_index=1,
                score=0.95
            )
        ]
        
        mock_session.execute.return_value = mock_rows
        
        # Make search request
        response = self.client.post("/index", json={
            "q": "test query",
            "top_k": 1
        })
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify truncation was called
        mock_truncate.assert_called_once_with(long_content, 300)
        
        # Check that preview is truncated
        self.assertEqual(data["results"][0]["preview"], "Truncated preview...")

if __name__ == "__main__":
    unittest.main()