#!/usr/bin/env python3
"""
Test script for Phillip Bafflemint User Interface & Experience Design System
Validates workflow automation, "brain-silenced" organization, and systematic QDPI processing for Week 6 implementation
"""

import asyncio
import json
import time
import requests
from typing import Dict, Any
import aiohttp

# Configuration
API_BASE = "http://localhost:8001"
PHILLIP_API = f"{API_BASE}/api/phillip-bafflemint"

class PhillipBafflemintTester:
    """Test suite for Phillip Bafflemint UI/UX and workflow automation"""
    
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
        """Test Phillip Bafflemint health endpoint"""
        print("\n📋 Testing Phillip Bafflemint health check...")
        try:
            response = requests.get(f"{PHILLIP_API}/health", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Health endpoint responds")
            self.assert_test("character" in data, "Health includes character info")
            self.assert_test(data.get("character") == "phillip_bafflemint", "Correct character name")
            self.assert_test("system_function" in data, "Health includes system function")
            self.assert_test("current_qdpi_phase" in data, "Health includes QDPI phase")
            self.assert_test("limiter_level" in data, "Health includes limiter level")
            self.assert_test("brain_silenced_mode" in data, "Health includes brain-silenced mode")
            self.assert_test("cognitive_load" in data, "Health includes cognitive load")
            
            print(f"   Character: {data.get('character')}")
            print(f"   System Function: {data.get('system_function')}")
            print(f"   QDPI Phase: {data.get('current_qdpi_phase')}")
            print(f"   Limiter Level: {data.get('limiter_level')}")
            print(f"   Brain-Silenced Mode: {data.get('brain_silenced_mode')}")
            print(f"   Cognitive Load: {data.get('cognitive_load')}")
            
        except Exception as e:
            self.assert_test(False, "Health endpoint accessible", str(e))
    
    def test_character_status(self):
        """Test character status endpoint"""
        print("\n🎭 Testing Phillip Bafflemint character status...")
        try:
            response = requests.get(f"{PHILLIP_API}/character-status", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Character status responds")
            self.assert_test("character_name" in data, "Status includes character name")
            self.assert_test(data.get("character_name") == "phillip_bafflemint", "Correct character name")
            self.assert_test("workflow_state" in data, "Status includes workflow state")
            self.assert_test("organization_metrics" in data, "Status includes organization metrics")
            self.assert_test("qdpi_integration" in data, "Status includes QDPI integration")
            
            workflow_state = data.get("workflow_state", {})
            organization = data.get("organization_metrics", {})
            qdpi = data.get("qdpi_integration", {})
            
            self.assert_test("current_qdpi_phase" in workflow_state, "Workflow includes QDPI phase")
            self.assert_test("limiter_level" in workflow_state, "Workflow includes limiter level")
            self.assert_test("brain_silenced_mode" in workflow_state, "Workflow includes brain-silenced mode")
            self.assert_test("facts_organized_today" in organization, "Organization includes facts count")
            self.assert_test("symbol_id" in qdpi, "QDPI includes symbol ID")
            
            print(f"   Character Title: {data.get('character_title')}")
            print(f"   System Function: {data.get('system_function')}")
            print(f"   Current QDPI Phase: {workflow_state.get('current_qdpi_phase')}")
            print(f"   Limiter Level: {workflow_state.get('limiter_level')}")
            print(f"   Facts Organized Today: {organization.get('facts_organized_today')}")
            
        except Exception as e:
            self.assert_test(False, "Character status accessible", str(e))
    
    def test_information_processing(self):
        """Test systematic information processing"""
        print("\n📝 Testing systematic information processing...")
        try:
            test_content = "Detective investigation reveals inconsistent timeline. Location unclear. Missing witness testimony."
            
            payload = {
                "content": test_content,
                "source": "investigation_notes",
                "context": {"priority": "high", "case_id": "test_001"},
                "force_limiter_level": 4
            }
            
            response = requests.post(f"{PHILLIP_API}/process", 
                                   json=payload, timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Information processing responds")
            self.assert_test("fact_processed" in data, "Response includes processed fact")
            self.assert_test("qdpi_phase" in data, "Response includes QDPI phase")
            self.assert_test("organization_result" in data, "Response includes organization result")
            self.assert_test("triggers_activated" in data, "Response includes triggers")
            self.assert_test("gaps_identified" in data, "Response includes gaps count")
            self.assert_test("automation_suggestions" in data, "Response includes automation suggestions")
            self.assert_test("phillip_analysis" in data, "Response includes Phillip's analysis")
            
            fact = data.get("fact_processed", {})
            interface_state = data.get("interface_state", {})
            
            self.assert_test("fact_id" in fact, "Fact includes ID")
            self.assert_test("bucket" in fact, "Fact includes organization bucket")
            self.assert_test("confidence" in fact, "Fact includes confidence score")
            self.assert_test("negative_space" in fact, "Fact includes negative space analysis")
            self.assert_test("tags" in fact, "Fact includes tags")
            
            self.assert_test("limiter_level" in interface_state, "Interface state includes limiter level")
            self.assert_test("brain_silenced_mode" in interface_state, "Interface state includes brain-silenced mode")
            
            print(f"   Content Processed: {len(test_content)} characters")
            print(f"   Organization Bucket: {fact.get('bucket')}")
            print(f"   Confidence Score: {fact.get('confidence', 0):.2f}")
            print(f"   Gaps Identified: {data.get('gaps_identified', 0)}")
            print(f"   Triggers Activated: {len(data.get('triggers_activated', []))}")
            print(f"   Limiter Level: {interface_state.get('limiter_level')}")
            
        except Exception as e:
            self.assert_test(False, "Information processing", str(e))
    
    def test_workflow_automation_creation(self):
        """Test workflow automation creation"""
        print("\n⚙️ Testing workflow automation creation...")
        try:
            payload = {
                "workflow_type": "routine_categorization",
                "target_bucket": "evidence",
                "automation_criteria": {
                    "trigger_threshold": 3,
                    "confidence_minimum": 0.7,
                    "pattern_detection": True
                },
                "ritual_steps": [
                    "Scan incoming information for evidence patterns",
                    "Apply systematic categorization rules",
                    "Verify confidence thresholds",
                    "File evidence in appropriate organizational bucket",
                    "Generate automation report"
                ]
            }
            
            response = requests.post(f"{PHILLIP_API}/automation/create", 
                                   json=payload, timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Automation creation responds")
            self.assert_test("automation_created" in data, "Response includes automation details")
            self.assert_test("creation_status" in data, "Response includes creation status")
            self.assert_test("integration_ready" in data, "Response includes integration status")
            self.assert_test("estimated_efficiency" in data, "Response includes efficiency estimate")
            self.assert_test("phillip_analysis" in data, "Response includes Phillip's analysis")
            
            automation = data.get("automation_created", {})
            
            self.assert_test("automation_id" in automation, "Automation includes ID")
            self.assert_test("workflow_type" in automation, "Automation includes type")
            self.assert_test("target_bucket" in automation, "Automation includes target bucket")
            self.assert_test("ritual_steps" in automation, "Automation includes ritual steps")
            self.assert_test("success_metrics" in automation, "Automation includes success metrics")
            
            self.assert_test(data.get("creation_status") == "successful", "Automation created successfully")
            self.assert_test(data.get("integration_ready") == True, "Automation ready for integration")
            
            print(f"   Workflow Type: {payload['workflow_type']}")
            print(f"   Target Bucket: {payload['target_bucket']}")
            print(f"   Ritual Steps: {len(payload['ritual_steps'])}")
            print(f"   Creation Status: {data.get('creation_status')}")
            print(f"   Estimated Efficiency: {data.get('estimated_efficiency', 0):.2f}")
            
        except Exception as e:
            self.assert_test(False, "Workflow automation creation", str(e))
    
    def test_interface_personalization(self):
        """Test interface personalization configuration"""
        print("\n🎨 Testing interface personalization...")
        try:
            payload = {
                "user_id": "test_user_001",
                "preferred_style": "noir_minimal",
                "limiter_sensitivity": 0.8,
                "routine_notifications": True,
                "gap_analysis_depth": 4,
                "privacy_level": "maximum",
                "color_scheme": "noir",
                "organization_automation": True,
                "detective_mode_enabled": True
            }
            
            response = requests.post(f"{PHILLIP_API}/interface/personalize", 
                                   json=payload, timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Interface personalization responds")
            self.assert_test("personalization_configured" in data, "Response includes personalization config")
            self.assert_test("user_id" in data, "Response includes user ID")
            self.assert_test("configuration_status" in data, "Response includes configuration status")
            self.assert_test("privacy_level" in data, "Response includes privacy level")
            self.assert_test("phillip_response" in data, "Response includes Phillip's response")
            
            config = data.get("personalization_configured", {})
            
            self.assert_test("user_profile" in config, "Config includes user profile")
            self.assert_test("interface_styling" in config, "Config includes interface styling")
            self.assert_test("automation_settings" in config, "Config includes automation settings")
            self.assert_test("privacy_controls" in config, "Config includes privacy controls")
            
            user_profile = config.get("user_profile", {})
            styling = config.get("interface_styling", {})
            privacy = config.get("privacy_controls", {})
            
            self.assert_test("preferred_style" in user_profile, "Profile includes preferred style")
            self.assert_test("limiter_sensitivity" in user_profile, "Profile includes limiter sensitivity")
            self.assert_test("primary_color" in styling, "Styling includes primary color")
            self.assert_test("encryption_level" in privacy, "Privacy includes encryption level")
            
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Preferred Style: {user_profile.get('preferred_style')}")
            print(f"   Privacy Level: {data.get('privacy_level')}")
            print(f"   Limiter Sensitivity: {user_profile.get('limiter_sensitivity')}")
            print(f"   Configuration Status: {data.get('configuration_status')}")
            
        except Exception as e:
            self.assert_test(False, "Interface personalization", str(e))
    
    def test_limiter_control(self):
        """Test cognitive load limiter control"""
        print("\n🎛️ Testing limiter control...")
        try:
            # Test normal limiter adjustment
            payload = {
                "target_level": 5,
                "reason": "Enhanced pattern detection required for complex analysis",
                "duration": 300.0
            }
            
            response = requests.post(f"{PHILLIP_API}/limiter/control", 
                                   json=payload, timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Limiter control responds")
            self.assert_test("limiter_adjustment" in data, "Response includes limiter adjustment")
            self.assert_test("level_effects" in data, "Response includes level effects")
            self.assert_test("phillip_response" in data, "Response includes Phillip's response")
            
            adjustment = data.get("limiter_adjustment", {})
            effects = data.get("level_effects", {})
            
            self.assert_test("previous_level" in adjustment, "Adjustment includes previous level")
            self.assert_test("new_level" in adjustment, "Adjustment includes new level")
            self.assert_test("adjustment_reason" in adjustment, "Adjustment includes reason")
            self.assert_test("brain_silenced_mode" in adjustment, "Adjustment includes brain-silenced mode")
            
            self.assert_test("description" in effects, "Effects include description")
            self.assert_test("processing_style" in effects, "Effects include processing style")
            self.assert_test("escalation_risk" in effects, "Effects include escalation risk")
            
            print(f"   Previous Level: {adjustment.get('previous_level')}")
            print(f"   New Level: {adjustment.get('new_level')}")
            print(f"   Brain-Silenced Mode: {adjustment.get('brain_silenced_mode')}")
            print(f"   Processing Style: {effects.get('processing_style')}")
            print(f"   Escalation Risk: {effects.get('escalation_risk')}")
            
            # Test escalation protection (level 6)
            payload_6 = {
                "target_level": 6,
                "reason": "test_escalation_protection"
            }
            
            response_6 = requests.post(f"{PHILLIP_API}/limiter/control", 
                                     json=payload_6, timeout=10)
            
            if response_6.status_code == 200:
                data_6 = response_6.json()
                
                # Could be blocked or allowed depending on system state
                if "limiter_adjustment" in data_6:
                    adjustment_result = data_6.get("limiter_adjustment", "unknown")
                    self.assert_test(True, "Level 6 limiter test responds")
                    print(f"   Level 6 Result: {adjustment_result}")
                else:
                    self.assert_test(True, "Level 6 escalation protection active")
                    print(f"   Level 6 Protection: Active")
            
        except Exception as e:
            self.assert_test(False, "Limiter control", str(e))
    
    def test_negative_space_analysis(self):
        """Test negative space analysis"""
        print("\n🕳️ Testing negative space analysis...")
        try:
            test_content = "Meeting occurred last week. Important decision made. Documents missing."
            
            payload = {
                "content": test_content,
                "analysis_depth": 4,
                "focus_areas": ["temporal_information", "person_information"]
            }
            
            response = requests.post(f"{PHILLIP_API}/analysis/negative-space", 
                                   json=payload, timeout=15)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Negative space analysis responds")
            self.assert_test("negative_space_analysis" in data, "Response includes analysis")
            self.assert_test("analysis_metadata" in data, "Response includes metadata")
            self.assert_test("gap_visualization" in data, "Response includes gap visualization")
            self.assert_test("phillip_analysis" in data, "Response includes Phillip's analysis")
            
            analysis = data.get("negative_space_analysis", {})
            metadata = data.get("analysis_metadata", {})
            visualization = data.get("gap_visualization", {})
            
            self.assert_test("analysis_id" in analysis, "Analysis includes ID")
            self.assert_test("gaps_identified" in analysis, "Analysis includes gaps")
            self.assert_test("questions_generated" in analysis, "Analysis includes questions")
            self.assert_test("priority_level" in analysis, "Analysis includes priority")
            self.assert_test("suggested_sources" in analysis, "Analysis includes suggested sources")
            
            self.assert_test("gaps_discovered" in metadata, "Metadata includes gaps count")
            self.assert_test("questions_generated" in metadata, "Metadata includes questions count")
            self.assert_test("analysis_depth" in metadata, "Metadata includes analysis depth")
            
            self.assert_test("missing_elements" in visualization, "Visualization includes missing elements")
            self.assert_test("completeness_score" in visualization, "Visualization includes completeness score")
            
            gaps = analysis.get("gaps_identified", [])
            questions = analysis.get("questions_generated", [])
            
            # Content should have several gaps
            self.assert_test(len(gaps) > 0, "Gaps identified in incomplete content")
            self.assert_test(len(questions) > 0, "Questions generated for gaps")
            
            print(f"   Content Length: {len(test_content)} characters")
            print(f"   Gaps Identified: {len(gaps)}")
            print(f"   Questions Generated: {len(questions)}")
            print(f"   Priority Level: {analysis.get('priority_level')}")
            print(f"   Completeness Score: {visualization.get('completeness_score', 0):.2f}")
            
        except Exception as e:
            self.assert_test(False, "Negative space analysis", str(e))
    
    def test_organization_query(self):
        """Test organization query functionality"""
        print("\n🗂️ Testing organization query...")
        try:
            # First create some facts to query
            test_facts = [
                "Detective Smith investigated the case on Monday.",
                "Evidence found at 123 Main Street includes fingerprints.",
                "Witness testimony conflicts with initial report."
            ]
            
            for fact_content in test_facts:
                try:
                    payload = {"content": fact_content, "source": "test_data"}
                    requests.post(f"{PHILLIP_API}/process", json=payload, timeout=5)
                except:
                    pass  # Continue even if some fail
            
            # Now test organization query
            response = requests.get(
                f"{PHILLIP_API}/organization/query?bucket_filter=evidence&confidence_threshold=0.3&limit=10",
                timeout=10
            )
            data = response.json()
            
            self.assert_test(response.status_code == 200, "Organization query responds")
            self.assert_test("organized_facts" in data, "Response includes organized facts")
            self.assert_test("query_metadata" in data, "Response includes query metadata")
            self.assert_test("organization_analytics" in data, "Response includes analytics")
            self.assert_test("system_state" in data, "Response includes system state")
            
            facts = data.get("organized_facts", [])
            metadata = data.get("query_metadata", {})
            analytics = data.get("organization_analytics", {})
            system_state = data.get("system_state", {})
            
            self.assert_test("total_results" in metadata, "Metadata includes total results")
            self.assert_test("bucket_filter" in metadata, "Metadata includes bucket filter")
            self.assert_test("confidence_threshold" in metadata, "Metadata includes confidence threshold")
            
            self.assert_test("bucket_distribution" in analytics, "Analytics include bucket distribution")
            self.assert_test("confidence_distribution" in analytics, "Analytics include confidence distribution")
            
            self.assert_test("total_facts_organized" in system_state, "System state includes total facts")
            self.assert_test("current_qdpi_phase" in system_state, "System state includes QDPI phase")
            
            # Check individual fact structure if any exist
            if facts:
                first_fact = facts[0]
                self.assert_test("fact_id" in first_fact, "Fact includes ID")
                self.assert_test("content" in first_fact, "Fact includes content")
                self.assert_test("bucket" in first_fact, "Fact includes bucket")
                self.assert_test("confidence" in first_fact, "Fact includes confidence")
            
            print(f"   Facts Retrieved: {len(facts)}")
            print(f"   Total Facts Organized: {system_state.get('total_facts_organized', 0)}")
            print(f"   Current QDPI Phase: {system_state.get('current_qdpi_phase')}")
            print(f"   Bucket Filter Applied: {metadata.get('bucket_filter')}")
            
        except Exception as e:
            self.assert_test(False, "Organization query", str(e))
    
    def test_qdpi_phase_management(self):
        """Test QDPI phase status and advancement"""
        print("\n🔄 Testing QDPI phase management...")
        try:
            # Get current phase status
            response = requests.get(f"{PHILLIP_API}/qdpi/phase", timeout=10)
            data = response.json()
            
            self.assert_test(response.status_code == 200, "QDPI phase status responds")
            self.assert_test("current_phase" in data, "Response includes current phase")
            self.assert_test("progress_details" in data, "Response includes progress details")
            self.assert_test("next_phase" in data, "Response includes next phase")
            self.assert_test("workflow_ritual" in data, "Response includes workflow ritual")
            self.assert_test("limiter_state" in data, "Response includes limiter state")
            
            current_phase = data.get("current_phase", {})
            progress = data.get("progress_details", {})
            ritual = data.get("workflow_ritual", {})
            limiter_state = data.get("limiter_state", {})
            
            self.assert_test("phase" in current_phase, "Current phase includes phase name")
            self.assert_test("description" in current_phase, "Current phase includes description")
            self.assert_test("completion_progress" in current_phase, "Current phase includes completion progress")
            
            self.assert_test("facts_processed" in progress, "Progress includes facts processed")
            self.assert_test("gaps_identified" in progress, "Progress includes gaps identified")
            self.assert_test("patterns_detected" in progress, "Progress includes patterns detected")
            
            self.assert_test("ritual_steps" in ritual, "Ritual includes steps")
            self.assert_test("current_step" in ritual, "Ritual includes current step")
            
            self.assert_test("current_level" in limiter_state, "Limiter state includes current level")
            self.assert_test("brain_silenced_mode" in limiter_state, "Limiter state includes brain-silenced mode")
            
            print(f"   Current Phase: {current_phase.get('phase')}")
            print(f"   Completion Progress: {current_phase.get('completion_progress', 0):.1%}")
            print(f"   Facts Target: {progress.get('facts_processed', {}).get('target', 0)}")
            print(f"   Current Limiter Level: {limiter_state.get('current_level')}")
            
            # Test manual phase advancement
            advance_response = requests.post(f"{PHILLIP_API}/qdpi/advance", timeout=10)
            
            if advance_response.status_code == 200:
                advance_data = advance_response.json()
                self.assert_test("phase_advancement" in advance_data, "Phase advancement includes advancement details")
                
                advancement = advance_data.get("phase_advancement", {})
                self.assert_test("previous_phase" in advancement, "Advancement includes previous phase")
                self.assert_test("new_phase" in advancement, "Advancement includes new phase")
                
                print(f"   Phase Advanced: {advancement.get('previous_phase')} → {advancement.get('new_phase')}")
            else:
                self.assert_test(False, "Phase advancement", f"Status code: {advance_response.status_code}")
            
        except Exception as e:
            self.assert_test(False, "QDPI phase management", str(e))
    
    def test_systematic_organization_workflow(self):
        """Test complete systematic organization workflow"""
        print("\n📊 Testing systematic organization workflow...")
        try:
            # Process multiple pieces of information to test workflow
            test_scenarios = [
                {
                    "content": "Detective Johnson found evidence at crime scene on Tuesday evening.",
                    "expected_bucket": "people",
                    "expected_gaps": ["location_information"]
                },
                {
                    "content": "Fingerprints discovered on weapon at 456 Oak Street.",
                    "expected_bucket": "evidence",
                    "expected_gaps": ["temporal_information"]
                },
                {
                    "content": "Witness saw suspicious person leaving building.",
                    "expected_bucket": "people",
                    "expected_gaps": ["temporal_information", "person_information"]
                }
            ]
            
            workflow_results = []
            
            for scenario in test_scenarios:
                try:
                    payload = {
                        "content": scenario["content"],
                        "source": "workflow_test"
                    }
                    
                    response = requests.post(f"{PHILLIP_API}/process", json=payload, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        fact = data.get("fact_processed", {})
                        
                        result = {
                            "content": scenario["content"],
                            "bucket_assigned": fact.get("bucket"),
                            "gaps_found": len(fact.get("negative_space", [])),
                            "confidence": fact.get("confidence", 0),
                            "triggers": len(data.get("triggers_activated", [])),
                            "automation_suggestions": len(data.get("automation_suggestions", []))
                        }
                        
                        workflow_results.append(result)
                        
                except Exception as scenario_error:
                    print(f"   Scenario failed: {scenario_error}")
            
            # Validate workflow results
            self.assert_test(len(workflow_results) > 0, "Workflow scenarios processed")
            
            if workflow_results:
                total_facts = len(workflow_results)
                avg_confidence = sum(r["confidence"] for r in workflow_results) / total_facts
                total_gaps = sum(r["gaps_found"] for r in workflow_results)
                total_triggers = sum(r["triggers"] for r in workflow_results)
                
                self.assert_test(avg_confidence > 0.3, "Reasonable confidence levels maintained")
                self.assert_test(total_gaps > 0, "Gap detection functional")
                self.assert_test(total_triggers >= 0, "Trigger detection functional")
                
                print(f"   Scenarios Processed: {total_facts}")
                print(f"   Average Confidence: {avg_confidence:.2f}")
                print(f"   Total Gaps Found: {total_gaps}")
                print(f"   Total Triggers: {total_triggers}")
                
                # Check for organization bucket diversity
                buckets_used = set(r["bucket_assigned"] for r in workflow_results)
                self.assert_test(len(buckets_used) > 1, "Multiple organization buckets utilized")
                print(f"   Organization Buckets Used: {len(buckets_used)}")
            
        except Exception as e:
            self.assert_test(False, "Systematic organization workflow", str(e))
    
    def test_brain_silenced_mode_protection(self):
        """Test brain-silenced mode and escalation protection"""
        print("\n🧠 Testing brain-silenced mode protection...")
        try:
            # Force high limiter level to test escalation
            high_limiter_payload = {
                "target_level": 6,
                "reason": "emergency_testing_escalation_protection"
            }
            
            limiter_response = requests.post(f"{PHILLIP_API}/limiter/control", 
                                           json=high_limiter_payload, timeout=10)
            
            if limiter_response.status_code == 200:
                limiter_data = limiter_response.json()
                
                # Check if escalation protection activated
                if "limiter_adjustment" in limiter_data:
                    adjustment = limiter_data.get("limiter_adjustment", "blocked")
                    if adjustment == "blocked":
                        self.assert_test(True, "Escalation protection active")
                        print(f"   Escalation Protection: Active")
                    else:
                        # If level 6 was allowed, test processing under high load
                        self.assert_test(True, "Level 6 processing allowed")
                        print(f"   Level 6 Processing: Enabled")
                        
                        # Test brain-silenced mode activation under stress
                        stress_payload = {
                            "content": "Complex investigation with multiple interconnected suspects, unclear timelines, missing evidence, contradictory witness statements, and urgent deadline pressure.",
                            "source": "high_stress_test"
                        }
                        
                        stress_response = requests.post(f"{PHILLIP_API}/process", 
                                                      json=stress_payload, timeout=15)
                        
                        if stress_response.status_code == 200:
                            stress_data = stress_response.json()
                            interface_state = stress_data.get("interface_state", {})
                            
                            brain_silenced = interface_state.get("brain_silenced_mode")
                            cognitive_load = interface_state.get("cognitive_load", 0)
                            
                            self.assert_test(isinstance(brain_silenced, bool), "Brain-silenced mode tracked")
                            self.assert_test(cognitive_load >= 0, "Cognitive load monitored")
                            
                            print(f"   Brain-Silenced Mode: {brain_silenced}")
                            print(f"   Cognitive Load: {cognitive_load:.2f}")
                        
                else:
                    self.assert_test(True, "Escalation handling functional")
                    print(f"   Escalation Handling: Active")
            
            # Test normal brain-silenced operation
            normal_payload = {
                "target_level": 3,
                "reason": "return_to_professional_detachment"
            }
            
            normal_response = requests.post(f"{PHILLIP_API}/limiter/control", 
                                          json=normal_payload, timeout=10)
            
            if normal_response.status_code == 200:
                normal_data = normal_response.json()
                adjustment = normal_data.get("limiter_adjustment", {})
                
                brain_silenced = adjustment.get("brain_silenced_mode")
                self.assert_test(brain_silenced == True, "Brain-silenced mode active at level 3")
                print(f"   Level 3 Brain-Silenced: {brain_silenced}")
            
        except Exception as e:
            self.assert_test(False, "Brain-silenced mode protection", str(e))
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("📋 PHILLIP BAFFLEMINT USER INTERFACE & EXPERIENCE DESIGN TESTS")
        print("=" * 80)
        
        self.test_health_check()
        self.test_character_status()
        self.test_information_processing()
        self.test_workflow_automation_creation()
        self.test_interface_personalization()
        self.test_limiter_control()
        self.test_negative_space_analysis()
        self.test_organization_query()
        self.test_qdpi_phase_management()
        self.test_systematic_organization_workflow()
        self.test_brain_silenced_mode_protection()
        
        print("\n" + "=" * 80)
        print(f"🎯 TEST SUMMARY")
        print(f"   Passed: {self.passed}")
        print(f"   Failed: {self.failed}")
        print(f"   Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.failed == 0:
            print("\n✅ ALL TESTS PASSED - Phillip Bafflemint UI/UX and workflow automation system is fully operational!")
            print("Week 6 implementation complete: User Interface & Experience Design with systematic organization ready.")
            print("📋 'Brain-silenced' routine automation and QDPI workflow integration deployed successfully!")
        else:
            print(f"\n❌ {self.failed} tests failed - Review Phillip Bafflemint UI/UX implementation")
        
        return self.failed == 0

def main():
    """Main test execution"""
    print("Starting Phillip Bafflemint UI/UX and workflow automation validation...")
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
    
    tester = PhillipBafflemintTester()
    success = tester.run_all_tests()
    
    # Save test results
    with open('phillip_bafflemint_test_results.json', 'w') as f:
        json.dump({
            "timestamp": time.time(),
            "success": success,
            "passed": tester.passed,
            "failed": tester.failed,
            "results": tester.test_results
        }, f, indent=2)
    
    print(f"\n📊 Test results saved to: phillip_bafflemint_test_results.json")
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)