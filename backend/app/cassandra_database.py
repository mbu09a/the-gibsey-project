"""
Cassandra database implementation for the Gibsey Mycelial Network
Replaces the mock database with real Cassandra + Stargate operations
"""

import os
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
import logging

from app.models import StoryPage, PromptOption, User, Branch, Motif, PageType, AuthorType, SymbolRotation
from app.stargate_client import StargateClient

logger = logging.getLogger(__name__)

class CassandraDatabase:
    """
    Production database implementation using Cassandra + Stargate
    Provides the same interface as MockDatabase for seamless replacement
    """
    
    def __init__(self):
        self.stargate_client = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize the database connection"""
        if self._initialized:
            return
        
        try:
            # Get configuration from environment
            stargate_url = os.getenv('STARGATE_URL', 'http://localhost:8082')
            keyspace = os.getenv('CASSANDRA_KEYSPACE', 'gibsey_network')
            
            # Create Stargate client
            self.stargate_client = StargateClient(base_url=stargate_url, keyspace=keyspace)
            
            # Initialize the client session
            await self.stargate_client.__aenter__()
            
            self._initialized = True
            logger.info("Cassandra database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Cassandra database: {e}")
            raise
    
    async def close(self):
        """Close database connections"""
        if self.stargate_client:
            await self.stargate_client.__aexit__(None, None, None)
            self._initialized = False
    
    # StoryPage operations
    async def get_page(self, page_id: str) -> Optional[StoryPage]:
        """Get a story page by ID"""
        await self.initialize()
        return await self.stargate_client.get_page(page_id)
    
    async def get_pages(self, skip: int = 0, limit: int = 100) -> List[StoryPage]:
        """Get pages with pagination"""
        await self.initialize()
        
        # Note: Cassandra doesn't support offset-based pagination well
        # For now, get all pages and slice in memory
        # TODO: Implement token-based pagination for production
        all_pages = await self.stargate_client.get_pages(page_size=1000)
        return all_pages[skip:skip + limit]
    
    async def get_pages_by_symbol(self, symbol_id: str) -> List[StoryPage]:
        """Get all pages for a specific symbol/character"""
        await self.initialize()
        return await self.stargate_client.get_pages_by_symbol(symbol_id)
    
    async def create_page(self, page: StoryPage) -> StoryPage:
        """Create a new story page"""
        await self.initialize()
        return await self.stargate_client.create_page(page)
    
    async def update_page(self, page_id: str, updates: Dict[str, Any]) -> Optional[StoryPage]:
        """Update a story page"""
        await self.initialize()
        return await self.stargate_client.update_page(page_id, updates)
    
    # PromptOption operations
    async def get_prompt(self, prompt_id: str) -> Optional[PromptOption]:
        """Get a prompt by ID"""
        await self.initialize()
        return await self.stargate_client.get_prompt(prompt_id)
    
    async def get_prompts_for_page(self, page_id: str) -> List[PromptOption]:
        """Get context-aware prompts for a page"""
        await self.initialize()
        
        # Get the page to determine symbol
        page = await self.get_page(page_id)
        if not page:
            return []
        
        # TODO: Implement real context-aware prompt generation
        # For now, return mock prompts like before
        return self._generate_mock_prompts(page.symbol_id, page_id)
    
    async def create_prompt(self, prompt: PromptOption) -> PromptOption:
        """Create a new prompt option"""
        await self.initialize()
        return await self.stargate_client.create_prompt(prompt)
    
    def _generate_mock_prompts(self, symbol_id: str, page_id: str) -> List[PromptOption]:
        """Generate mock prompts for development (TODO: Replace with AI generation)"""
        
        base_prompts = {
            "london-fox": [
                {
                    "text": "Challenge London's consciousness theories",
                    "prompt_type": "user_prompt",
                    "rotation": 180
                },
                {
                    "text": "What does London do next?",
                    "prompt_type": "character_prompt",
                    "rotation": 90
                },
                {
                    "text": "Ask about Synchromy-M.Y.S.S.T.E.R.Y",
                    "prompt_type": "character_response",
                    "rotation": 270
                }
            ],
            "glyph-marrow": [
                {
                    "text": "Enter the queue with Glyph",
                    "prompt_type": "user_prompt",
                    "rotation": 180
                },
                {
                    "text": "What word comes next?",
                    "prompt_type": "character_prompt",
                    "rotation": 90
                },
                {
                    "text": "Ask about the waiting",
                    "prompt_type": "character_response",
                    "rotation": 270
                }
            ]
        }
        
        prompt_templates = base_prompts.get(symbol_id, base_prompts["london-fox"])
        
        prompts = []
        for i, template in enumerate(prompt_templates):
            prompt = PromptOption(
                id=f"prompt_{page_id}_{i}",
                text=template["text"],
                target_symbol_id=symbol_id,
                prompt_type=template["prompt_type"],
                rotation=template["rotation"]
            )
            prompts.append(prompt)
        
        return prompts
    
    # User operations
    async def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID"""
        await self.initialize()
        return await self.stargate_client.get_user(user_id)
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username"""
        await self.initialize()
        return await self.stargate_client.get_user_by_username(username)
    
    async def create_user(self, user: User) -> User:
        """Create a new user"""
        await self.initialize()
        return await self.stargate_client.create_user(user)
    
    async def update_user(self, user_id: str, updates: Dict[str, Any]) -> Optional[User]:
        """Update user information"""
        await self.initialize()
        
        # Get current user
        user = await self.get_user(user_id)
        if not user:
            return None
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        # Convert back to dict for Cassandra update
        user_dict = {
            'username': user.username,
            'email': user.email,
            'last_active': user.last_active.isoformat(),
            'history': user.history,
            'authored_pages': user.authored_pages,
            'session_id': user.session_id,
            'permissions': user.permissions
        }
        
        return await self.stargate_client.update_user(user_id, user_dict)
    
    # Session operations
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        await self.initialize()
        return await self.stargate_client.get_session(session_id)
    
    async def create_session(self, user_id: str) -> str:
        """Create a new session"""
        await self.initialize()
        return await self.stargate_client.create_session(user_id)
    
    async def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session data"""
        await self.initialize()
        return await self.stargate_client.update_session(session_id, updates)
    
    # Branch operations (TODO: Implement when needed)
    async def get_branch(self, branch_id: str) -> Optional[Branch]:
        """Get a branch by ID"""
        await self.initialize()
        # TODO: Implement branch operations
        return None
    
    async def create_branch(self, branch: Branch) -> Branch:
        """Create a new branch"""
        await self.initialize()
        # TODO: Implement branch operations
        return branch
    
    # Motif operations (TODO: Implement when needed)
    async def get_motif(self, motif_id: str) -> Optional[Motif]:
        """Get a motif by ID"""
        await self.initialize()
        # TODO: Implement motif operations
        return None
    
    async def search_motifs(self, query: str) -> List[Motif]:
        """Search motifs by query"""
        await self.initialize()
        # TODO: Implement vector search for motifs
        return []

# Database instance management
_db_instance = None

async def get_cassandra_database() -> CassandraDatabase:
    """Get the global Cassandra database instance"""
    global _db_instance
    
    if _db_instance is None:
        _db_instance = CassandraDatabase()
        await _db_instance.initialize()
    
    return _db_instance

async def close_database():
    """Close the database connection"""
    global _db_instance
    
    if _db_instance:
        await _db_instance.close()
        _db_instance = None