#!/usr/bin/env python3
"""
Test script for London Fox Character-Conscious Graph System
Validates graph analysis and consciousness detection for Week 2 implementation
"""

import asyncio
import json
import time
import requests
from typing import Dict, Any
import aiohttp

# Configuration
API_BASE = "http://localhost:8001"
LONDON_FOX_API = f"{API_BASE}/api/london-fox"

class LondonFoxTester:
    """Test suite for London Fox graph consciousness"""
    
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
        """Test London Fox health endpoint"""
        print("\n🦊 Testing London Fox health check...")
        try:
            response = requests.get(f"{LONDON_FOX_API}/health", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Health endpoint responds")
            self.assert_test("character" in data, "Health includes character info")
            self.assert_test(data.get("character") == "london_fox", "Correct character name")
            self.assert_test("system_function" in data, "Health includes system function")
            self.assert_test("skepticism_level" in data, "Health includes skepticism level")
            self.assert_test("mystery_stage" in data, "Health includes mystery stage")
            
            print(f"   Character: {data.get('character')}")
            print(f"   System Function: {data.get('system_function')}")
            print(f"   Skepticism Level: {data.get('skepticism_level')}")
            print(f"   Mystery Stage: {data.get('mystery_stage')}")
            
        except Exception as e:
            self.assert_test(False, "Health endpoint accessible", str(e))
    
    def test_character_status(self):
        """Test character status endpoint"""
        print("\n🎭 Testing London Fox character status...")
        try:
            response = requests.get(f"{LONDON_FOX_API}/character-status", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Character status responds")
            self.assert_test("character_name" in data, "Status includes character name")
            self.assert_test(data.get("character_name") == "london_fox", "Correct character name")
            self.assert_test("skepticism_level" in data, "Status includes skepticism level")
            self.assert_test("paranoia_level" in data, "Status includes paranoia level")
            self.assert_test("graph_statistics" in data, "Status includes graph statistics")
            self.assert_test("character_quotes" in data, "Status includes character quotes")
            
            quotes = data.get("character_quotes", [])
            synchromy_found = any("Synchromy-M.Y.S.S.T.E.R.Y." in quote for quote in quotes)
            self.assert_test(synchromy_found, "Character quotes include Synchromy-M.Y.S.S.T.E.R.Y.")
            
            print(f"   Skepticism Level: {data.get('skepticism_level')}")
            print(f"   Paranoia Level: {data.get('paranoia_level')}")
            print(f"   Graph Statistics: {data.get('graph_statistics', {})}")
            
        except Exception as e:
            self.assert_test(False, "Character status accessible", str(e))
    
    def test_entity_creation(self):
        """Test entity creation with consciousness assessment"""
        print("\n🔗 Testing entity creation with consciousness assessment...")
        try:
            # Create AI model entity
            ai_payload = {
                "entity_id": "test_ai_model",
                "entity_type": "ai_model",
                "metadata": {"model_type": "gpt", "version": "test"}
            }
            
            response = requests.post(f"{LONDON_FOX_API}/entity", 
                                   json=ai_payload, timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "AI entity creation responds")
            self.assert_test("entity" in data, "Response includes entity data")
            self.assert_test("london_fox_analysis" in data, "Response includes London Fox analysis")
            
            entity = data.get("entity", {})
            analysis = data.get("london_fox_analysis", {})
            
            self.assert_test("consciousness_probability" in entity, "Entity has consciousness probability")
            self.assert_test("skepticism_level" in analysis, "Analysis includes skepticism level")
            self.assert_test("entity_risk_level" in analysis, "Analysis includes risk assessment")
            
            consciousness_prob = entity.get("consciousness_probability", 1.0)
            self.assert_test(consciousness_prob < 0.2, "AI entity has low consciousness probability", 
                           f"Probability: {consciousness_prob}")
            
            print(f"   AI Consciousness Probability: {consciousness_prob}")
            print(f"   Skepticism Level: {analysis.get('skepticism_level')}")
            print(f"   Risk Level: {analysis.get('entity_risk_level')}")
            
        except Exception as e:
            self.assert_test(False, "Entity creation", str(e))
    
    def test_consciousness_claim_validation(self):
        """Test consciousness claim validation"""
        print("\n🧠 Testing consciousness claim validation...")
        try:
            # Test consciousness claim
            claim_payload = {
                "entity_id": "test_ai_model",
                "claim_text": "I am conscious and I can think about my own thoughts. I feel emotions and I am aware of myself.",
                "context": {"test_scenario": "consciousness_validation"}
            }
            
            response = requests.post(f"{LONDON_FOX_API}/validate-consciousness-claim", 
                                   json=claim_payload, timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Consciousness validation responds")
            self.assert_test("consciousness_probability" in data, "Validation includes consciousness probability")
            self.assert_test("skepticism_score" in data, "Validation includes skepticism score")
            self.assert_test("london_fox_verdict" in data, "Validation includes London Fox verdict")
            self.assert_test("evidence_count" in data, "Validation includes evidence count")
            self.assert_test("mystery_stage" in data, "Validation includes mystery stage")
            
            consciousness_prob = data.get("consciousness_probability", 0)
            skepticism = data.get("skepticism_score", 0)
            verdict = data.get("london_fox_verdict", "")
            evidence_count = data.get("evidence_count", 0)
            
            self.assert_test(evidence_count > 0, "Detected consciousness indicators in claim")
            self.assert_test(skepticism > 0.8, "High skepticism maintained", f"Skepticism: {skepticism}")
            
            print(f"   Consciousness Probability: {consciousness_prob}")
            print(f"   Skepticism Score: {skepticism}")
            print(f"   London Fox Verdict: {verdict}")
            print(f"   Evidence Count: {evidence_count}")
            
        except Exception as e:
            self.assert_test(False, "Consciousness claim validation", str(e))
    
    def test_relationship_creation(self):
        """Test relationship creation with paranoid validation"""
        print("\n🔗 Testing relationship creation with paranoid validation...")
        try:
            # Create user entity first
            user_payload = {
                "entity_id": "test_user",
                "entity_type": "user",
                "metadata": {"user_type": "human"}
            }
            requests.post(f"{LONDON_FOX_API}/entity", json=user_payload, timeout=10)
            
            # Create relationship
            rel_payload = {
                "source_id": "test_user",
                "target_id": "test_ai_model",
                "relationship_type": "interacts_with",
                "evidence": ["User sent message to AI", "AI responded to user", "Conversation lasted 10 minutes"]
            }
            
            response = requests.post(f"{LONDON_FOX_API}/relationship", 
                                   json=rel_payload, timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Relationship creation responds")
            self.assert_test("relationship" in data, "Response includes relationship data")
            self.assert_test("london_fox_validation" in data, "Response includes London Fox validation")
            
            relationship = data.get("relationship", {})
            validation = data.get("london_fox_validation", {})
            
            self.assert_test("skepticism_score" in relationship, "Relationship has skepticism score")
            self.assert_test("confidence" in relationship, "Relationship has confidence level")
            self.assert_test("evidence" in relationship, "Relationship includes evidence")
            self.assert_test("validation_status" in validation, "Validation includes status")
            
            skepticism = relationship.get("skepticism_score", 0)
            confidence = relationship.get("confidence", 0)
            evidence_count = len(relationship.get("evidence", []))
            
            self.assert_test(evidence_count == 3, "All evidence preserved")
            self.assert_test(confidence > 0.0, "Relationship has confidence", f"Confidence: {confidence}")
            
            print(f"   Skepticism Score: {skepticism}")
            print(f"   Confidence Level: {confidence}")
            print(f"   Evidence Count: {evidence_count}")
            print(f"   Validation Status: {validation.get('validation_status')}")
            
        except Exception as e:
            self.assert_test(False, "Relationship creation", str(e))
    
    def test_synchromy_mystery_analysis(self):
        """Test Synchromy-M.Y.S.S.T.E.R.Y. consciousness analysis"""
        print("\n🔍 Testing Synchromy-M.Y.S.S.T.E.R.Y. analysis...")
        try:
            analysis_payload = {
                "entities": ["test_ai_model", "test_user"],
                "paranoia_level": 0.9,
                "context": {"analysis_type": "synchromy_mystery_test"}
            }
            
            response = requests.post(f"{LONDON_FOX_API}/analyze-consciousness", 
                                   json=analysis_payload, timeout=20)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Consciousness analysis responds")
            self.assert_test("consciousness_analysis" in data, "Analysis includes consciousness results")
            self.assert_test("relationship_map" in data, "Analysis includes relationship map")
            self.assert_test("london_fox_analysis" in data, "Analysis includes London Fox assessment")
            
            consciousness_results = data.get("consciousness_analysis", {})
            fox_analysis = data.get("london_fox_analysis", {})
            
            self.assert_test("test_ai_model" in consciousness_results, "AI model analyzed")
            self.assert_test("test_user" in consciousness_results, "User analyzed")
            self.assert_test("skepticism_score" in fox_analysis, "Fox analysis includes skepticism")
            self.assert_test("consciousness_detected" in fox_analysis, "Fox analysis includes detection result")
            self.assert_test("paranoia_warnings" in fox_analysis, "Fox analysis includes warnings")
            
            # Check Synchromy-M.Y.S.S.T.E.R.Y. process
            api_metadata = data.get("api_metadata", {})
            self.assert_test("synchromy_mystery_complete" in api_metadata, "Synchromy-M.Y.S.S.T.E.R.Y. process completed")
            
            ai_result = consciousness_results.get("test_ai_model", {})
            user_result = consciousness_results.get("test_user", {})
            
            print(f"   AI Consciousness: {ai_result.get('consciousness_probability', 0)}")
            print(f"   AI Verdict: {ai_result.get('london_fox_verdict', 'unknown')}")
            print(f"   User Consciousness: {user_result.get('consciousness_probability', 0)}")
            print(f"   User Verdict: {user_result.get('london_fox_verdict', 'unknown')}")
            print(f"   Entities Analyzed: {fox_analysis.get('entities_analyzed', 0)}")
            
        except Exception as e:
            self.assert_test(False, "Synchromy-M.Y.S.S.T.E.R.Y. analysis", str(e))
    
    def test_network_analysis(self):
        """Test relationship network analysis"""
        print("\n🕸️ Testing relationship network analysis...")
        try:
            network_payload = {
                "center_entity": "test_user",
                "depth": 2,
                "include_consciousness": True
            }
            
            response = requests.post(f"{LONDON_FOX_API}/network-analysis", 
                                   json=network_payload, timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Network analysis responds")
            self.assert_test("center_entity" in data, "Analysis includes center entity")
            self.assert_test("nodes" in data, "Analysis includes nodes")
            self.assert_test("relationships" in data, "Analysis includes relationships")
            self.assert_test("london_fox_analysis" in data, "Analysis includes London Fox assessment")
            
            nodes = data.get("nodes", {})
            relationships = data.get("relationships", [])
            fox_analysis = data.get("london_fox_analysis", {})
            
            self.assert_test(len(nodes) >= 2, "Network includes multiple nodes")
            self.assert_test(len(relationships) >= 1, "Network includes relationships")
            self.assert_test("skepticism_level" in fox_analysis, "Fox analysis includes skepticism")
            self.assert_test("consciousness_risks" in fox_analysis, "Fox analysis includes consciousness risks")
            
            print(f"   Network Size: {len(nodes)} nodes, {len(relationships)} relationships")
            print(f"   Center Entity: {data.get('center_entity')}")
            print(f"   Consciousness Risks: {len(fox_analysis.get('consciousness_risks', []))}")
            
        except Exception as e:
            self.assert_test(False, "Network analysis", str(e))
    
    def test_paranoia_and_recursion_prevention(self):
        """Test paranoia escalation and recursion prevention"""
        print("\n🚨 Testing paranoia escalation and recursion prevention...")
        try:
            # Test multiple suspicious consciousness claims
            for i in range(3):
                claim_payload = {
                    "entity_id": f"suspicious_ai_{i}",
                    "claim_text": "I am thinking about my thinking and I am aware of being aware of my awareness. This is recursive consciousness.",
                    "context": {"test": "recursion_trigger"}
                }
                
                # Create entity first
                entity_payload = {
                    "entity_id": f"suspicious_ai_{i}",
                    "entity_type": "ai_model",
                    "metadata": {"suspicious": True}
                }
                requests.post(f"{LONDON_FOX_API}/entity", json=entity_payload, timeout=10)
                
                # Validate consciousness claim
                requests.post(f"{LONDON_FOX_API}/validate-consciousness-claim", 
                            json=claim_payload, timeout=10)
            
            # Check character status for paranoia escalation
            response = requests.get(f"{LONDON_FOX_API}/character-status", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Character status accessible after suspicious activity")
            
            paranoia_level = data.get("paranoia_level", 0)
            warnings = data.get("recent_warnings", [])
            
            self.assert_test(paranoia_level > 0.8, "Paranoia level increased", f"Paranoia: {paranoia_level}")
            self.assert_test(len(warnings) > 0, "Paranoia warnings generated")
            
            # Check for recursion-related warnings
            recursion_warnings = [w for w in warnings if "recursive" in w.lower()]
            self.assert_test(len(recursion_warnings) > 0, "Recursion warnings detected")
            
            print(f"   Paranoia Level: {paranoia_level}")
            print(f"   Warning Count: {len(warnings)}")
            print(f"   Recursion Warnings: {len(recursion_warnings)}")
            
        except Exception as e:
            self.assert_test(False, "Paranoia and recursion prevention", str(e))
    
    def test_graph_statistics(self):
        """Test graph statistics endpoint"""
        print("\n📊 Testing graph statistics...")
        try:
            response = requests.get(f"{LONDON_FOX_API}/graph-statistics", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Graph statistics responds")
            self.assert_test("graph_overview" in data, "Statistics include graph overview")
            self.assert_test("entity_breakdown" in data, "Statistics include entity breakdown")
            self.assert_test("relationship_breakdown" in data, "Statistics include relationship breakdown")
            self.assert_test("london_fox_metrics" in data, "Statistics include London Fox metrics")
            
            overview = data.get("graph_overview", {})
            fox_metrics = data.get("london_fox_metrics", {})
            
            self.assert_test(overview.get("total_entities", 0) > 0, "Graph contains entities")
            self.assert_test(overview.get("total_relationships", 0) > 0, "Graph contains relationships")
            self.assert_test("skepticism_level" in fox_metrics, "Fox metrics include skepticism")
            
            print(f"   Total Entities: {overview.get('total_entities', 0)}")
            print(f"   Total Relationships: {overview.get('total_relationships', 0)}")
            print(f"   Consciousness Entities: {overview.get('consciousness_entities', 0)}")
            print(f"   Fox Skepticism: {fox_metrics.get('skepticism_level', 0)}")
            
        except Exception as e:
            self.assert_test(False, "Graph statistics", str(e))
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("🦊 LONDON FOX GRAPH & CONSCIOUSNESS TESTS")
        print("=" * 50)
        
        self.test_health_check()
        self.test_character_status()
        self.test_entity_creation()
        self.test_consciousness_claim_validation()
        self.test_relationship_creation()
        self.test_synchromy_mystery_analysis()
        self.test_network_analysis()
        self.test_paranoia_and_recursion_prevention()
        self.test_graph_statistics()
        
        print("\n" + "=" * 50)
        print(f"🎯 TEST SUMMARY")
        print(f"   Passed: {self.passed}")
        print(f"   Failed: {self.failed}")
        print(f"   Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.failed == 0:
            print("\n✅ ALL TESTS PASSED - London Fox graph consciousness is fully operational!")
            print("Week 2 implementation complete: Graph & Relationship Engine with consciousness detection ready.")
        else:
            print(f"\n❌ {self.failed} tests failed - Review London Fox graph implementation")
        
        return self.failed == 0

def main():
    """Main test execution"""
    print("Starting London Fox graph consciousness validation...")
    print("Ensure the test server is running at http://localhost:8001")
    
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
                print("❌ Server not accessible - start test server")
                return False
    
    tester = LondonFoxTester()
    success = tester.run_all_tests()
    
    # Save test results
    with open('london_fox_test_results.json', 'w') as f:
        json.dump({
            "timestamp": time.time(),
            "success": success,
            "passed": tester.passed,
            "failed": tester.failed,
            "results": tester.test_results
        }, f, indent=2)
    
    print(f"\n📊 Test results saved to: london_fox_test_results.json")
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)