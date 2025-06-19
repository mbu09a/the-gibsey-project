"""
Pydantic models for the Gibsey Mycelial Network API
Based on the schema defined in the PRD
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from enum import Enum

# Enums
class SymbolRotation(int, Enum):
    ZERO = 0
    NINETY = 90
    ONE_EIGHTY = 180
    TWO_SEVENTY = 270

class PageType(str, Enum):
    PRIMARY = "primary"
    PROMPT = "prompt"
    USER_QUERY = "user_query"
    AI_RESPONSE = "ai_response"

class PromptType(str, Enum):
    CHARACTER_PROMPT = "character_prompt"
    USER_PROMPT = "user_prompt"
    CHARACTER_RESPONSE = "character_response"

class AuthorType(str, Enum):
    USER = "user"
    AI = "AI"
    SYSTEM = "system"

# Core Models
class StoryPage(BaseModel):
    id: str
    symbol_id: str
    rotation: SymbolRotation = SymbolRotation.ZERO
    page_type: PageType
    parent_id: Optional[str] = None
    prompt_type: Optional[PromptType] = None
    text: str
    author: AuthorType
    branch_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    embedding: Optional[List[float]] = None  # TODO: Vector embeddings
    canonical: bool = True
    version: str = "1.0"
    
    # Additional metadata for compatibility with current frontend
    title: Optional[str] = None
    section: Optional[int] = None
    child_ids: List[str] = Field(default_factory=list)
    branches: List[Dict[str, Any]] = Field(default_factory=list)
    prompts: List[Dict[str, Any]] = Field(default_factory=list)

class PromptOption(BaseModel):
    id: str
    text: str
    rotation: SymbolRotation
    target_symbol_id: str
    prompt_type: PromptType
    embedding: Optional[List[float]] = None  # TODO: Vector embeddings
    description: Optional[str] = None

class Motif(BaseModel):
    id: str
    text: str
    embedding: Optional[List[float]] = None  # TODO: Vector embeddings
    color: str
    symbol: str
    occurrences: List[str] = Field(default_factory=list)  # StoryPage IDs

class Branch(BaseModel):
    id: str
    root_page_id: str
    pages: List[str] = Field(default_factory=list)  # StoryPage IDs
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ClusterEvent(BaseModel):
    id: str
    event_type: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    related_page_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class User(BaseModel):
    id: str
    username: str
    email: Optional[str] = None
    history: List[str] = Field(default_factory=list)  # StoryPage IDs
    authored_pages: List[str] = Field(default_factory=list)  # StoryPage IDs
    session_id: Optional[str] = None
    permissions: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)

# Request/Response Models
class CreatePageRequest(BaseModel):
    symbol_id: str
    text: str
    page_type: PageType = PageType.AI_RESPONSE
    parent_id: Optional[str] = None
    prompt_type: Optional[PromptType] = None
    rotation: SymbolRotation = SymbolRotation.ZERO

class CreatePromptRequest(BaseModel):
    text: str
    target_symbol_id: str
    prompt_type: PromptType
    rotation: SymbolRotation = SymbolRotation.NINETY

class CreateUserRequest(BaseModel):
    username: str
    email: Optional[str] = None

class PageListResponse(BaseModel):
    pages: List[StoryPage]
    total: int
    page: int
    size: int

class WebSocketMessage(BaseModel):
    type: str
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Session Models
class SessionData(BaseModel):
    id: str
    user_id: str
    current_page_index: int = 0
    furthest_page_index: int = 0
    session_start: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)