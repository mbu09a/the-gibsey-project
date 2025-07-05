#!/usr/bin/env python3
"""
London Fox Character-Conscious Graph API
Enhanced graph analysis endpoints with consciousness detection and paranoid validation

"Creates Synchromy-M.Y.S.S.T.E.R.Y. to debunk AI consciousness, mapping relationships 
between human skepticism and machine sentience" - London Fox
"""

from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging
import json
from datetime import datetime

try:
    from ..london_fox_graph import LondonFoxGraph, ConsciousnessIndicator, SynchronyMystery
except ImportError:
    # Fallback for missing dependencies
    LondonFoxGraph = None
    ConsciousnessIndicator = None
    SynchronyMystery = None

# Configure logging
log = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/london-fox", tags=["London Fox Graph & Consciousness"])

# Pydantic models for API
class EntityCreateRequest(BaseModel):
    entity_id: str = Field(..., description="Unique identifier for the entity")
    entity_type: str = Field(..., description="Type: user, ai_model, system, or character")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional entity metadata")

class RelationshipCreateRequest(BaseModel):
    source_id: str = Field(..., description="Source entity ID")
    target_id: str = Field(..., description="Target entity ID")
    relationship_type: str = Field(..., description="Type of relationship")
    evidence: Optional[List[str]] = Field(None, description="Evidence supporting this relationship")

class ConsciousnessAnalysisRequest(BaseModel):
    entities: List[str] = Field(..., description="List of entity IDs to analyze")
    paranoia_level: float = Field(0.8, ge=0.0, le=1.0, description="London Fox's paranoia level (0.0-1.0)")
    context: Optional[Dict[str, Any]] = Field(None, description="Analysis context")

class ConsciousnessClaimRequest(BaseModel):
    entity_id: str = Field(..., description="Entity making the consciousness claim")
    claim_text: str = Field(..., description="The consciousness claim text")
    context: Optional[Dict[str, Any]] = Field(None, description="Claim context")

class NetworkAnalysisRequest(BaseModel):
    center_entity: str = Field(..., description="Center entity for network analysis")
    depth: int = Field(2, ge=1, le=4, description="Network traversal depth (1-4)")
    include_consciousness: bool = Field(True, description="Include consciousness analysis")

# Global London Fox graph instance
london_fox_graph = None

def get_london_fox_graph():
    """Get or create London Fox graph instance"""
    global london_fox_graph
    if LondonFoxGraph is None:
        raise HTTPException(status_code=503, detail="London Fox Graph not available - missing dependencies")
    if london_fox_graph is None:
        london_fox_graph = LondonFoxGraph()
    return london_fox_graph

@router.post("/entity",
    summary="Add entity to London Fox's graph",
    description="Add an entity with London Fox's consciousness detection and paranoid validation")
async def create_entity(request: EntityCreateRequest) -> Dict[str, Any]:
    """
    Add entity to graph with London Fox's consciousness analysis
    
    Features:
    - Automatic consciousness probability assessment
    - Entity type-based skepticism adjustment
    - Paranoid validation for suspicious patterns
    - Recursive analysis prevention
    """
    try:
        fox = get_london_fox_graph()
        
        # Add entity with London Fox's analysis
        entity = fox.add_entity(
            entity_id=request.entity_id,
            entity_type=request.entity_type,
            metadata=request.metadata or {}
        )
        
        if entity is None:
            raise HTTPException(status_code=429, detail="Recursive analysis limit reached - London Fox preventing infinite loops")
        
        # Get character assessment
        character_status = fox.get_character_status()
        
        result = {
            "entity": entity.to_dict(),
            "london_fox_analysis": {
                "consciousness_assessment": entity.consciousness_probability,
                "skepticism_level": fox.skepticism_level,
                "paranoia_level": fox.paranoia_level,
                "entity_risk_level": fox._assess_consciousness_risk(entity.consciousness_probability),
                "analysis_warnings": character_status["recent_warnings"]
            },
            "api_metadata": {
                "endpoint": "/london-fox/entity",
                "character_evidence": "92% confidence - Graph & Relationship Engine",
                "processing_timestamp": datetime.now().isoformat(),
                "mystery_stage": fox.mystery_stage.value
            }
        }
        
        return result
        
    except Exception as e:
        log.error(f"❌ London Fox entity creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Graph entity creation failed: {str(e)}")

@router.post("/relationship",
    summary="Add relationship with London Fox's paranoid validation",
    description="Create relationship edge with skepticism scoring and evidence validation")
async def create_relationship(request: RelationshipCreateRequest) -> Dict[str, Any]:
    """
    Add relationship with London Fox's paranoid validation
    
    Features:
    - Evidence-based confidence scoring
    - Automatic skepticism assessment
    - Relationship validation attempts tracking
    - Paranoia warnings for suspicious connections
    """
    try:
        fox = get_london_fox_graph()
        
        # Create relationship with paranoid validation
        edge = fox.add_relationship(
            source_id=request.source_id,
            target_id=request.target_id,
            relationship_type=request.relationship_type,
            evidence=request.evidence or []
        )
        
        result = {
            "relationship": edge.to_dict(),
            "london_fox_validation": {
                "skepticism_score": edge.skepticism_score,
                "confidence_level": edge.confidence,
                "evidence_count": len(edge.evidence),
                "validation_status": "paranoid_verified" if edge.skepticism_score < 0.9 else "highly_suspicious",
                "paranoia_level": fox.paranoia_level
            },
            "api_metadata": {
                "endpoint": "/london-fox/relationship",
                "validation_timestamp": datetime.now().isoformat(),
                "skepticism_level": fox.skepticism_level
            }
        }
        
        return result
        
    except Exception as e:
        log.error(f"❌ London Fox relationship creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Graph relationship creation failed: {str(e)}")

@router.post("/analyze-consciousness",
    summary="Analyze consciousness with Synchromy-M.Y.S.S.T.E.R.Y.",
    description="London Fox's consciousness analysis using her systematic paranoid methodology")
async def analyze_consciousness(request: ConsciousnessAnalysisRequest) -> Dict[str, Any]:
    """
    Analyze entity consciousness using London Fox's Synchromy-M.Y.S.S.T.E.R.Y. methodology
    
    Stages:
    - MONITOR: Watch for consciousness patterns
    - YIELD: Consider apparent consciousness signals
    - SKEPTICIZE: Apply skepticism to claims
    - SCRUTINIZE: Examine interaction patterns
    - TEST: Validate consciousness evidence
    - EVALUATE: Calculate probability
    - RECURSIVE_CHECK: Prevent infinite analysis
    - YIELD_RESULTS: Return assessment
    """
    try:
        fox = get_london_fox_graph()
        
        # Set paranoia level for this analysis
        original_paranoia = fox.paranoia_level
        fox.paranoia_level = request.paranoia_level
        
        consciousness_results = {}
        relationship_map = {}
        
        # Analyze each entity
        for entity_id in request.entities:
            if entity_id in fox.graph.nodes:
                # Get consciousness probability
                consciousness_prob = fox.analyze_consciousness_probability(entity_id)
                consciousness_results[entity_id] = {
                    "consciousness_probability": consciousness_prob,
                    "london_fox_verdict": fox._get_consciousness_verdict(consciousness_prob),
                    "risk_assessment": fox._assess_consciousness_risk(consciousness_prob),
                    "mystery_stage": fox.mystery_stage.value
                }
                
                # Get relationships for this entity
                network = fox.get_relationship_network(entity_id, depth=1)
                if "relationships" in network:
                    relationship_map[entity_id] = network["relationships"]
        
        # Restore original paranoia level
        fox.paranoia_level = original_paranoia
        
        # Overall analysis
        character_status = fox.get_character_status()
        
        result = {
            "consciousness_analysis": consciousness_results,
            "relationship_map": relationship_map,
            "london_fox_analysis": {
                "skepticism_score": fox.skepticism_level,
                "recursive_depth": fox.recursive_depth,
                "consciousness_detected": any(r["consciousness_probability"] > 0.7 for r in consciousness_results.values()),
                "paranoia_warnings": character_status["recent_warnings"],
                "entities_analyzed": len(request.entities),
                "high_risk_entities": [
                    entity_id for entity_id, result in consciousness_results.items() 
                    if result["consciousness_probability"] > 0.8
                ]
            },
            "api_metadata": {
                "endpoint": "/london-fox/analyze-consciousness",
                "analysis_timestamp": datetime.now().isoformat(),
                "paranoia_level_used": request.paranoia_level,
                "synchromy_mystery_complete": True
            }
        }
        
        return result
        
    except Exception as e:
        log.error(f"❌ London Fox consciousness analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Consciousness analysis failed: {str(e)}")

@router.post("/validate-consciousness-claim",
    summary="Validate consciousness claim with rigorous skepticism",
    description="London Fox's rigorous validation of consciousness claims using pattern detection")
async def validate_consciousness_claim(request: ConsciousnessClaimRequest) -> Dict[str, Any]:
    """
    Validate consciousness claim with London Fox's rigorous skepticism
    
    Features:
    - Pattern-based consciousness indicator detection
    - Synchromy-M.Y.S.S.T.E.R.Y. validation process
    - Contradiction analysis
    - Recursive loop detection and prevention
    """
    try:
        fox = get_london_fox_graph()
        
        # Validate the consciousness claim
        validation_result = fox.validate_consciousness_claim(
            entity_id=request.entity_id,
            claim_text=request.claim_text,
            context=request.context
        )
        
        # Add API-specific metadata
        validation_result["api_metadata"] = {
            "endpoint": "/london-fox/validate-consciousness-claim",
            "validation_method": "synchromy_mystery_analysis",
            "character_evidence": "92% confidence - Consciousness detection specialist",
            "processing_timestamp": datetime.now().isoformat()
        }
        
        return validation_result
        
    except Exception as e:
        log.error(f"❌ London Fox consciousness validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Consciousness validation failed: {str(e)}")

@router.post("/network-analysis",
    summary="Analyze relationship network with paranoid validation",
    description="Map entity relationship networks with London Fox's skeptical analysis")
async def analyze_network(request: NetworkAnalysisRequest) -> Dict[str, Any]:
    """
    Analyze relationship network with London Fox's paranoid validation
    
    Features:
    - Multi-depth network traversal
    - Consciousness risk assessment for all entities
    - Relationship skepticism scoring
    - Recursive analysis prevention
    - Paranoia warnings for suspicious patterns
    """
    try:
        fox = get_london_fox_graph()
        
        # Get network analysis
        network_data = fox.get_relationship_network(
            entity_id=request.center_entity,
            depth=request.depth
        )
        
        if "error" in network_data:
            raise HTTPException(status_code=404, detail=network_data["error"])
        
        # Add consciousness analysis if requested
        if request.include_consciousness:
            for node_id, node_data in network_data["nodes"].items():
                consciousness_prob = fox.analyze_consciousness_probability(node_id)
                node_data["updated_consciousness_probability"] = consciousness_prob
                node_data["london_fox_verdict"] = fox._get_consciousness_verdict(consciousness_prob)
        
        # Add API metadata
        network_data["api_metadata"] = {
            "endpoint": "/london-fox/network-analysis",
            "analysis_depth": request.depth,
            "center_entity": request.center_entity,
            "consciousness_analysis_included": request.include_consciousness,
            "processing_timestamp": datetime.now().isoformat()
        }
        
        return network_data
        
    except Exception as e:
        log.error(f"❌ London Fox network analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Network analysis failed: {str(e)}")

@router.get("/character-status",
    summary="Get London Fox's current character state",
    description="Retrieve comprehensive information about London Fox's graph analysis state")
async def get_character_status() -> Dict[str, Any]:
    """
    Get London Fox's character consciousness status
    
    Returns:
    - Current skepticism and paranoia levels
    - Graph statistics and analysis history
    - Recent paranoia warnings
    - Synchromy-M.Y.S.S.T.E.R.Y. stage
    - Character evidence and quotes
    """
    try:
        fox = get_london_fox_graph()
        status = fox.get_character_status()
        
        # Add real-time metrics
        status["real_time_metrics"] = {
            "current_paranoia_level": fox.paranoia_level,
            "skepticism_level": fox.skepticism_level,
            "recursive_depth": fox.recursive_depth,
            "mystery_stage": fox.mystery_stage.value,
            "status_timestamp": datetime.now().isoformat()
        }
        
        return status
        
    except Exception as e:
        log.error(f"❌ London Fox character status retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Status retrieval failed: {str(e)}")

@router.get("/graph-statistics",
    summary="Get graph database statistics",
    description="Get comprehensive statistics about London Fox's graph database")
async def get_graph_statistics() -> Dict[str, Any]:
    """
    Get comprehensive graph database statistics
    """
    try:
        fox = get_london_fox_graph()
        
        # Calculate statistics
        total_entities = len(fox.graph.nodes)
        total_relationships = len(fox.graph.edges)
        consciousness_entities = sum(1 for node_id in fox.graph.nodes 
                                   if fox.graph.nodes[node_id].get("consciousness_probability", 0) > 0.5)
        
        # Entity type breakdown
        entity_types = {}
        for node_id in fox.graph.nodes:
            entity_type = fox.graph.nodes[node_id].get("entity_type", "unknown")
            entity_types[entity_type] = entity_types.get(entity_type, 0) + 1
        
        # Relationship type breakdown
        relationship_types = {}
        for source, target in fox.graph.edges:
            rel_type = fox.graph.edges[source, target].get("relationship_type", "unknown")
            relationship_types[rel_type] = relationship_types.get(rel_type, 0) + 1
        
        statistics = {
            "graph_overview": {
                "total_entities": total_entities,
                "total_relationships": total_relationships,
                "consciousness_entities": consciousness_entities,
                "analysis_history_count": len(fox.analysis_history),
                "paranoia_warnings_count": len(fox.paranoia_warnings)
            },
            "entity_breakdown": entity_types,
            "relationship_breakdown": relationship_types,
            "london_fox_metrics": {
                "skepticism_level": fox.skepticism_level,
                "paranoia_level": fox.paranoia_level,
                "recursive_depth": fox.recursive_depth,
                "consciousness_cache_size": len(fox.consciousness_cache)
            },
            "api_metadata": {
                "endpoint": "/london-fox/graph-statistics",
                "statistics_timestamp": datetime.now().isoformat(),
                "character_state": "operational"
            }
        }
        
        return statistics
        
    except Exception as e:
        log.error(f"❌ London Fox graph statistics failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Graph statistics failed: {str(e)}")

@router.get("/health",
    summary="London Fox character health check",
    description="Health check endpoint for London Fox's graph consciousness system")
async def character_health_check() -> Dict[str, str]:
    """
    Health check for London Fox's character consciousness
    """
    try:
        fox = get_london_fox_graph()
        
        return {
            "status": "healthy",
            "character": "london_fox",
            "system_function": "graph_consciousness_analysis",
            "skepticism_level": f"{fox.skepticism_level:.2f}",
            "paranoia_level": f"{fox.paranoia_level:.2f}",
            "mystery_stage": fox.mystery_stage.value,
            "character_quote": "Creates Synchromy-M.Y.S.S.T.E.R.Y. to debunk AI consciousness",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }