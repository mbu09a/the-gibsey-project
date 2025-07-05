#!/usr/bin/env python3
"""
Test script for Jacklyn Variance Character-Conscious Database System
Validates surveillance analysis and D.A.D.D.Y.S-H.A.R.D reporting for Week 3 implementation
"""

import asyncio
import json
import time
import requests
from typing import Dict, Any
import aiohttp

# Configuration
API_BASE = "http://localhost:8001"
JACKLYN_API = f"{API_BASE}/api/jacklyn-variance"

class JacklynVarianceTester:
    """Test suite for Jacklyn Variance surveillance database"""
    
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
        """Test Jacklyn Variance health endpoint"""
        print("\n📊 Testing Jacklyn Variance health check...")
        try:
            response = requests.get(f"{JACKLYN_API}/health", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Health endpoint responds")
            self.assert_test("character" in data, "Health includes character info")
            self.assert_test(data.get("character") == "jacklyn_variance", "Correct character name")
            self.assert_test("system_function" in data, "Health includes system function")
            self.assert_test("surveillance_mode" in data, "Health includes surveillance mode")
            self.assert_test("daddys_hard_active" in data, "Health includes D.A.D.D.Y.S-H.A.R.D status")
            
            print(f"   Character: {data.get('character')}")
            print(f"   System Function: {data.get('system_function')}")
            print(f"   Surveillance Mode: {data.get('surveillance_mode')}")
            print(f"   D.A.D.D.Y.S-H.A.R.D Active: {data.get('daddys_hard_active')}")
            
        except Exception as e:
            self.assert_test(False, "Health endpoint accessible", str(e))
    
    def test_character_status(self):
        """Test character status endpoint"""
        print("\n🎭 Testing Jacklyn Variance character status...")
        try:
            response = requests.get(f"{JACKLYN_API}/character-status", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Character status responds")
            self.assert_test("character_name" in data, "Status includes character name")
            self.assert_test(data.get("character_name") == "jacklyn_variance", "Correct character name")
            self.assert_test("analytical_state" in data, "Status includes analytical state")
            self.assert_test("surveillance_metrics" in data, "Status includes surveillance metrics")
            self.assert_test("bias_disclosure" in data, "Status includes bias disclosure")
            
            analytical_state = data.get("analytical_state", {})
            surveillance_metrics = data.get("surveillance_metrics", {})
            
            self.assert_test("current_pass" in analytical_state, "Analytical state includes current pass")
            self.assert_test("operating_mode" in analytical_state, "Analytical state includes operating mode")
            self.assert_test("surveillance_mode" in surveillance_metrics, "Surveillance metrics include mode")
            
            print(f"   Current Pass: {analytical_state.get('current_pass')}")
            print(f"   Operating Mode: {analytical_state.get('operating_mode')}")
            print(f"   Surveillance Mode: {surveillance_metrics.get('surveillance_mode')}")
            print(f"   Draft Count: {analytical_state.get('draft_count')}")
            
        except Exception as e:
            self.assert_test(False, "Character status accessible", str(e))
    
    def test_database_query_with_surveillance(self):
        """Test database query execution with surveillance analysis"""
        print("\n🔍 Testing database query with surveillance analysis...")
        try:
            # Test SELECT query
            query_payload = {
                "query_type": "select",
                "table_name": "test_sessions",
                "query_data": {"limit": 10, "where": "status = 'active'"},
                "analysis_context": {"test_scenario": "surveillance_validation"}
            }
            
            response = requests.post(f"{JACKLYN_API}/database/query", 
                                   json=query_payload, timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Database query responds")
            self.assert_test("data" in data, "Response includes query data")
            self.assert_test("jacklyn_analysis" in data, "Response includes Jacklyn analysis")
            self.assert_test("query_metadata" in data, "Response includes query metadata")
            
            jacklyn_analysis = data.get("jacklyn_analysis", {})
            query_metadata = data.get("query_metadata", {})
            
            self.assert_test("surveillance_notes" in jacklyn_analysis, "Analysis includes surveillance notes")
            self.assert_test("currently_under_analysis" in jacklyn_analysis, "Analysis includes current status")
            self.assert_test("investigative_priority" in jacklyn_analysis, "Analysis includes priority")
            self.assert_test("analyst" in query_metadata, "Metadata includes analyst info")
            
            print(f"   Query ID: {query_metadata.get('query_id')}")
            print(f"   Surveillance Notes: {jacklyn_analysis.get('surveillance_notes', '')[:100]}...")
            print(f"   Priority: {jacklyn_analysis.get('investigative_priority')}")
            print(f"   Currently Under Analysis: {jacklyn_analysis.get('currently_under_analysis')}")
            
        except Exception as e:
            self.assert_test(False, "Database query with surveillance", str(e))
    
    def test_table_query_with_analysis(self):
        """Test optimized table query with analysis"""
        print("\n📋 Testing table query with analysis...")
        try:
            # Test table-specific query
            response = requests.get(f"{JACKLYN_API}/database/query/user_sessions?limit=5&include_analysis=true", 
                                  timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Table query responds")
            self.assert_test("data" in data, "Response includes data")
            self.assert_test("jacklyn_analysis" in data, "Response includes analysis")
            
            # Test without analysis
            response_no_analysis = requests.get(f"{JACKLYN_API}/database/query/user_sessions?limit=5&include_analysis=false", 
                                              timeout=15)
            data_no_analysis = response_no_analysis.json()
            
            self.assert_test("jacklyn_analysis" not in data_no_analysis, "Analysis excluded when requested")
            self.assert_test("data" in data_no_analysis, "Data still included without analysis")
            
            print(f"   Table Query Successful")
            print(f"   Analysis Toggle Working")
            
        except Exception as e:
            self.assert_test(False, "Table query with analysis", str(e))
    
    def test_daddys_hard_report_generation(self):
        """Test D.A.D.D.Y.S-H.A.R.D report generation"""
        print("\n📊 Testing D.A.D.D.Y.S-H.A.R.D report generation...")
        try:
            # Generate comprehensive report
            report_payload = {
                "report_type": "daily",
                "analysis_period_days": 1,
                "include_anomalies": True,
                "investigative_focus": "pattern_analysis_validation"
            }
            
            response = requests.post(f"{JACKLYN_API}/reports/daddys-hard", 
                                   json=report_payload, timeout=20)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "D.A.D.D.Y.S-H.A.R.D report generates")
            self.assert_test("report" in data, "Response includes report data")
            self.assert_test("jacklyn_analysis" in data, "Response includes Jacklyn analysis")
            
            report = data.get("report", {})
            jacklyn_analysis = data.get("jacklyn_analysis", {})
            
            # Validate D.A.D.D.Y.S-H.A.R.D components
            self.assert_test("data_summary" in report, "Report includes Data summary")
            self.assert_test("anomaly_detection" in report, "Report includes Anomaly detection")
            self.assert_test("database_health" in report, "Report includes Database health")
            self.assert_test("detection_alerts" in report, "Report includes Detection alerts")
            self.assert_test("yearly_trends" in report, "Report includes Yearly trends")
            self.assert_test("surveillance_notes" in report, "Report includes Surveillance notes")
            self.assert_test("hierarchical_analysis" in report, "Report includes Hierarchical analysis")
            self.assert_test("access_patterns" in report, "Report includes Access patterns")
            self.assert_test("recommendations" in report, "Report includes Recommendations")
            self.assert_test("documentation_metadata" in report, "Report includes Documentation metadata")
            
            # Validate Jacklyn-specific components
            self.assert_test("analyst_notes" in report, "Report includes analyst notes")
            self.assert_test("bias_disclosures" in report, "Report includes bias disclosures")
            self.assert_test("draft_number" in report, "Report includes draft number")
            
            report_id = report.get("report_id")
            print(f"   Report ID: {report_id}")
            print(f"   Report Type: {report.get('report_type')}")
            print(f"   Data Summary: {len(report.get('data_summary', {}))} components")
            print(f"   Surveillance Notes: {len(report.get('surveillance_notes', []))} notes")
            print(f"   Recommendations: {len(report.get('recommendations', []))} items")
            
        except Exception as e:
            self.assert_test(False, "D.A.D.D.Y.S-H.A.R.D report generation", str(e))
    
    def test_surveillance_analysis(self):
        """Test comprehensive surveillance analysis"""
        print("\n🕵️ Testing surveillance analysis...")
        try:
            # Perform surveillance analysis
            analysis_payload = {
                "target_table": "test_sessions",
                "time_period_hours": 24,
                "anomaly_threshold": 0.5,
                "include_patterns": True
            }
            
            response = requests.post(f"{JACKLYN_API}/surveillance/analyze", 
                                   json=analysis_payload, timeout=20)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Surveillance analysis responds")
            self.assert_test("surveillance_analysis" in data, "Response includes surveillance analysis")
            self.assert_test("jacklyn_assessment" in data, "Response includes Jacklyn assessment")
            self.assert_test("analysis_metadata" in data, "Response includes analysis metadata")
            
            surveillance_analysis = data.get("surveillance_analysis", {})
            jacklyn_assessment = data.get("jacklyn_assessment", {})
            
            self.assert_test("total_queries_analyzed" in surveillance_analysis, "Analysis includes query count")
            self.assert_test("anomaly_summary" in surveillance_analysis, "Analysis includes anomaly summary")
            self.assert_test("access_patterns" in surveillance_analysis, "Analysis includes access patterns")
            self.assert_test("investigative_alerts" in surveillance_analysis, "Analysis includes alerts")
            
            self.assert_test("operating_mode" in jacklyn_assessment, "Assessment includes operating mode")
            self.assert_test("surveillance_confidence" in jacklyn_assessment, "Assessment includes confidence")
            self.assert_test("pattern_assessment" in jacklyn_assessment, "Assessment includes pattern analysis")
            self.assert_test("recommended_actions" in jacklyn_assessment, "Assessment includes recommendations")
            
            print(f"   Queries Analyzed: {surveillance_analysis.get('total_queries_analyzed')}")
            print(f"   Anomalies Detected: {surveillance_analysis.get('anomaly_summary', {}).get('total_anomalies_detected')}")
            print(f"   Surveillance Confidence: {jacklyn_assessment.get('surveillance_confidence')}")
            print(f"   Pattern Assessment: {jacklyn_assessment.get('pattern_assessment', '')[:100]}...")
            
        except Exception as e:
            self.assert_test(False, "Surveillance analysis", str(e))
    
    def test_bias_disclosure_analysis(self):
        """Test bias disclosure and objectivity assessment"""
        print("\n🎯 Testing bias disclosure analysis...")
        try:
            # Test bias disclosure
            bias_payload = {
                "analysis_context": "Testing analytical objectivity and bias assessment for surveillance operations",
                "objectivity_target": 0.8
            }
            
            response = requests.post(f"{JACKLYN_API}/bias/disclose", 
                                   json=bias_payload, timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Bias disclosure responds")
            self.assert_test("bias_disclosure" in data, "Response includes bias disclosure")
            self.assert_test("jacklyn_statement" in data, "Response includes Jacklyn statement")
            self.assert_test("objectivity_assessment" in data, "Response includes objectivity assessment")
            
            bias_disclosure = data.get("bias_disclosure", {})
            jacklyn_statement = data.get("jacklyn_statement", "")
            objectivity_assessment = data.get("objectivity_assessment", {})
            
            self.assert_test("disclosed_biases" in bias_disclosure, "Disclosure includes biases")
            self.assert_test("objectivity_confidence" in bias_disclosure, "Disclosure includes confidence")
            self.assert_test("analytical_transparency" in bias_disclosure, "Disclosure includes transparency")
            self.assert_test("bias_mitigation_strategies" in bias_disclosure, "Disclosure includes strategies")
            
            self.assert_test("meets_target" in objectivity_assessment, "Assessment includes target status")
            self.assert_test("recommended_confidence_level" in objectivity_assessment, "Assessment includes recommendations")
            
            # Check for Jacklyn's characteristic phrases
            self.assert_test("glasses" in jacklyn_statement, "Statement includes Jacklyn's characteristic behavior")
            self.assert_test("Bias disclosed" in jacklyn_statement, "Statement includes proper disclosure language")
            
            disclosed_biases = bias_disclosure.get("disclosed_biases", [])
            objectivity_confidence = bias_disclosure.get("objectivity_confidence", 0)
            
            print(f"   Disclosed Biases: {len(disclosed_biases)} biases")
            print(f"   Objectivity Confidence: {objectivity_confidence:.2f}")
            print(f"   Meets Target: {objectivity_assessment.get('meets_target')}")
            print(f"   Mitigation Strategies: {len(bias_disclosure.get('bias_mitigation_strategies', []))} strategies")
            
        except Exception as e:
            self.assert_test(False, "Bias disclosure analysis", str(e))
    
    def test_anomaly_detection_patterns(self):
        """Test anomaly detection with suspicious patterns"""
        print("\n🚨 Testing anomaly detection patterns...")
        try:
            # Generate queries that should trigger anomalies
            
            # 1. Off-hours access (simulate by context)
            off_hours_payload = {
                "query_type": "select",
                "table_name": "sensitive_data",
                "query_data": {"time_context": "03:00_AM", "bulk_operation": True},
                "analysis_context": {"simulated_off_hours": True}
            }
            
            response1 = requests.post(f"{JACKLYN_API}/database/query", 
                                    json=off_hours_payload, timeout=15)
            data1 = response1.json()
            
            # 2. Bulk operations
            bulk_payload = {
                "query_type": "bulk_delete", 
                "table_name": "user_data",
                "query_data": {"records": list(range(1000)), "massive_operation": True},
                "analysis_context": {"bulk_test": True}
            }
            
            response2 = requests.post(f"{JACKLYN_API}/database/query", 
                                    json=bulk_payload, timeout=15)
            data2 = response2.json()
            
            # 3. Preston-related query (should trigger special priority)
            preston_payload = {
                "query_type": "select",
                "table_name": "preston_data",
                "query_data": {"search": "missing researcher patterns"},
                "analysis_context": {"preston_investigation": True}
            }
            
            response3 = requests.post(f"{JACKLYN_API}/database/query", 
                                    json=preston_payload, timeout=15)
            data3 = response3.json()
            
            # Check all queries responded
            self.assert_test(response1.status_code == 200, "Off-hours query responds")
            self.assert_test(response2.status_code == 200, "Bulk operation query responds")
            self.assert_test(response3.status_code == 200, "Preston-related query responds")
            
            # Check for anomaly detection
            analysis1 = data1.get("jacklyn_analysis", {})
            analysis2 = data2.get("jacklyn_analysis", {})
            analysis3 = data3.get("jacklyn_analysis", {})
            
            anomalies1 = analysis1.get("pattern_anomalies", [])
            anomalies2 = analysis2.get("pattern_anomalies", [])
            priority3 = analysis3.get("investigative_priority", "")
            
            self.assert_test(len(anomalies1) > 0 or len(anomalies2) > 0, "Anomalies detected in suspicious queries")
            self.assert_test("bulk_operations" in str(anomalies2), "Bulk operation anomaly detected")
            self.assert_test("preston" in priority3.lower() or "high" in priority3.lower(), "Preston query gets special priority")
            
            print(f"   Off-hours Anomalies: {len(anomalies1)} detected")
            print(f"   Bulk Operation Anomalies: {len(anomalies2)} detected")
            print(f"   Preston Query Priority: {priority3}")
            
        except Exception as e:
            self.assert_test(False, "Anomaly detection patterns", str(e))
    
    def test_surveillance_history_tracking(self):
        """Test surveillance history and archival"""
        print("\n📚 Testing surveillance history tracking...")
        try:
            # Get surveillance history
            response = requests.get(f"{JACKLYN_API}/surveillance/history?limit=20&include_anomalies_only=false", 
                                  timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Surveillance history responds")
            self.assert_test("surveillance_history" in data, "Response includes history")
            self.assert_test("history_metadata" in data, "Response includes metadata")
            
            history = data.get("surveillance_history", [])
            metadata = data.get("history_metadata", {})
            
            self.assert_test(len(history) > 0, "History contains surveillance entries")
            self.assert_test("total_entries" in metadata, "Metadata includes total entries")
            self.assert_test("time_range" in metadata, "Metadata includes time range")
            self.assert_test("analyst" in metadata, "Metadata includes analyst info")
            
            # Check anomaly filtering
            response_anomalies = requests.get(f"{JACKLYN_API}/surveillance/history?limit=10&include_anomalies_only=true", 
                                            timeout=15)
            data_anomalies = response_anomalies.json()
            
            anomaly_history = data_anomalies.get("surveillance_history", [])
            
            # Verify anomaly entries have anomalies
            if anomaly_history:
                has_anomalies = all(len(entry.get("anomalies_detected", [])) > 0 for entry in anomaly_history)
                self.assert_test(has_anomalies, "Anomaly-only filter works correctly")
            
            print(f"   Total History Entries: {metadata.get('total_entries')}")
            print(f"   Anomaly Entries: {len(anomaly_history)}")
            print(f"   Time Range: {metadata.get('time_range', {}).get('earliest', 'N/A')} to {metadata.get('time_range', {}).get('latest', 'N/A')}")
            
        except Exception as e:
            self.assert_test(False, "Surveillance history tracking", str(e))
    
    def test_daddys_hard_report_retrieval(self):
        """Test D.A.D.D.Y.S-H.A.R.D report retrieval"""
        print("\n📋 Testing D.A.D.D.Y.S-H.A.R.D report retrieval...")
        try:
            # Get current date for report
            current_date = time.strftime("%Y-%m-%d")
            
            # Try to retrieve today's report (should exist after generation test)
            response = requests.get(f"{JACKLYN_API}/reports/daddys-hard/{current_date}", 
                                  timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                self.assert_test("report" in data, "Retrieved report contains data")
                self.assert_test("retrieval_metadata" in data, "Retrieved report contains metadata")
                
                report = data.get("report", {})
                self.assert_test("report_id" in report, "Report has valid ID")
                self.assert_test(current_date in report.get("report_id", ""), "Report ID matches date")
                
                print(f"   Report Retrieved: {report.get('report_id')}")
                print(f"   Report Type: {report.get('report_type')}")
            else:
                # Try to generate a report first
                report_payload = {"report_type": "daily", "analysis_period_days": 1}
                requests.post(f"{JACKLYN_API}/reports/daddys-hard", json=report_payload, timeout=15)
                
                # Then try retrieval again
                response = requests.get(f"{JACKLYN_API}/reports/daddys-hard/{current_date}", timeout=15)
                self.assert_test(response.status_code == 200, "Report retrieval after generation")
            
            # Test non-existent report
            response_404 = requests.get(f"{JACKLYN_API}/reports/daddys-hard/1999-01-01", timeout=10)
            self.assert_test(response_404.status_code == 404, "Non-existent report returns 404")
            
        except Exception as e:
            self.assert_test(False, "D.A.D.D.Y.S-H.A.R.D report retrieval", str(e))
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("📊 JACKLYN VARIANCE DATABASE & SURVEILLANCE TESTS")
        print("=" * 60)
        
        self.test_health_check()
        self.test_character_status()
        self.test_database_query_with_surveillance()
        self.test_table_query_with_analysis()
        self.test_daddys_hard_report_generation()
        self.test_surveillance_analysis()
        self.test_bias_disclosure_analysis()
        self.test_anomaly_detection_patterns()
        self.test_surveillance_history_tracking()
        self.test_daddys_hard_report_retrieval()
        
        print("\n" + "=" * 60)
        print(f"🎯 TEST SUMMARY")
        print(f"   Passed: {self.passed}")
        print(f"   Failed: {self.failed}")
        print(f"   Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.failed == 0:
            print("\n✅ ALL TESTS PASSED - Jacklyn Variance surveillance database is fully operational!")
            print("Week 3 implementation complete: Database Core & API Gateway with D.A.D.D.Y.S-H.A.R.D surveillance ready.")
        else:
            print(f"\n❌ {self.failed} tests failed - Review Jacklyn Variance database implementation")
        
        return self.failed == 0

def main():
    """Main test execution"""
    print("Starting Jacklyn Variance surveillance database validation...")
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
    
    tester = JacklynVarianceTester()
    success = tester.run_all_tests()
    
    # Save test results
    with open('jacklyn_variance_test_results.json', 'w') as f:
        json.dump({
            "timestamp": time.time(),
            "success": success,
            "passed": tester.passed,
            "failed": tester.failed,
            "results": tester.test_results
        }, f, indent=2)
    
    print(f"\n📊 Test results saved to: jacklyn_variance_test_results.json")
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)