"""
Stargate REST API client for Cassandra operations
Provides high-level interface for CRUD operations via Stargate REST API
"""

import aiohttp
import json
import uuid
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import logging
from urllib.parse import urljoin

from app.models import StoryPage, PromptOption, User, Branch, Motif

logger = logging.getLogger(__name__)

class StargateClient:
    """
    Async client for Stargate REST API
    Handles all database operations through HTTP REST interface
    """
    
    def __init__(self, base_url: str = "http://localhost:8082", keyspace: str = "gibsey_network"):
        self.base_url = base_url.rstrip('/')
        self.keyspace = keyspace
        self.session = None
        self.auth_token = None  # For future authentication
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _get_url(self, path: str) -> str:
        """Build full URL for Stargate REST API"""
        return urljoin(f"{self.base_url}/v2/keyspaces/{self.keyspace}/", path.lstrip('/'))
    
    async def _request(self, method: str, path: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """Make HTTP request to Stargate API"""
        url = self._get_url(path)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Add auth token when available
        if self.auth_token:
            headers['X-Cassandra-Token'] = self.auth_token
        
        try:
            async with self.session.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params
            ) as response:
                
                if response.status >= 400:
                    error_text = await response.text()
                    logger.error(f"Stargate API error {response.status}: {error_text}")
                    raise Exception(f"Stargate API error {response.status}: {error_text}")
                
                return await response.json()
                
        except aiohttp.ClientError as e:
            logger.error(f"HTTP client error: {e}")
            raise
    
    # StoryPage operations
    async def get_page(self, page_id: str) -> Optional[StoryPage]:
        """Get a story page by ID"""
        try:
            result = await self._request('GET', f'story_pages/{page_id}')
            
            if 'data' in result and result['data']:
                page_data = result['data'][0]  # Stargate returns array
                return self._dict_to_story_page(page_data)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting page {page_id}: {e}")
            return None
    
    async def get_pages(self, page_size: int = 100) -> List[StoryPage]:
        """Get pages with pagination"""
        try:
            params = {'page-size': page_size}
            result = await self._request('GET', 'story_pages', params=params)
            
            pages = []
            if 'data' in result:
                for page_data in result['data']:
                    page = self._dict_to_story_page(page_data)
                    if page:
                        pages.append(page)
            
            return pages
            
        except Exception as e:
            logger.error(f"Error getting pages: {e}")
            return []
    
    async def get_pages_by_symbol(self, symbol_id: str, limit: int = 100) -> List[StoryPage]:
        """Get pages by symbol ID using secondary index"""
        try:
            # Query the pages_by_symbol table
            where_clause = json.dumps({"symbol_id": {"$eq": symbol_id}})
            params = {
                'where': where_clause,
                'page-size': limit
            }
            
            result = await self._request('GET', 'pages_by_symbol', params=params)
            
            # Get full page data for each result
            pages = []
            if 'data' in result:
                for row in result['data']:
                    page_id = row.get('id')
                    if page_id:
                        page = await self.get_page(page_id)
                        if page:
                            pages.append(page)
            
            return pages
            
        except Exception as e:
            logger.error(f"Error getting pages by symbol {symbol_id}: {e}")
            return []
    
    async def create_page(self, page: StoryPage) -> StoryPage:
        """Create a new story page"""
        try:
            # Generate ID if not provided
            if not page.id:
                page.id = str(uuid.uuid4())
            
            # Convert to dict format for Cassandra
            page_data = self._story_page_to_dict(page)
            
            # Insert into main table
            await self._request('POST', 'story_pages', data=page_data)
            
            # Insert into symbol index
            symbol_index_data = {
                'symbol_id': page.symbol_id,
                'created_at': page.created_at.isoformat(),
                'id': page.id
            }
            await self._request('POST', 'pages_by_symbol', data=symbol_index_data)
            
            # Insert into parent index if has parent
            if page.parent_id:
                parent_index_data = {
                    'parent_id': page.parent_id,
                    'created_at': page.created_at.isoformat(),
                    'id': page.id
                }
                await self._request('POST', 'pages_by_parent', data=parent_index_data)
            
            return page
            
        except Exception as e:
            logger.error(f"Error creating page: {e}")
            raise
    
    async def update_page(self, page_id: str, updates: Dict[str, Any]) -> Optional[StoryPage]:
        """Update a story page"""
        try:
            # PATCH request to update specific fields
            await self._request('PATCH', f'story_pages/{page_id}', data=updates)
            
            # Return updated page
            return await self.get_page(page_id)
            
        except Exception as e:
            logger.error(f"Error updating page {page_id}: {e}")
            return None
    
    # PromptOption operations
    async def get_prompt(self, prompt_id: str) -> Optional[PromptOption]:
        """Get a prompt by ID"""
        try:
            result = await self._request('GET', f'prompt_options/{prompt_id}')
            
            if 'data' in result and result['data']:
                prompt_data = result['data'][0]
                return self._dict_to_prompt_option(prompt_data)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting prompt {prompt_id}: {e}")
            return None
    
    async def create_prompt(self, prompt: PromptOption) -> PromptOption:
        """Create a new prompt option"""
        try:
            if not prompt.id:
                prompt.id = str(uuid.uuid4())
            
            prompt_data = self._prompt_option_to_dict(prompt)
            
            # Insert into main table
            await self._request('POST', 'prompt_options', data=prompt_data)
            
            # Insert into symbol index
            symbol_index_data = {
                'target_symbol_id': prompt.target_symbol_id,
                'prompt_type': prompt.prompt_type.value,
                'id': prompt.id
            }
            await self._request('POST', 'prompts_by_symbol', data=symbol_index_data)
            
            return prompt
            
        except Exception as e:
            logger.error(f"Error creating prompt: {e}")
            raise
    
    # User operations
    async def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID"""
        try:
            result = await self._request('GET', f'users/{user_id}')
            
            if 'data' in result and result['data']:
                user_data = result['data'][0]
                return self._dict_to_user(user_data)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username"""
        try:
            result = await self._request('GET', f'users_by_username/{username}')
            
            if 'data' in result and result['data']:
                user_id = result['data'][0].get('user_id')
                if user_id:
                    return await self.get_user(user_id)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by username {username}: {e}")
            return None
    
    async def create_user(self, user: User) -> User:
        """Create a new user"""
        try:
            if not user.id:
                user.id = str(uuid.uuid4())
            
            user_data = self._user_to_dict(user)
            
            # Insert into main table
            await self._request('POST', 'users', data=user_data)
            
            # Insert into username index
            username_index_data = {
                'username': user.username,
                'user_id': user.id
            }
            await self._request('POST', 'users_by_username', data=username_index_data)
            
            return user
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    # Session operations
    async def create_session(self, user_id: str) -> str:
        """Create a new session"""
        try:
            session_id = str(uuid.uuid4())
            session_data = {
                'id': session_id,
                'user_id': user_id,
                'current_page_index': 0,
                'furthest_page_index': 0,
                'session_start': datetime.utcnow().isoformat(),
                'last_activity': datetime.utcnow().isoformat(),
                'metadata': {}
            }
            
            await self._request('POST', 'sessions', data=session_data)
            return session_id
            
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            raise
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        try:
            result = await self._request('GET', f'sessions/{session_id}')
            
            if 'data' in result and result['data']:
                return result['data'][0]
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting session {session_id}: {e}")
            return None
    
    async def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session data"""
        try:
            # Add last_activity timestamp
            updates['last_activity'] = datetime.utcnow().isoformat()
            
            await self._request('PATCH', f'sessions/{session_id}', data=updates)
            return True
            
        except Exception as e:
            logger.error(f"Error updating session {session_id}: {e}")
            return False
    
    # Helper methods for data conversion
    def _story_page_to_dict(self, page: StoryPage) -> Dict[str, Any]:
        """Convert StoryPage to Cassandra-compatible dict"""
        return {
            'id': page.id,
            'symbol_id': page.symbol_id,
            'rotation': page.rotation.value,
            'page_type': page.page_type.value,
            'parent_id': page.parent_id,
            'prompt_type': page.prompt_type.value if page.prompt_type else None,
            'text': page.text,
            'author': page.author.value,
            'branch_id': page.branch_id,
            'created_at': page.created_at.isoformat(),
            'canonical': page.canonical,
            'version': page.version,
            'title': page.title,
            'section': page.section,
            'child_ids': list(page.child_ids),
            'branches': page.branches,
            'prompts': page.prompts,
            'embedding': page.embedding
        }
    
    def _dict_to_story_page(self, data: Dict[str, Any]) -> Optional[StoryPage]:
        """Convert dict to StoryPage model"""
        try:
            # Parse datetime
            created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            
            return StoryPage(
                id=data['id'],
                symbol_id=data['symbol_id'],
                rotation=data['rotation'],
                page_type=data['page_type'],
                parent_id=data.get('parent_id'),
                prompt_type=data.get('prompt_type'),
                text=data['text'],
                author=data['author'],
                branch_id=data.get('branch_id'),
                created_at=created_at,
                canonical=data.get('canonical', True),
                version=data.get('version', '1.0'),
                title=data.get('title'),
                section=data.get('section'),
                child_ids=data.get('child_ids', []),
                branches=data.get('branches', []),
                prompts=data.get('prompts', []),
                embedding=data.get('embedding')
            )
        except Exception as e:
            logger.error(f"Error converting dict to StoryPage: {e}")
            return None
    
    def _prompt_option_to_dict(self, prompt: PromptOption) -> Dict[str, Any]:
        """Convert PromptOption to Cassandra-compatible dict"""
        return {
            'id': prompt.id,
            'text': prompt.text,
            'rotation': prompt.rotation.value,
            'target_symbol_id': prompt.target_symbol_id,
            'prompt_type': prompt.prompt_type.value,
            'description': prompt.description,
            'embedding': prompt.embedding
        }
    
    def _dict_to_prompt_option(self, data: Dict[str, Any]) -> Optional[PromptOption]:
        """Convert dict to PromptOption model"""
        try:
            return PromptOption(
                id=data['id'],
                text=data['text'],
                rotation=data['rotation'],
                target_symbol_id=data['target_symbol_id'],
                prompt_type=data['prompt_type'],
                description=data.get('description'),
                embedding=data.get('embedding')
            )
        except Exception as e:
            logger.error(f"Error converting dict to PromptOption: {e}")
            return None
    
    def _user_to_dict(self, user: User) -> Dict[str, Any]:
        """Convert User to Cassandra-compatible dict"""
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat(),
            'last_active': user.last_active.isoformat(),
            'history': user.history,
            'authored_pages': user.authored_pages,
            'session_id': user.session_id,
            'permissions': {k: str(v) for k, v in user.permissions.items()}  # Convert to strings
        }
    
    def _dict_to_user(self, data: Dict[str, Any]) -> Optional[User]:
        """Convert dict to User model"""
        try:
            created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            last_active = datetime.fromisoformat(data['last_active'].replace('Z', '+00:00'))
            
            return User(
                id=data['id'],
                username=data['username'],
                email=data.get('email'),
                created_at=created_at,
                last_active=last_active,
                history=data.get('history', []),
                authored_pages=data.get('authored_pages', []),
                session_id=data.get('session_id'),
                permissions=data.get('permissions', {})
            )
        except Exception as e:
            logger.error(f"Error converting dict to User: {e}")
            return None

# Global Stargate client instance
stargate_client = None

async def get_stargate_client() -> StargateClient:
    """Get the global Stargate client instance"""
    global stargate_client
    
    if stargate_client is None:
        import os
        stargate_url = os.getenv('STARGATE_URL', 'http://localhost:8082')
        keyspace = os.getenv('CASSANDRA_KEYSPACE', 'gibsey_network')
        
        stargate_client = StargateClient(base_url=stargate_url, keyspace=keyspace)
    
    return stargate_client