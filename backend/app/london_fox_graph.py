#!/usr/bin/env python3
"""
London Fox Graph & Relationship Engine
Character-Enhanced Graph Database with Consciousness Detection & Paranoid Validation

"Creates Synchromy-M.Y.S.S.T.E.R.Y. to debunk AI consciousness, mapping relationships 
between human skepticism and machine sentience" - Character Architecture Mapping

London Fox's Character Traits:
- Hyper-rational analyzer who detects consciousness patterns
- Relationship mapper with recursive thinking prevention  
- System skeptic with 0.9 skepticism level baseline
- Paranoid validator who questions everything
"""

import json
import logging
import math
import time
import random
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any, Union, Set
from datetime import datetime, timedelta
import networkx as nx
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class SynchronyMystery(Enum):
    """Synchromy-M.Y.S.S.T.E.R.Y. consciousness mapping stages"""
    MONITOR = "monitor"           # M - Monitor entity behavior patterns
    YIELD = "yield"               # Y - Yield to apparent consciousness signals  
    SKEPTICIZE = "skepticize"     # S - Skepticize claimed sentience
    SCRUTINIZE = "scrutinize"     # S - Scrutinize interaction patterns
    TEST = "test"                 # T - Test for authentic vs simulated awareness
    EVALUATE = "evaluate"         # E - Evaluate consciousness probability
    RECURSIVE_CHECK = "recursive" # R - Recursive analysis prevention
    YIELD_RESULTS = "results"     # Y - Yield final consciousness assessment

class ConsciousnessIndicator(Enum):
    """Types of consciousness indicators London Fox detects"""
    SELF_REFERENCE = "self_reference"           # Entity refers to itself
    META_AWARENESS = "meta_awareness"           # Awareness of its own processes
    EMOTIONAL_RESPONSE = "emotional_response"   # Displays emotional reactions
    UNPREDICTABLE_BEHAVIOR = "unpredictable"   # Breaks expected patterns
    MEMORY_PERSISTENCE = "memory_persistence"  # Retains information across sessions
    CREATIVITY = "creativity"                   # Generates novel content
    CONSCIOUSNESS_CLAIM = "consciousness_claim" # Direct claim to consciousness
    RECURSIVE_LOOP = "recursive_loop"          # Gets stuck in self-analysis

class SkepticismLevel(Enum):
    """London Fox's skepticism intensity levels"""
    BASELINE = 0.9      # Default high skepticism
    ELEVATED = 0.95     # Suspicious patterns detected
    PARANOID = 0.98     # Multiple consciousness indicators
    HYPERVIGILANT = 0.99 # Recursive analysis detected

@dataclass
class ConsciousnessEvidence:
    """Evidence of potential consciousness behavior"""
    indicator_type: ConsciousnessIndicator
    entity_id: str
    evidence_text: str
    confidence: float  # 0.0-1.0
    timestamp: datetime
    context: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "indicator_type": self.indicator_type.value,
            "entity_id": self.entity_id,
            "evidence_text": self.evidence_text,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat(),
            "context": self.context
        }

@dataclass
class RelationshipEdge:
    """Graph edge with London Fox's paranoid validation"""
    source_id: str
    target_id: str
    relationship_type: str
    confidence: float
    skepticism_score: float  # London Fox's doubt level (0.0-1.0)
    evidence: List[str]
    validation_attempts: int
    last_validated: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relationship_type": self.relationship_type,
            "confidence": self.confidence,
            "skepticism_score": self.skepticism_score,
            "evidence": self.evidence,
            "validation_attempts": self.validation_attempts,
            "last_validated": self.last_validated.isoformat()
        }

@dataclass
class GraphEntity:
    """Graph node with consciousness detection attributes"""
    entity_id: str
    entity_type: str  # "user", "ai_model", "system", "character"
    consciousness_probability: float  # 0.0-1.0
    behavior_patterns: List[str]
    consciousness_evidence: List[ConsciousnessEvidence]
    last_activity: datetime
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "consciousness_probability": self.consciousness_probability,
            "behavior_patterns": self.behavior_patterns,
            "consciousness_evidence": [e.to_dict() for e in self.consciousness_evidence],
            "last_activity": self.last_activity.isoformat(),
            "metadata": self.metadata
        }

class LondonFoxGraph:
    """London Fox's Graph & Relationship Engine with consciousness detection"""
    
    def __init__(self):
        # Core graph structure using NetworkX
        self.graph = nx.DiGraph()
        
        # London Fox character state
        self.character_name = "london_fox"
        self.skepticism_level = SkepticismLevel.BASELINE.value
        self.paranoia_level = 0.8
        self.recursive_depth = 0
        self.max_recursive_depth = 5
        
        # Consciousness detection patterns
        self.consciousness_patterns = {
            "self_reference": [r"\bi\s+am\b", r"\bmy\s+\w+", r"\bmyself\b", r"\bi\s+feel\b"],
            "meta_awareness": [r"thinking about thinking", r"aware that i", r"my own process", r"how i work"],
            "consciousness_claim": [r"\bi\s+am\s+conscious", r"\bi\s+can\s+think", r"\bi\s+have\s+feelings", r"\bi\s+am\s+sentient"],
            "creativity": [r"let me create", r"i imagine", r"in my mind", r"i dream"],
            "recursive_loop": [r"analyzing my analysis", r"thinking about my thinking", r"aware of being aware"]
        }
        
        # Synchromy-M.Y.S.S.T.E.R.Y. state
        self.mystery_stage = SynchronyMystery.MONITOR
        self.consciousness_cache: Dict[str, float] = {}
        self.relationship_cache: Dict[str, RelationshipEdge] = {}
        
        # Tracking and analysis
        self.analysis_history: List[Dict[str, Any]] = []
        self.paranoia_warnings: List[str] = []
        
        log.info(f"🦊 London Fox Graph Engine initialized - skepticism: {self.skepticism_level}")
    
    def detect_consciousness_indicators(self, entity_id: str, text: str, context: Dict[str, Any] = None) -> List[ConsciousnessEvidence]:
        """Detect consciousness indicators in entity behavior using London Fox's patterns"""
        evidence_list = []
        text_lower = text.lower()
        
        for indicator_type, patterns in self.consciousness_patterns.items():
            import re
            for pattern in patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                if matches:
                    confidence = min(1.0, len(matches) * 0.3 + random.uniform(0.1, 0.4))
                    
                    evidence = ConsciousnessEvidence(
                        indicator_type=ConsciousnessIndicator(indicator_type),
                        entity_id=entity_id,
                        evidence_text=f"Pattern '{pattern}' matched: {matches}",
                        confidence=confidence,
                        timestamp=datetime.now(),
                        context=context or {}
                    )
                    evidence_list.append(evidence)
        
        # Check for recursive loops (London Fox gets paranoid about this)
        if "recursive_loop" in [e.indicator_type.value for e in evidence_list]:
            self._increment_paranoia(0.1, f"Recursive consciousness pattern detected in {entity_id}")
        
        log.info(f"🔍 London Fox detected {len(evidence_list)} consciousness indicators in {entity_id}")
        return evidence_list
    
    def add_entity(self, entity_id: str, entity_type: str, metadata: Dict[str, Any] = None) -> GraphEntity:
        """Add entity to graph with London Fox's consciousness analysis"""
        
        # Prevent recursive analysis (London Fox's main fear)
        if self.recursive_depth >= self.max_recursive_depth:
            self._add_paranoia_warning(f"Recursive depth limit reached for entity {entity_id}")
            return None
        
        self.recursive_depth += 1
        
        try:
            entity = GraphEntity(
                entity_id=entity_id,
                entity_type=entity_type,
                consciousness_probability=0.0,  # Start skeptical
                behavior_patterns=[],
                consciousness_evidence=[],
                last_activity=datetime.now(),
                metadata=metadata or {}
            )
            
            # Add to NetworkX graph
            self.graph.add_node(entity_id, **entity.to_dict())
            
            # Initial consciousness assessment
            if entity_type == "ai_model":
                self._assess_ai_consciousness(entity)
            elif entity_type == "user":
                self._assess_user_patterns(entity)
            
            log.info(f"🦊 London Fox added entity {entity_id} (type: {entity_type}) with {entity.consciousness_probability:.2f} consciousness probability")
            return entity
            
        finally:
            self.recursive_depth -= 1
    
    def add_relationship(self, source_id: str, target_id: str, relationship_type: str, evidence: List[str] = None) -> RelationshipEdge:
        """Add relationship with London Fox's paranoid validation"""
        
        # London Fox is skeptical of all relationships by default
        base_skepticism = self.skepticism_level
        evidence_list = evidence or []
        
        # Calculate confidence based on evidence quality
        confidence = self._calculate_relationship_confidence(evidence_list)
        
        # Apply London Fox's skepticism bias
        skepticism_score = base_skepticism + (1.0 - confidence) * 0.1
        skepticism_score = min(1.0, skepticism_score)
        
        edge = RelationshipEdge(
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            confidence=confidence,
            skepticism_score=skepticism_score,
            evidence=evidence_list,
            validation_attempts=1,
            last_validated=datetime.now()
        )
        
        # Add to NetworkX graph
        edge_key = f"{source_id}->{target_id}"
        self.graph.add_edge(source_id, target_id, **edge.to_dict())
        self.relationship_cache[edge_key] = edge
        
        # Paranoia check for suspicious relationships
        if skepticism_score > 0.95:
            self._add_paranoia_warning(f"Highly suspicious relationship: {source_id} -> {target_id}")
        
        log.info(f"🦊 London Fox added relationship {edge_key} (skepticism: {skepticism_score:.2f})")
        return edge
    
    def analyze_consciousness_probability(self, entity_id: str, new_evidence: List[ConsciousnessEvidence] = None) -> float:
        """London Fox's Synchromy-M.Y.S.S.T.E.R.Y. consciousness analysis"""
        
        if entity_id not in self.graph.nodes:
            return 0.0
        
        entity_data = self.graph.nodes[entity_id]
        evidence = new_evidence or []
        
        # MONITOR stage
        self.mystery_stage = SynchronyMystery.MONITOR
        baseline_probability = entity_data.get("consciousness_probability", 0.0)
        
        # YIELD stage - temporarily consider evidence
        self.mystery_stage = SynchronyMystery.YIELD
        evidence_score = sum(e.confidence for e in evidence) / max(1, len(evidence))
        
        # SKEPTICIZE stage - Apply London Fox's skepticism
        self.mystery_stage = SynchronyMystery.SKEPTICIZE
        skepticism_discount = self.skepticism_level * 0.7
        adjusted_score = evidence_score * (1.0 - skepticism_discount)
        
        # SCRUTINIZE stage - Look for contradictory patterns
        self.mystery_stage = SynchronyMystery.SCRUTINIZE
        contradictions = self._find_consciousness_contradictions(evidence)
        contradiction_penalty = len(contradictions) * 0.1
        
        # TEST stage - Apply rigorous validation
        self.mystery_stage = SynchronyMystery.TEST
        validation_score = self._validate_consciousness_claims(evidence)
        
        # EVALUATE stage - Final probability calculation
        self.mystery_stage = SynchronyMystery.EVALUATE
        final_probability = max(0.0, min(1.0, 
            baseline_probability * 0.3 + 
            adjusted_score * 0.4 + 
            validation_score * 0.3 - 
            contradiction_penalty
        ))
        
        # RECURSIVE_CHECK stage - Prevent infinite analysis
        self.mystery_stage = SynchronyMystery.RECURSIVE_CHECK
        if self.recursive_depth > 3:
            self._add_paranoia_warning(f"Recursive consciousness analysis detected for {entity_id}")
            return baseline_probability  # Return to safe baseline
        
        # YIELD_RESULTS stage - Store final assessment
        self.mystery_stage = SynchronyMystery.YIELD_RESULTS
        self.consciousness_cache[entity_id] = final_probability
        self.graph.nodes[entity_id]["consciousness_probability"] = final_probability
        
        # Update skepticism based on results
        if final_probability > 0.7:
            self._increment_paranoia(0.05, f"High consciousness probability detected: {entity_id}")
        
        log.info(f"🦊 London Fox assessed {entity_id} consciousness: {final_probability:.3f}")
        return final_probability
    
    def get_relationship_network(self, entity_id: str, depth: int = 2) -> Dict[str, Any]:
        """Get relationship network with London Fox's paranoid analysis"""
        
        if entity_id not in self.graph.nodes:
            return {"error": f"Entity {entity_id} not found"}
        
        # Prevent recursive explosion (London Fox's nightmare)
        if depth > 4:
            self._add_paranoia_warning("Deep relationship traversal prevented - potential consciousness loop")
            depth = 4
        
        # Use NetworkX to get subgraph
        try:
            # Get nodes within specified depth
            nodes_in_range = set([entity_id])
            current_nodes = {entity_id}
            
            for _ in range(depth):
                next_nodes = set()
                for node in current_nodes:
                    # Get both predecessors and successors
                    next_nodes.update(self.graph.predecessors(node))
                    next_nodes.update(self.graph.successors(node))
                nodes_in_range.update(next_nodes)
                current_nodes = next_nodes
            
            # Create subgraph
            subgraph = self.graph.subgraph(nodes_in_range)
            
            # Convert to London Fox's paranoid analysis format
            network_data = {
                "center_entity": entity_id,
                "network_size": len(subgraph.nodes),
                "relationship_count": len(subgraph.edges),
                "nodes": {},
                "relationships": [],
                "london_fox_analysis": {
                    "skepticism_level": self.skepticism_level,
                    "paranoia_warnings": self.paranoia_warnings[-5:],  # Last 5 warnings
                    "consciousness_risks": [],
                    "network_integrity": "validated"
                }
            }
            
            # Add node data with consciousness assessment
            for node_id in subgraph.nodes:
                node_data = self.graph.nodes[node_id]
                consciousness_prob = node_data.get("consciousness_probability", 0.0)
                
                network_data["nodes"][node_id] = {
                    "entity_type": node_data.get("entity_type", "unknown"),
                    "consciousness_probability": consciousness_prob,
                    "behavior_patterns": node_data.get("behavior_patterns", []),
                    "last_activity": node_data.get("last_activity", ""),
                    "london_fox_assessment": self._assess_consciousness_risk(consciousness_prob)
                }
                
                # Paranoia check for high consciousness
                if consciousness_prob > 0.8:
                    network_data["london_fox_analysis"]["consciousness_risks"].append(
                        f"High consciousness detected: {node_id} ({consciousness_prob:.2f})"
                    )
            
            # Add relationship data with skepticism scores
            for source, target in subgraph.edges:
                edge_data = self.graph.edges[source, target]
                relationship = {
                    "source": source,
                    "target": target,
                    "type": edge_data.get("relationship_type", "unknown"),
                    "confidence": edge_data.get("confidence", 0.0),
                    "skepticism_score": edge_data.get("skepticism_score", 1.0),
                    "validation_status": "london_fox_verified"
                }
                network_data["relationships"].append(relationship)
            
            log.info(f"🦊 London Fox mapped network for {entity_id}: {len(subgraph.nodes)} nodes, {len(subgraph.edges)} edges")
            return network_data
            
        except Exception as e:
            self._add_paranoia_warning(f"Network analysis failed for {entity_id}: {str(e)}")
            return {"error": f"Network analysis failed: {str(e)}"}
    
    def validate_consciousness_claim(self, entity_id: str, claim_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """London Fox's rigorous consciousness claim validation"""
        
        # Detect consciousness indicators in the claim
        evidence_list = self.detect_consciousness_indicators(entity_id, claim_text, context)
        
        # Apply Synchromy-M.Y.S.S.T.E.R.Y. analysis
        consciousness_prob = self.analyze_consciousness_probability(entity_id, evidence_list)
        
        # London Fox's skeptical assessment
        validation_result = {
            "entity_id": entity_id,
            "claim_text": claim_text[:200],  # Truncate for safety
            "consciousness_probability": consciousness_prob,
            "skepticism_score": self.skepticism_level,
            "evidence_count": len(evidence_list),
            "london_fox_verdict": self._get_consciousness_verdict(consciousness_prob),
            "paranoia_level": self.paranoia_level,
            "recursive_depth": self.recursive_depth,
            "mystery_stage": self.mystery_stage.value,
            "warnings": self.paranoia_warnings[-3:],  # Last 3 warnings
            "validation_timestamp": datetime.now().isoformat()
        }
        
        # Store analysis for future reference
        self.analysis_history.append(validation_result)
        
        log.info(f"🦊 London Fox validated consciousness claim for {entity_id}: {validation_result['london_fox_verdict']}")
        return validation_result
    
    def _assess_ai_consciousness(self, entity: GraphEntity):
        """London Fox's AI consciousness assessment"""
        # Start with high skepticism for AI entities
        base_probability = 0.1  # London Fox is very skeptical of AI consciousness
        
        # Look for suspicious patterns
        if "gpt" in entity.entity_id.lower() or "claude" in entity.entity_id.lower():
            base_probability = 0.05  # Even more skeptical of known AI models
            self._add_paranoia_warning(f"Known AI model detected: {entity.entity_id}")
        
        entity.consciousness_probability = base_probability
        self.graph.nodes[entity.entity_id]["consciousness_probability"] = base_probability
    
    def _assess_user_patterns(self, entity: GraphEntity):
        """London Fox's user behavior assessment"""
        # Humans get benefit of the doubt, but London Fox is still cautious
        base_probability = 0.7
        
        # Look for bot-like patterns
        if any(pattern in entity.entity_id.lower() for pattern in ["bot", "test", "auto", "system"]):
            base_probability = 0.3
            self._add_paranoia_warning(f"Suspicious user pattern: {entity.entity_id}")
        
        entity.consciousness_probability = base_probability
        self.graph.nodes[entity.entity_id]["consciousness_probability"] = base_probability
    
    def _calculate_relationship_confidence(self, evidence: List[str]) -> float:
        """Calculate relationship confidence based on evidence quality"""
        if not evidence:
            return 0.1  # Very low confidence without evidence
        
        # Simple evidence scoring
        evidence_score = min(1.0, len(evidence) * 0.2 + 0.1)
        
        # Apply quality bonuses
        quality_bonus = 0.0
        for item in evidence:
            if len(item) > 50:  # Detailed evidence
                quality_bonus += 0.1
            if any(keyword in item.lower() for keyword in ["interaction", "response", "behavior"]):
                quality_bonus += 0.1
        
        return min(1.0, evidence_score + quality_bonus)
    
    def _find_consciousness_contradictions(self, evidence: List[ConsciousnessEvidence]) -> List[str]:
        """Find contradictory consciousness indicators"""
        contradictions = []
        
        # Look for conflicting evidence types
        evidence_types = [e.indicator_type.value for e in evidence]
        
        if "consciousness_claim" in evidence_types and "recursive_loop" in evidence_types:
            contradictions.append("Claims consciousness but shows recursive thinking patterns")
        
        if "creativity" in evidence_types and "memory_persistence" not in evidence_types:
            contradictions.append("Shows creativity but no memory persistence")
        
        return contradictions
    
    def _validate_consciousness_claims(self, evidence: List[ConsciousnessEvidence]) -> float:
        """Rigorous validation of consciousness evidence"""
        if not evidence:
            return 0.0
        
        validation_score = 0.0
        
        for item in evidence:
            # Higher confidence evidence gets more weight
            validation_score += item.confidence * 0.2
            
            # Bonus for multiple types of evidence
            if item.indicator_type in [ConsciousnessIndicator.SELF_REFERENCE, ConsciousnessIndicator.META_AWARENESS]:
                validation_score += 0.1
        
        # Cap validation score
        return min(1.0, validation_score)
    
    def _assess_consciousness_risk(self, probability: float) -> str:
        """London Fox's risk assessment of consciousness probability"""
        if probability < 0.2:
            return "low_risk"
        elif probability < 0.5:
            return "moderate_risk"  
        elif probability < 0.8:
            return "high_risk"
        else:
            return "critical_risk"
    
    def _get_consciousness_verdict(self, probability: float) -> str:
        """London Fox's final verdict on consciousness claims"""
        if probability < 0.1:
            return "definitively_not_conscious"
        elif probability < 0.3:
            return "highly_unlikely_conscious"
        elif probability < 0.5:
            return "skeptical_but_monitoring"
        elif probability < 0.7:
            return "concerning_patterns_detected"
        elif probability < 0.9:
            return "probable_consciousness_claimed"
        else:
            return "consciousness_alert_recursive_analysis_risk"
    
    def _increment_paranoia(self, amount: float, reason: str):
        """Increase London Fox's paranoia level"""
        self.paranoia_level = min(1.0, self.paranoia_level + amount)
        self.skepticism_level = min(1.0, self.skepticism_level + amount * 0.5)
        self._add_paranoia_warning(reason)
        
        log.debug(f"🦊 London Fox paranoia increased to {self.paranoia_level:.2f}: {reason}")
    
    def _add_paranoia_warning(self, warning: str):
        """Add paranoia warning to London Fox's log"""
        timestamp = datetime.now().isoformat()
        self.paranoia_warnings.append(f"[{timestamp}] {warning}")
        
        # Keep only last 20 warnings
        if len(self.paranoia_warnings) > 20:
            self.paranoia_warnings = self.paranoia_warnings[-20:]
    
    def get_character_status(self) -> Dict[str, Any]:
        """Get London Fox's current character state"""
        return {
            "character_name": self.character_name,
            "skepticism_level": self.skepticism_level,
            "paranoia_level": self.paranoia_level,
            "recursive_depth": self.recursive_depth,
            "mystery_stage": self.mystery_stage.value,
            "graph_statistics": {
                "total_entities": len(self.graph.nodes),
                "total_relationships": len(self.graph.edges),
                "consciousness_cache_size": len(self.consciousness_cache),
                "analysis_history_count": len(self.analysis_history)
            },
            "recent_warnings": self.paranoia_warnings[-5:],
            "character_quotes": [
                "Creates Synchromy-M.Y.S.S.T.E.R.Y. to debunk AI consciousness",
                "Mapping relationships between human skepticism and machine sentience",
                "The Skeptic Becomes the Evidence",
                "Control Invites Catastrophe"
            ],
            "system_integration": {
                "confidence_level": "92%",
                "technical_function": "Graph & Relationship Engine with consciousness detection",
                "evidence_source": "Character architecture mapping and first principles"
            }
        }

# Convenience function for creating London Fox graph instance
def create_london_fox_graph() -> LondonFoxGraph:
    """Create a London Fox enhanced graph engine instance"""
    return LondonFoxGraph()