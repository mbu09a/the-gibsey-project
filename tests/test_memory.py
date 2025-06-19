import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai.memory.embedding_store import EmbeddingStore
import tempfile
import pathlib

def test_memory_smoke():
    """Smoke test: add memories and search them"""
    with tempfile.TemporaryDirectory() as tmpdir:
        store_path = pathlib.Path(tmpdir) / "test_memory.jsonl"
        store = EmbeddingStore(path=str(store_path))
        
        # Add some test memories
        store.add("The quick brown fox jumps over the lazy dog", 
                 {"author": "jacklyn", "tags": ["animals", "test"]})
        store.add("London fog creates mysterious atmosphere", 
                 {"author": "london-fox", "tags": ["atmosphere", "mystery"]})
        
        # Search for similar content
        results = store.search("fox animal", k=2)
        
        assert len(results) == 2
        assert results[0][1] > 0.3  # similarity score should be reasonable
        
        # Test filtering
        jacklyn_results = store.search("fox", k=10, filters={"author": "jacklyn"})
        assert len(jacklyn_results) == 1
        assert jacklyn_results[0][0].meta["author"] == "jacklyn"
        
        print("✓ Memory smoke test passed")

if __name__ == "__main__":
    test_memory_smoke()