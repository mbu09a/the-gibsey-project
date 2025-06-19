"""
Production Cassandra database implementation with vector search
Uses optimized schema and Stargate for high-performance operations
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timezone
import uuid
import json
import os

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import DCAwareRoundRobinPolicy
import httpx

from .models import StoryPage, PromptOption, User, SessionData, Branch, Motif

logger = logging.getLogger(__name__)

# Vector service imports - optional for now
try:
    from .vector_service import get_vector_service, EmbeddingResult
    VECTOR_SERVICE_AVAILABLE = True
except ImportError:
    VECTOR_SERVICE_AVAILABLE = False
    logger.warning("Vector service not available - using mock embeddings")

class ProductionCassandraDatabase:
    """Production Cassandra database with vector search capabilities"""
    
    def __init__(self, 
                 hosts: List[str] = None,
                 keyspace: str = "gibsey_network",
                 stargate_url: str = None):
        """
        Initialize production Cassandra database
        
        Args:
            hosts: Cassandra host addresses
            keyspace: Keyspace name
            stargate_url: Stargate REST API URL
        """
        self.hosts = hosts or ['localhost']
        self.keyspace = keyspace
        self.stargate_url = stargate_url or "http://localhost:8082"
        
        # Database connections
        self.cluster = None
        self.session = None
        self.http_client = httpx.AsyncClient(timeout=30.0)
        
        # Vector service
        if VECTOR_SERVICE_AVAILABLE:
            self.vector_service = get_vector_service()
        else:
            self.vector_service = None
        
        # Connection status
        self._connected = False
    
    async def connect(self) -> bool:
        """Connect to Cassandra cluster"""
        try:
            # Connect via native driver
            self.cluster = Cluster(
                self.hosts,
                port=9042,
                protocol_version=4,  # Use protocol version 4 for Cassandra 3.11
                load_balancing_policy=DCAwareRoundRobinPolicy()
            )
            
            # Test connection in thread pool
            loop = asyncio.get_event_loop()
            self.session = await loop.run_in_executor(
                None, 
                lambda: self.cluster.connect(self.keyspace)
            )
            
            # Test Stargate connection
            health_url = f"{self.stargate_url}/health"
            response = await self.http_client.get(health_url)
            
            if response.status_code == 200:
                self._connected = True
                logger.info("Connected to Cassandra via Stargate and native driver")
                return True
            else:
                logger.error(f"Stargate health check failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to connect to Cassandra: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from Cassandra"""
        try:
            if self.http_client:
                await self.http_client.aclose()
            
            if self.session:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self.session.shutdown)
            
            if self.cluster:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self.cluster.shutdown)
            
            self._connected = False
            logger.info("Disconnected from Cassandra")
            
        except Exception as e:
            logger.error(f"Error disconnecting from Cassandra: {e}")
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self._connected
    
    # ========================= STORY PAGES =========================
    
    async def create_page(self, page: StoryPage) -> StoryPage:
        """Create a new story page with vector embedding"""
        try:
            # Generate embedding for the page (or use mock)
            if self.vector_service:
                embedding_result = await self.vector_service.embed_story_page(page.model_dump())
            else:
                # Mock embedding result
                embedding_result = type('MockEmbedding', (), {
                    'embedding': [0.1] * 384,  # Mock 384-dimensional embedding
                    'model': 'mock',
                    'content_id': page.id,
                    'content_type': 'page',
                    'metadata': {}
                })()
            
            # Prepare page data
            page_data = {
                'id': page.id,
                'symbol_id': page.symbol_id,
                'rotation': page.rotation,
                'page_type': page.page_type,
                'parent_id': page.parent_id,
                'prompt_type': page.prompt_type,
                'text': page.text,
                'author': page.author or 'AI',
                'branch_id': page.branch_id,
                'created_at': int(page.created_at.timestamp() * 1000) if page.created_at else int(datetime.now(timezone.utc).timestamp() * 1000),
                'canonical': page.canonical,
                'version': page.version,
                'title': page.title,
                'section': page.section,
                'child_ids': list(page.child_ids) if page.child_ids else [],
                'branches': [dict(b) for b in page.branches] if page.branches else [],
                'prompts': [dict(p) for p in page.prompts] if page.prompts else [],
                'embedding': embedding_result.embedding,
                'embedding_model': embedding_result.model,
                'last_updated': int(datetime.now(timezone.utc).timestamp() * 1000)
            }
            
            # Insert into main table
            await self._stargate_request('POST', 'story_pages', data=page_data)
            
            # Insert into index tables
            await asyncio.gather(
                self._insert_page_by_symbol(page_data),
                self._insert_page_by_section(page_data),
                self._insert_page_by_parent(page_data),
                self._insert_vector_embedding(embedding_result),
                self._insert_recent_page(page_data)
            )
            
            logger.info(f"Created page {page.id} with embedding")
            return page
            
        except Exception as e:
            logger.error(f"Failed to create page {page.id}: {e}")
            raise
    
    async def get_page(self, page_id: str) -> Optional[StoryPage]:
        """Get a story page by ID"""
        try:
            response = await self._stargate_request('GET', f'story_pages/{page_id}')
            if response:
                return self._dict_to_story_page(response)
            return None
            
        except Exception as e:
            logger.error(f"Failed to get page {page_id}: {e}")
            return None
    
    async def get_pages(self, skip: int = 0, limit: int = 20) -> Tuple[List[StoryPage], int]:
        """Get paginated list of story pages"""
        try:
            # Get recent pages for better performance
            bucket = datetime.now(timezone.utc).strftime('%Y-%m-%d-%H')
            
            params = {
                'page-size': limit,
                'where': json.dumps({
                    'bucket': {'$eq': bucket}
                })
            }
            
            response = await self._stargate_request('GET', 'recent_pages', params=params)
            
            pages = []
            if response and 'data' in response:
                # Get full page data for each ID
                page_ids = [row['id'] for row in response['data']]
                page_tasks = [self.get_page(page_id) for page_id in page_ids[skip:skip+limit]]
                pages = [p for p in await asyncio.gather(*page_tasks) if p is not None]
            
            total = len(pages)  # Simplified - in production, implement proper counting
            
            return pages, total
            
        except Exception as e:
            logger.error(f"Failed to get pages: {e}")
            return [], 0
    
    async def get_pages_by_symbol(self, symbol_id: str, page_type: str = None, limit: int = 20) -> List[StoryPage]:
        """Get pages by character symbol (optimized hot path)"""
        try:
            where_clause = {'symbol_id': {'$eq': symbol_id}}
            if page_type:
                where_clause['page_type'] = {'$eq': page_type}
            
            params = {
                'page-size': limit,
                'where': json.dumps(where_clause)
            }
            
            response = await self._stargate_request('GET', 'pages_by_symbol', params=params)
            
            pages = []
            if response and 'data' in response:
                # Get full page data
                page_ids = [row['id'] for row in response['data']]
                page_tasks = [self.get_page(page_id) for page_id in page_ids]
                pages = [p for p in await asyncio.gather(*page_tasks) if p is not None]
            
            return pages
            
        except Exception as e:
            logger.error(f"Failed to get pages by symbol {symbol_id}: {e}")
            return []
    
    async def get_pages_by_section(self, section: int, symbol_id: str = None, limit: int = 20) -> List[StoryPage]:
        """Get pages by book section (optimized for navigation)"""
        try:
            where_clause = {'section': {'$eq': section}}
            if symbol_id:
                where_clause['symbol_id'] = {'$eq': symbol_id}
            
            params = {
                'page-size': limit,
                'where': json.dumps(where_clause)
            }
            
            response = await self._stargate_request('GET', 'pages_by_section', params=params)
            
            pages = []
            if response and 'data' in response:
                page_ids = [row['id'] for row in response['data']]
                page_tasks = [self.get_page(page_id) for page_id in page_ids]
                pages = [p for p in await asyncio.gather(*page_tasks) if p is not None]
            
            return pages
            
        except Exception as e:
            logger.error(f"Failed to get pages by section {section}: {e}")
            return []
    
    # ========================= VECTOR SEARCH =========================
    
    async def search_similar_pages(self, query_text: str, limit: int = 10, content_type: str = 'page') -> List[Tuple[StoryPage, float]]:
        """Search for pages similar to query text using vector embeddings"""
        if not self.vector_service:
            logger.warning("Vector search not available - falling back to text search")
            # Fallback to simple text search
            pages = await self.get_pages_by_symbol(query_text.lower())
            return [(page, 0.5) for page in pages[:limit]]
        
        try:
            # Generate embedding for query
            query_embedding_result = await self.vector_service.embed_text(
                text=query_text,
                content_id='query',
                content_type='query'
            )
            
            # Get all embeddings for comparison (in production, use vector index)
            params = {
                'where': json.dumps({
                    'content_type': {'$eq': content_type}
                })
            }
            
            response = await self._stargate_request('GET', 'vector_embeddings', params=params)
            
            if not response or 'data' not in response:
                return []
            
            # Calculate similarities
            candidate_embeddings = [
                (row['content_id'], row['embedding']) 
                for row in response['data']
                if row.get('embedding')
            ]
            
            similar_items = self.vector_service.find_most_similar(
                query_embedding_result.embedding,
                candidate_embeddings,
                top_k=limit
            )
            
            # Get full page data for similar items
            results = []
            for content_id, similarity in similar_items:
                page = await self.get_page(content_id)
                if page:
                    results.append((page, similarity))
            
            return results
            
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []
    
    async def get_related_pages(self, page_id: str, limit: int = 5) -> List[Tuple[StoryPage, float]]:
        """Get pages related to a specific page using vector similarity"""
        try:
            # Get the page's embedding
            page = await self.get_page(page_id)
            if not page:
                return []
            
            if not self.vector_service:
                # Fallback: return pages by same symbol
                pages = await self.get_pages_by_symbol(page.symbol_id, limit=limit + 1)
                filtered_pages = [p for p in pages if p.id != page_id][:limit]
                return [(p, 0.7) for p in filtered_pages]
            
            # Search for similar pages
            return await self.search_similar_pages(page.text, limit=limit + 1)  # +1 to exclude self
            
        except Exception as e:
            logger.error(f"Failed to get related pages for {page_id}: {e}")
            return []
    
    # ========================= USERS & SESSIONS =========================
    
    async def create_user(self, user: User) -> User:
        """Create a new user"""
        try:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': int(user.created_at.timestamp() * 1000) if user.created_at else int(datetime.now(timezone.utc).timestamp() * 1000),
                'last_active': int(user.last_active.timestamp() * 1000) if user.last_active else int(datetime.now(timezone.utc).timestamp() * 1000),
                'history': user.history or [],
                'authored_pages': user.authored_pages or [],
                'current_session_id': user.session_id,
                'permissions': dict(user.permissions) if user.permissions else {},
                'preferences': {}
            }
            
            # Insert into main table and username index
            await asyncio.gather(
                self._stargate_request('POST', 'users', data=user_data),
                self._stargate_request('POST', 'users_by_username', data={
                    'username': user.username,
                    'user_id': user.id,
                    'email': user.email,
                    'created_at': user_data['created_at']
                })
            )
            
            logger.info(f"Created user {user.id} ({user.username})")
            return user
            
        except Exception as e:
            logger.error(f"Failed to create user {user.id}: {e}")
            raise
    
    async def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            response = await self._stargate_request('GET', f'users/{user_id}')
            if response:
                return self._dict_to_user(response)
            return None
            
        except Exception as e:
            logger.error(f"Failed to get user {user_id}: {e}")
            return None
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            response = await self._stargate_request('GET', f'users_by_username/{username}')
            if response and 'user_id' in response:
                return await self.get_user(response['user_id'])
            return None
            
        except Exception as e:
            logger.error(f"Failed to get user by username {username}: {e}")
            return None
    
    async def create_session(self, session: SessionData) -> SessionData:
        """Create a new user session"""
        try:
            session_data = {
                'id': session.id,
                'user_id': session.user_id,
                'current_page_index': session.current_page_index,
                'furthest_page_index': session.furthest_page_index,
                'session_start': int(session.session_start.timestamp() * 1000) if session.session_start else int(datetime.now(timezone.utc).timestamp() * 1000),
                'last_activity': int(session.last_activity.timestamp() * 1000) if session.last_activity else int(datetime.now(timezone.utc).timestamp() * 1000),
                'metadata': dict(session.metadata) if session.metadata else {},
                'pages_visited': [],
                'current_branch_id': None
            }
            
            # Insert into main table and user index
            await asyncio.gather(
                self._stargate_request('POST', 'sessions', data=session_data),
                self._stargate_request('POST', 'sessions_by_user', data={
                    'user_id': session.user_id,
                    'session_start': session_data['session_start'],
                    'id': session.id,
                    'last_activity': session_data['last_activity'],
                    'current_page_index': session.current_page_index
                })
            )
            
            logger.info(f"Created session {session.id} for user {session.user_id}")
            return session
            
        except Exception as e:
            logger.error(f"Failed to create session {session.id}: {e}")
            raise
    
    # ========================= HELPER METHODS =========================
    
    async def _stargate_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
        """Make request to Stargate REST API"""
        try:
            url = f"{self.stargate_url}/v2/keyspaces/{self.keyspace}/{endpoint}"
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            if method == 'GET':
                response = await self.http_client.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = await self.http_client.post(url, headers=headers, json=data)
            elif method == 'PUT':
                response = await self.http_client.put(url, headers=headers, json=data)
            elif method == 'DELETE':
                response = await self.http_client.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            if response.status_code in [200, 201]:
                return response.json() if response.content else {}
            else:
                logger.error(f"Stargate request failed: {response.status_code} - {response.text}")
                return {}
                
        except Exception as e:
            logger.error(f"Stargate request error: {e}")
            return {}
    
    async def _insert_page_by_symbol(self, page_data: Dict):
        """Insert into pages_by_symbol index"""
        index_data = {
            'symbol_id': page_data['symbol_id'],
            'page_type': page_data['page_type'],
            'created_at': page_data['created_at'],
            'id': page_data['id'],
            'text': page_data['text'][:500],  # Truncated for index
            'rotation': page_data['rotation'],
            'section': page_data.get('section')
        }
        await self._stargate_request('POST', 'pages_by_symbol', data=index_data)
    
    async def _insert_page_by_section(self, page_data: Dict):
        """Insert into pages_by_section index"""
        if page_data.get('section'):
            index_data = {
                'section': page_data['section'],
                'symbol_id': page_data['symbol_id'],
                'created_at': page_data['created_at'],
                'id': page_data['id'],
                'text': page_data['text'][:500],
                'title': page_data.get('title')
            }
            await self._stargate_request('POST', 'pages_by_section', data=index_data)
    
    async def _insert_page_by_parent(self, page_data: Dict):
        """Insert into pages_by_parent index"""
        if page_data.get('parent_id'):
            index_data = {
                'parent_id': page_data['parent_id'],
                'created_at': page_data['created_at'],
                'id': page_data['id'],
                'symbol_id': page_data['symbol_id'],
                'page_type': page_data['page_type']
            }
            await self._stargate_request('POST', 'pages_by_parent', data=index_data)
    
    async def _insert_vector_embedding(self, embedding_result):
        """Insert into vector_embeddings table"""
        embedding_data = {
            'content_type': embedding_result.content_type,
            'content_id': embedding_result.content_id,
            'embedding': embedding_result.embedding,
            'embedding_model': embedding_result.model,
            'created_at': int(datetime.now(timezone.utc).timestamp() * 1000),
            'metadata': getattr(embedding_result, 'metadata', {})
        }
        await self._stargate_request('POST', 'vector_embeddings', data=embedding_data)
    
    async def _insert_recent_page(self, page_data: Dict):
        """Insert into recent_pages for global feed"""
        bucket = datetime.now(timezone.utc).strftime('%Y-%m-%d-%H')
        recent_data = {
            'bucket': bucket,
            'created_at': page_data['created_at'],
            'id': page_data['id'],
            'symbol_id': page_data['symbol_id'],
            'page_type': page_data['page_type'],
            'author': page_data['author'],
            'text': page_data['text'][:200]  # Truncated
        }
        await self._stargate_request('POST', 'recent_pages', data=recent_data)
    
    def _dict_to_story_page(self, data: Dict) -> StoryPage:
        """Convert dict to StoryPage model"""
        return StoryPage(
            id=data['id'],
            symbol_id=data['symbol_id'],
            rotation=data.get('rotation', 0),
            page_type=data.get('page_type', 'story'),
            parent_id=data.get('parent_id'),
            prompt_type=data.get('prompt_type'),
            text=data.get('text', ''),
            author=data.get('author', 'AI'),
            branch_id=data.get('branch_id'),
            created_at=datetime.fromtimestamp(data['created_at'] / 1000, tz=timezone.utc) if data.get('created_at') else datetime.now(timezone.utc),
            canonical=data.get('canonical', True),
            version=data.get('version', '1.0'),
            title=data.get('title'),
            section=data.get('section'),
            child_ids=set(data.get('child_ids', [])),
            branches=data.get('branches', []),
            prompts=data.get('prompts', []),
            embedding=data.get('embedding')
        )
    
    def _dict_to_user(self, data: Dict) -> User:
        """Convert dict to User model"""
        return User(
            id=data['id'],
            username=data['username'],
            email=data['email'],
            created_at=datetime.fromtimestamp(data['created_at'] / 1000, tz=timezone.utc) if data.get('created_at') else datetime.now(timezone.utc),
            last_active=datetime.fromtimestamp(data['last_active'] / 1000, tz=timezone.utc) if data.get('last_active') else datetime.now(timezone.utc),
            history=data.get('history', []),
            authored_pages=data.get('authored_pages', []),
            session_id=data.get('current_session_id'),
            permissions=data.get('permissions', {})
        )
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            stats = {
                'type': 'cassandra',
                'status': 'connected' if self._connected else 'disconnected',
                'pages': 0,
                'users': 0,
                'sessions': 0,
                'embeddings': 0
            }
            
            # Get approximate counts (simplified)
            if self._connected:
                # In production, use COUNT queries or maintain counters
                stats.update({
                    'pages': 'N/A',  # Implement proper counting
                    'users': 'N/A',
                    'sessions': 'N/A',
                    'embeddings': 'N/A'
                })
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {'type': 'cassandra', 'status': 'error'}

# Global database instance
_cassandra_db = None

def get_cassandra_database() -> ProductionCassandraDatabase:
    """Get or create global Cassandra database instance"""
    global _cassandra_db
    if _cassandra_db is None:
        hosts = os.getenv('CASSANDRA_HOSTS', 'localhost').split(',')
        keyspace = os.getenv('CASSANDRA_KEYSPACE', 'gibsey_network')
        stargate_url = os.getenv('STARGATE_URL', 'http://localhost:8082')
        
        _cassandra_db = ProductionCassandraDatabase(
            hosts=hosts,
            keyspace=keyspace,
            stargate_url=stargate_url
        )
    return _cassandra_db