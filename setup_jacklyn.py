#!/usr/bin/env python3
"""
Quick setup script for Jacklyn Variance Agent
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    print("🔍 Checking requirements...")
    
    required_packages = [
        ("sentence-transformers", "sentence_transformers"),
        ("torch", "torch"),
        ("dspy", "dspy"),
        ("mlflow", "mlflow"),
        ("openai", "openai"),
        ("python-dotenv", "dotenv")
    ]
    
    missing = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✓ {package_name}")
        except ImportError:
            print(f"✗ {package_name} - MISSING")
            missing.append(package_name)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All packages installed!")
    return True

def check_env():
    """Check environment configuration"""
    print("\n🔍 Checking environment...")
    
    if not Path(".env").exists():
        print("❌ .env file not found!")
        print("Copy .env.example to .env and add your OpenAI API key")
        return False
    
    # Load env vars
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set in .env!")
        return False
    
    print("✅ Environment configured!")
    return True

def check_memory():
    """Check if memories are loaded"""
    print("\n🔍 Checking Jacklyn's memory...")
    
    memory_file = Path("src/ai/memory/memory.jsonl")
    if not memory_file.exists():
        print("❌ No memory file found!")
        print("Run: python src/ai/memory/ingest_entrance_way.py")
        return False
    
    # Count memories
    with open(memory_file) as f:
        count = sum(1 for _ in f)
    
    print(f"✅ Found {count} memories!")
    return True

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║               JACKLYN VARIANCE AGENT SETUP                   ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    all_good = True
    all_good &= check_requirements()
    all_good &= check_env()
    all_good &= check_memory()
    
    if all_good:
        print("""
🎉 Everything is ready!

To talk to Jacklyn:
  python src/ai/agents/jacklyn_cli.py

To test the agent directly:
  python src/ai/agents/jacklyn_agent.py
""")
    else:
        print("""
⚠️  Setup incomplete. Fix the issues above and run this again.
""")
        sys.exit(1)

if __name__ == "__main__":
    main()