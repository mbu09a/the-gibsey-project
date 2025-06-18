#!/usr/bin/env python3
"""
Debug LLM service within the server context
"""

import asyncio
import requests
import json

def test_server_llm():
    """Test LLM via server API"""
    
    print("🔍 Testing LLM through server...")
    
    try:
        # Test health first
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"📊 Server health: {health_response.status_code}")
        print(f"🏥 Health data: {health_response.json()}")
        
        # Test our direct LLM test
        print("🤖 Testing direct LLM integration...")
        test_response = requests.post(
            "http://localhost:8000/test-llm-direct",
            timeout=30
        )
        
        if test_response.status_code == 404:
            print("⚠️ Test endpoint not found, server might not have our LLM test route")
            return False
        
        print(f"📊 LLM test response: {test_response.status_code}")
        print(f"📝 Response: {test_response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Server test failed: {e}")
        return False

def main():
    """Debug main"""
    return test_server_llm()

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)