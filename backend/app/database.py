"""
Database abstraction layer for the Gibsey Mycelial Network
Currently using in-memory storage, will be replaced with Cassandra + Stargate
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import uuid
from pathlib import Path

from app.models import StoryPage, PromptOption, User, Branch, Motif, PageType, AuthorType, SymbolRotation

class MockDatabase:
    """
    In-memory database implementation for development
    TODO: Replace with Cassandra + Stargate integration
    """
    
    def __init__(self):
        self.pages: Dict[str, StoryPage] = {}
        self.prompts: Dict[str, PromptOption] = {}
        self.users: Dict[str, User] = {}
        self.branches: Dict[str, Branch] = {}
        self.motifs: Dict[str, Motif] = {}
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
        # Load initial data from frontend JSON
        self._load_initial_data()
    
    def _load_initial_data(self):
        """Load existing story data from frontend JSON file"""
        try:
            frontend_data_path = Path(__file__).parent.parent.parent / "src" / "assets" / "texts.json"
            if frontend_data_path.exists():
                with open(frontend_data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convert frontend pages to API format
                for i, page_data in enumerate(data.get('pages', [])):
                    story_page = StoryPage(
                        id=page_data.get('id', f"page_{i}"),
                        symbol_id=page_data.get('symbolId', 'unknown'),
                        rotation=SymbolRotation(page_data.get('rotation', 0)),
                        page_type=PageType.PRIMARY,
                        text=page_data.get('text', ''),
                        author=AuthorType.SYSTEM,
                        title=page_data.get('title'),
                        section=page_data.get('section'),
                        child_ids=page_data.get('childIds', []),
                        branches=page_data.get('branches', []),
                        prompts=page_data.get('prompts', [])
                    )
                    self.pages[story_page.id] = story_page
                
                print(f"Loaded {len(self.pages)} pages from frontend data")
            else:
                print("Frontend data file not found, starting with empty database")
        except Exception as e:
            print(f"Error loading initial data: {e}")
    
    # StoryPage operations
    async def get_page(self, page_id: str) -> Optional[StoryPage]:
        return self.pages.get(page_id)
    
    async def get_pages(self, skip: int = 0, limit: int = 100) -> List[StoryPage]:
        all_pages = list(self.pages.values())
        return all_pages[skip:skip + limit]
    
    async def get_pages_by_symbol(self, symbol_id: str) -> List[StoryPage]:
        return [page for page in self.pages.values() if page.symbol_id == symbol_id]
    
    async def create_page(self, page: StoryPage) -> StoryPage:
        if not page.id:
            page.id = str(uuid.uuid4())
        self.pages[page.id] = page
        return page
    
    async def update_page(self, page_id: str, updates: Dict[str, Any]) -> Optional[StoryPage]:
        if page_id not in self.pages:
            return None
        
        page = self.pages[page_id]
        for key, value in updates.items():
            if hasattr(page, key):
                setattr(page, key, value)
        
        return page
    
    # PromptOption operations
    async def get_prompt(self, prompt_id: str) -> Optional[PromptOption]:
        return self.prompts.get(prompt_id)
    
    async def get_prompts_for_page(self, page_id: str) -> List[PromptOption]:
        # TODO: Implement context-aware prompt generation
        return list(self.prompts.values())
    
    async def create_prompt(self, prompt: PromptOption) -> PromptOption:
        if not prompt.id:
            prompt.id = str(uuid.uuid4())
        self.prompts[prompt.id] = prompt
        return prompt
    
    # User operations
    async def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    async def create_user(self, user: User) -> User:
        if not user.id:
            user.id = str(uuid.uuid4())
        self.users[user.id] = user
        return user
    
    async def update_user(self, user_id: str, updates: Dict[str, Any]) -> Optional[User]:
        if user_id not in self.users:
            return None
        
        user = self.users[user_id]
        for key, value in updates.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        return user
    
    # Session operations
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self.sessions.get(session_id)
    
    async def create_session(self, user_id: str) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "user_id": user_id,
            "current_page_index": 0,
            "furthest_page_index": 0,
            "session_start": datetime.utcnow(),
            "last_activity": datetime.utcnow()
        }
        return session_id
    
    async def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        if session_id not in self.sessions:
            return False
        
        self.sessions[session_id].update(updates)
        self.sessions[session_id]["last_activity"] = datetime.utcnow()
        return True
    
    # Branch operations (TODO: Implement when needed)
    async def get_branch(self, branch_id: str) -> Optional[Branch]:
        return self.branches.get(branch_id)
    
    async def create_branch(self, branch: Branch) -> Branch:
        if not branch.id:
            branch.id = str(uuid.uuid4())
        self.branches[branch.id] = branch
        return branch
    
    # Motif operations (TODO: Implement when needed)
    async def get_motif(self, motif_id: str) -> Optional[Motif]:
        return self.motifs.get(motif_id)
    
    async def search_motifs(self, query: str) -> List[Motif]:
        # TODO: Implement vector search
        return [motif for motif in self.motifs.values() if query.lower() in motif.text.lower()]

# Global database instances
_mock_db = MockDatabase()
_cassandra_db = None

# Database selection based on environment
async def get_database():
    """Dependency for FastAPI to get database instance"""
    import os
    
    database_url = os.getenv('DATABASE_URL', 'mock://localhost')
    
    if database_url.startswith('cassandra://'):
        # Use production Cassandra database with vector search
        global _cassandra_db
        if _cassandra_db is None:
            from app.cassandra_database_v2 import get_cassandra_database
            _cassandra_db = get_cassandra_database()
            # Ensure connection is established
            if not _cassandra_db.is_connected():
                await _cassandra_db.connect()
        return _cassandra_db
    else:
        # Use mock database (default for development)
        return _mock_db

# Helper function to close database connections
async def close_database():
    """Close database connections on shutdown"""
    global _cassandra_db
    if _cassandra_db:
        from app.cassandra_database import close_database
        await close_database()
        _cassandra_db = None