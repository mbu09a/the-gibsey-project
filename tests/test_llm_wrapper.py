#!/usr/bin/env python3
"""
Unit tests for the LLM wrapper with fallback logic.
"""

import sys
import unittest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from backend.app.llm_wrapper import LLMWrapper, LLMResponse


class TestLLMWrapper(unittest.TestCase):
    """Test the LLM wrapper functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.wrapper = LLMWrapper()
    
    def test_init(self):
        """Test LLM wrapper initialization."""
        self.assertIsNotNone(self.wrapper.ollama_client)
        # Other attributes depend on environment variables
    
    @patch('backend.app.llm_wrapper.httpx.AsyncClient.get')
    async def test_check_ollama_health_success(self, mock_get):
        """Test successful Ollama health check."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        is_healthy = await self.wrapper._check_ollama_health()
        self.assertTrue(is_healthy)
    
    @patch('backend.app.llm_wrapper.httpx.AsyncClient.get')
    async def test_check_ollama_health_failure(self, mock_get):
        """Test failed Ollama health check."""
        mock_get.side_effect = Exception("Connection refused")
        
        is_healthy = await self.wrapper._check_ollama_health()
        self.assertFalse(is_healthy)
    
    @patch('backend.app.llm_wrapper.httpx.AsyncClient.post')
    @patch.object(LLMWrapper, '_check_ollama_health')
    async def test_call_ollama_success(self, mock_health, mock_post):
        """Test successful Ollama API call."""
        # Mock health check to pass
        mock_health.return_value = True
        
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Test response from Ollama"}
        mock_post.return_value = mock_response
        
        result = await self.wrapper._call_ollama("Test prompt")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.text, "Test response from Ollama")
        self.assertEqual(result.backend, "ollama")
        self.assertGreater(result.generation_time_ms, 0)
    
    @patch.object(LLMWrapper, '_check_ollama_health')
    async def test_call_ollama_unhealthy(self, mock_health):
        """Test Ollama call when service is unhealthy."""
        mock_health.return_value = False
        
        result = await self.wrapper._call_ollama("Test prompt")
        self.assertIsNone(result)
    
    @patch('backend.app.llm_wrapper.openai.ChatCompletion.create')
    @patch('backend.app.llm_wrapper.asyncio.to_thread')
    async def test_call_openai_success(self, mock_to_thread, mock_create):
        """Test successful OpenAI API call."""
        # Mock the wrapper to have OpenAI available
        self.wrapper.openai_available = True
        
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response from OpenAI"
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 15
        
        mock_to_thread.return_value = mock_response
        
        result = await self.wrapper._call_openai("Test prompt")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.text, "Test response from OpenAI")
        self.assertEqual(result.backend, "openai")
        self.assertEqual(result.prompt_tokens, 10)
        self.assertEqual(result.completion_tokens, 15)
    
    async def test_call_openai_unavailable(self):
        """Test OpenAI call when not available."""
        self.wrapper.openai_available = False
        
        result = await self.wrapper._call_openai("Test prompt")
        self.assertIsNone(result)
    
    @patch.object(LLMWrapper, '_call_ollama')
    @patch.object(LLMWrapper, '_call_openai')
    @patch.object(LLMWrapper, '_call_anthropic')
    async def test_generate_response_ollama_success(self, mock_anthropic, mock_openai, mock_ollama):
        """Test successful response generation with Ollama."""
        # Mock Ollama to succeed
        mock_ollama.return_value = LLMResponse(
            text="Ollama response",
            model_used="llama2",
            backend="ollama",
            generation_time_ms=100.0
        )
        
        result = await self.wrapper.generate_response("Test prompt")
        
        self.assertEqual(result.text, "Ollama response")
        self.assertEqual(result.backend, "ollama")
        
        # Should not call other backends
        mock_openai.assert_not_called()
        mock_anthropic.assert_not_called()
    
    @patch.object(LLMWrapper, '_call_ollama')
    @patch.object(LLMWrapper, '_call_openai')
    @patch.object(LLMWrapper, '_call_anthropic')
    async def test_generate_response_fallback_to_openai(self, mock_anthropic, mock_openai, mock_ollama):
        """Test fallback to OpenAI when Ollama fails."""
        # Mock Ollama to fail
        mock_ollama.return_value = None
        
        # Mock OpenAI to succeed
        mock_openai.return_value = LLMResponse(
            text="OpenAI response",
            model_used="gpt-4",
            backend="openai",
            generation_time_ms=200.0
        )
        
        result = await self.wrapper.generate_response("Test prompt")
        
        self.assertEqual(result.text, "OpenAI response")
        self.assertEqual(result.backend, "openai")
        
        # Should have tried Ollama first
        mock_ollama.assert_called_once()
        mock_openai.assert_called_once()
    
    @patch.object(LLMWrapper, '_call_ollama')
    @patch.object(LLMWrapper, '_call_openai')
    @patch.object(LLMWrapper, '_call_anthropic')
    async def test_generate_response_all_backends_fail(self, mock_anthropic, mock_openai, mock_ollama):
        """Test when all backends fail."""
        # Mock all backends to fail
        mock_ollama.return_value = None
        mock_openai.return_value = None
        mock_anthropic.return_value = None
        
        with self.assertRaises(Exception) as context:
            await self.wrapper.generate_response("Test prompt")
        
        self.assertIn("All LLM backends failed", str(context.exception))
    
    async def test_ensure_z_receive_prefix_missing(self):
        """Test adding Z_RECEIVE prefix when missing."""
        response = LLMResponse(
            text="This is a response without prefix",
            model_used="test",
            backend="test",
            generation_time_ms=100.0
        )
        
        result = await self.wrapper.ensure_z_receive_prefix(response)
        
        self.assertTrue(result.text.startswith("<Z_RECEIVE>"))
        self.assertIn("This is a response without prefix", result.text)
    
    async def test_ensure_z_receive_prefix_present(self):
        """Test Z_RECEIVE prefix when already present."""
        original_text = "<Z_RECEIVE>\nThis already has the prefix"
        response = LLMResponse(
            text=original_text,
            model_used="test",
            backend="test",
            generation_time_ms=100.0
        )
        
        result = await self.wrapper.ensure_z_receive_prefix(response)
        
        # Should not duplicate the prefix
        self.assertEqual(result.text, original_text)
        self.assertEqual(result.text.count("<Z_RECEIVE>"), 1)


class TestLLMWrapperAsync(unittest.IsolatedAsyncioTestCase):
    """Async test cases for LLM wrapper."""
    
    async def test_wrapper_lifecycle(self):
        """Test wrapper creation and cleanup."""
        wrapper = LLMWrapper()
        
        # Test that we can create and close the wrapper
        await wrapper.close()
        
        # Should be able to create a new one
        wrapper2 = LLMWrapper()
        await wrapper2.close()


def run_async_test(coro):
    """Helper to run async tests in sync test methods."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# Add async test runner for sync test methods
for method_name in dir(TestLLMWrapper):
    if method_name.startswith('test_') and method_name.endswith('_async'):
        # Skip - these will be handled by async test case
        continue
    elif method_name.startswith('test_'):
        method = getattr(TestLLMWrapper, method_name)
        if asyncio.iscoroutinefunction(method):
            # Wrap async test methods for sync execution
            setattr(TestLLMWrapper, method_name, 
                   lambda self, orig_method=method: run_async_test(orig_method(self)))


if __name__ == "__main__":
    # Run both sync and async tests
    unittest.main()