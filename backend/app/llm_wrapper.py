"""
LLM wrapper service with Ollama primary and cloud API fallbacks.

Provides a unified interface for language model calls with automatic fallback
from local Ollama to OpenAI or Claude APIs when needed.
"""

import os
import json
import logging
import time
from typing import Optional, Dict, Any, List, AsyncGenerator
from dataclasses import dataclass
import asyncio
import httpx
import openai
from anthropic import AsyncAnthropic

logger = logging.getLogger(__name__)

# Configuration from environment
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:8b")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")

# Timeout configuration
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "30"))
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "60"))


@dataclass
class LLMResponse:
    """Unified response format from any LLM backend."""
    text: str
    model_used: str
    backend: str  # "ollama", "openai", or "anthropic"
    generation_time_ms: float
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None


class LLMWrapper:
    """
    Wrapper for multiple LLM backends with automatic fallback.
    
    Attempts to use Ollama first, then falls back to OpenAI or Claude.
    """
    
    def __init__(self):
        """Initialize the LLM wrapper with available backends."""
        self.ollama_client = httpx.AsyncClient(timeout=OLLAMA_TIMEOUT)
        
        # Initialize cloud API clients if keys are available
        self.openai_available = bool(OPENAI_API_KEY)
        if self.openai_available:
            openai.api_key = OPENAI_API_KEY
            
        self.anthropic_available = bool(ANTHROPIC_API_KEY)
        if self.anthropic_available:
            self.anthropic_client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    
    async def _check_ollama_health(self) -> bool:
        """Check if Ollama is running and responsive."""
        try:
            response = await self.ollama_client.get(f"{OLLAMA_BASE_URL}/api/tags")
            return response.status_code == 200
        except Exception as e:
            logger.debug(f"Ollama health check failed: {e}")
            return False
    
    async def _call_ollama(self, prompt: str, system: Optional[str] = None) -> Optional[LLMResponse]:
        """Call Ollama API with the given prompt."""
        start_time = time.time()
        
        try:
            # Check if Ollama is available
            if not await self._check_ollama_health():
                logger.warning("Ollama service not available")
                return None
            
            # Prepare the request
            full_prompt = prompt
            if system:
                full_prompt = f"{system}\n\n{prompt}"
            
            payload = {
                "model": OLLAMA_MODEL,
                "prompt": full_prompt,
                "stream": False
            }
            
            # Make the API call
            response = await self.ollama_client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json=payload
            )
            
            if response.status_code != 200:
                logger.error(f"Ollama returned status {response.status_code}: {response.text}")
                return None
            
            data = response.json()
            generation_time = (time.time() - start_time) * 1000
            
            return LLMResponse(
                text=data.get("response", ""),
                model_used=OLLAMA_MODEL,
                backend="ollama",
                generation_time_ms=generation_time
            )
            
        except Exception as e:
            logger.error(f"Ollama call failed: {e}")
            return None
    
    async def _call_openai(self, prompt: str, system: Optional[str] = None) -> Optional[LLMResponse]:
        """Call OpenAI API with the given prompt."""
        if not self.openai_available:
            return None
            
        start_time = time.time()
        
        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            # Use the async OpenAI client
            response = await asyncio.to_thread(
                openai.ChatCompletion.create,
                model=OPENAI_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            generation_time = (time.time() - start_time) * 1000
            
            return LLMResponse(
                text=response.choices[0].message.content,
                model_used=OPENAI_MODEL,
                backend="openai",
                generation_time_ms=generation_time,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens
            )
            
        except Exception as e:
            logger.error(f"OpenAI call failed: {e}")
            return None
    
    async def _call_anthropic(self, prompt: str, system: Optional[str] = None) -> Optional[LLMResponse]:
        """Call Anthropic Claude API with the given prompt."""
        if not self.anthropic_available:
            return None
            
        start_time = time.time()
        
        try:
            # Claude expects messages in a specific format
            messages = [{"role": "user", "content": prompt}]
            
            response = await self.anthropic_client.messages.create(
                model=ANTHROPIC_MODEL,
                messages=messages,
                system=system if system else None,
                max_tokens=2000,
                temperature=0.7
            )
            
            generation_time = (time.time() - start_time) * 1000
            
            return LLMResponse(
                text=response.content[0].text,
                model_used=ANTHROPIC_MODEL,
                backend="anthropic", 
                generation_time_ms=generation_time,
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens
            )
            
        except Exception as e:
            logger.error(f"Anthropic call failed: {e}")
            return None
    
    async def generate_response(
        self, 
        prompt: str, 
        system: Optional[str] = None,
        preferred_backend: Optional[str] = None
    ) -> LLMResponse:
        """
        Generate a response using available LLM backends.
        
        Args:
            prompt: The user prompt/question
            system: Optional system message for context/instructions
            preferred_backend: Optionally specify which backend to try first
            
        Returns:
            LLMResponse with the generated text and metadata
            
        Raises:
            Exception if all backends fail
        """
        backends = []
        
        # Determine order of backends to try
        if preferred_backend == "openai" and self.openai_available:
            backends = ["openai", "ollama", "anthropic"]
        elif preferred_backend == "anthropic" and self.anthropic_available:
            backends = ["anthropic", "ollama", "openai"]
        else:
            # Default order: Ollama first, then cloud services
            backends = ["ollama", "openai", "anthropic"]
        
        # Try each backend in order
        for backend in backends:
            logger.info(f"Attempting to use {backend} backend")
            
            if backend == "ollama":
                response = await self._call_ollama(prompt, system)
            elif backend == "openai":
                response = await self._call_openai(prompt, system)
            elif backend == "anthropic":
                response = await self._call_anthropic(prompt, system)
            else:
                continue
                
            if response:
                logger.info(f"Successfully generated response using {backend}")
                return response
            else:
                logger.warning(f"{backend} backend failed or unavailable, trying next...")
        
        # All backends failed
        raise Exception("All LLM backends failed to generate a response")
    
    async def ensure_z_receive_prefix(self, response: LLMResponse) -> LLMResponse:
        """
        Ensure the response starts with <Z_RECEIVE> token.
        
        Args:
            response: The LLM response to check
            
        Returns:
            LLMResponse with <Z_RECEIVE> prefix guaranteed
        """
        if not response.text.startswith("<Z_RECEIVE>"):
            response.text = f"<Z_RECEIVE>\n{response.text}"
        return response
    
    async def close(self):
        """Clean up resources."""
        await self.ollama_client.aclose()
        if self.anthropic_available:
            await self.anthropic_client.close()


# Singleton instance
_llm_wrapper: Optional[LLMWrapper] = None


def get_llm_wrapper() -> LLMWrapper:
    """Get or create the singleton LLM wrapper instance."""
    global _llm_wrapper
    if _llm_wrapper is None:
        _llm_wrapper = LLMWrapper()
    return _llm_wrapper


async def close_llm_wrapper():
    """Close the LLM wrapper and clean up resources."""
    global _llm_wrapper
    if _llm_wrapper:
        await _llm_wrapper.close()
        _llm_wrapper = None