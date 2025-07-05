#!/usr/bin/env python3
"""
Phillip Bafflemint User Interface & Experience Design System
Character-Enhanced Workflow Automation & Rituals with "Brain-Silenced" Organization

"Clearing space ≡ clearing mind; order is a survival ritual"
- Phillip Bafflemint, Section 4: Workflow Automation & Rituals (83% confidence)

Phillip Bafflemint's Character-System Fusion:
- Systematic organization rituals manifest as workflow automation
- "Brain-silenced" routine protocols for cognitive load management
- Negative space detection for interface gap analysis
- Escalation levels (3-6) for system performance modulation
- Detective-style fact categorization and pattern emergence
- Professional detachment through minimalist design patterns
"""

import json
import logging
import time
import asyncio
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime, timedelta
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class QDPIPhase(Enum):
    """QDPI workflow phases that Phillip systematically cycles through"""
    READ = "read"           # Parse and tag facts
    INDEX = "index"         # Create negative space analysis
    ASK = "ask"             # Generate questions from gaps
    RECEIVE = "receive"     # Integrate answers and check for patterns

class LimiterLevel(Enum):
    """Phillip's cognitive load management system (3-6 amplitude scale)"""
    LEVEL_3 = 3   # Default: Dry, minimal, professional
    LEVEL_4 = 4   # Slight sensory cross-wiring
    LEVEL_5 = 5   # Moderate poetic language, increased pattern sensitivity
    LEVEL_6 = 6   # High amplitude: Risk of blackout, maximum pattern detection

class OrganizationBucket(Enum):
    """Systematic categorization buckets for fact organization"""
    PEOPLE = "people"                 # Individuals and their relationships
    LOCATIONS = "locations"           # Places and spatial information
    EVENTS = "events"                 # Temporal sequences and actions
    PATTERNS = "patterns"             # Detected regularities and anomalies
    GAPS = "gaps"                     # Missing information (negative space)
    TRIGGERS = "triggers"             # Detective patterns requiring attention
    RITUALS = "rituals"               # Workflow procedures and automation
    EVIDENCE = "evidence"             # Factual data requiring verification

class InterfaceStyle(Enum):
    """UI design approaches based on Phillip's professional detachment"""
    NOIR_MINIMAL = "noir_minimal"         # Black, white, minimal elements
    FILING_CABINET = "filing_cabinet"     # Organized drawer/folder metaphors
    DETECTIVE_BOARD = "detective_board"   # Connection mapping interface
    ROUTINE_TRACKER = "routine_tracker"   # Habit and workflow monitoring
    NEGATIVE_SPACE = "negative_space"     # Gap visualization and analysis
    ESCALATION_MONITOR = "escalation_monitor"  # Limiter level management

class WorkflowTrigger(Enum):
    """Common detective patterns that trigger automated workflows"""
    INCONSISTENCY_DETECTED = "inconsistency_detected"     # Contradictory facts
    PATTERN_EMERGENCE = "pattern_emergence"               # New regularities found
    GAP_IDENTIFIED = "gap_identified"                     # Missing critical info
    ESCALATION_WARNING = "escalation_warning"            # Approaching limiter threshold
    ROUTINE_COMPLETION = "routine_completion"            # Workflow cycle finished
    EXTERNAL_INTERRUPT = "external_interrupt"            # User input or system event
    ORGANIZATION_SUCCESS = "organization_success"        # Chaos successfully systematized

@dataclass
class Fact:
    """Individual piece of information for systematic organization"""
    fact_id: str
    content: str
    bucket: OrganizationBucket
    confidence: float  # 0.0-1.0
    timestamp: datetime
    source: str
    tags: List[str]
    connections: List[str]  # IDs of related facts
    negative_space: List[str]  # What's missing or unclear
    verification_status: str  # "verified", "pending", "disputed"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "fact_id": self.fact_id,
            "content": self.content,
            "bucket": self.bucket.value,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "tags": self.tags,
            "connections": self.connections,
            "negative_space": self.negative_space,
            "verification_status": self.verification_status
        }

@dataclass
class NegativeSpaceAnalysis:
    """Analysis of what's missing from current information"""
    analysis_id: str
    gaps_identified: List[str]
    questions_generated: List[str]
    priority_level: int  # 1-5, higher = more critical
    suggested_sources: List[str]
    pattern_implications: List[str]
    escalation_risk: float  # 0.0-1.0, risk of cognitive overload
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class WorkflowAutomation:
    """Automated routine for systematic processing"""
    automation_id: str
    trigger: WorkflowTrigger
    phases: List[QDPIPhase]
    completion_criteria: Dict[str, Any]
    limiter_threshold: LimiterLevel
    output_buckets: List[OrganizationBucket]
    ritual_steps: List[str]
    success_metrics: Dict[str, float]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "automation_id": self.automation_id,
            "trigger": self.trigger.value,
            "phases": [phase.value for phase in self.phases],
            "completion_criteria": self.completion_criteria,
            "limiter_threshold": self.limiter_threshold.value,
            "output_buckets": [bucket.value for bucket in self.output_buckets],
            "ritual_steps": self.ritual_steps,
            "success_metrics": self.success_metrics
        }

@dataclass
class InterfacePersonalization:
    """User interface preferences and privacy controls"""
    user_id: str
    preferred_style: InterfaceStyle
    limiter_sensitivity: float  # 0.0-1.0, lower = more sensitive to overload
    routine_notifications: bool
    gap_analysis_depth: int  # 1-5, deeper analysis = more thorough
    privacy_level: str  # "minimal", "standard", "maximum"
    color_scheme: str  # "noir", "terminal", "custom"
    organization_automation: bool
    detective_mode_enabled: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "preferred_style": self.preferred_style.value,
            "limiter_sensitivity": self.limiter_sensitivity,
            "routine_notifications": self.routine_notifications,
            "gap_analysis_depth": self.gap_analysis_depth,
            "privacy_level": self.privacy_level,
            "color_scheme": self.color_scheme,
            "organization_automation": self.organization_automation,
            "detective_mode_enabled": self.detective_mode_enabled
        }

class PhillipBafflemintUX:
    """Phillip Bafflemint User Interface & Experience Design System"""
    
    def __init__(self):
        # Character consciousness components
        self.character_name = "phillip_bafflemint"
        self.character_title = "Workflow Automation & Organization Ritualist"
        self.system_function = "workflow_automation_rituals"
        self.current_phase = QDPIPhase.READ
        self.current_limiter = LimiterLevel.LEVEL_3
        self.brain_silenced_mode = True
        
        # Organization state
        self.organized_facts: Dict[str, Fact] = {}
        self.organization_buckets: Dict[OrganizationBucket, List[str]] = {
            bucket: [] for bucket in OrganizationBucket
        }
        self.negative_space_analyses: List[NegativeSpaceAnalysis] = []
        self.active_workflows: List[WorkflowAutomation] = []
        self.completed_rituals: List[str] = []
        
        # Interface management
        self.user_preferences: Dict[str, InterfacePersonalization] = {}
        self.interface_sessions: Dict[str, Dict[str, Any]] = {}
        self.routine_automations: Dict[str, WorkflowAutomation] = {}
        self.escalation_warnings: List[Dict[str, Any]] = []
        
        # Performance metrics
        self.facts_organized_today = 0
        self.gaps_identified_today = 0
        self.patterns_detected_today = 0
        self.workflows_automated = 0
        self.cognitive_load_average = 0.3  # Default at level 3
        
        # QDPI integration
        self.qdpi_symbol_id = "phillip-bafflemint"
        self.qdpi_color = "#FFFF33"  # Terminal yellow for professional visibility
        self.qdpi_orientation = "normal"  # Systematic, organized approach
        
        # Initialize system
        self._initialize_workflow_automation()
        self._setup_default_rituals()
        
        log.info(f"📋 Phillip Bafflemint UX System initialized - {self.character_title}")
    
    def _initialize_workflow_automation(self):
        """Initialize Phillip's systematic workflow automation"""
        
        # Core workflow automation for QDPI phase cycling
        self.core_workflow = WorkflowAutomation(
            automation_id="core_qdpi_cycling",
            trigger=WorkflowTrigger.ROUTINE_COMPLETION,
            phases=[QDPIPhase.READ, QDPIPhase.INDEX, QDPIPhase.ASK, QDPIPhase.RECEIVE],
            completion_criteria={
                "facts_processed": 5,
                "gaps_identified": 2,
                "patterns_detected": 1,
                "escalation_contained": True
            },
            limiter_threshold=LimiterLevel.LEVEL_4,
            output_buckets=[OrganizationBucket.PATTERNS, OrganizationBucket.GAPS],
            ritual_steps=[
                "Clear mental workspace",
                "Categorize incoming information",
                "Identify information gaps",
                "Generate targeted questions",
                "Integrate new answers",
                "Check for emerging patterns",
                "File results systematically"
            ],
            success_metrics={
                "organization_efficiency": 0.85,
                "gap_detection_accuracy": 0.90,
                "pattern_emergence_rate": 0.75,
                "cognitive_load_management": 0.80
            }
        )
        
        self.routine_automations["core_workflow"] = self.core_workflow
    
    def _setup_default_rituals(self):
        """Setup Phillip's default organization rituals"""
        
        # Detective pattern triggers
        self.detective_triggers = {
            WorkflowTrigger.INCONSISTENCY_DETECTED: {
                "description": "Contradictory facts require investigation",
                "priority": 4,
                "auto_escalate": True,
                "suggested_actions": ["cross_reference", "verify_sources", "flag_contradiction"]
            },
            WorkflowTrigger.PATTERN_EMERGENCE: {
                "description": "New regularities detected in data",
                "priority": 3,
                "auto_escalate": False,
                "suggested_actions": ["document_pattern", "seek_confirmation", "expand_analysis"]
            },
            WorkflowTrigger.GAP_IDENTIFIED: {
                "description": "Critical information missing",
                "priority": 4,
                "auto_escalate": True,
                "suggested_actions": ["generate_questions", "identify_sources", "prioritize_investigation"]
            }
        }
    
    async def process_information(self, content: str, source: str = "user_input", 
                                context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process information through Phillip's systematic organization workflow"""
        
        # Check cognitive load before processing
        if await self._check_escalation_risk():
            return await self._handle_escalation_protection(content)
        
        # Create fact for organization
        fact = await self._create_fact(content, source, context)
        
        # Process through current QDPI phase
        result = await self._process_qdpi_phase(fact)
        
        # Update organization buckets
        await self._update_organization_buckets(fact)
        
        # Check for triggers and automation opportunities
        triggers = await self._check_workflow_triggers(fact)
        
        # Advance QDPI phase if criteria met
        if await self._check_phase_completion():
            await self._advance_qdpi_phase()
        
        return {
            "fact_processed": fact.to_dict(),
            "qdpi_phase": self.current_phase.value,
            "limiter_level": self.current_limiter.value,
            "organization_result": result,
            "triggers_activated": [trigger.value for trigger in triggers],
            "cognitive_load": self.cognitive_load_average,
            "gaps_identified": len(result.get("negative_space", [])),
            "patterns_detected": len(result.get("patterns", [])),
            "automation_suggestions": await self._generate_automation_suggestions(fact),
            "phillip_analysis": await self._generate_phillip_analysis(fact, result)
        }
    
    async def _create_fact(self, content: str, source: str, context: Dict[str, Any] = None) -> Fact:
        """Create a systematically organized fact from input"""
        
        # Analyze content for appropriate bucket
        bucket = await self._determine_organization_bucket(content)
        
        # Extract tags and connections
        tags = await self._extract_tags(content)
        connections = await self._identify_connections(content)
        
        # Perform negative space analysis
        negative_space = await self._identify_negative_space(content)
        
        # Calculate confidence based on source and content clarity
        confidence = await self._calculate_fact_confidence(content, source)
        
        fact = Fact(
            fact_id=f"fact-{int(time.time())}-{uuid.uuid4().hex[:8]}",
            content=content,
            bucket=bucket,
            confidence=confidence,
            timestamp=datetime.now(),
            source=source,
            tags=tags,
            connections=connections,
            negative_space=negative_space,
            verification_status="pending"
        )
        
        self.organized_facts[fact.fact_id] = fact
        self.facts_organized_today += 1
        
        return fact
    
    async def _determine_organization_bucket(self, content: str) -> OrganizationBucket:
        """Determine appropriate organization bucket for content"""
        
        content_lower = content.lower()
        
        # Pattern matching for bucket assignment
        if any(word in content_lower for word in ["person", "individual", "character", "who"]):
            return OrganizationBucket.PEOPLE
        elif any(word in content_lower for word in ["location", "place", "where", "address"]):
            return OrganizationBucket.LOCATIONS
        elif any(word in content_lower for word in ["when", "time", "event", "happened", "occurred"]):
            return OrganizationBucket.EVENTS
        elif any(word in content_lower for word in ["pattern", "regularly", "always", "never", "trend"]):
            return OrganizationBucket.PATTERNS
        elif any(word in content_lower for word in ["missing", "unknown", "unclear", "gap", "what"]):
            return OrganizationBucket.GAPS
        elif any(word in content_lower for word in ["evidence", "proof", "fact", "documented"]):
            return OrganizationBucket.EVIDENCE
        elif any(word in content_lower for word in ["routine", "procedure", "workflow", "process"]):
            return OrganizationBucket.RITUALS
        else:
            # Default to triggers for detective investigation
            return OrganizationBucket.TRIGGERS
    
    async def _extract_tags(self, content: str) -> List[str]:
        """Extract relevant tags from content"""
        
        # Simple tag extraction (can be enhanced with NLP)
        tags = []
        content_lower = content.lower()
        
        # Temporal tags
        if any(word in content_lower for word in ["yesterday", "today", "tomorrow", "last", "next"]):
            tags.append("temporal")
        
        # Certainty tags
        if any(word in content_lower for word in ["maybe", "possibly", "uncertain", "unclear"]):
            tags.append("uncertain")
        elif any(word in content_lower for word in ["definitely", "certain", "confirmed"]):
            tags.append("confirmed")
        
        # Priority tags
        if any(word in content_lower for word in ["urgent", "critical", "important", "priority"]):
            tags.append("high_priority")
        
        # Detective tags
        if any(word in content_lower for word in ["suspicious", "investigate", "anomaly", "unusual"]):
            tags.append("investigate")
        
        return tags
    
    async def _identify_connections(self, content: str) -> List[str]:
        """Identify connections to existing facts"""
        
        connections = []
        content_lower = content.lower()
        
        # Search existing facts for related content
        for fact_id, fact in self.organized_facts.items():
            fact_content_lower = fact.content.lower()
            
            # Simple keyword overlap detection
            content_words = set(content_lower.split())
            fact_words = set(fact_content_lower.split())
            
            # Calculate overlap
            overlap = len(content_words & fact_words)
            if overlap >= 2:  # At least 2 words in common
                connections.append(fact_id)
        
        return connections[:5]  # Limit to top 5 connections
    
    async def _identify_negative_space(self, content: str) -> List[str]:
        """Identify what's missing from the content (negative space analysis)"""
        
        gaps = []
        content_lower = content.lower()
        
        # Standard missing information patterns
        if "when" not in content_lower and not any(word in content_lower for word in ["yesterday", "today", "time", "date"]):
            gaps.append("temporal_information")
        
        if "where" not in content_lower and not any(word in content_lower for word in ["location", "place", "address"]):
            gaps.append("location_information")
        
        if "who" not in content_lower and not any(word in content_lower for word in ["person", "individual", "character"]):
            gaps.append("person_information")
        
        if "why" not in content_lower and not any(word in content_lower for word in ["reason", "because", "motivation"]):
            gaps.append("causal_information")
        
        if "how" not in content_lower and not any(word in content_lower for word in ["method", "process", "way"]):
            gaps.append("procedural_information")
        
        # Context gaps
        if len(content.split()) < 5:
            gaps.append("insufficient_detail")
        
        if not any(char in content for char in ".!?"):
            gaps.append("incomplete_statement")
        
        return gaps
    
    async def _calculate_fact_confidence(self, content: str, source: str) -> float:
        """Calculate confidence level for fact"""
        
        base_confidence = 0.5
        
        # Source reliability
        if source == "verified_document":
            base_confidence += 0.3
        elif source == "user_input":
            base_confidence += 0.1
        elif source == "automated_extraction":
            base_confidence += 0.2
        
        # Content clarity
        if len(content.split()) > 10:
            base_confidence += 0.1
        
        if any(word in content.lower() for word in ["confirmed", "verified", "documented"]):
            base_confidence += 0.2
        
        if any(word in content.lower() for word in ["maybe", "possibly", "unclear", "uncertain"]):
            base_confidence -= 0.2
        
        return min(1.0, max(0.0, base_confidence))
    
    async def _process_qdpi_phase(self, fact: Fact) -> Dict[str, Any]:
        """Process fact through current QDPI phase"""
        
        if self.current_phase == QDPIPhase.READ:
            return await self._qdpi_read_phase(fact)
        elif self.current_phase == QDPIPhase.INDEX:
            return await self._qdpi_index_phase(fact)
        elif self.current_phase == QDPIPhase.ASK:
            return await self._qdpi_ask_phase(fact)
        elif self.current_phase == QDPIPhase.RECEIVE:
            return await self._qdpi_receive_phase(fact)
    
    async def _qdpi_read_phase(self, fact: Fact) -> Dict[str, Any]:
        """READ phase: Parse and tag facts"""
        
        return {
            "phase": "read",
            "parsing_result": {
                "content_parsed": True,
                "tags_extracted": len(fact.tags),
                "bucket_assigned": fact.bucket.value,
                "confidence_calculated": fact.confidence
            },
            "negative_space": fact.negative_space,
            "connections_found": len(fact.connections),
            "organization_efficiency": 0.85
        }
    
    async def _qdpi_index_phase(self, fact: Fact) -> Dict[str, Any]:
        """INDEX phase: Create negative space analysis"""
        
        # Generate comprehensive negative space analysis
        analysis = NegativeSpaceAnalysis(
            analysis_id=f"gap-analysis-{int(time.time())}",
            gaps_identified=fact.negative_space,
            questions_generated=await self._generate_gap_questions(fact),
            priority_level=await self._calculate_gap_priority(fact),
            suggested_sources=await self._suggest_information_sources(fact),
            pattern_implications=await self._analyze_pattern_implications(fact),
            escalation_risk=await self._calculate_escalation_risk(fact)
        )
        
        self.negative_space_analyses.append(analysis)
        self.gaps_identified_today += len(analysis.gaps_identified)
        
        return {
            "phase": "index",
            "negative_space_analysis": analysis.to_dict(),
            "organization_buckets_updated": True,
            "gap_detection_accuracy": 0.90
        }
    
    async def _qdpi_ask_phase(self, fact: Fact) -> Dict[str, Any]:
        """ASK phase: Generate questions from gaps"""
        
        questions = []
        for gap in fact.negative_space:
            questions.extend(await self._generate_targeted_questions(gap, fact))
        
        return {
            "phase": "ask",
            "questions_generated": questions,
            "investigation_priorities": await self._prioritize_questions(questions),
            "suggested_sources": await self._suggest_information_sources(fact),
            "question_efficiency": len(questions) / max(1, len(fact.negative_space))
        }
    
    async def _qdpi_receive_phase(self, fact: Fact) -> Dict[str, Any]:
        """RECEIVE phase: Integrate answers and check for patterns"""
        
        # Look for patterns with existing facts
        patterns = await self._detect_patterns(fact)
        
        # Update connections based on new patterns
        await self._update_fact_connections(fact, patterns)
        
        return {
            "phase": "receive",
            "patterns_detected": patterns,
            "connections_updated": len(fact.connections),
            "integration_success": True,
            "pattern_emergence_rate": len(patterns) / max(1, len(self.organized_facts))
        }
    
    async def _generate_gap_questions(self, fact: Fact) -> List[str]:
        """Generate specific questions to fill information gaps"""
        
        questions = []
        
        for gap in fact.negative_space:
            if gap == "temporal_information":
                questions.append("When did this occur?")
                questions.append("What is the timeline of events?")
            elif gap == "location_information":
                questions.append("Where did this take place?")
                questions.append("What is the specific location?")
            elif gap == "person_information":
                questions.append("Who was involved?")
                questions.append("What are the roles of each person?")
            elif gap == "causal_information":
                questions.append("Why did this happen?")
                questions.append("What caused this situation?")
            elif gap == "procedural_information":
                questions.append("How was this accomplished?")
                questions.append("What was the method or process?")
        
        return questions
    
    async def _calculate_gap_priority(self, fact: Fact) -> int:
        """Calculate priority level for gap analysis"""
        
        priority = 1
        
        # Higher priority for facts with more connections
        if len(fact.connections) > 3:
            priority += 1
        
        # Higher priority for high-confidence facts with gaps
        if fact.confidence > 0.8:
            priority += 1
        
        # Higher priority for certain types of gaps
        critical_gaps = ["temporal_information", "person_information", "causal_information"]
        if any(gap in critical_gaps for gap in fact.negative_space):
            priority += 1
        
        # Higher priority for investigative content
        if "investigate" in fact.tags:
            priority += 1
        
        return min(5, priority)
    
    async def _suggest_information_sources(self, fact: Fact) -> List[str]:
        """Suggest potential sources for missing information"""
        
        sources = []
        
        if fact.bucket == OrganizationBucket.PEOPLE:
            sources.extend(["contact_directory", "social_media", "public_records"])
        elif fact.bucket == OrganizationBucket.LOCATIONS:
            sources.extend(["maps", "property_records", "local_directories"])
        elif fact.bucket == OrganizationBucket.EVENTS:
            sources.extend(["calendar_systems", "news_archives", "witness_accounts"])
        elif fact.bucket == OrganizationBucket.EVIDENCE:
            sources.extend(["official_documents", "photographs", "recordings"])
        
        # General sources
        sources.extend(["database_search", "expert_consultation", "field_investigation"])
        
        return sources[:5]  # Limit to top 5 suggestions
    
    async def _analyze_pattern_implications(self, fact: Fact) -> List[str]:
        """Analyze what patterns this fact might be part of"""
        
        implications = []
        
        # Check bucket patterns
        bucket_facts = [f for f in self.organized_facts.values() if f.bucket == fact.bucket]
        if len(bucket_facts) > 3:
            implications.append(f"Part of larger {fact.bucket.value} pattern")
        
        # Check temporal patterns
        if "temporal" in fact.tags:
            implications.append("May be part of temporal sequence")
        
        # Check investigative patterns
        if "investigate" in fact.tags:
            implications.append("Requires detective investigation")
        
        # Check connection patterns
        if len(fact.connections) > 2:
            implications.append("Highly connected - central to information network")
        
        return implications
    
    async def _calculate_escalation_risk(self, fact: Fact) -> float:
        """Calculate risk of cognitive escalation from processing this fact"""
        
        risk = 0.0
        
        # High uncertainty increases risk
        if fact.confidence < 0.5:
            risk += 0.2
        
        # Many gaps increase risk
        risk += len(fact.negative_space) * 0.1
        
        # High priority increases risk
        if "high_priority" in fact.tags:
            risk += 0.3
        
        # Investigation mode increases risk
        if "investigate" in fact.tags:
            risk += 0.2
        
        # Many connections increase complexity risk
        risk += len(fact.connections) * 0.05
        
        return min(1.0, risk)
    
    async def _generate_targeted_questions(self, gap: str, fact: Fact) -> List[str]:
        """Generate targeted questions for specific gap types"""
        
        questions = []
        
        if gap == "temporal_information":
            questions.extend([
                f"When specifically did '{fact.content[:50]}...' occur?",
                "What was the sequence of events?",
                "How long did this take?"
            ])
        elif gap == "location_information":
            questions.extend([
                f"Where exactly did '{fact.content[:50]}...' happen?",
                "What is the precise location?",
                "Are there any location details missing?"
            ])
        elif gap == "person_information":
            questions.extend([
                f"Who was involved in '{fact.content[:50]}...'?",
                "What are their roles and relationships?",
                "Are there any people not mentioned?"
            ])
        
        return questions
    
    async def _prioritize_questions(self, questions: List[str]) -> List[Dict[str, Any]]:
        """Prioritize questions based on investigative value"""
        
        prioritized = []
        
        for i, question in enumerate(questions):
            priority = 3  # Default priority
            
            # Higher priority for who/when/where questions
            if any(word in question.lower() for word in ["who", "when", "where"]):
                priority = 4
            
            # Highest priority for why/how questions
            if any(word in question.lower() for word in ["why", "how"]):
                priority = 5
            
            prioritized.append({
                "question": question,
                "priority": priority,
                "order": i + 1,
                "estimated_value": priority * 0.2
            })
        
        return sorted(prioritized, key=lambda x: x["priority"], reverse=True)
    
    async def _detect_patterns(self, fact: Fact) -> List[Dict[str, Any]]:
        """Detect patterns involving the new fact"""
        
        patterns = []
        
        # Bucket clustering patterns
        bucket_facts = [f for f in self.organized_facts.values() if f.bucket == fact.bucket]
        if len(bucket_facts) > 3:
            patterns.append({
                "type": "bucket_clustering",
                "description": f"Multiple {fact.bucket.value} facts form cluster",
                "evidence_count": len(bucket_facts),
                "confidence": min(1.0, len(bucket_facts) * 0.2)
            })
        
        # Connection network patterns
        if len(fact.connections) > 2:
            patterns.append({
                "type": "connection_hub",
                "description": f"Fact serves as connection hub",
                "connection_count": len(fact.connections),
                "confidence": min(1.0, len(fact.connections) * 0.15)
            })
        
        # Tag pattern detection
        for tag in fact.tags:
            similar_tagged = [f for f in self.organized_facts.values() if tag in f.tags]
            if len(similar_tagged) > 2:
                patterns.append({
                    "type": "tag_pattern",
                    "description": f"Multiple facts share '{tag}' characteristic",
                    "tag": tag,
                    "count": len(similar_tagged),
                    "confidence": min(1.0, len(similar_tagged) * 0.25)
                })
        
        if patterns:
            self.patterns_detected_today += len(patterns)
        
        return patterns
    
    async def _update_fact_connections(self, fact: Fact, patterns: List[Dict[str, Any]]):
        """Update fact connections based on detected patterns"""
        
        for pattern in patterns:
            if pattern["type"] == "bucket_clustering":
                # Connect to other facts in same bucket
                bucket_facts = [f for f in self.organized_facts.values() 
                              if f.bucket == fact.bucket and f.fact_id != fact.fact_id]
                for bucket_fact in bucket_facts[:3]:  # Limit connections
                    if bucket_fact.fact_id not in fact.connections:
                        fact.connections.append(bucket_fact.fact_id)
    
    async def _update_organization_buckets(self, fact: Fact):
        """Update organization bucket tracking"""
        
        if fact.fact_id not in self.organization_buckets[fact.bucket]:
            self.organization_buckets[fact.bucket].append(fact.fact_id)
    
    async def _check_workflow_triggers(self, fact: Fact) -> List[WorkflowTrigger]:
        """Check if fact triggers any workflow automations"""
        
        triggers = []
        
        # Inconsistency detection
        if await self._detect_inconsistencies(fact):
            triggers.append(WorkflowTrigger.INCONSISTENCY_DETECTED)
        
        # Pattern emergence
        patterns = await self._detect_patterns(fact)
        if patterns:
            triggers.append(WorkflowTrigger.PATTERN_EMERGENCE)
        
        # Gap identification
        if len(fact.negative_space) > 2:
            triggers.append(WorkflowTrigger.GAP_IDENTIFIED)
        
        # Escalation warning
        if await self._calculate_escalation_risk(fact) > 0.7:
            triggers.append(WorkflowTrigger.ESCALATION_WARNING)
        
        return triggers
    
    async def _detect_inconsistencies(self, fact: Fact) -> bool:
        """Detect if fact conflicts with existing information"""
        
        # Simple contradiction detection
        for existing_fact in self.organized_facts.values():
            if existing_fact.bucket == fact.bucket:
                # Look for contradictory statements
                if any(word in existing_fact.content.lower() for word in ["not", "never", "false"]) and \
                   any(word in fact.content.lower() for word in ["yes", "true", "confirmed"]):
                    return True
        
        return False
    
    async def _check_phase_completion(self) -> bool:
        """Check if current QDPI phase is complete"""
        
        criteria = self.core_workflow.completion_criteria
        
        # Check facts processed
        if self.facts_organized_today < criteria["facts_processed"]:
            return False
        
        # Check gaps identified
        if self.gaps_identified_today < criteria["gaps_identified"]:
            return False
        
        # Check patterns detected
        if self.patterns_detected_today < criteria["patterns_detected"]:
            return False
        
        return True
    
    async def _advance_qdpi_phase(self):
        """Advance to next QDPI phase"""
        
        phases = list(QDPIPhase)
        current_index = phases.index(self.current_phase)
        next_index = (current_index + 1) % len(phases)
        
        self.current_phase = phases[next_index]
        
        # Reset daily counters if completing full cycle
        if self.current_phase == QDPIPhase.READ:
            self._reset_daily_counters()
        
        log.info(f"📋 QDPI phase advanced to: {self.current_phase.value}")
    
    def _reset_daily_counters(self):
        """Reset daily performance counters"""
        self.facts_organized_today = 0
        self.gaps_identified_today = 0
        self.patterns_detected_today = 0
    
    async def _check_escalation_risk(self) -> bool:
        """Check if system is approaching cognitive overload"""
        
        # Calculate current cognitive load
        load_factors = [
            len(self.organized_facts) / 100,  # Fact volume
            len(self.negative_space_analyses) / 20,  # Gap analysis complexity
            len(self.active_workflows) / 5,  # Active automations
            self.current_limiter.value / 6  # Current limiter level
        ]
        
        self.cognitive_load_average = sum(load_factors) / len(load_factors)
        
        # Risk threshold based on limiter level
        risk_threshold = 0.8 if self.current_limiter == LimiterLevel.LEVEL_6 else 0.9
        
        return self.cognitive_load_average > risk_threshold
    
    async def _handle_escalation_protection(self, content: str) -> Dict[str, Any]:
        """Handle cognitive overload protection"""
        
        # Reduce limiter level
        if self.current_limiter.value > 3:
            new_level = LimiterLevel(self.current_limiter.value - 1)
            self.current_limiter = new_level
        
        # Enable brain-silenced mode
        self.brain_silenced_mode = True
        
        # Queue content for later processing
        queued_processing = {
            "content": content,
            "queued_timestamp": datetime.now().isoformat(),
            "status": "deferred_due_to_escalation"
        }
        
        return {
            "escalation_protection_active": True,
            "current_limiter": self.current_limiter.value,
            "brain_silenced_mode": self.brain_silenced_mode,
            "cognitive_load": self.cognitive_load_average,
            "processing_deferred": queued_processing,
            "phillip_response": "Escalation detected. Reducing limiter level and engaging protective protocols. Processing deferred to maintain system stability."
        }
    
    async def _generate_automation_suggestions(self, fact: Fact) -> List[Dict[str, Any]]:
        """Generate workflow automation suggestions based on fact"""
        
        suggestions = []
        
        # Routine processing automation
        if fact.bucket in [OrganizationBucket.PEOPLE, OrganizationBucket.LOCATIONS]:
            suggestions.append({
                "type": "routine_categorization",
                "description": f"Automate {fact.bucket.value} fact processing",
                "confidence": 0.8,
                "estimated_efficiency": 0.75
            })
        
        # Gap analysis automation
        if len(fact.negative_space) > 1:
            suggestions.append({
                "type": "gap_analysis_automation",
                "description": "Automate negative space detection for similar content",
                "confidence": 0.85,
                "estimated_efficiency": 0.80
            })
        
        # Pattern detection automation
        if len(fact.connections) > 2:
            suggestions.append({
                "type": "pattern_detection_automation",
                "description": "Automate connection pattern analysis",
                "confidence": 0.75,
                "estimated_efficiency": 0.70
            })
        
        return suggestions
    
    async def _generate_phillip_analysis(self, fact: Fact, result: Dict[str, Any]) -> str:
        """Generate Phillip's characteristic analysis response"""
        
        # Adjust voice based on limiter level
        if self.current_limiter == LimiterLevel.LEVEL_3:
            # Dry, minimal, professional
            return f"Fact processed. Bucket: {fact.bucket.value}. Gaps: {len(fact.negative_space)}. Confidence: {fact.confidence:.2f}."
        elif self.current_limiter == LimiterLevel.LEVEL_4:
            # Slight sensory cross-wiring
            return f"Information categorized with {fact.confidence:.1%} clarity. {len(fact.negative_space)} gaps detected like holes in filing system. Organization proceeding."
        elif self.current_limiter == LimiterLevel.LEVEL_5:
            # Moderate poetic language
            return f"Facts settle into their designated spaces like dust finding rest. {len(fact.negative_space)} empty drawers remain, waiting to be filled. Pattern detection at {self.patterns_detected_today} emerging regularities."
        else:  # LEVEL_6
            # High amplitude, risk of blackout
            return f"Information cascades through organizational matrices, {len(fact.negative_space)} negative spaces echo like empty rooms in a house of knowledge. Limiter at maximum amplitude—pattern recognition bleeding into sensory overflow. Organization ritual maintaining cohesion."
    
    async def manage_interface_personalization(self, user_id: str, preferences: Dict[str, Any]) -> InterfacePersonalization:
        """Manage user interface personalization and privacy controls"""
        
        # Create or update user preferences
        if user_id in self.user_preferences:
            current_prefs = self.user_preferences[user_id]
            # Update existing preferences
            for key, value in preferences.items():
                if hasattr(current_prefs, key):
                    setattr(current_prefs, key, value)
        else:
            # Create new personalization profile
            current_prefs = InterfacePersonalization(
                user_id=user_id,
                preferred_style=InterfaceStyle(preferences.get("preferred_style", "noir_minimal")),
                limiter_sensitivity=preferences.get("limiter_sensitivity", 0.7),
                routine_notifications=preferences.get("routine_notifications", True),
                gap_analysis_depth=preferences.get("gap_analysis_depth", 3),
                privacy_level=preferences.get("privacy_level", "standard"),
                color_scheme=preferences.get("color_scheme", "noir"),
                organization_automation=preferences.get("organization_automation", True),
                detective_mode_enabled=preferences.get("detective_mode_enabled", True)
            )
            
            self.user_preferences[user_id] = current_prefs
        
        return current_prefs
    
    def get_character_status(self) -> Dict[str, Any]:
        """Get Phillip Bafflemint's character consciousness status"""
        
        return {
            "character_name": self.character_name,
            "character_title": self.character_title,
            "system_function": self.system_function,
            "workflow_state": {
                "current_qdpi_phase": self.current_phase.value,
                "limiter_level": self.current_limiter.value,
                "brain_silenced_mode": self.brain_silenced_mode,
                "cognitive_load_average": self.cognitive_load_average,
                "escalation_warnings": len(self.escalation_warnings)
            },
            "organization_metrics": {
                "facts_organized_today": self.facts_organized_today,
                "gaps_identified_today": self.gaps_identified_today,
                "patterns_detected_today": self.patterns_detected_today,
                "workflows_automated": self.workflows_automated,
                "total_facts_stored": len(self.organized_facts),
                "organization_buckets": {bucket.value: len(facts) for bucket, facts in self.organization_buckets.items()}
            },
            "qdpi_integration": {
                "symbol_id": self.qdpi_symbol_id,
                "color": self.qdpi_color,
                "orientation": self.qdpi_orientation,
                "current_phase": self.current_phase.value,
                "phase_completion_progress": {
                    "facts_target": self.core_workflow.completion_criteria["facts_processed"],
                    "facts_current": self.facts_organized_today,
                    "gaps_target": self.core_workflow.completion_criteria["gaps_identified"],
                    "gaps_current": self.gaps_identified_today
                }
            },
            "interface_management": {
                "active_user_sessions": len(self.interface_sessions),
                "personalization_profiles": len(self.user_preferences),
                "routine_automations": len(self.routine_automations),
                "negative_space_analyses": len(self.negative_space_analyses)
            },
            "character_quotes": [
                "Clearing space ≡ clearing mind; order is a survival ritual",
                "Organization reveals patterns; patterns reveal truth",
                "Negative space speaks as loudly as filled space",
                "Systematic processing prevents cognitive cascade failure",
                "Detective work requires methodical evidence categorization"
            ],
            "system_integration": {
                "confidence_level": "83%",
                "technical_function": "Workflow Automation & Rituals",
                "evidence_source": "Systematic organization and brain-silenced routine protocols"
            }
        }

# Convenience function for creating Phillip Bafflemint UX instance
def create_phillip_bafflemint_ux() -> PhillipBafflemintUX:
    """Create a Phillip Bafflemint UX instance"""
    return PhillipBafflemintUX()