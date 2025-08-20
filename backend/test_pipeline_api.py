#!/usr/bin/env python3
"""Test the QDPI pipeline API endpoints"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from qdpi.program import MockQDPIProgram
from qdpi.symbols import get_symbol_info

def test_pipeline():
    """Test the pipeline locally without HTTP"""
    
    print("Testing QDPI Pipeline...")
    
    # Initialize mock program
    prog = MockQDPIProgram()
    
    # Test symbol 0x00 (an author:XC)
    print("\nTest 1: Symbol 0x00 (an author:XC)")
    result = prog.forward(symbol_code=0x00, user_intent="continue")
    print(f"Symbol: {result.symbol_info['notation']}")
    print(f"Text preview: {result.page_text[:100]}...")
    print(f"Edges: {result.edges}")
    print(f"Trajectory: {result.trajectory}")
    
    # Test symbol 0x4C (jacklyn-variance:ZC)
    print("\n\nTest 2: Symbol 0x4C (jacklyn-variance:ZC)")
    result = prog.forward(symbol_code=0x4C, user_intent="observe deeper")
    print(f"Symbol: {result.symbol_info['notation']}")
    print(f"Text preview: {result.page_text[:100]}...")
    print(f"Index signals: {result.index_signals}")
    
    # Test symbol info for various codes
    print("\n\nTest 3: Symbol mappings")
    test_codes = [0x00, 0x10, 0x2A, 0x7F, 0xFF]
    for code in test_codes:
        info = get_symbol_info(code)
        print(f"  {code:3d} (0x{code:02X}): {info['notation']}")
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_pipeline()