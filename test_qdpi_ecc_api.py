#!/usr/bin/env python3
"""
Test QDPI Error Correction API Integration
Validates that the complete ECC system works through the FastAPI endpoints
"""

import requests
import json
import time
import base64

# API base URL (adjust for your setup)
BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test all QDPI ECC API endpoints"""
    
    print("🧪 QDPI Error Correction API Integration Test")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n## Test 1: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/qdpi/ecc/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health Check: {health_data['status']}")
        else:
            print(f"❌ Health Check Failed: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is the FastAPI server running?")
        print("Start server with: uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    # Test 2: Symbol Validation
    print("\n## Test 2: Symbol Validation")
    test_symbols = ["cop-e-right", "VALIDATE", "london_fox", "invalid_symbol"]
    
    for symbol in test_symbols:
        response = requests.get(f"{BASE_URL}/qdpi/ecc/canon/validate/{symbol}")
        if response.status_code == 200:
            data = response.json()
            status = "✅ VALID" if data['valid'] else "❌ INVALID"
            print(f"   {symbol}: {status}")
        else:
            print(f"   {symbol}: ❌ API ERROR")
    
    # Test 3: Narrative Encoding
    print("\n## Test 3: Narrative Encoding")
    
    narrative_request = {
        "description": "User login flow with security validation",
        "symbol_sequence": [
            {"symbol_name": "cop-e-right", "rotation": 90},
            {"symbol_name": "VALIDATE", "rotation": 270},
            {"symbol_name": "phillip_bafflemint", "rotation": 270},
            {"symbol_name": "london_fox", "rotation": 180}
        ]
    }
    
    response = requests.post(f"{BASE_URL}/qdpi/ecc/encode", json=narrative_request)
    
    if response.status_code == 200:
        encode_data = response.json()
        print(f"✅ Encoding Success:")
        print(f"   Block ID: {encode_data['block_id']}")
        print(f"   Symbol Sequence: {encode_data['symbol_sequence']}")
        print(f"   Narrative: {encode_data['narrative_meaning']}")
        print(f"   Encoding Time: {encode_data['encoding_time_ms']:.2f}ms")
        print(f"   Protection: {encode_data['protection_metadata']['protection_level']}")
        
        # Store for next test
        protected_data = encode_data['protected_data_base64']
        block_id = encode_data['block_id']
        original_length = len(narrative_request['symbol_sequence'])
        
    else:
        print(f"❌ Encoding Failed: {response.status_code} - {response.text}")
        return
    
    # Test 4: Narrative Decoding
    print("\n## Test 4: Narrative Decoding")
    
    decode_request = {
        "protected_data": protected_data,
        "original_length": original_length,
        "block_id": block_id
    }
    
    response = requests.post(f"{BASE_URL}/qdpi/ecc/decode", json=decode_request)
    
    if response.status_code == 200:
        decode_data = response.json()
        print(f"✅ Decoding Success:")
        print(f"   Recovery: {'✅ SUCCESS' if decode_data['recovery_successful'] else '❌ FAILED'}")
        print(f"   Narrative: {decode_data['narrative_meaning']}")
        print(f"   Decode Time: {decode_data['decode_statistics']['decode_time_ms']:.2f}ms")
        print(f"   Performance: {'✅ <4ms' if decode_data['performance_target_met'] else '❌ >4ms'}")
        
    else:
        print(f"❌ Decoding Failed: {response.status_code} - {response.text}")
        return
    
    # Test 5: Transmission Error Testing
    print("\n## Test 5: Transmission Error Testing")
    
    error_rates = [0.005, 0.01, 0.02]  # 0.5%, 1%, 2%
    
    for error_rate in error_rates:
        test_request = {
            "block_id": block_id,
            "error_rate": error_rate
        }
        
        response = requests.post(f"{BASE_URL}/qdpi/ecc/test-transmission", json=test_request)
        
        if response.status_code == 200:
            test_data = response.json()
            preserved = test_data['narrative_preserved']
            status = "✅ PRESERVED" if preserved else "❌ CORRUPTED"
            
            print(f"   {error_rate*100:0.1f}% Error Rate: {status}")
            print(f"      Decode Time: {test_data['performance_metrics']['decode_time_ms']:.2f}ms")
            
            if not preserved:
                print(f"      Original: {test_data['original_narrative'][:50]}...")
                print(f"      Corrupted: {test_data['recovered_narrative'][:50]}...")
        else:
            print(f"   {error_rate*100:0.1f}% Error Rate: ❌ API ERROR")
    
    # Test 6: Performance Summary
    print("\n## Test 6: Performance Summary")
    
    response = requests.get(f"{BASE_URL}/qdpi/ecc/performance")
    
    if response.status_code == 200:
        perf_data = response.json()
        print(f"✅ Performance Summary:")
        print(f"   System Status: {perf_data['system_status']}")
        print(f"   Messages Processed: {perf_data['total_messages_processed']}")
        
        meets_specs = perf_data['meets_specifications']
        print(f"   Meets Decode Target: {'✅ YES' if meets_specs['decode_time_target'] else '❌ NO'}")
        print(f"   Error Correction: {meets_specs['error_correction_capacity']}")
        print(f"   Protection Overhead: {meets_specs['protection_overhead']}")
        
    else:
        print(f"❌ Performance Summary Failed: {response.status_code}")
    
    print(f"\n{'='*60}")
    print("🎉 QDPI Error Correction API Integration Complete!")
    print("The bulletproof narrative preservation system is now available via REST API.")

def test_complex_narrative():
    """Test encoding and decoding of a complex multi-step narrative"""
    
    print(f"\n{'='*60}")
    print("📚 Complex Narrative API Test")
    print(f"{'='*60}")
    
    # Complex system startup narrative
    complex_narrative = {
        "description": "Complete system startup with AI coordination and monitoring",
        "symbol_sequence": [
            {"symbol_name": "The_Author", "rotation": 90},
            {"symbol_name": "SYNCHRONIZE", "rotation": 270},
            {"symbol_name": "oren_progresso", "rotation": 270},
            {"symbol_name": "arieol_owlist", "rotation": 90},
            {"symbol_name": "OBSERVE", "rotation": 0},
            {"symbol_name": "princhetta", "rotation": 90},
            {"symbol_name": "TRANSFORM", "rotation": 270},
            {"symbol_name": "phillip_bafflemint", "rotation": 270}
        ]
    }
    
    print(f"**Complex Narrative**: {complex_narrative['description']}")
    print(f"**Sequence Length**: {len(complex_narrative['symbol_sequence'])} symbols")
    
    # Encode
    response = requests.post(f"{BASE_URL}/qdpi/ecc/encode", json=complex_narrative)
    
    if response.status_code == 200:
        encode_data = response.json()
        print(f"✅ Complex Encoding Success:")
        print(f"   Narrative: {encode_data['narrative_meaning']}")
        print(f"   Encoding Time: {encode_data['encoding_time_ms']:.2f}ms")
        
        # Test extreme error rate
        extreme_test = {
            "block_id": encode_data['block_id'],
            "error_rate": 0.025  # 2.5% - very high error rate
        }
        
        response = requests.post(f"{BASE_URL}/qdpi/ecc/test-transmission", json=extreme_test)
        
        if response.status_code == 200:
            test_data = response.json()
            preserved = test_data['narrative_preserved']
            
            print(f"\n**Extreme Error Test (2.5% corruption)**:")
            print(f"   Result: {'✅ NARRATIVE SURVIVED' if preserved else '❌ NARRATIVE CORRUPTED'}")
            
            if preserved:
                print(f"   Impact: ✅ Complete 8-step system startup preserved")
            else:
                print(f"   Impact: ❌ System startup would fail")
                
        else:
            print(f"❌ Extreme test failed: {response.status_code}")
            
    else:
        print(f"❌ Complex encoding failed: {response.status_code}")

if __name__ == "__main__":
    test_api_endpoints()
    test_complex_narrative()