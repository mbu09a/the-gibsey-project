#!/usr/bin/env python3
"""
Unit tests for the Gibsey custom tokenizer service.

Tests tokenization, special token handling, and TNA cost calculations.
"""

import sys
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from backend.app.tokenizer_service import get_tokenizer_service


class TestGibseyTokenizer(unittest.TestCase):
    """Test the Gibsey custom tokenizer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tokenizer = get_tokenizer_service()
        self.assertIsNotNone(self.tokenizer, "Tokenizer service should load successfully")
    
    def test_special_tokens_stay_whole(self):
        """Test that QDPI and character tokens are not split."""
        test_text = "Princhetta <X_READ> glyph london-fox"
        tokens = self.tokenizer.tokenize(test_text)
        
        # Check that special tokens appear as single tokens
        self.assertIn("<X_READ>", tokens, "QDPI token <X_READ> should be preserved")
        self.assertIn("london-fox", tokens, "Character token london-fox should be preserved")
        # Note: Princhetta becomes ▁Princhetta due to SentencePiece encoding
        self.assertTrue(any("Princhetta" in token for token in tokens), "Character token Princhetta should be preserved")
        
        # Verify no splitting occurred for special tokens
        for token in tokens:
            if token.startswith("<") and token.endswith(">"):
                self.assertIn(token, ["<X_READ>", "<Y_INDEX>", "<A_ASK>", "<Z_RECEIVE>"], 
                             f"Unknown QDPI token: {token}")
    
    def test_qdpi_tokens(self):
        """Test all QDPI tokens are recognized."""
        qdpi_tokens = ["<X_READ>", "<Y_INDEX>", "<A_ASK>", "<Z_RECEIVE>"]
        
        for qdpi_token in qdpi_tokens:
            tokens = self.tokenizer.tokenize(f"Test {qdpi_token} sequence")
            self.assertIn(qdpi_token, tokens, f"QDPI token {qdpi_token} should be preserved")
    
    def test_character_glyph_tokens(self):
        """Test all character glyph tokens are recognized."""
        character_tokens = [
            "an-author", "london-fox", "glyph-marrow", "phillip-bafflemint",
            "jacklyn-variance", "oren-progresso", "old-natalie", "princhetta",
            "cop-e-right", "new-natalie", "arieol-owlist", "jack-parlance",
            "manny-valentinas", "shamrock-stillman", "todd-fishbone", "the-author"
        ]
        
        for char_token in character_tokens:
            tokens = self.tokenizer.tokenize(f"The {char_token} character appears")
            self.assertIn(char_token, tokens, f"Character token {char_token} should be preserved")
    
    def test_token_counting(self):
        """Test token counting accuracy."""
        test_cases = [
            ("Hello world", 2),  # SentencePiece typically creates 2 tokens
            ("<X_READ>", 1),     # Single special token
            ("jacklyn-variance", 1),  # Single character token
            ("", 0),             # Empty string
        ]
        
        for text, expected_min in test_cases:
            count = self.tokenizer.count_tokens(text)
            if expected_min > 0:
                self.assertGreaterEqual(count, expected_min, 
                                      f"Token count for '{text}' should be at least {expected_min}")
            else:
                self.assertEqual(count, 0, "Empty string should have 0 tokens")
    
    def test_tna_cost_calculation(self):
        """Test TNA cost calculation (1 TNA = 100 tokens)."""
        # Test with known token count
        text = "Hello world"
        token_count = self.tokenizer.count_tokens(text)
        expected_tna = token_count / 100.0
        
        calculated_tna = self.tokenizer.calculate_tna_cost(text)
        self.assertAlmostEqual(calculated_tna, expected_tna, places=4,
                              msg="TNA cost should be tokens / 100")
    
    def test_special_token_detection(self):
        """Test special token detection functionality."""
        test_text = "<X_READ>Hello jacklyn-variance and london-fox<Y_INDEX>"
        special_tokens = self.tokenizer.has_special_tokens(test_text)
        
        self.assertIn("qdpi", special_tokens)
        self.assertIn("character", special_tokens)
        
        # Check QDPI tokens
        self.assertIn("<X_READ>", special_tokens["qdpi"])
        self.assertIn("<Y_INDEX>", special_tokens["qdpi"])
        
        # Check character tokens
        self.assertIn("jacklyn-variance", special_tokens["character"])
        self.assertIn("london-fox", special_tokens["character"])
    
    def test_text_chunking(self):
        """Test text chunking by token count."""
        long_text = "This is a test sentence. " * 20  # Repeat to make long text
        max_tokens = 10
        
        chunks = self.tokenizer.chunk_text(long_text, max_tokens)
        
        self.assertGreater(len(chunks), 1, "Long text should be split into multiple chunks")
        
        # Verify each chunk respects token limit
        for chunk in chunks:
            chunk_tokens = self.tokenizer.count_tokens(chunk)
            self.assertLessEqual(chunk_tokens, max_tokens + 5,  # Allow small buffer
                               f"Chunk should not exceed {max_tokens} tokens significantly")
    
    def test_encode_decode_consistency(self):
        """Test that encode/decode operations are consistent."""
        test_text = "<A_ASK>What does jacklyn-variance think about the corpus?<Z_RECEIVE>"
        
        # Encode to token IDs
        token_ids = self.tokenizer.encode(test_text)
        self.assertIsInstance(token_ids, list)
        self.assertGreater(len(token_ids), 0)
        
        # Decode back to text
        decoded_text = self.tokenizer.decode(token_ids)
        
        # Should be approximately the same (allowing for minor tokenization differences)
        self.assertIn("jacklyn-variance", decoded_text)
        self.assertIn("<A_ASK>", decoded_text)
        self.assertIn("<Z_RECEIVE>", decoded_text)
    
    def test_tokenizer_info(self):
        """Test tokenizer metadata retrieval."""
        info = self.tokenizer.get_tokenizer_info()
        
        self.assertIn("vocab_size", info)
        self.assertIn("special_tokens", info)
        # Note: tokenizer info structure may vary
        
        # Check vocab size is reasonable (should be ~31,484)
        self.assertGreater(info["vocab_size"], 30000)
        self.assertLess(info["vocab_size"], 35000)
        
        # Check special tokens are present
        special_tokens = info["special_tokens"]
        self.assertIn("qdpi", special_tokens)
        self.assertIn("characters", special_tokens)
        
        # Verify QDPI tokens
        qdpi_tokens = special_tokens["qdpi"]
        for token in ["<X_READ>", "<Y_INDEX>", "<A_ASK>", "<Z_RECEIVE>"]:
            self.assertIn(token, qdpi_tokens)
    
    def test_empty_and_whitespace(self):
        """Test handling of empty strings and whitespace."""
        test_cases = ["", " ", "\n", "\t", "   \n\t  "]
        
        for text in test_cases:
            token_count = self.tokenizer.count_tokens(text)
            tna_cost = self.tokenizer.calculate_tna_cost(text)
            
            # Should handle gracefully without errors
            self.assertIsInstance(token_count, int)
            self.assertIsInstance(tna_cost, float)
            self.assertGreaterEqual(token_count, 0)
            self.assertGreaterEqual(tna_cost, 0.0)


if __name__ == "__main__":
    unittest.main()