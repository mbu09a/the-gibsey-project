"""
LLM service for the Gibsey Mycelial Network
Supports Ollama (local), OpenAI, and Claude with streaming capabilities
"""

import asyncio
import logging
import os
import json
from typing import List, Dict, Any, Optional, AsyncGenerator, Tuple
from enum import Enum
from dataclasses import dataclass
import aiohttp
import tiktoken

logger = logging.getLogger(__name__)

class LLMProvider(str, Enum):
    """Available LLM providers"""
    OLLAMA = "ollama"
    OPENAI = "openai"
    CLAUDE = "claude"
    AUTO = "auto"  # Automatic fallback

@dataclass
class LLMConfig:
    """LLM configuration"""
    provider: LLMProvider
    model: str
    max_tokens: int = 2000
    temperature: float = 0.7
    streaming: bool = True
    base_url: Optional[str] = None
    api_key: Optional[str] = None

@dataclass
class ChatMessage:
    """Chat message format"""
    role: str  # system, user, assistant
    content: str
    metadata: Dict[str, Any] = None

@dataclass
class StreamToken:
    """Streaming response token"""
    token: str
    is_complete: bool = False
    metadata: Dict[str, Any] = None

class LLMService:
    """
    Unified LLM service supporting multiple providers with streaming
    """
    
    def __init__(self):
        self.configs = self._load_configs()
        self.fallback_order = [LLMProvider.OLLAMA, LLMProvider.OPENAI, LLMProvider.CLAUDE]
        
        # Initialize clients
        self.http_session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60))
        
        # OpenAI client (lazy loaded)
        self._openai_client = None
        
        # Claude client (lazy loaded) 
        self._claude_client = None
        
        # Token encoder for context management
        try:
            self.token_encoder = tiktoken.get_encoding("cl100k_base")
        except Exception:
            self.token_encoder = None
            logger.warning("Could not load tiktoken encoder")
    
    def _load_configs(self) -> Dict[LLMProvider, LLMConfig]:
        """Load LLM configurations from environment"""
        return {
            LLMProvider.OLLAMA: LLMConfig(
                provider=LLMProvider.OLLAMA,
                model=os.getenv("OLLAMA_MODEL", "llama3:8b"),
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                temperature=float(os.getenv("OLLAMA_TEMPERATURE", "0.7")),
                max_tokens=int(os.getenv("OLLAMA_MAX_TOKENS", "2000"))
            ),
            LLMProvider.OPENAI: LLMConfig(
                provider=LLMProvider.OPENAI,
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
                max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
            ),
            LLMProvider.CLAUDE: LLMConfig(
                provider=LLMProvider.CLAUDE,
                model=os.getenv("CLAUDE_MODEL", "claude-3-haiku-20240307"),
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                temperature=float(os.getenv("CLAUDE_TEMPERATURE", "0.7")),
                max_tokens=int(os.getenv("CLAUDE_MAX_TOKENS", "2000"))
            )
        }
    
    async def get_available_providers(self) -> List[LLMProvider]:
        """Get list of available providers (with health checks)"""
        available = []
        
        # Check Ollama
        try:
            config = self.configs[LLMProvider.OLLAMA]
            async with self.http_session.get(f"{config.base_url}/api/tags") as response:
                if response.status == 200:
                    available.append(LLMProvider.OLLAMA)
        except Exception:
            logger.debug("Ollama not available")
        
        # Check OpenAI
        if self.configs[LLMProvider.OPENAI].api_key:
            available.append(LLMProvider.OPENAI)
        
        # Check Claude
        if self.configs[LLMProvider.CLAUDE].api_key:
            available.append(LLMProvider.CLAUDE)
        
        return available
    
    async def chat_stream(self, 
                         messages: List[ChatMessage], 
                         provider: LLMProvider = LLMProvider.AUTO,
                         **kwargs) -> AsyncGenerator[StreamToken, None]:
        """
        Stream chat completion from LLM
        """
        # Auto-select provider if needed
        if provider == LLMProvider.AUTO:
            available = await self.get_available_providers()
            if not available:
                raise RuntimeError("No LLM providers available")
            
            # Use first available in fallback order
            for prov in self.fallback_order:
                if prov in available:
                    provider = prov
                    break
        
        logger.info(f"Using LLM provider: {provider}")
        
        try:
            # Route to appropriate provider
            if provider == LLMProvider.OLLAMA:
                async for token in self._ollama_stream(messages, **kwargs):
                    yield token
            elif provider == LLMProvider.OPENAI:
                async for token in self._openai_stream(messages, **kwargs):
                    yield token
            elif provider == LLMProvider.CLAUDE:
                async for token in self._claude_stream(messages, **kwargs):
                    yield token
            else:
                raise ValueError(f"Unsupported provider: {provider}")
                
        except Exception as e:
            logger.error(f"LLM streaming failed with {provider}: {e}")
            
            # Try fallback if using AUTO
            if provider != LLMProvider.AUTO:
                raise
            
            # Attempt fallback to next provider
            available = await self.get_available_providers()
            remaining = [p for p in self.fallback_order if p != provider and p in available]
            
            if remaining:
                logger.info(f"Falling back to {remaining[0]}")
                async for token in self.chat_stream(messages, remaining[0], **kwargs):
                    yield token
            else:
                raise RuntimeError(f"All LLM providers failed. Last error: {e}")
    
    async def _ollama_stream(self, messages: List[ChatMessage], **kwargs) -> AsyncGenerator[StreamToken, None]:
        """Stream from Ollama"""
        config = self.configs[LLMProvider.OLLAMA]
        
        # Convert messages to Ollama format
        ollama_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        payload = {
            "model": config.model,
            "messages": ollama_messages,
            "stream": True,
            "options": {
                "temperature": config.temperature,
                "num_predict": config.max_tokens
            }
        }
        
        url = f"{config.base_url}/api/chat"
        
        try:
            headers = {"Content-Type": "application/json"}
            async with self.http_session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    response_text = await response.text()
                    raise RuntimeError(f"Ollama API error: {response.status} - {response_text}")
                
                async for line in response.content:
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            
                            if 'message' in data and 'content' in data['message']:
                                content = data['message']['content']
                                is_done = data.get('done', False)
                                
                                yield StreamToken(
                                    token=content,
                                    is_complete=is_done,
                                    metadata={"provider": "ollama", "model": config.model}
                                )
                                
                                if is_done:
                                    break
                                    
                        except json.JSONDecodeError:
                            continue
                            
        except Exception as e:
            logger.error(f"Ollama streaming error: {e}")
            raise
    
    async def _openai_stream(self, messages: List[ChatMessage], **kwargs) -> AsyncGenerator[StreamToken, None]:
        """Stream from OpenAI"""
        config = self.configs[LLMProvider.OPENAI]
        
        if not config.api_key:
            raise ValueError("OpenAI API key not configured")
        
        # Lazy load OpenAI client
        if not self._openai_client:
            try:
                from openai import AsyncOpenAI
                self._openai_client = AsyncOpenAI(api_key=config.api_key)
            except ImportError:
                raise RuntimeError("OpenAI library not installed")
        
        # Convert messages to OpenAI format
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        try:
            stream = await self._openai_client.chat.completions.create(
                model=config.model,
                messages=openai_messages,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta:
                    content = chunk.choices[0].delta.content
                    if content:
                        is_done = chunk.choices[0].finish_reason is not None
                        
                        yield StreamToken(
                            token=content,
                            is_complete=is_done,
                            metadata={"provider": "openai", "model": config.model}
                        )
                        
        except Exception as e:
            logger.error(f"OpenAI streaming error: {e}")
            raise
    
    async def _claude_stream(self, messages: List[ChatMessage], **kwargs) -> AsyncGenerator[StreamToken, None]:
        """Stream from Claude (Anthropic)"""
        config = self.configs[LLMProvider.CLAUDE]
        
        if not config.api_key:
            raise ValueError("Claude API key not configured")
        
        # Lazy load Anthropic client
        if not self._claude_client:
            try:
                from anthropic import AsyncAnthropic
                self._claude_client = AsyncAnthropic(api_key=config.api_key)
            except ImportError:
                raise RuntimeError("Anthropic library not installed")
        
        # Convert messages to Claude format (separate system message)
        system_message = None
        claude_messages = []
        
        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                claude_messages.append({"role": msg.role, "content": msg.content})
        
        try:
            stream = self._claude_client.messages.stream(
                model=config.model,
                messages=claude_messages,
                system=system_message or "",
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
            
            async with stream as stream_manager:
                async for event in stream_manager:
                    if hasattr(event, 'delta') and hasattr(event.delta, 'text'):
                        yield StreamToken(
                            token=event.delta.text,
                            is_complete=False,
                            metadata={"provider": "claude", "model": config.model}
                        )
            
            # Send completion signal
            yield StreamToken(
                token="",
                is_complete=True,
                metadata={"provider": "claude", "model": config.model}
            )
            
        except Exception as e:
            logger.error(f"Claude streaming error: {e}")
            raise
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        if self.token_encoder:
            return len(self.token_encoder.encode(text))
        else:
            # Rough estimate: ~4 chars per token
            return len(text) // 4
    
    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to max tokens"""
        if self.token_encoder:
            tokens = self.token_encoder.encode(text)
            if len(tokens) <= max_tokens:
                return text
            truncated_tokens = tokens[:max_tokens]
            return self.token_encoder.decode(truncated_tokens)
        else:
            # Rough truncation
            max_chars = max_tokens * 4
            return text[:max_chars]
    
    async def close(self):
        """Clean up resources"""
        if self.http_session:
            await self.http_session.close()

# Global LLM service instance
_llm_service = None

def get_llm_service() -> LLMService:
    """Get or create global LLM service instance"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service

async def close_llm_service():
    """Close the global LLM service"""
    global _llm_service
    if _llm_service:
        await _llm_service.close()
        _llm_service = None