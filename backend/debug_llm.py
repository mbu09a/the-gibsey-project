#!/usr/bin/env python3
"""
Debug LLM service - check what's wrong with Ollama integration
"""

import asyncio
import aiohttp
import json
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app.llm_service import LLMConfig, LLMProvider

async def debug_ollama():
    """Debug Ollama connection"""
    
    print("🔍 Debugging Ollama connection...")
    
    # Test direct aiohttp connection
    config = LLMConfig(
        provider=LLMProvider.OLLAMA,
        model="llama3:8b",
        base_url="http://localhost:11434",
        temperature=0.7,
        max_tokens=100
    )
    
    payload = {
        "model": config.model,
        "messages": [{"role": "user", "content": "Hello, test message"}],
        "stream": True,
        "options": {
            "temperature": config.temperature,
            "num_predict": config.max_tokens
        }
    }
    
    url = f"{config.base_url}/api/chat"
    print(f"🌐 Testing URL: {url}")
    print(f"📦 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            print("📡 Making request...")
            
            async with session.post(url, json=payload) as response:
                print(f"📊 Response status: {response.status}")
                print(f"📋 Response headers: {dict(response.headers)}")
                
                if response.status != 200:
                    error_text = await response.text()
                    print(f"❌ Error response: {error_text}")
                    return False
                
                # Read streaming response
                token_count = 0
                async for line in response.content:
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            token_count += 1
                            
                            if token_count <= 5:
                                print(f"🔤 Token {token_count}: {data}")
                            
                            if data.get('done', False):
                                print(f"✅ Streaming complete! {token_count} tokens")
                                break
                                
                        except json.JSONDecodeError as e:
                            print(f"⚠️ JSON decode error: {e}, line: {line}")
                            continue
                
                return True
                
    except Exception as e:
        print(f"❌ Request failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Debug main"""
    success = await debug_ollama()
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)