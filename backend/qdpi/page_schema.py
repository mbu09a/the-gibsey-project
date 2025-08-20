"""QDPI Page Schema using Pydantic"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime

class PageSchema(BaseModel):
    """Schema for a QDPI page"""
    
    # Core identifiers
    page_id: str
    symbol_code: int = Field(ge=0, le=255)
    
    # Character and behavior
    character: str
    orientation: str = Field(pattern="^[XYAZ]$")
    provenance: str = Field(pattern="^[CPUS]$")
    
    # Narrative properties
    trajectory: str = Field(default="T0", pattern="^T[0-3]$")
    voice_preset: Optional[str] = None
    section: Optional[int] = Field(None, ge=1, le=16)
    page_num: Optional[int] = Field(None, ge=1)
    
    # Content
    text: str
    inputs: Dict[str, Any] = Field(default_factory=dict)
    
    # Navigation
    edges: Dict[str, Any] = Field(default_factory=dict)
    return_to: Optional[str] = None
    
    # Validation and metadata
    validation: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class EdgeSchema(BaseModel):
    """Schema for page edges/connections"""
    page_id: str
    edge_type: str
    target_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class IndexSignalsSchema(BaseModel):
    """Schema for page index signals"""
    page_id: str
    entities: List[str] = Field(default_factory=list)
    motifs: List[str] = Field(default_factory=list) 
    unresolved_anchors: List[str] = Field(default_factory=list)
    novelty: float = Field(ge=0.0, le=1.0)
    coherence: float = Field(ge=0.0, le=1.0)
    
class PlanSchema(BaseModel):
    """Schema for narrative plans"""
    plan_id: str
    page_id: str
    symbol_code: int
    trajectory: str
    voice: Dict[str, Any] = Field(default_factory=dict)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    sources: List[str] = Field(default_factory=list)
    plan_json: str
    created_at: datetime = Field(default_factory=datetime.utcnow)