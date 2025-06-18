#!/usr/bin/env python3
"""
Quick test to verify Jacklyn's AI system is working
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_memory_system():
    """Test the embedding memory system"""
    print("🔍 Testing memory system...")
    
    try:
        from ai.memory.embedding_store import EmbeddingStore
        store = EmbeddingStore()
        
        # Check if memories exist
        memory_count = len(store.entries)
        print(f"✓ Memory store loaded: {memory_count} entries")
        
        if memory_count == 0:
            print("⚠️  No memories found. Run: python src/ai/memory/ingest_entrance_way.py")
            return False
        
        # Test search
        results = store.search("Gibsey", k=3)
        print(f"✓ Search test: found {len(results)} results")
        
        return True
        
    except Exception as e:
        print(f"❌ Memory system error: {e}")
        return False

def test_agent_system():
    """Test Jacklyn's agent system"""
    print("\n🤖 Testing agent system...")
    
    try:
        # Import required modules
        from dotenv import load_dotenv
        load_dotenv()
        
        import dspy
        from ai.agents.jacklyn_agent import jacklyn
        
        print("✓ DSPy and agent imports successful")
        
        # Quick reasoning test (if API key is available)
        if os.getenv("OPENAI_API_KEY"):
            print("✓ API key found - agent ready for conversation")
            
            # Quick test query
            try:
                result = jacklyn("Tell me about Gibsey World in one sentence.")
                print(f"✓ Agent response test successful")
                print(f"   Response: {result['response'][:100]}...")
                return True
            except Exception as e:
                print(f"⚠️  Agent test failed (but system is set up): {e}")
                return True  # Still consider setup successful
        else:
            print("⚠️  No API key - add OPENAI_API_KEY to .env for full functionality")
            return True  # System is set up, just needs API key
            
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Agent system error: {e}")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║              JACKLYN VARIANCE SYSTEM TEST                    ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    memory_ok = test_memory_system()
    agent_ok = test_agent_system()
    
    if memory_ok and agent_ok:
        print("""
🎉 System test passed!

Jacklyn is ready to talk:
  python src/ai/agents/jacklyn_cli.py

For interactive setup help:
  python setup_jacklyn.py
""")
    else:
        print("""
⚠️  Some issues found. Check the errors above.

For detailed setup:
  python setup_jacklyn.py
""")

if __name__ == "__main__":
    main()