"""Basic QDPI tests for symbol encoding/decoding"""

import pytest
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from qdpi.symbols import encode_symbol, decode_symbol, get_symbol_info, CHARACTER_MAP, BEHAVIORS
from qdpi.policy import allow_fork, require_return, calculate_trajectory_weight
from qdpi.page_schema import PageSchema

class TestSymbolEncoding:
    """Test symbol encoding and decoding"""
    
    def test_encode_decode_roundtrip(self):
        """Test that encoding and decoding are inverse operations"""
        for code in range(256):
            char_hex, behavior = decode_symbol(code)
            reconstructed = encode_symbol(char_hex, behavior)
            assert reconstructed == code, f"Roundtrip failed for code {code}"
    
    def test_encode_boundary_values(self):
        """Test encoding with boundary values"""
        # Test min values
        assert encode_symbol(0, 0) == 0
        
        # Test max values
        assert encode_symbol(15, 15) == 255
        
        # Test mixed values
        assert encode_symbol(0, 15) == 15
        assert encode_symbol(15, 0) == 240
    
    def test_encode_invalid_values(self):
        """Test encoding with invalid values raises errors"""
        with pytest.raises(ValueError):
            encode_symbol(-1, 0)
            
        with pytest.raises(ValueError):
            encode_symbol(16, 0)
            
        with pytest.raises(ValueError):
            encode_symbol(0, -1)
            
        with pytest.raises(ValueError):
            encode_symbol(0, 16)
    
    def test_decode_boundary_values(self):
        """Test decoding with boundary values"""
        # Test code 0
        char_hex, behavior = decode_symbol(0)
        assert char_hex == 0 and behavior == 0
        
        # Test code 255
        char_hex, behavior = decode_symbol(255)
        assert char_hex == 15 and behavior == 15
        
        # Test other specific codes
        char_hex, behavior = decode_symbol(0x4C)  # 76 decimal
        assert char_hex == 4 and behavior == 12  # jacklyn-variance:ZC
    
    def test_decode_invalid_values(self):
        """Test decoding with invalid values"""
        with pytest.raises(ValueError):
            decode_symbol(-1)
            
        with pytest.raises(ValueError):
            decode_symbol(256)
    
    def test_get_symbol_info(self):
        """Test getting complete symbol information"""
        info = get_symbol_info(0x00)
        assert info["code"] == 0
        assert info["character"] == "an author"
        assert info["orientation"] == "X"
        assert info["provenance"] == "C"
        assert info["notation"] == "an author:XC"
        
        info = get_symbol_info(0x4C)  # jacklyn-variance:ZC
        assert info["character"] == "jacklyn-variance"
        assert info["orientation"] == "Z"
        assert info["provenance"] == "C"

class TestPolicy:
    """Test QDPI policy rules"""
    
    def test_allow_fork(self):
        """Test fork permission logic"""
        # Should allow fork with low debt and branches
        assert allow_fork(open_branches=1, return_debt=0) == True
        assert allow_fork(open_branches=2, return_debt=1) == True
        
        # Should deny fork with high debt
        assert allow_fork(open_branches=1, return_debt=3) == False
        
        # Should deny fork with too many branches
        assert allow_fork(open_branches=3, return_debt=0) == False
    
    def test_require_return(self):
        """Test return requirement logic"""
        # Should not require return for short branches
        assert require_return(branch_length=1) == False
        assert require_return(branch_length=2) == False
        
        # Should require return for long branches
        assert require_return(branch_length=3) == True
        assert require_return(branch_length=5) == True
    
    def test_calculate_trajectory_weight(self):
        """Test trajectory weight calculation"""
        # Test basic weights
        weight = calculate_trajectory_weight("T0", 0.5, 0.8, 0)
        assert 0.0 <= weight <= 1.0
        
        # T0 should be preferred with high coherence
        weight_high_coh = calculate_trajectory_weight("T0", 0.5, 0.9, 0)
        weight_low_coh = calculate_trajectory_weight("T0", 0.5, 0.3, 0)
        assert weight_high_coh > weight_low_coh
        
        # T2 should be penalized with high debt
        weight_no_debt = calculate_trajectory_weight("T2", 0.8, 0.5, 0)
        weight_high_debt = calculate_trajectory_weight("T2", 0.8, 0.5, 2)
        assert weight_no_debt > weight_high_debt

class TestPageSchema:
    """Test Pydantic schemas"""
    
    def test_page_schema_valid(self):
        """Test creating valid page schema"""
        page = PageSchema(
            page_id="test-001",
            symbol_code=0x00,
            character="an author",
            orientation="X",
            provenance="C",
            text="This is a test page."
        )
        
        assert page.page_id == "test-001"
        assert page.symbol_code == 0
        assert page.trajectory == "T0"  # default
        assert page.text == "This is a test page."
    
    def test_page_schema_validation(self):
        """Test schema validation"""
        # Invalid symbol code
        with pytest.raises(ValueError):
            PageSchema(
                page_id="test",
                symbol_code=256,  # too high
                character="test",
                orientation="X",
                provenance="C",
                text="test"
            )
        
        # Invalid orientation
        with pytest.raises(ValueError):
            PageSchema(
                page_id="test",
                symbol_code=0,
                character="test",
                orientation="Q",  # invalid
                provenance="C",
                text="test"
            )
        
        # Invalid trajectory
        with pytest.raises(ValueError):
            PageSchema(
                page_id="test",
                symbol_code=0,
                character="test",
                orientation="X",
                provenance="C",
                trajectory="T5",  # invalid
                text="test"
            )

def test_character_behavior_completeness():
    """Test that we have complete character and behavior mappings"""
    # Should have exactly 16 characters
    assert len(CHARACTER_MAP) == 16
    assert set(CHARACTER_MAP.keys()) == set(range(16))
    
    # Should have exactly 16 behaviors
    assert len(BEHAVIORS) == 16
    assert set(BEHAVIORS.keys()) == set(range(16))
    
    # Each behavior should be a (orientation, provenance) tuple
    for behavior_id, (orientation, provenance) in BEHAVIORS.items():
        assert orientation in ["X", "Y", "A", "Z"]
        assert provenance in ["C", "P", "U", "S"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])