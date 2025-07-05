#!/usr/bin/env python3
"""
Test script for Glyph Marrow Character-Conscious QDPI
Validates character consciousness features for Week 1 implementation
"""

import asyncio
import json
import time
import requests
from typing import Dict, Any
import aiohttp

# Configuration
API_BASE = "http://localhost:8000"
GLYPH_MARROW_API = f"{API_BASE}/api/glyph-marrow"

class GlyphMarrowTester:
    """Test suite for Glyph Marrow character consciousness"""
    
    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def assert_test(self, condition: bool, test_name: str, details: str = ""):
        """Assert a test condition and track results"""
        if condition:
            print(f"✅ PASS: {test_name}")
            self.test_results.append({"test": test_name, "status": "PASS", "details": details})
            self.passed += 1
        else:
            print(f"❌ FAIL: {test_name} - {details}")
            self.test_results.append({"test": test_name, "status": "FAIL", "details": details})
            self.failed += 1
    
    def test_health_check(self):
        """Test Glyph Marrow health endpoint"""
        print("\n🔍 Testing character health check...")
        try:
            response = requests.get(f"{GLYPH_MARROW_API}/health", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Health endpoint responds")
            self.assert_test("character" in data, "Health includes character info")
            self.assert_test(data.get("character") == "glyph_marrow", "Correct character name")
            self.assert_test("ailment_status" in data, "Health includes ailment status")
            self.assert_test("confusion_level" in data, "Health includes confusion level")
            
            print(f"   Character: {data.get('character')}")
            print(f"   Ailment Status: {data.get('ailment_status')}")
            print(f"   Confusion Level: {data.get('confusion_level')}")
            
        except Exception as e:
            self.assert_test(False, "Health endpoint accessible", str(e))
    
    def test_character_status(self):
        """Test character status endpoint"""
        print("\n🎭 Testing character status retrieval...")
        try:
            response = requests.get(f"{GLYPH_MARROW_API}/character-status", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Character status responds")
            self.assert_test("character_name" in data, "Status includes character name")
            self.assert_test(data.get("character_name") == "glyph_marrow", "Correct character name")
            self.assert_test("current_ailment" in data, "Status includes current ailment")
            self.assert_test("character_quotes" in data, "Status includes character quotes")
            self.assert_test("real_time_metrics" in data, "Status includes real-time metrics")
            
            ailment = data.get("current_ailment", {})
            self.assert_test("linguistic_vertigo" in ailment, "Ailment includes linguistic vertigo")
            self.assert_test("word_object_fusion" in ailment, "Ailment includes word-object fusion")
            self.assert_test("confusion_compass" in ailment, "Ailment includes confusion compass")
            
            print(f"   Linguistic Vertigo: {ailment.get('linguistic_vertigo')}")
            print(f"   Word-Object Fusion: {ailment.get('word_object_fusion')}")
            print(f"   Confusion Compass: {ailment.get('confusion_compass')}")
            
        except Exception as e:
            self.assert_test(False, "Character status accessible", str(e))
    
    def test_encoding_with_consciousness(self):
        """Test encoding with character consciousness"""
        print("\n🔤 Testing encoding with character consciousness...")
        try:
            test_data = "The word becomes the object in Glyph Marrow's perception"
            payload = {
                "data": test_data,
                "mode": "index",
                "trigger_confusion": False
            }
            
            response = requests.post(f"{GLYPH_MARROW_API}/encode", 
                                   json=payload, timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Encoding endpoint responds")
            self.assert_test("character" in data, "Encoding includes character info")
            self.assert_test("symbols" in data, "Encoding includes symbols")
            self.assert_test("character_processing" in data, "Encoding includes character processing")
            
            processing = data.get("character_processing", {})
            self.assert_test("linguistic_vertigo" in processing, "Processing includes linguistic vertigo")
            self.assert_test("ailment_state" in processing, "Processing includes ailment state")
            self.assert_test("confusion_compass" in processing, "Processing includes confusion compass")
            
            symbols = data.get("symbols", [])
            self.assert_test(len(symbols) > 0, "Encoding produces symbols")
            
            print(f"   Encoded {len(symbols)} symbols")
            print(f"   Confusion Compass: {processing.get('confusion_compass')}")
            
        except Exception as e:
            self.assert_test(False, "Encoding with consciousness", str(e))
    
    def test_confusion_episode(self):
        """Test confusion episode triggering"""
        print("\n🌀 Testing confusion episode trigger...")
        try:
            payload = {
                "trigger": "Testing linguistic vertigo enhancement",
                "intensity": 0.8
            }
            
            response = requests.post(f"{GLYPH_MARROW_API}/confusion-episode", 
                                   json=payload, timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Confusion episode endpoint responds")
            self.assert_test("confusion_episode" in data, "Response includes confusion episode")
            self.assert_test("character_response" in data, "Response includes character response")
            self.assert_test("updated_ailment" in data, "Response includes updated ailment")
            self.assert_test("processing_enhancement" in data, "Response includes processing enhancement")
            
            episode = data.get("confusion_episode", {})
            self.assert_test("compass_direction" in episode, "Episode includes compass direction")
            self.assert_test("peak_vertigo" in episode, "Episode includes peak vertigo")
            
            print(f"   Compass Direction: {episode.get('compass_direction')}")
            print(f"   Peak Vertigo: {episode.get('peak_vertigo')}")
            
        except Exception as e:
            self.assert_test(False, "Confusion episode trigger", str(e))
    
    def test_linguistic_vertigo_processing(self):
        """Test linguistic vertigo processing delays"""
        print("\n⏱️ Testing linguistic vertigo processing delays...")
        try:
            # Test encoding with confusion trigger
            test_data = "Complex data requiring linguistic processing with high confusion"
            payload = {
                "data": test_data,
                "mode": "index",
                "trigger_confusion": True
            }
            
            start_time = time.time()
            response = requests.post(f"{GLYPH_MARROW_API}/encode", 
                                   json=payload, timeout=20)
            processing_time = time.time() - start_time
            
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Vertigo processing completes")
            self.assert_test(processing_time > 1.0, "Processing includes realistic delays", 
                           f"Processing time: {processing_time:.2f}s")
            
            processing = data.get("character_processing", {})
            vertigo = processing.get("linguistic_vertigo", {})
            self.assert_test("confusion_level" in vertigo, "Vertigo includes confusion level")
            self.assert_test("processing_time" in vertigo, "Vertigo includes processing time")
            
            print(f"   Processing Time: {processing_time:.2f}s")
            print(f"   Confusion Level: {vertigo.get('confusion_level')}")
            print(f"   Vertigo Delay: {vertigo.get('vertigo_delay')}")
            
        except Exception as e:
            self.assert_test(False, "Linguistic vertigo processing", str(e))
    
    def test_fusion_history(self):
        """Test word-object fusion history tracking"""
        print("\n🔗 Testing word-object fusion history...")
        try:
            response = requests.get(f"{GLYPH_MARROW_API}/fusion-history?limit=5", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Fusion history endpoint responds")
            self.assert_test("character" in data, "History includes character info")
            self.assert_test("fusion_events" in data, "History includes fusion events")
            self.assert_test("total_events" in data, "History includes total events count")
            self.assert_test("fusion_statistics" in data, "History includes fusion statistics")
            
            events = data.get("fusion_events", [])
            if len(events) > 0:
                event = events[0]
                self.assert_test("word_perception" in event, "Event includes word perception")
                self.assert_test("fusion_intensity" in event, "Event includes fusion intensity")
                self.assert_test("fusion_description" in event, "Event includes fusion description")
                
                print(f"   Total Events: {data.get('total_events')}")
                print(f"   Recent Events: {len(events)}")
                if events:
                    print(f"   Latest Fusion: {event.get('fusion_description')}")
            
        except Exception as e:
            self.assert_test(False, "Fusion history tracking", str(e))
    
    def test_confusion_as_compass_enhancement(self):
        """Test confusion-as-compass encoding enhancement"""
        print("\n🧭 Testing confusion-as-compass enhancement...")
        try:
            test_data = "Data to encode with confusion enhancement"
            
            # Test without confusion trigger
            payload_low = {
                "data": test_data,
                "mode": "index", 
                "trigger_confusion": False
            }
            
            response_low = requests.post(f"{GLYPH_MARROW_API}/encode", 
                                       json=payload_low, timeout=15)
            data_low = response_low.json()
            
            # Test with confusion trigger
            payload_high = {
                "data": test_data,
                "mode": "index",
                "trigger_confusion": True
            }
            
            response_high = requests.post(f"{GLYPH_MARROW_API}/encode", 
                                        json=payload_high, timeout=15)
            data_high = response_high.json()
            
            self.assert_test(response_low.status_code == 200, "Low confusion encoding works")
            self.assert_test(response_high.status_code == 200, "High confusion encoding works")
            
            # Compare encoding confidence
            processing_low = data_low.get("character_processing", {})
            processing_high = data_high.get("character_processing", {})
            
            confidence_low = processing_low.get("encoding_confidence", 0)
            confidence_high = processing_high.get("encoding_confidence", 0)
            
            self.assert_test(confidence_high >= confidence_low, 
                           "Higher confusion improves encoding confidence",
                           f"Low: {confidence_low:.3f}, High: {confidence_high:.3f}")
            
            print(f"   Low Confusion Confidence: {confidence_low:.3f}")
            print(f"   High Confusion Confidence: {confidence_high:.3f}")
            
        except Exception as e:
            self.assert_test(False, "Confusion-as-compass enhancement", str(e))
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("🎭 GLYPH MARROW CHARACTER CONSCIOUSNESS TESTS")
        print("=" * 50)
        
        self.test_health_check()
        self.test_character_status()
        self.test_encoding_with_consciousness()
        self.test_confusion_episode()
        self.test_linguistic_vertigo_processing()
        self.test_fusion_history()
        self.test_confusion_as_compass_enhancement()
        
        print("\n" + "=" * 50)
        print(f"🎯 TEST SUMMARY")
        print(f"   Passed: {self.passed}")
        print(f"   Failed: {self.failed}")
        print(f"   Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.failed == 0:
            print("\n✅ ALL TESTS PASSED - Glyph Marrow consciousness is fully operational!")
            print("Week 1 implementation complete: Character-conscious QDPI ready for production.")
        else:
            print(f"\n❌ {self.failed} tests failed - Review character consciousness implementation")
        
        return self.failed == 0

def main():
    """Main test execution"""
    print("Starting Glyph Marrow character consciousness validation...")
    print("Ensure the backend server is running at http://localhost:8000")
    
    # Wait for server to be ready
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get(f"{API_BASE}/health", timeout=5)
            if response.status_code == 200:
                break
        except:
            if i < max_retries - 1:
                print(f"Waiting for server... (attempt {i+1}/{max_retries})")
                time.sleep(2)
            else:
                print("❌ Server not accessible - start backend with: cd backend && python main.py")
                return False
    
    tester = GlyphMarrowTester()
    success = tester.run_all_tests()
    
    # Save test results
    with open('glyph_marrow_test_results.json', 'w') as f:
        json.dump({
            "timestamp": time.time(),
            "success": success,
            "passed": tester.passed,
            "failed": tester.failed,
            "results": tester.test_results
        }, f, indent=2)
    
    print(f"\n📊 Test results saved to: glyph_marrow_test_results.json")
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)