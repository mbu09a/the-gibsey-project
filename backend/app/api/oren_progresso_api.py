#!/usr/bin/env python3
"""
Oren Progresso Executive Orchestration API
CEO-Level Monitoring and Decision Making Endpoints

"CEO of the whole damn civilization - monitors and controls all productions"
- Oren Progresso
"""

from fastapi import APIRouter, HTTPException, Request, Depends, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging
import json
from datetime import datetime, timedelta

try:
    from ..oren_progresso_orchestration import OrenProgressoOrchestration, ExecutiveDecisionType, SystemStressLevel, CivilizationComponent, ProductionPhase
except ImportError:
    # Fallback for missing dependencies
    OrenProgressoOrchestration = None
    ExecutiveDecisionType = None
    SystemStressLevel = None
    CivilizationComponent = None
    ProductionPhase = None

# Configure logging
log = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/oren-progresso", tags=["Oren Progresso Executive Orchestration"])

# Pydantic models for API
class ExecutiveDecisionRequest(BaseModel):
    decision_type: str = Field(..., description="Type of executive decision (budget_cut, resource_reallocation, etc.)")
    target_component: str = Field(..., description="Target civilization component")
    rationale: str = Field(..., description="Business justification for the decision")
    budget_impact: float = Field(0.0, description="Expected budget impact (positive = savings)")
    implementation_priority: int = Field(3, ge=1, le=5, description="Implementation priority (1-5)")
    expected_roi: float = Field(100.0, ge=0.0, description="Expected return on investment percentage")

class ProductionPhaseRequest(BaseModel):
    new_phase: str = Field(..., description="New production phase (development, staging, production, etc.)")
    transition_rationale: str = Field(..., description="Reason for phase transition")

class BudgetAllocationRequest(BaseModel):
    component_allocations: Dict[str, float] = Field(..., description="New budget allocations by component")
    total_budget: float = Field(..., ge=0.0, description="Total budget available")

class CivilizationMetricsFilter(BaseModel):
    time_range_hours: int = Field(24, ge=1, le=168, description="Time range for metrics analysis")
    include_predictions: bool = Field(True, description="Include predictive analytics")
    component_filter: Optional[List[str]] = Field(None, description="Filter by specific components")

# Global Oren Progresso orchestration instance
oren_orchestration = None

def get_oren_orchestration():
    """Get or create Oren Progresso orchestration instance"""
    global oren_orchestration
    if OrenProgressoOrchestration is None:
        raise HTTPException(status_code=503, detail="Oren Progresso Orchestration not available - missing dependencies")
    if oren_orchestration is None:
        oren_orchestration = OrenProgressoOrchestration()
    return oren_orchestration

@router.get("/dashboard",
    summary="Executive Dashboard - Whole Damn Civilization Overview",
    description="Get Oren's comprehensive executive dashboard with real-time civilization monitoring")
async def get_executive_dashboard() -> Dict[str, Any]:
    """
    Get Oren Progresso's executive dashboard
    
    Features:
    - Real-time civilization health monitoring
    - Budget utilization and cost optimization tracking
    - Executive decision history and impact analysis
    - Component status with performance metrics
    - Narrative coherence assessment
    - Stress-responsive system scaling indicators
    """
    try:
        oren = get_oren_orchestration()
        
        # Get current civilization metrics
        current_metrics = await oren.monitor_civilization_health()
        
        # Get executive dashboard data
        dashboard_data = oren.get_executive_dashboard()
        
        # Add real-time metrics to dashboard
        dashboard_data["real_time_metrics"] = {
            "current_timestamp": datetime.now().isoformat(),
            "civilization_health": current_metrics.overall_health,
            "budget_utilization": current_metrics.budget_utilization,
            "production_efficiency": current_metrics.production_efficiency,
            "narrative_coherence": current_metrics.narrative_coherence,
            "executive_stress_level": current_metrics.executive_stress_level.value,
            "active_components": current_metrics.active_components,
            "failed_components": current_metrics.failed_components,
            "budget_burn_rate": current_metrics.budget_burn_rate,
            "cost_savings_achieved": current_metrics.cost_savings_achieved,
            "requests_per_minute": current_metrics.total_requests_per_minute,
            "average_response_time": current_metrics.average_response_time,
            "resource_utilization": current_metrics.resource_utilization
        }
        
        # Add API metadata
        dashboard_data["api_metadata"] = {
            "endpoint": "/oren-progresso/dashboard",
            "character_evidence": "88% confidence - Orchestration & Observability",
            "processing_timestamp": datetime.now().isoformat(),
            "ceo_oversight": "active",
            "civilization_status": "under_executive_monitoring"
        }
        
        return dashboard_data
        
    except Exception as e:
        log.error(f"❌ Executive dashboard failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Executive dashboard failed: {str(e)}")

@router.get("/civilization/health",
    summary="Civilization Health Monitoring",
    description="Real-time health assessment of the whole damn civilization")
async def get_civilization_health(
    include_components: bool = Query(True, description="Include detailed component health data"),
    include_predictions: bool = Query(False, description="Include predictive health analytics")
) -> Dict[str, Any]:
    """
    Get comprehensive civilization health metrics
    """
    try:
        oren = get_oren_orchestration()
        
        # Get current metrics
        metrics = await oren.monitor_civilization_health()
        
        result = {
            "civilization_metrics": metrics.to_dict(),
            "health_assessment": {
                "overall_status": "healthy" if metrics.overall_health > 0.7 else "degraded" if metrics.overall_health > 0.4 else "critical",
                "executive_intervention_needed": metrics.executive_stress_level in [SystemStressLevel.CRITICAL, SystemStressLevel.EXECUTIVE_OVERRIDE],
                "budget_status": "under_budget" if metrics.budget_utilization < 0.9 else "over_budget",
                "narrative_status": "coherent" if metrics.narrative_coherence > 0.7 else "fragmented"
            },
            "monitoring_metadata": {
                "last_update": oren.last_metrics_update.isoformat(),
                "ceo_stress_level": metrics.executive_stress_level.value,
                "decisions_today": oren.decisions_made_today,
                "executive_override_active": oren.executive_override_active
            }
        }
        
        if include_components:
            result["component_health"] = oren.component_status
        
        if include_predictions:
            # Add simple predictive analytics
            recent_metrics = oren.metrics_history[-10:] if len(oren.metrics_history) >= 10 else oren.metrics_history
            if len(recent_metrics) > 1:
                health_trend = (recent_metrics[-1].overall_health - recent_metrics[0].overall_health) / len(recent_metrics)
                result["predictions"] = {
                    "health_trend": "improving" if health_trend > 0.01 else "declining" if health_trend < -0.01 else "stable",
                    "projected_health_1h": min(1.0, max(0.0, metrics.overall_health + health_trend * 6)),  # 6 = 1 hour in 10-minute intervals
                    "intervention_probability": max(0.0, min(1.0, (0.8 - metrics.overall_health) * 2))
                }
        
        return result
        
    except Exception as e:
        log.error(f"❌ Civilization health monitoring failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Health monitoring failed: {str(e)}")

@router.post("/decisions/execute",
    summary="Execute Executive Decision",
    description="Execute CEO-level decision across civilization components")
async def execute_executive_decision(request: ExecutiveDecisionRequest) -> Dict[str, Any]:
    """
    Execute an executive decision with Oren's authority
    
    Features:
    - Budget impact analysis and implementation
    - Resource reallocation across components
    - Performance optimization directives
    - Narrative restructuring commands
    - Emergency intervention protocols
    """
    try:
        oren = get_oren_orchestration()
        
        # Validate decision type
        try:
            decision_type = ExecutiveDecisionType(request.decision_type)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid decision type: {request.decision_type}")
        
        # Validate target component
        try:
            target_component = CivilizationComponent(request.target_component)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid component: {request.target_component}")
        
        # Create and implement decision
        from ..oren_progresso_orchestration import ExecutiveDecision
        
        decision = ExecutiveDecision(
            decision_id=f"EXEC-{int(datetime.now().timestamp())}",
            decision_type=decision_type,
            target_component=target_component,
            rationale=request.rationale,
            budget_impact=request.budget_impact,
            implementation_priority=request.implementation_priority,
            expected_roi=request.expected_roi,
            stress_trigger=oren.current_stress_level,
            narrative_context=f"Executive decision executed via API: {request.rationale}",
            executive_override=False
        )
        
        # Implement the decision
        await oren._implement_decision(decision)
        
        # Get post-decision metrics
        post_metrics = await oren.monitor_civilization_health()
        
        result = {
            "decision_executed": decision.to_dict(),
            "implementation_status": "completed",
            "impact_analysis": {
                "budget_impact_applied": request.budget_impact,
                "component_health_change": oren.component_status[target_component]["health"],
                "civilization_health_after": post_metrics.overall_health,
                "executive_stress_after": post_metrics.executive_stress_level.value
            },
            "oren_response": f"Executive decision implemented. {request.rationale} Budget impact: ${request.budget_impact:.2f}. ROI expected: {request.expected_roi}%.",
            "api_metadata": {
                "endpoint": "/oren-progresso/decisions/execute",
                "execution_timestamp": datetime.now().isoformat(),
                "ceo_authorization": "granted",
                "decision_number_today": oren.decisions_made_today
            }
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Executive decision execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Decision execution failed: {str(e)}")

@router.get("/decisions/history",
    summary="Executive Decision History",
    description="Get history of CEO decisions and their impact on civilization")
async def get_executive_decision_history(
    limit: int = Query(50, ge=1, le=500, description="Number of decisions to return"),
    decision_type_filter: Optional[str] = Query(None, description="Filter by decision type"),
    component_filter: Optional[str] = Query(None, description="Filter by target component")
) -> Dict[str, Any]:
    """
    Get executive decision history with impact analysis
    """
    try:
        oren = get_oren_orchestration()
        
        # Filter decisions
        decisions = oren.executive_decisions[-limit:] if not decision_type_filter and not component_filter else []
        
        if decision_type_filter or component_filter:
            filtered = oren.executive_decisions
            
            if decision_type_filter:
                try:
                    filter_type = ExecutiveDecisionType(decision_type_filter)
                    filtered = [d for d in filtered if d.decision_type == filter_type]
                except ValueError:
                    raise HTTPException(status_code=400, detail=f"Invalid decision type filter: {decision_type_filter}")
            
            if component_filter:
                try:
                    filter_component = CivilizationComponent(component_filter)
                    filtered = [d for d in filtered if d.target_component == filter_component]
                except ValueError:
                    raise HTTPException(status_code=400, detail=f"Invalid component filter: {component_filter}")
            
            decisions = filtered[-limit:]
        
        # Calculate impact metrics
        total_budget_impact = sum(d.budget_impact for d in decisions)
        decision_type_counts = {}
        component_impact_counts = {}
        
        for decision in decisions:
            decision_type_counts[decision.decision_type.value] = decision_type_counts.get(decision.decision_type.value, 0) + 1
            component_impact_counts[decision.target_component.value] = component_impact_counts.get(decision.target_component.value, 0) + 1
        
        result = {
            "decision_history": [decision.to_dict() for decision in decisions],
            "history_analytics": {
                "total_decisions": len(decisions),
                "total_budget_impact": total_budget_impact,
                "average_roi": sum(d.expected_roi for d in decisions) / len(decisions) if decisions else 0.0,
                "decision_type_breakdown": decision_type_counts,
                "component_impact_breakdown": component_impact_counts,
                "executive_overrides": sum(1 for d in decisions if d.executive_override)
            },
            "current_executive_state": {
                "decisions_made_today": oren.decisions_made_today,
                "budget_saved_today": oren.budget_saved_today,
                "stress_level": oren.current_stress_level.value,
                "override_active": oren.executive_override_active
            },
            "api_metadata": {
                "endpoint": "/oren-progresso/decisions/history",
                "retrieval_timestamp": datetime.now().isoformat(),
                "ceo_oversight": "historical_analysis"
            }
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Decision history retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Decision history failed: {str(e)}")

@router.post("/production/phase-transition",
    summary="Execute Production Phase Transition",
    description="Execute CEO-authorized production phase transition")
async def execute_phase_transition(request: ProductionPhaseRequest) -> Dict[str, Any]:
    """
    Execute production phase transition under CEO authority
    """
    try:
        oren = get_oren_orchestration()
        
        # Validate new phase
        try:
            new_phase = ProductionPhase(request.new_phase)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid production phase: {request.new_phase}")
        
        previous_phase = oren.production_phase
        oren.production_phase = new_phase
        
        # Create decision record for phase transition
        from ..oren_progresso_orchestration import ExecutiveDecision
        
        decision = ExecutiveDecision(
            decision_id=f"PHASE-{int(datetime.now().timestamp())}",
            decision_type=ExecutiveDecisionType.NARRATIVE_RESTRUCTURE,
            target_component=CivilizationComponent.DOCKER_INFRASTRUCTURE,  # Phase changes affect infrastructure
            rationale=f"Production phase transition: {previous_phase.value} → {new_phase.value}. {request.transition_rationale}",
            budget_impact=0.0,  # Phase transitions are typically cost-neutral
            implementation_priority=4,
            expected_roi=200.0,  # High ROI from proper phase management
            stress_trigger=oren.current_stress_level,
            narrative_context=f"CEO-authorized phase transition: {request.transition_rationale}",
            executive_override=True
        )
        
        await oren._implement_decision(decision)
        
        result = {
            "phase_transition": {
                "previous_phase": previous_phase.value,
                "new_phase": new_phase.value,
                "transition_rationale": request.transition_rationale,
                "ceo_authorization": "granted"
            },
            "decision_record": decision.to_dict(),
            "civilization_impact": {
                "components_affected": len(oren.component_status),
                "narrative_threads_updated": len(oren.narrative_threads),
                "budget_implications": "phase_appropriate_resource_allocation"
            },
            "oren_statement": f"Production phase transition authorized. Moving from {previous_phase.value} to {new_phase.value}. {request.transition_rationale} All departments adjust operations accordingly.",
            "api_metadata": {
                "endpoint": "/oren-progresso/production/phase-transition",
                "transition_timestamp": datetime.now().isoformat(),
                "ceo_authority": "executive_override"
            }
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Phase transition failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Phase transition failed: {str(e)}")

@router.get("/budget/allocation",
    summary="Budget Allocation Overview",
    description="Get current budget allocations across civilization components")
async def get_budget_allocation() -> Dict[str, Any]:
    """
    Get detailed budget allocation and utilization data
    """
    try:
        oren = get_oren_orchestration()
        
        # Calculate utilization for each component
        component_utilization = {}
        for component, allocation in oren.budget_allocations.items():
            status = oren.component_status.get(component, {})
            consumption = status.get("budget_consumption", 0.0)
            utilization = consumption / allocation if allocation > 0 else 0.0
            
            component_utilization[component.value] = {
                "allocated": allocation,
                "consumed": consumption,
                "utilization_percent": utilization * 100,
                "remaining": allocation - consumption,
                "health": status.get("health", 0.0),
                "efficiency": status.get("health", 0.0) / max(0.1, utilization) if utilization > 0 else 1.0
            }
        
        # Calculate overall budget metrics
        total_allocated = sum(oren.budget_allocations.values())
        total_consumed = sum(status.get("budget_consumption", 0.0) for status in oren.component_status.values())
        
        result = {
            "budget_overview": {
                "total_allocated": total_allocated,
                "total_consumed": total_consumed,
                "utilization_percent": (total_consumed / total_allocated * 100) if total_allocated > 0 else 0.0,
                "remaining_budget": total_allocated - total_consumed,
                "burn_rate_per_hour": oren._calculate_budget_burn_rate(),
                "savings_achieved_today": oren.budget_saved_today
            },
            "component_allocations": component_utilization,
            "budget_efficiency": {
                "most_efficient": max(component_utilization.items(), key=lambda x: x[1]["efficiency"])[0] if component_utilization else None,
                "least_efficient": min(component_utilization.items(), key=lambda x: x[1]["efficiency"])[0] if component_utilization else None,
                "over_budget_components": [comp for comp, data in component_utilization.items() if data["utilization_percent"] > 100],
                "under_utilized_components": [comp for comp, data in component_utilization.items() if data["utilization_percent"] < 50]
            },
            "executive_controls": {
                "cost_cutting_mode": oren.cost_cutting_mode,
                "budget_authority": oren.budget_authority,
                "decisions_made_today": oren.decisions_made_today,
                "next_budget_review": "daily_00:00_utc"
            },
            "api_metadata": {
                "endpoint": "/oren-progresso/budget/allocation",
                "retrieval_timestamp": datetime.now().isoformat(),
                "ceo_oversight": "budget_monitoring"
            }
        }
        
        return result
        
    except Exception as e:
        log.error(f"❌ Budget allocation retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Budget allocation failed: {str(e)}")

@router.post("/budget/reallocate",
    summary="Execute Budget Reallocation",
    description="Execute CEO-authorized budget reallocation across components")
async def execute_budget_reallocation(request: BudgetAllocationRequest) -> Dict[str, Any]:
    """
    Execute budget reallocation with executive authority
    """
    try:
        oren = get_oren_orchestration()
        
        # Validate component names
        valid_components = set(comp.value for comp in CivilizationComponent)
        invalid_components = set(request.component_allocations.keys()) - valid_components
        
        if invalid_components:
            raise HTTPException(status_code=400, detail=f"Invalid components: {invalid_components}")
        
        # Validate total allocation
        total_requested = sum(request.component_allocations.values())
        if abs(total_requested - request.total_budget) > 0.01:  # Allow small floating point differences
            raise HTTPException(status_code=400, detail=f"Component allocations ({total_requested}) don't match total budget ({request.total_budget})")
        
        # Store previous allocations for impact analysis
        previous_allocations = dict(oren.budget_allocations)
        
        # Apply new allocations
        for component_name, allocation in request.component_allocations.items():
            component = CivilizationComponent(component_name)
            oren.budget_allocations[component] = allocation
        
        # Create decision record
        from ..oren_progresso_orchestration import ExecutiveDecision
        
        decision = ExecutiveDecision(
            decision_id=f"BUDGET-{int(datetime.now().timestamp())}",
            decision_type=ExecutiveDecisionType.RESOURCE_REALLOCATION,
            target_component=CivilizationComponent.API_GATEWAY,  # Affects all components
            rationale=f"Executive budget reallocation across civilization components. Total budget: ${request.total_budget}",
            budget_impact=0.0,  # Reallocation is cost-neutral
            implementation_priority=5,
            expected_roi=150.0,
            stress_trigger=oren.current_stress_level,
            narrative_context="CEO-mandated budget optimization to improve component efficiency and narrative coherence.",
            executive_override=True
        )
        
        await oren._implement_decision(decision)
        
        # Calculate impact analysis
        allocation_changes = {}
        for component in CivilizationComponent:
            old_allocation = previous_allocations.get(component, 0.0)
            new_allocation = oren.budget_allocations.get(component, 0.0)
            change = new_allocation - old_allocation
            allocation_changes[component.value] = {
                "previous": old_allocation,
                "new": new_allocation,
                "change": change,
                "change_percent": (change / old_allocation * 100) if old_allocation > 0 else 0.0
            }
        
        result = {
            "reallocation_executed": {
                "total_budget": request.total_budget,
                "components_affected": len(request.component_allocations),
                "ceo_authorization": "granted"
            },
            "allocation_changes": allocation_changes,
            "decision_record": decision.to_dict(),
            "impact_analysis": {
                "largest_increase": max(allocation_changes.items(), key=lambda x: x[1]["change"])[0] if allocation_changes else None,
                "largest_decrease": min(allocation_changes.items(), key=lambda x: x[1]["change"])[0] if allocation_changes else None,
                "efficiency_improvement_expected": "budget_optimization_algorithms_activated"
            },
            "oren_statement": f"Budget reallocation executed across {len(request.component_allocations)} components. Total budget of ${request.total_budget} strategically distributed for optimal civilization efficiency.",
            "api_metadata": {
                "endpoint": "/oren-progresso/budget/reallocate",
                "reallocation_timestamp": datetime.now().isoformat(),
                "ceo_authority": "budget_control"
            }
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Budget reallocation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Budget reallocation failed: {str(e)}")

@router.get("/character-status",
    summary="CEO Character Status",
    description="Get Oren Progresso's current executive state and consciousness")
async def get_character_status() -> Dict[str, Any]:
    """
    Get Oren Progresso's character consciousness status
    
    Returns:
    - Executive state and decision-making status
    - Civilization oversight metrics
    - Budget authority and financial controls
    - Stress levels and system response patterns
    - Character evidence and quotes
    """
    try:
        oren = get_oren_orchestration()
        status = oren.get_character_status()
        
        # Add real-time metrics
        current_metrics = await oren.monitor_civilization_health()
        
        status["real_time_executive_metrics"] = {
            "current_stress_level": current_metrics.executive_stress_level.value,
            "civilization_health": current_metrics.overall_health,
            "budget_utilization": current_metrics.budget_utilization,
            "production_efficiency": current_metrics.production_efficiency,
            "narrative_coherence": current_metrics.narrative_coherence,
            "status_timestamp": datetime.now().isoformat()
        }
        
        return status
        
    except Exception as e:
        log.error(f"❌ Oren Progresso character status retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Status retrieval failed: {str(e)}")

@router.get("/health",
    summary="Oren Progresso Executive Health Check",
    description="Health check endpoint for CEO orchestration system")
async def character_health_check() -> Dict[str, str]:
    """
    Health check for Oren Progresso's character consciousness
    """
    try:
        oren = get_oren_orchestration()
        
        return {
            "status": "healthy",
            "character": "oren_progresso",
            "system_function": "executive_orchestration_observability",
            "stress_level": oren.current_stress_level.value,
            "production_phase": oren.production_phase.value,
            "budget_authority": str(oren.budget_authority),
            "executive_override_active": str(oren.executive_override_active),
            "decisions_today": str(oren.decisions_made_today),
            "character_quote": "CEO of the whole damn civilization - monitors and controls all productions",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }