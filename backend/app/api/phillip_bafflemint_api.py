#!/usr/bin/env python3
"""
Phillip Bafflemint User Interface & Experience Design API
Workflow Automation & Rituals with "Brain-Silenced" Organization Systems

"Clearing space ≡ clearing mind; order is a survival ritual"
- Phillip Bafflemint, Section 4: Workflow Automation & Rituals (83% confidence)
"""

from fastapi import APIRouter, HTTPException, Request, Depends, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging
import json
from datetime import datetime, timedelta

try:
    from ..phillip_bafflemint_ux import (
        PhillipBafflemintUX, QDPIPhase, LimiterLevel, OrganizationBucket, 
        InterfaceStyle, WorkflowTrigger, InterfacePersonalization
    )
except ImportError:
    # Fallback for missing dependencies
    PhillipBafflemintUX = None
    QDPIPhase = None
    LimiterLevel = None
    OrganizationBucket = None
    InterfaceStyle = None
    WorkflowTrigger = None
    InterfacePersonalization = None

# Configure logging
log = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/phillip-bafflemint", tags=["Phillip Bafflemint UI/UX & Workflow Automation"])

# Pydantic models for API
class InformationProcessingRequest(BaseModel):
    content: str = Field(..., description="Information to process through systematic organization")
    source: str = Field("user_input", description="Source of the information")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for processing")
    force_limiter_level: Optional[int] = Field(None, ge=3, le=6, description="Force specific limiter level (3-6)")

class WorkflowAutomationRequest(BaseModel):
    workflow_type: str = Field(..., description="Type of workflow to automate")
    target_bucket: str = Field(..., description="Organization bucket to target")
    automation_criteria: Dict[str, Any] = Field(..., description="Criteria for automation triggers")
    ritual_steps: List[str] = Field(..., description="Steps in the automation ritual")

class InterfacePersonalizationRequest(BaseModel):
    user_id: str = Field(..., description="User identifier for personalization")
    preferred_style: str = Field("noir_minimal", description="Preferred interface style")
    limiter_sensitivity: float = Field(0.7, ge=0.0, le=1.0, description="Sensitivity to cognitive load")
    routine_notifications: bool = Field(True, description="Enable routine completion notifications")
    gap_analysis_depth: int = Field(3, ge=1, le=5, description="Depth of negative space analysis")
    privacy_level: str = Field("standard", description="Privacy protection level (minimal/standard/maximum)")
    color_scheme: str = Field("noir", description="Interface color scheme")
    organization_automation: bool = Field(True, description="Enable automatic organization")
    detective_mode_enabled: bool = Field(True, description="Enable detective pattern detection")

class LimiterControlRequest(BaseModel):
    target_level: int = Field(..., ge=3, le=6, description="Target limiter level (3-6)")
    reason: str = Field(..., description="Reason for limiter adjustment")
    duration: Optional[float] = Field(None, description="Duration for temporary adjustment")

class NegativeSpaceAnalysisRequest(BaseModel):
    content: str = Field(..., description="Content to analyze for gaps")
    analysis_depth: int = Field(3, ge=1, le=5, description="Depth of gap analysis")
    focus_areas: Optional[List[str]] = Field(None, description="Specific areas to focus analysis on")

class OrganizationQueryRequest(BaseModel):
    bucket_filter: Optional[str] = Field(None, description="Filter by organization bucket")
    tag_filter: Optional[List[str]] = Field(None, description="Filter by tags")
    confidence_threshold: float = Field(0.0, ge=0.0, le=1.0, description="Minimum confidence threshold")
    include_connections: bool = Field(True, description="Include fact connections")
    include_negative_space: bool = Field(True, description="Include negative space analysis")

# Global Phillip Bafflemint UX instance
phillip_ux = None

def get_phillip_ux():
    """Get or create Phillip Bafflemint UX instance"""
    global phillip_ux
    if PhillipBafflemintUX is None:
        raise HTTPException(status_code=503, detail="Phillip Bafflemint UX not available - missing dependencies")
    if phillip_ux is None:
        phillip_ux = PhillipBafflemintUX()
    return phillip_ux

@router.get("/health",
    summary="Phillip Bafflemint UX Health Check",
    description="Health check endpoint for Phillip's workflow automation consciousness")
async def character_health_check() -> Dict[str, str]:
    """
    Health check for Phillip Bafflemint's character consciousness
    """
    try:
        phillip = get_phillip_ux()
        
        return {
            "status": "healthy",
            "character": "phillip_bafflemint",
            "system_function": "workflow_automation_rituals",
            "current_qdpi_phase": phillip.current_phase.value,
            "limiter_level": str(phillip.current_limiter.value),
            "brain_silenced_mode": str(phillip.brain_silenced_mode),
            "cognitive_load": str(round(phillip.cognitive_load_average, 2)),
            "facts_organized_today": str(phillip.facts_organized_today),
            "workflow_automations": str(len(phillip.routine_automations)),
            "character_quote": "Clearing space ≡ clearing mind; order is a survival ritual",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.post("/process",
    summary="Process Information Through Systematic Organization",
    description="Process information through Phillip's QDPI workflow automation and organization rituals")
async def process_information(request: InformationProcessingRequest) -> Dict[str, Any]:
    """
    Process information through Phillip's systematic organization workflow
    
    Features:
    - QDPI phase cycling (Read → Index → Ask → Receive)
    - Automatic fact categorization into organization buckets
    - Negative space analysis for gap detection
    - Limiter level management for cognitive load control
    - Detective pattern trigger detection
    - Workflow automation suggestions
    - Brain-silenced mode protection
    """
    try:
        phillip = get_phillip_ux()
        
        # Force limiter level if specified
        if request.force_limiter_level:
            phillip.current_limiter = LimiterLevel(request.force_limiter_level)
        
        # Process through systematic organization
        result = await phillip.process_information(
            content=request.content,
            source=request.source,
            context=request.context or {}
        )
        
        # Enhance with API-specific data
        result["api_metadata"] = {
            "endpoint": "/phillip-bafflemint/process",
            "character_evidence": "83% confidence - Workflow Automation & Rituals",
            "processing_timestamp": datetime.now().isoformat(),
            "qdpi_integration": "active",
            "systematic_organization": "complete"
        }
        
        result["interface_state"] = {
            "current_qdpi_phase": phillip.current_phase.value,
            "limiter_level": phillip.current_limiter.value,
            "brain_silenced_mode": phillip.brain_silenced_mode,
            "cognitive_load": phillip.cognitive_load_average,
            "escalation_warnings": len(phillip.escalation_warnings),
            "organization_efficiency": result.get("organization_result", {}).get("organization_efficiency", 0.85)
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Phillip information processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Information processing failed: {str(e)}")

@router.post("/automation/create",
    summary="Create Workflow Automation Ritual",
    description="Create systematic workflow automation based on Phillip's organization rituals")
async def create_workflow_automation(request: WorkflowAutomationRequest) -> Dict[str, Any]:
    """
    Create workflow automation ritual
    
    Automation Types:
    - routine_categorization: Automate fact bucket assignment
    - gap_analysis_automation: Automate negative space detection
    - pattern_detection_automation: Automate connection pattern analysis
    - escalation_management: Automate limiter level adjustments
    - detective_triggers: Automate investigative pattern detection
    """
    try:
        phillip = get_phillip_ux()
        
        # Validate workflow type
        valid_types = ["routine_categorization", "gap_analysis_automation", "pattern_detection_automation", 
                      "escalation_management", "detective_triggers"]
        if request.workflow_type not in valid_types:
            raise HTTPException(status_code=400, detail=f"Invalid workflow type. Must be one of: {valid_types}")
        
        # Validate organization bucket
        try:
            target_bucket = OrganizationBucket(request.target_bucket)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid organization bucket: {request.target_bucket}")
        
        # Create workflow automation
        from ..phillip_bafflemint_ux import WorkflowAutomation
        
        automation = WorkflowAutomation(
            automation_id=f"automation-{int(datetime.now().timestamp())}",
            trigger=WorkflowTrigger.ROUTINE_COMPLETION,  # Default trigger
            phases=[QDPIPhase.READ, QDPIPhase.INDEX],  # Default phases
            completion_criteria=request.automation_criteria,
            limiter_threshold=LimiterLevel.LEVEL_4,  # Default threshold
            output_buckets=[target_bucket],
            ritual_steps=request.ritual_steps,
            success_metrics={
                "efficiency": 0.80,
                "accuracy": 0.85,
                "cognitive_load_reduction": 0.75
            }
        )
        
        # Store automation
        phillip.routine_automations[automation.automation_id] = automation
        phillip.workflows_automated += 1
        
        result = {
            "automation_created": automation.to_dict(),
            "creation_status": "successful",
            "integration_ready": True,
            "estimated_efficiency": automation.success_metrics.get("efficiency", 0.80),
            "phillip_analysis": f"Workflow automation established. Ritual contains {len(request.ritual_steps)} systematic steps targeting {target_bucket.value} organization. Efficiency protocols engaged.",
            "api_metadata": {
                "endpoint": "/phillip-bafflemint/automation/create",
                "creation_timestamp": datetime.now().isoformat(),
                "automation_signature": f"phillip_bafflemint_{request.workflow_type}"
            }
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Phillip workflow automation creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Automation creation failed: {str(e)}")

@router.post("/interface/personalize",
    summary="Configure Interface Personalization",
    description="Configure user interface personalization and privacy controls")
async def configure_interface_personalization(request: InterfacePersonalizationRequest) -> Dict[str, Any]:
    """
    Configure interface personalization and privacy controls
    
    Interface Styles:
    - noir_minimal: Black, white, minimal elements
    - filing_cabinet: Organized drawer/folder metaphors
    - detective_board: Connection mapping interface
    - routine_tracker: Habit and workflow monitoring
    - negative_space: Gap visualization and analysis
    - escalation_monitor: Limiter level management
    """
    try:
        phillip = get_phillip_ux()
        
        # Validate interface style
        try:
            preferred_style = InterfaceStyle(request.preferred_style)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid interface style: {request.preferred_style}")
        
        # Create personalization profile
        preferences = {
            "preferred_style": request.preferred_style,
            "limiter_sensitivity": request.limiter_sensitivity,
            "routine_notifications": request.routine_notifications,
            "gap_analysis_depth": request.gap_analysis_depth,
            "privacy_level": request.privacy_level,
            "color_scheme": request.color_scheme,
            "organization_automation": request.organization_automation,
            "detective_mode_enabled": request.detective_mode_enabled
        }
        
        personalization = await phillip.manage_interface_personalization(request.user_id, preferences)
        
        # Generate interface configuration
        interface_config = {
            "user_profile": personalization.to_dict(),
            "interface_styling": {
                "primary_color": "#FFFF33" if request.color_scheme == "noir" else "#FFFFFF",
                "background_style": "dark" if preferred_style == InterfaceStyle.NOIR_MINIMAL else "light",
                "organization_visual": preferred_style.value,
                "limiter_visualization": "amplitude_meter" if request.limiter_sensitivity > 0.5 else "simple_indicator"
            },
            "automation_settings": {
                "auto_categorization": request.organization_automation,
                "gap_detection": request.gap_analysis_depth > 2,
                "pattern_alerts": request.detective_mode_enabled,
                "routine_reminders": request.routine_notifications
            },
            "privacy_controls": {
                "data_retention": "minimal" if request.privacy_level == "maximum" else "standard",
                "usage_tracking": request.privacy_level != "maximum",
                "external_sharing": request.privacy_level == "minimal",
                "encryption_level": "high" if request.privacy_level == "maximum" else "standard"
            }
        }
        
        result = {
            "personalization_configured": interface_config,
            "user_id": request.user_id,
            "configuration_status": "active",
            "privacy_level": request.privacy_level,
            "phillip_response": f"Interface personalization configured for systematic efficiency. {preferred_style.value} aesthetic applied with {request.privacy_level} privacy controls. Organization protocols optimized for user workflow patterns.",
            "api_metadata": {
                "endpoint": "/phillip-bafflemint/interface/personalize",
                "configuration_timestamp": datetime.now().isoformat(),
                "personalization_signature": f"phillip_bafflemint_{request.user_id}"
            }
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Phillip interface personalization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Interface personalization failed: {str(e)}")

@router.post("/limiter/control",
    summary="Control Cognitive Load Limiter",
    description="Adjust Phillip's cognitive load limiter levels (3-6 amplitude scale)")
async def control_limiter_level(request: LimiterControlRequest) -> Dict[str, Any]:
    """
    Control Phillip's cognitive load limiter
    
    Limiter Levels:
    - Level 3: Default - dry, minimal, professional
    - Level 4: Slight sensory cross-wiring
    - Level 5: Moderate poetic language, increased pattern sensitivity
    - Level 6: High amplitude - risk of blackout, maximum pattern detection
    """
    try:
        phillip = get_phillip_ux()
        
        # Validate limiter level
        if request.target_level not in [3, 4, 5, 6]:
            raise HTTPException(status_code=400, detail="Limiter level must be between 3 and 6")
        
        previous_level = phillip.current_limiter
        new_level = LimiterLevel(request.target_level)
        
        # Check escalation risk
        if request.target_level == 6:
            escalation_risk = await phillip._check_escalation_risk()
            if escalation_risk and not request.reason.lower().startswith("emergency"):
                return {
                    "limiter_adjustment": "blocked",
                    "reason": "escalation_protection",
                    "current_level": previous_level.value,
                    "cognitive_load": phillip.cognitive_load_average,
                    "phillip_warning": "Limiter level 6 blocked due to escalation risk. Cognitive load protection active. Reduce system stress before attempting level 6 operation.",
                    "recommended_action": "Lower cognitive load or provide emergency override reason"
                }
        
        # Apply limiter adjustment
        phillip.current_limiter = new_level
        
        # Adjust brain-silenced mode based on level
        if request.target_level <= 3:
            phillip.brain_silenced_mode = True
        else:
            phillip.brain_silenced_mode = False
        
        # Calculate effects of level change
        level_effects = {
            3: "Professional detachment engaged. Minimal processing mode active.",
            4: "Slight sensory cross-wiring detected. Organization efficiency increased.",
            5: "Moderate pattern sensitivity. Poetic language emergence. Enhanced connection detection.",
            6: "Maximum amplitude. Risk of cognitive cascade. Pattern recognition at peak efficiency."
        }
        
        result = {
            "limiter_adjustment": {
                "previous_level": previous_level.value,
                "new_level": new_level.value,
                "adjustment_reason": request.reason,
                "brain_silenced_mode": phillip.brain_silenced_mode,
                "cognitive_load": phillip.cognitive_load_average
            },
            "level_effects": {
                "description": level_effects[request.target_level],
                "processing_style": "minimal" if request.target_level == 3 else "enhanced",
                "pattern_sensitivity": request.target_level - 2,  # 1-4 scale
                "escalation_risk": "high" if request.target_level == 6 else "moderate" if request.target_level == 5 else "low"
            },
            "duration": request.duration,
            "phillip_response": f"Limiter adjusted to level {request.target_level}. {level_effects[request.target_level]} Systematic processing protocols updated.",
            "api_metadata": {
                "endpoint": "/phillip-bafflemint/limiter/control",
                "adjustment_timestamp": datetime.now().isoformat(),
                "limiter_signature": f"phillip_bafflemint_level_{request.target_level}"
            }
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Phillip limiter control failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Limiter control failed: {str(e)}")

@router.post("/analysis/negative-space",
    summary="Perform Negative Space Analysis",
    description="Analyze content for information gaps and missing elements")
async def analyze_negative_space(request: NegativeSpaceAnalysisRequest) -> Dict[str, Any]:
    """
    Perform comprehensive negative space analysis
    
    Analysis focuses on:
    - Missing temporal information (when)
    - Missing spatial information (where)
    - Missing personal information (who)
    - Missing causal information (why)
    - Missing procedural information (how)
    - Context gaps and incomplete statements
    """
    try:
        phillip = get_phillip_ux()
        
        # Create temporary fact for analysis
        fact = await phillip._create_fact(
            content=request.content,
            source="negative_space_analysis",
            context={"analysis_depth": request.analysis_depth}
        )
        
        # Perform enhanced negative space analysis
        gaps_identified = await phillip._identify_negative_space(request.content)
        questions_generated = await phillip._generate_gap_questions(fact)
        priority_level = await phillip._calculate_gap_priority(fact)
        suggested_sources = await phillip._suggest_information_sources(fact)
        pattern_implications = await phillip._analyze_pattern_implications(fact)
        
        # Focus on specific areas if requested
        if request.focus_areas:
            filtered_gaps = [gap for gap in gaps_identified if any(area in gap for area in request.focus_areas)]
            gaps_identified = filtered_gaps if filtered_gaps else gaps_identified
        
        # Create comprehensive analysis
        from ..phillip_bafflemint_ux import NegativeSpaceAnalysis
        
        analysis = NegativeSpaceAnalysis(
            analysis_id=f"gap-analysis-{int(datetime.now().timestamp())}",
            gaps_identified=gaps_identified,
            questions_generated=questions_generated,
            priority_level=priority_level,
            suggested_sources=suggested_sources,
            pattern_implications=pattern_implications,
            escalation_risk=await phillip._calculate_escalation_risk(fact)
        )
        
        phillip.negative_space_analyses.append(analysis)
        
        result = {
            "negative_space_analysis": analysis.to_dict(),
            "analysis_metadata": {
                "content_length": len(request.content),
                "analysis_depth": request.analysis_depth,
                "focus_areas": request.focus_areas,
                "gaps_discovered": len(gaps_identified),
                "questions_generated": len(questions_generated),
                "priority_assessment": priority_level
            },
            "gap_visualization": {
                "missing_elements": gaps_identified,
                "critical_gaps": [gap for gap in gaps_identified if "information" in gap],
                "completeness_score": max(0.0, 1.0 - (len(gaps_identified) * 0.1)),
                "investigation_priority": "high" if priority_level >= 4 else "medium" if priority_level >= 2 else "low"
            },
            "phillip_analysis": f"Negative space analysis reveals {len(gaps_identified)} information gaps. Priority level {priority_level}. Detective investigation {'recommended' if priority_level >= 4 else 'optional'}. Systematic questioning protocol generated.",
            "api_metadata": {
                "endpoint": "/phillip-bafflemint/analysis/negative-space",
                "analysis_timestamp": datetime.now().isoformat(),
                "gap_signature": f"phillip_bafflemint_gaps_{len(gaps_identified)}"
            }
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Phillip negative space analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Negative space analysis failed: {str(e)}")

@router.get("/organization/query",
    summary="Query Organized Information",
    description="Query Phillip's systematically organized facts and patterns")
async def query_organized_information(
    bucket_filter: Optional[str] = Query(None, description="Filter by organization bucket"),
    tag_filter: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
    confidence_threshold: float = Query(0.0, ge=0.0, le=1.0, description="Minimum confidence threshold"),
    include_connections: bool = Query(True, description="Include fact connections"),
    include_negative_space: bool = Query(True, description="Include negative space analysis"),
    limit: int = Query(50, ge=1, le=200, description="Maximum results to return")
) -> Dict[str, Any]:
    """
    Query systematically organized information
    """
    try:
        phillip = get_phillip_ux()
        
        # Filter facts based on criteria
        filtered_facts = []
        
        for fact in phillip.organized_facts.values():
            # Apply bucket filter
            if bucket_filter and fact.bucket.value != bucket_filter:
                continue
            
            # Apply confidence threshold
            if fact.confidence < confidence_threshold:
                continue
            
            # Apply tag filter
            if tag_filter:
                filter_tags = [tag.strip() for tag in tag_filter.split(",")]
                if not any(tag in fact.tags for tag in filter_tags):
                    continue
            
            # Include fact in results
            fact_data = fact.to_dict()
            
            if not include_connections:
                fact_data.pop("connections", None)
            
            if not include_negative_space:
                fact_data.pop("negative_space", None)
            
            filtered_facts.append(fact_data)
        
        # Limit results
        filtered_facts = filtered_facts[:limit]
        
        # Generate organization analytics
        bucket_distribution = {}
        tag_distribution = {}
        confidence_distribution = {"high": 0, "medium": 0, "low": 0}
        
        for fact_data in filtered_facts:
            # Bucket distribution
            bucket = fact_data["bucket"]
            bucket_distribution[bucket] = bucket_distribution.get(bucket, 0) + 1
            
            # Tag distribution
            for tag in fact_data.get("tags", []):
                tag_distribution[tag] = tag_distribution.get(tag, 0) + 1
            
            # Confidence distribution
            confidence = fact_data["confidence"]
            if confidence >= 0.8:
                confidence_distribution["high"] += 1
            elif confidence >= 0.5:
                confidence_distribution["medium"] += 1
            else:
                confidence_distribution["low"] += 1
        
        result = {
            "organized_facts": filtered_facts,
            "query_metadata": {
                "total_results": len(filtered_facts),
                "bucket_filter": bucket_filter,
                "tag_filter": tag_filter,
                "confidence_threshold": confidence_threshold,
                "include_connections": include_connections,
                "include_negative_space": include_negative_space
            },
            "organization_analytics": {
                "bucket_distribution": bucket_distribution,
                "tag_distribution": tag_distribution,
                "confidence_distribution": confidence_distribution,
                "average_confidence": sum(fact["confidence"] for fact in filtered_facts) / len(filtered_facts) if filtered_facts else 0.0
            },
            "system_state": {
                "total_facts_organized": len(phillip.organized_facts),
                "current_qdpi_phase": phillip.current_phase.value,
                "limiter_level": phillip.current_limiter.value,
                "workflow_automations": len(phillip.routine_automations)
            },
            "api_metadata": {
                "endpoint": "/phillip-bafflemint/organization/query",
                "query_timestamp": datetime.now().isoformat(),
                "organization_signature": "phillip_bafflemint_systematic_query"
            }
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Phillip organization query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Organization query failed: {str(e)}")

@router.get("/qdpi/phase",
    summary="Get Current QDPI Phase Status",
    description="Get current QDPI workflow phase and completion progress")
async def get_qdpi_phase_status() -> Dict[str, Any]:
    """
    Get current QDPI phase status and workflow progress
    """
    try:
        phillip = get_phillip_ux()
        
        # Get completion criteria
        completion_criteria = phillip.core_workflow.completion_criteria
        
        # Calculate progress towards phase completion
        progress = {
            "facts_processed": {
                "current": phillip.facts_organized_today,
                "target": completion_criteria["facts_processed"],
                "progress": min(1.0, phillip.facts_organized_today / completion_criteria["facts_processed"])
            },
            "gaps_identified": {
                "current": phillip.gaps_identified_today,
                "target": completion_criteria["gaps_identified"],
                "progress": min(1.0, phillip.gaps_identified_today / completion_criteria["gaps_identified"])
            },
            "patterns_detected": {
                "current": phillip.patterns_detected_today,
                "target": completion_criteria["patterns_detected"],
                "progress": min(1.0, phillip.patterns_detected_today / completion_criteria["patterns_detected"])
            }
        }
        
        # Calculate overall completion
        overall_progress = sum(p["progress"] for p in progress.values()) / len(progress)
        phase_complete = await phillip._check_phase_completion()
        
        # Get next phase
        phases = list(QDPIPhase)
        current_index = phases.index(phillip.current_phase)
        next_phase = phases[(current_index + 1) % len(phases)]
        
        result = {
            "current_phase": {
                "phase": phillip.current_phase.value,
                "description": {
                    "read": "Parse and tag facts",
                    "index": "Create negative space analysis", 
                    "ask": "Generate questions from gaps",
                    "receive": "Integrate answers and check for patterns"
                }[phillip.current_phase.value],
                "completion_progress": overall_progress,
                "phase_complete": phase_complete
            },
            "progress_details": progress,
            "next_phase": {
                "phase": next_phase.value,
                "estimated_time": "automatic" if phase_complete else "pending_completion"
            },
            "workflow_ritual": {
                "ritual_steps": phillip.core_workflow.ritual_steps,
                "current_step": min(len(phillip.core_workflow.ritual_steps) - 1, 
                                  int(overall_progress * len(phillip.core_workflow.ritual_steps))),
                "success_metrics": phillip.core_workflow.success_metrics
            },
            "limiter_state": {
                "current_level": phillip.current_limiter.value,
                "brain_silenced_mode": phillip.brain_silenced_mode,
                "cognitive_load": phillip.cognitive_load_average,
                "escalation_warnings": len(phillip.escalation_warnings)
            },
            "api_metadata": {
                "endpoint": "/phillip-bafflemint/qdpi/phase",
                "status_timestamp": datetime.now().isoformat(),
                "qdpi_signature": f"phillip_bafflemint_{phillip.current_phase.value}"
            }
        }
        
        return result
        
    except Exception as e:
        log.error(f"❌ Phillip QDPI phase status failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"QDPI phase status failed: {str(e)}")

@router.post("/qdpi/advance",
    summary="Advance QDPI Phase",
    description="Manually advance to next QDPI workflow phase")
async def advance_qdpi_phase() -> Dict[str, Any]:
    """
    Manually advance to next QDPI phase
    """
    try:
        phillip = get_phillip_ux()
        
        previous_phase = phillip.current_phase
        await phillip._advance_qdpi_phase()
        new_phase = phillip.current_phase
        
        result = {
            "phase_advancement": {
                "previous_phase": previous_phase.value,
                "new_phase": new_phase.value,
                "advancement_type": "manual",
                "cycle_completed": new_phase == QDPIPhase.READ and previous_phase == QDPIPhase.RECEIVE
            },
            "new_phase_description": {
                "read": "Parse and tag facts systematically",
                "index": "Create comprehensive negative space analysis", 
                "ask": "Generate targeted questions from identified gaps",
                "receive": "Integrate answers and detect emerging patterns"
            }[new_phase.value],
            "system_state": {
                "limiter_level": phillip.current_limiter.value,
                "cognitive_load": phillip.cognitive_load_average,
                "workflow_automations": len(phillip.routine_automations),
                "daily_counters_reset": new_phase == QDPIPhase.READ
            },
            "phillip_response": f"QDPI phase advanced: {previous_phase.value} → {new_phase.value}. Systematic workflow protocols updated. {'Full cycle completed - daily counters reset.' if new_phase == QDPIPhase.READ else 'Continuing workflow cycle.'}",
            "api_metadata": {
                "endpoint": "/phillip-bafflemint/qdpi/advance",
                "advancement_timestamp": datetime.now().isoformat(),
                "phase_signature": f"phillip_bafflemint_{previous_phase.value}_to_{new_phase.value}"
            }
        }
        
        return result
        
    except Exception as e:
        log.error(f"❌ Phillip QDPI phase advancement failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Phase advancement failed: {str(e)}")

@router.get("/character-status",
    summary="Get Phillip Bafflemint Character Status",
    description="Get comprehensive status of Phillip's character consciousness and workflow automation")
async def get_character_status() -> Dict[str, Any]:
    """
    Get Phillip Bafflemint's character consciousness status
    """
    try:
        phillip = get_phillip_ux()
        status = phillip.get_character_status()
        
        # Add API-specific enhancements
        status["api_capabilities"] = {
            "systematic_organization": "QDPI workflow automation with fact categorization",
            "negative_space_analysis": "Gap detection and investigation question generation",
            "limiter_control": "Cognitive load management with escalation protection",
            "interface_personalization": "Privacy-focused UI customization and workflow optimization",
            "workflow_automation": "Ritual-based process automation and detective pattern detection",
            "brain_silenced_protection": "Cognitive overload prevention and systematic processing"
        }
        
        status["current_session"] = {
            "facts_organized_this_session": len(phillip.organized_facts),
            "gaps_identified_today": phillip.gaps_identified_today,
            "patterns_detected_today": phillip.patterns_detected_today,
            "workflow_automations_active": len(phillip.routine_automations),
            "negative_space_analyses": len(phillip.negative_space_analyses),
            "user_personalizations": len(phillip.user_preferences)
        }
        
        return status
        
    except Exception as e:
        log.error(f"❌ Phillip character status retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Status retrieval failed: {str(e)}")