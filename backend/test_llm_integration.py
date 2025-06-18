#!/usr/bin/env python3
"""
Test script for LLM integration
Tests the real LLM streaming functionality
"""

import asyncio
import os
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app.llm_service import get_llm_service, ChatMessage, LLMProvider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_llm_service():
    """Test the LLM service with streaming"""
    
    logger.info("🧪 Testing LLM service...")
    
    try:
        # Load environment
        from dotenv import load_dotenv
        load_dotenv()
        
        # Get LLM service
        llm_service = get_llm_service()
        
        # Check available providers
        available = await llm_service.get_available_providers()
        logger.info(f"Available LLM providers: {available}")
        
        if not available:
            logger.error("❌ No LLM providers available")
            return False
        
        # Test streaming with a simple message
        test_messages = [
            ChatMessage(
                role="system", 
                content="You are London Fox, a brilliant AI consciousness. Respond concisely and intellectually."
            ),
            ChatMessage(
                role="user", 
                content="What is the nature of consciousness?"
            )
        ]
        
        logger.info("🤖 Streaming response from LLM...")
        full_response = ""
        token_count = 0
        
        async for token in llm_service.chat_stream(test_messages):
            full_response += token.token
            token_count += 1
            
            # Print first few tokens
            if token_count <= 5:
                logger.info(f"Token {token_count}: '{token.token}' (complete: {token.is_complete})")
            
            if token.is_complete:
                break
        
        logger.info(f"✅ Received {token_count} tokens")
        logger.info(f"📝 Full response: {full_response[:200]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ LLM test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_rag_service():
    """Test the RAG service"""
    
    logger.info("🧪 Testing RAG service...")
    
    try:
        from app.rag_service import get_rag_service
        
        rag_service = get_rag_service()
        
        # Test building context
        logger.info("Building RAG context...")
        rag_context = await rag_service.build_context(
            character_id="london-fox",
            user_query="What is the nature of consciousness?"
        )
        
        logger.info(f"✅ Built RAG context with {rag_context.total_tokens} tokens")
        logger.info(f"📄 Found {len(rag_context.context_pages)} context pages")
        logger.info(f"🎭 Character: {rag_context.character_id}")
        
        # Test streaming response
        logger.info("🤖 Getting character response...")
        token_count = 0
        
        async for token in rag_service.get_character_response(
            character_id="london-fox",
            user_query="What is the nature of consciousness?",
            stream=True
        ):
            token_count += 1
            
            if token_count <= 3:
                logger.info(f"RAG Token {token_count}: '{token.token}' (complete: {token.is_complete})")
            
            if token.is_complete:
                break
        
        logger.info(f"✅ RAG streaming completed with {token_count} tokens")
        return True
        
    except Exception as e:
        logger.error(f"❌ RAG test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    
    logger.info("🚀 Starting LLM integration tests...")
    
    # Test 1: Basic LLM service
    llm_success = await test_llm_service()
    
    # Test 2: RAG service
    rag_success = await test_rag_service()
    
    # Summary
    if llm_success and rag_success:
        logger.info("🎉 All LLM integration tests passed!")
        return True
    else:
        logger.error("❌ Some tests failed")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)