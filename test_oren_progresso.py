#!/usr/bin/env python3
"""
Test script for Oren Progresso Executive Orchestration & Observability System
Validates CEO-level decision making, budget control, and civilization monitoring for Week 4 implementation
"""

import asyncio
import json
import time
import requests
from typing import Dict, Any
import aiohttp

# Configuration
API_BASE = "http://localhost:8001"
OREN_API = f"{API_BASE}/api/oren-progresso"

class OrenProgressoTester:
    """Test suite for Oren Progresso executive orchestration"""
    
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
        """Test Oren Progresso health endpoint"""
        print("\n🎩 Testing Oren Progresso health check...")
        try:
            response = requests.get(f"{OREN_API}/health", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Health endpoint responds")
            self.assert_test("character" in data, "Health includes character info")
            self.assert_test(data.get("character") == "oren_progresso", "Correct character name")
            self.assert_test("system_function" in data, "Health includes system function")
            self.assert_test("stress_level" in data, "Health includes stress level")
            self.assert_test("budget_authority" in data, "Health includes budget authority")
            self.assert_test("executive_override_active" in data, "Health includes executive override status")
            
            print(f"   Character: {data.get('character')}")
            print(f"   System Function: {data.get('system_function')}")
            print(f"   Stress Level: {data.get('stress_level')}")
            print(f"   Budget Authority: {data.get('budget_authority')}")
            print(f"   Executive Override: {data.get('executive_override_active')}")
            
        except Exception as e:
            self.assert_test(False, "Health endpoint accessible", str(e))
    
    def test_character_status(self):
        """Test character status endpoint"""
        print("\n🎭 Testing Oren Progresso character status...")
        try:
            response = requests.get(f"{OREN_API}/character-status", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Character status responds")
            self.assert_test("character_name" in data, "Status includes character name")
            self.assert_test(data.get("character_name") == "oren_progresso", "Correct character name")
            self.assert_test("executive_state" in data, "Status includes executive state")
            self.assert_test("financial_metrics" in data, "Status includes financial metrics")
            self.assert_test("civilization_oversight" in data, "Status includes civilization oversight")
            
            executive_state = data.get("executive_state", {})
            financial_metrics = data.get("financial_metrics", {})
            civilization_oversight = data.get("civilization_oversight", {})
            
            self.assert_test("title" in executive_state, "Executive state includes title")
            self.assert_test("stress_level" in executive_state, "Executive state includes stress level")
            self.assert_test("budget_saved_today" in financial_metrics, "Financial metrics include savings")
            self.assert_test("total_components" in civilization_oversight, "Oversight includes component count")
            
            print(f"   Executive Title: {executive_state.get('title')}")
            print(f"   Stress Level: {executive_state.get('stress_level')}")
            print(f"   Budget Saved Today: ${financial_metrics.get('budget_saved_today', 0):.2f}")
            print(f"   Total Components: {civilization_oversight.get('total_components')}")
            
        except Exception as e:
            self.assert_test(False, "Character status accessible", str(e))
    
    def test_executive_dashboard(self):
        """Test executive dashboard with civilization monitoring"""
        print("\n📊 Testing executive dashboard...")
        try:
            response = requests.get(f"{OREN_API}/dashboard", timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Executive dashboard responds")
            self.assert_test("character_name" in data, "Dashboard includes character name")
            self.assert_test("executive_title" in data, "Dashboard includes executive title")
            self.assert_test("current_status" in data, "Dashboard includes current status")
            self.assert_test("civilization_overview" in data, "Dashboard includes civilization overview")
            self.assert_test("real_time_metrics" in data, "Dashboard includes real-time metrics")
            
            current_status = data.get("current_status", {})
            civilization_overview = data.get("civilization_overview", {})
            real_time_metrics = data.get("real_time_metrics", {})
            
            self.assert_test("stress_level" in current_status, "Status includes stress level")
            self.assert_test("production_phase" in current_status, "Status includes production phase")
            self.assert_test("component_count" in civilization_overview, "Overview includes component count")
            self.assert_test("civilization_health" in real_time_metrics, "Metrics include civilization health")
            self.assert_test("budget_utilization" in real_time_metrics, "Metrics include budget utilization")
            
            print(f"   Executive Title: {data.get('executive_title')}")
            print(f"   Stress Level: {current_status.get('stress_level')}")
            print(f"   Production Phase: {current_status.get('production_phase')}")
            print(f"   Civilization Health: {real_time_metrics.get('civilization_health', 0):.2f}")
            print(f"   Budget Utilization: {real_time_metrics.get('budget_utilization', 0):.2f}")
            
        except Exception as e:
            self.assert_test(False, "Executive dashboard accessible", str(e))
    
    def test_civilization_health_monitoring(self):
        """Test comprehensive civilization health monitoring"""
        print("\n🏛️ Testing civilization health monitoring...")
        try:
            response = requests.get(f"{OREN_API}/civilization/health?include_components=true&include_predictions=true", timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Civilization health responds")
            self.assert_test("civilization_metrics" in data, "Response includes civilization metrics")
            self.assert_test("health_assessment" in data, "Response includes health assessment")
            self.assert_test("monitoring_metadata" in data, "Response includes monitoring metadata")
            self.assert_test("component_health" in data, "Response includes component health")
            self.assert_test("predictions" in data, "Response includes predictions")
            
            civilization_metrics = data.get("civilization_metrics", {})
            health_assessment = data.get("health_assessment", {})
            monitoring_metadata = data.get("monitoring_metadata", {})
            
            self.assert_test("overall_health" in civilization_metrics, "Metrics include overall health")
            self.assert_test("budget_utilization" in civilization_metrics, "Metrics include budget utilization")
            self.assert_test("production_efficiency" in civilization_metrics, "Metrics include production efficiency")
            self.assert_test("narrative_coherence" in civilization_metrics, "Metrics include narrative coherence")
            self.assert_test("overall_status" in health_assessment, "Assessment includes overall status")
            self.assert_test("ceo_stress_level" in monitoring_metadata, "Metadata includes CEO stress level")
            
            print(f"   Overall Health: {civilization_metrics.get('overall_health', 0):.2f}")
            print(f"   Production Efficiency: {civilization_metrics.get('production_efficiency', 0):.2f}")
            print(f"   Narrative Coherence: {civilization_metrics.get('narrative_coherence', 0):.2f}")
            print(f"   Overall Status: {health_assessment.get('overall_status')}")
            
        except Exception as e:
            self.assert_test(False, "Civilization health monitoring", str(e))
    
    def test_executive_decision_execution(self):
        """Test executive decision making and implementation"""
        print("\n💼 Testing executive decision execution...")
        try:
            # Test budget cut decision
            decision_payload = {
                "decision_type": "budget_cut",
                "target_component": "narrative_engine",
                "rationale": "Cost optimization required for improved operational efficiency",
                "budget_impact": 15.0,
                "implementation_priority": 4,
                "expected_roi": 180.0
            }
            
            response = requests.post(f"{OREN_API}/decisions/execute", 
                                   json=decision_payload, timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Executive decision executes")
            self.assert_test("decision_executed" in data, "Response includes decision details")
            self.assert_test("implementation_status" in data, "Response includes implementation status")
            self.assert_test("impact_analysis" in data, "Response includes impact analysis")
            self.assert_test("oren_response" in data, "Response includes Oren's statement")
            
            decision_executed = data.get("decision_executed", {})
            impact_analysis = data.get("impact_analysis", {})
            
            self.assert_test("decision_type" in decision_executed, "Decision includes type")
            self.assert_test("target_component" in decision_executed, "Decision includes target")
            self.assert_test("budget_impact_applied" in impact_analysis, "Impact includes budget change")
            self.assert_test("civilization_health_after" in impact_analysis, "Impact includes health after")
            
            print(f"   Decision Type: {decision_executed.get('decision_type')}")
            print(f"   Target Component: {decision_executed.get('target_component')}")
            print(f"   Budget Impact: ${impact_analysis.get('budget_impact_applied', 0):.2f}")
            print(f"   Implementation: {data.get('implementation_status')}")
            
        except Exception as e:
            self.assert_test(False, "Executive decision execution", str(e))
    
    def test_budget_allocation_management(self):
        """Test budget allocation and reallocation functionality"""
        print("\n💰 Testing budget allocation management...")
        try:
            # First get current budget allocation
            response = requests.get(f"{OREN_API}/budget/allocation", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Budget allocation responds")
            self.assert_test("budget_overview" in data, "Response includes budget overview")
            self.assert_test("component_allocations" in data, "Response includes component allocations")
            self.assert_test("budget_efficiency" in data, "Response includes efficiency metrics")
            self.assert_test("executive_controls" in data, "Response includes executive controls")
            
            budget_overview = data.get("budget_overview", {})
            component_allocations = data.get("component_allocations", {})
            budget_efficiency = data.get("budget_efficiency", {})
            
            self.assert_test("total_allocated" in budget_overview, "Overview includes total allocated")
            self.assert_test("utilization_percent" in budget_overview, "Overview includes utilization")
            self.assert_test("burn_rate_per_hour" in budget_overview, "Overview includes burn rate")
            self.assert_test(len(component_allocations) > 0, "Allocations include components")
            
            print(f"   Total Allocated: ${budget_overview.get('total_allocated', 0):.2f}")
            print(f"   Utilization: {budget_overview.get('utilization_percent', 0):.1f}%")
            print(f"   Burn Rate: ${budget_overview.get('burn_rate_per_hour', 0):.2f}/hour")
            print(f"   Components: {len(component_allocations)}")
            
        except Exception as e:
            self.assert_test(False, "Budget allocation management", str(e))
    
    def test_budget_reallocation(self):
        """Test executive budget reallocation"""
        print("\n🔄 Testing budget reallocation...")
        try:
            # Test budget reallocation
            reallocation_payload = {
                "component_allocations": {
                    "api_gateway": 55.0,
                    "docker_infrastructure": 40.0,
                    "jacklyn_variance_db": 35.0,
                    "websocket_realtime": 30.0,
                    "vector_search": 25.0,
                    "glyph_marrow_qdpi": 20.0,
                    "london_fox_graph": 15.0,
                    "narrative_engine": 10.0
                },
                "total_budget": 230.0
            }
            
            response = requests.post(f"{OREN_API}/budget/reallocate", 
                                   json=reallocation_payload, timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Budget reallocation executes")
            self.assert_test("reallocation_executed" in data, "Response includes reallocation details")
            self.assert_test("allocation_changes" in data, "Response includes allocation changes")
            self.assert_test("decision_record" in data, "Response includes decision record")
            self.assert_test("impact_analysis" in data, "Response includes impact analysis")
            self.assert_test("oren_statement" in data, "Response includes Oren's statement")
            
            reallocation_executed = data.get("reallocation_executed", {})
            allocation_changes = data.get("allocation_changes", {})
            
            self.assert_test("total_budget" in reallocation_executed, "Reallocation includes total budget")
            self.assert_test("components_affected" in reallocation_executed, "Reallocation includes components count")
            self.assert_test(len(allocation_changes) > 0, "Changes include component details")
            
            print(f"   Total Budget: ${reallocation_executed.get('total_budget', 0):.2f}")
            print(f"   Components Affected: {reallocation_executed.get('components_affected')}")
            print(f"   Changes Applied: {len(allocation_changes)} components")
            
        except Exception as e:
            self.assert_test(False, "Budget reallocation", str(e))
    
    def test_production_phase_transition(self):
        """Test production phase transitions"""
        print("\n🏭 Testing production phase transition...")
        try:
            # Test phase transition
            phase_payload = {
                "new_phase": "maintenance", 
                "transition_rationale": "Scheduled maintenance window for system optimization and executive oversight review"
            }
            
            response = requests.post(f"{OREN_API}/production/phase-transition", 
                                   json=phase_payload, timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Phase transition executes")
            self.assert_test("phase_transition" in data, "Response includes transition details")
            self.assert_test("decision_record" in data, "Response includes decision record")
            self.assert_test("civilization_impact" in data, "Response includes civilization impact")
            self.assert_test("oren_statement" in data, "Response includes Oren's statement")
            
            phase_transition = data.get("phase_transition", {})
            civilization_impact = data.get("civilization_impact", {})
            
            self.assert_test("previous_phase" in phase_transition, "Transition includes previous phase")
            self.assert_test("new_phase" in phase_transition, "Transition includes new phase")
            self.assert_test("ceo_authorization" in phase_transition, "Transition includes CEO authorization")
            self.assert_test("components_affected" in civilization_impact, "Impact includes components affected")
            
            print(f"   Previous Phase: {phase_transition.get('previous_phase')}")
            print(f"   New Phase: {phase_transition.get('new_phase')}")
            print(f"   CEO Authorization: {phase_transition.get('ceo_authorization')}")
            print(f"   Components Affected: {civilization_impact.get('components_affected')}")
            
        except Exception as e:
            self.assert_test(False, "Production phase transition", str(e))
    
    def test_executive_decision_history(self):
        """Test executive decision history and analytics"""
        print("\n📚 Testing executive decision history...")
        try:
            response = requests.get(f"{OREN_API}/decisions/history?limit=20", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Decision history responds")
            self.assert_test("decision_history" in data, "Response includes decision history")
            self.assert_test("history_analytics" in data, "Response includes analytics")
            self.assert_test("current_executive_state" in data, "Response includes executive state")
            
            decision_history = data.get("decision_history", [])
            history_analytics = data.get("history_analytics", {})
            current_executive_state = data.get("current_executive_state", {})
            
            self.assert_test("total_decisions" in history_analytics, "Analytics include total decisions")
            self.assert_test("total_budget_impact" in history_analytics, "Analytics include budget impact")
            self.assert_test("decision_type_breakdown" in history_analytics, "Analytics include type breakdown")
            self.assert_test("decisions_made_today" in current_executive_state, "State includes today's decisions")
            
            print(f"   Total Decisions: {history_analytics.get('total_decisions')}")
            print(f"   Budget Impact: ${history_analytics.get('total_budget_impact', 0):.2f}")
            print(f"   Decisions Today: {current_executive_state.get('decisions_made_today')}")
            print(f"   History Entries: {len(decision_history)}")
            
        except Exception as e:
            self.assert_test(False, "Executive decision history", str(e))
    
    def test_stress_response_system(self):
        """Test executive stress response and system scaling"""
        print("\n🚨 Testing stress response system...")
        try:
            # Get current stress level from dashboard
            response = requests.get(f"{OREN_API}/dashboard", timeout=10)
            dashboard_data = response.json()
            
            self.assert_test(response.status_code == 200, "Dashboard accessible for stress testing")
            
            current_status = dashboard_data.get("current_status", {})
            real_time_metrics = dashboard_data.get("real_time_metrics", {})
            
            self.assert_test("stress_level" in current_status, "Status includes stress level")
            self.assert_test("executive_override_active" in current_status, "Status includes override state")
            self.assert_test("executive_stress_level" in real_time_metrics, "Metrics include stress level")
            
            stress_level = current_status.get("stress_level")
            executive_stress = real_time_metrics.get("executive_stress_level")
            override_active = current_status.get("executive_override_active")
            
            # Test stress level mapping
            valid_stress_levels = ["optimal", "elevated", "high_stress", "critical", "executive_override"]
            self.assert_test(stress_level in valid_stress_levels, "Valid stress level detected")
            self.assert_test(executive_stress in valid_stress_levels, "Valid executive stress detected")
            self.assert_test(isinstance(override_active, bool), "Override state is boolean")
            
            print(f"   Current Stress Level: {stress_level}")
            print(f"   Executive Stress: {executive_stress}")
            print(f"   Override Active: {override_active}")
            print(f"   System Response: {'Executive intervention engaged' if override_active else 'Normal operations'}")
            
        except Exception as e:
            self.assert_test(False, "Stress response system", str(e))
    
    def test_narrative_coherence_monitoring(self):
        """Test narrative coherence assessment and construction"""
        print("\n📖 Testing narrative coherence monitoring...")
        try:
            response = requests.get(f"{OREN_API}/civilization/health?include_components=true", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Narrative monitoring accessible")
            
            civilization_metrics = data.get("civilization_metrics", {})
            
            self.assert_test("narrative_coherence" in civilization_metrics, "Metrics include narrative coherence")
            
            narrative_coherence = civilization_metrics.get("narrative_coherence", 0.0)
            
            self.assert_test(isinstance(narrative_coherence, (int, float)), "Narrative coherence is numeric")
            self.assert_test(0.0 <= narrative_coherence <= 1.0, "Narrative coherence in valid range")
            
            # Test narrative status assessment
            if narrative_coherence > 0.8:
                narrative_status = "highly_coherent"
            elif narrative_coherence > 0.6:
                narrative_status = "coherent"
            elif narrative_coherence > 0.4:
                narrative_status = "fragmented"
            else:
                narrative_status = "incoherent"
            
            self.assert_test(narrative_status in ["highly_coherent", "coherent", "fragmented", "incoherent"], "Valid narrative assessment")
            
            print(f"   Narrative Coherence: {narrative_coherence:.2f}")
            print(f"   Narrative Status: {narrative_status}")
            print(f"   Executive Oversight: {'Active narrative construction' if narrative_coherence > 0.7 else 'Narrative restructuring recommended'}")
            
        except Exception as e:
            self.assert_test(False, "Narrative coherence monitoring", str(e))
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("🎩 OREN PROGRESSO EXECUTIVE ORCHESTRATION & OBSERVABILITY TESTS")
        print("=" * 70)
        
        self.test_health_check()
        self.test_character_status()
        self.test_executive_dashboard()
        self.test_civilization_health_monitoring()
        self.test_executive_decision_execution()
        self.test_budget_allocation_management()
        self.test_budget_reallocation()
        self.test_production_phase_transition()
        self.test_executive_decision_history()
        self.test_stress_response_system()
        self.test_narrative_coherence_monitoring()
        
        print("\n" + "=" * 70)
        print(f"🎯 TEST SUMMARY")
        print(f"   Passed: {self.passed}")
        print(f"   Failed: {self.failed}")
        print(f"   Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.failed == 0:
            print("\n✅ ALL TESTS PASSED - Oren Progresso executive orchestration system is fully operational!")
            print("Week 4 implementation complete: Orchestration & Observability with CEO-level decision making ready.")
        else:
            print(f"\n❌ {self.failed} tests failed - Review Oren Progresso orchestration implementation")
        
        return self.failed == 0

def main():
    """Main test execution"""
    print("Starting Oren Progresso executive orchestration validation...")
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
    
    tester = OrenProgressoTester()
    success = tester.run_all_tests()
    
    # Save test results
    with open('oren_progresso_test_results.json', 'w') as f:
        json.dump({
            "timestamp": time.time(),
            "success": success,
            "passed": tester.passed,
            "failed": tester.failed,
            "results": tester.test_results
        }, f, indent=2)
    
    print(f"\n📊 Test results saved to: oren_progresso_test_results.json")
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)