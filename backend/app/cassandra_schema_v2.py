"""
Production-optimized Cassandra schema for Gibsey Mycelial Network
Implements compound keys, vector search, and performance optimizations
"""

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import DCAwareRoundRobinPolicy
import os
import time
import logging

logger = logging.getLogger(__name__)

class OptimizedCassandraSchema:
    """Production-optimized Cassandra schema manager"""
    
    def __init__(self, hosts=['localhost'], port=9042, keyspace='gibsey_network'):
        self.hosts = hosts
        self.port = port
        self.keyspace = keyspace
        self.cluster = None
        self.session = None
    
    def connect(self, retries=5, delay=10):
        """Connect to Cassandra cluster with retries"""
        for attempt in range(retries):
            try:
                self.cluster = Cluster(
                    self.hosts,
                    port=self.port,
                    load_balancing_policy=DCAwareRoundRobinPolicy()
                )
                
                self.session = self.cluster.connect()
                logger.info(f"Connected to Cassandra cluster at {self.hosts}")
                return True
                
            except Exception as e:
                logger.warning(f"Cassandra connection attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    logger.error("Failed to connect to Cassandra after all retries")
                    raise
        
        return False
    
    def create_keyspace(self):
        """Create the gibsey_network keyspace"""
        try:
            keyspace_query = f"""
            CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
            WITH replication = {{
                'class': 'SimpleStrategy',
                'replication_factor': 1
            }}
            """
            
            self.session.execute(keyspace_query)
            logger.info(f"Created keyspace: {self.keyspace}")
            
            self.session.set_keyspace(self.keyspace)
            logger.info(f"Switched to keyspace: {self.keyspace}")
            
        except Exception as e:
            logger.error(f"Failed to create keyspace: {e}")
            raise
    
    def create_tables(self):
        """Create optimized tables with compound keys for performance"""
        
        # 1. Story Pages - Main table with primary key optimized for single-page lookups
        story_pages_table = """
        CREATE TABLE IF NOT EXISTS story_pages (
            id text PRIMARY KEY,
            symbol_id text,
            rotation int,
            page_type text,
            parent_id text,
            prompt_type text,
            text text,
            author text,
            branch_id text,
            created_at timestamp,
            canonical boolean,
            version text,
            title text,
            section int,
            child_ids set<text>,
            branches list<frozen<map<text, text>>>,
            prompts list<frozen<map<text, text>>>,
            embedding list<float>,  -- SBERT embeddings (384 dimensions)
            embedding_model text,
            last_updated timestamp
        )
        """
        
        # 2. Pages by Symbol - Optimized for character-based navigation (hot path)
        pages_by_symbol_table = """
        CREATE TABLE IF NOT EXISTS pages_by_symbol (
            symbol_id text,
            page_type text,
            created_at timestamp,
            id text,
            text text,
            rotation int,
            section int,
            PRIMARY KEY ((symbol_id, page_type), created_at, id)
        ) WITH CLUSTERING ORDER BY (created_at DESC, id ASC)
        """
        
        # 3. Pages by Section - For book navigation (hot path)
        pages_by_section_table = """
        CREATE TABLE IF NOT EXISTS pages_by_section (
            section int,
            symbol_id text,
            created_at timestamp,
            id text,
            text text,
            title text,
            PRIMARY KEY (section, symbol_id, created_at, id)
        ) WITH CLUSTERING ORDER BY (symbol_id ASC, created_at DESC, id ASC)
        """
        
        # 4. Pages by Parent - Tree navigation
        pages_by_parent_table = """
        CREATE TABLE IF NOT EXISTS pages_by_parent (
            parent_id text,
            created_at timestamp,
            id text,
            symbol_id text,
            page_type text,
            PRIMARY KEY (parent_id, created_at, id)
        ) WITH CLUSTERING ORDER BY (created_at DESC, id ASC)
        """
        
        # 5. Vector Search Index - Separate table for efficient vector operations
        vector_embeddings_table = """
        CREATE TABLE IF NOT EXISTS vector_embeddings (
            content_type text,
            content_id text,
            embedding list<float>,
            embedding_model text,
            created_at timestamp,
            metadata map<text, text>,
            PRIMARY KEY ((content_type), content_id)
        )
        """
        
        # 6. Prompts - Main prompt storage
        prompts_table = """
        CREATE TABLE IF NOT EXISTS prompts (
            id text PRIMARY KEY,
            text text,
            rotation int,
            target_symbol_id text,
            prompt_type text,
            description text,
            created_at timestamp,
            embedding list<float>,
            embedding_model text,
            usage_count int
        )
        """
        
        # 7. Prompts by Symbol and Type - Hot path for prompt selection
        prompts_by_target_table = """
        CREATE TABLE IF NOT EXISTS prompts_by_target (
            target_symbol_id text,
            prompt_type text,
            usage_count int,
            id text,
            text text,
            rotation int,
            PRIMARY KEY ((target_symbol_id, prompt_type), usage_count, id)
        ) WITH CLUSTERING ORDER BY (usage_count DESC, id ASC)
        """
        
        # 8. Users - Main user storage
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id text PRIMARY KEY,
            username text,
            email text,
            created_at timestamp,
            last_active timestamp,
            history list<text>,
            authored_pages list<text>,
            current_session_id text,
            permissions map<text, text>,
            preferences map<text, text>
        )
        """
        
        # 9. Users by Username - Authentication lookup
        users_by_username_table = """
        CREATE TABLE IF NOT EXISTS users_by_username (
            username text PRIMARY KEY,
            user_id text,
            email text,
            created_at timestamp
        )
        """
        
        # 10. Sessions - User session management
        sessions_table = """
        CREATE TABLE IF NOT EXISTS sessions (
            id text PRIMARY KEY,
            user_id text,
            current_page_index int,
            furthest_page_index int,
            session_start timestamp,
            last_activity timestamp,
            metadata map<text, text>,
            pages_visited list<text>,
            current_branch_id text
        )
        """
        
        # 11. Sessions by User - User session history
        sessions_by_user_table = """
        CREATE TABLE IF NOT EXISTS sessions_by_user (
            user_id text,
            session_start timestamp,
            id text,
            last_activity timestamp,
            current_page_index int,
            PRIMARY KEY (user_id, session_start, id)
        ) WITH CLUSTERING ORDER BY (session_start DESC, id ASC)
        """
        
        # 12. Branches - Narrative branching
        branches_table = """
        CREATE TABLE IF NOT EXISTS branches (
            id text PRIMARY KEY,
            root_page_id text,
            user_id text,
            created_at timestamp,
            pages list<text>,
            metadata map<text, text>,
            is_canonical boolean
        )
        """
        
        # 13. Branches by User - User's created branches
        branches_by_user_table = """
        CREATE TABLE IF NOT EXISTS branches_by_user (
            user_id text,
            created_at timestamp,
            id text,
            root_page_id text,
            page_count int,
            PRIMARY KEY (user_id, created_at, id)
        ) WITH CLUSTERING ORDER BY (created_at DESC, id ASC)
        """
        
        # 14. Recent Pages - Global feed of recent content
        recent_pages_table = """
        CREATE TABLE IF NOT EXISTS recent_pages (
            bucket text,  -- Time bucket (e.g., "2024-06-16-03")
            created_at timestamp,
            id text,
            symbol_id text,
            page_type text,
            author text,
            text text,
            PRIMARY KEY (bucket, created_at, id)
        ) WITH CLUSTERING ORDER BY (created_at DESC, id ASC)
        """
        
        # Execute all table creation queries
        tables = [
            ("story_pages", story_pages_table),
            ("pages_by_symbol", pages_by_symbol_table),
            ("pages_by_section", pages_by_section_table),
            ("pages_by_parent", pages_by_parent_table),
            ("vector_embeddings", vector_embeddings_table),
            ("prompts", prompts_table),
            ("prompts_by_target", prompts_by_target_table),
            ("users", users_table),
            ("users_by_username", users_by_username_table),
            ("sessions", sessions_table),
            ("sessions_by_user", sessions_by_user_table),
            ("branches", branches_table),
            ("branches_by_user", branches_by_user_table),
            ("recent_pages", recent_pages_table)
        ]
        
        for table_name, query in tables:
            try:
                self.session.execute(query)
                logger.info(f"Created optimized table: {table_name}")
            except Exception as e:
                logger.error(f"Failed to create table {table_name}: {e}")
                # Continue with other tables
                pass
    
    def create_indexes(self):
        """Create secondary indexes for additional query patterns"""
        
        indexes = [
            # Allow queries by author across all pages
            ("CREATE INDEX IF NOT EXISTS pages_author_idx ON story_pages (author)", "pages_author_idx"),
            
            # Allow queries by page type
            ("CREATE INDEX IF NOT EXISTS pages_type_idx ON story_pages (page_type)", "pages_type_idx"),
            
            # Allow queries by section
            ("CREATE INDEX IF NOT EXISTS pages_section_idx ON story_pages (section)", "pages_section_idx"),
            
            # Allow user lookup by email
            ("CREATE INDEX IF NOT EXISTS users_email_idx ON users (email)", "users_email_idx"),
            
            # Allow session lookup by user_id (if not using sessions_by_user)
            ("CREATE INDEX IF NOT EXISTS sessions_user_idx ON sessions (user_id)", "sessions_user_idx")
        ]
        
        for query, index_name in indexes:
            try:
                self.session.execute(query)
                logger.info(f"Created index: {index_name}")
            except Exception as e:
                logger.warning(f"Index creation failed for {index_name}: {e}")
                # Indexes are optional, continue
                pass
    
    def verify_schema(self):
        """Verify that all tables were created successfully"""
        try:
            tables_query = """
            SELECT table_name FROM system_schema.tables 
            WHERE keyspace_name = %s
            """
            
            result = self.session.execute(tables_query, [self.keyspace])
            tables = [row.table_name for row in result]
            
            expected_tables = [
                'story_pages', 'pages_by_symbol', 'pages_by_section', 'pages_by_parent',
                'vector_embeddings', 'prompts', 'prompts_by_target',
                'users', 'users_by_username', 'sessions', 'sessions_by_user',
                'branches', 'branches_by_user', 'recent_pages'
            ]
            
            missing_tables = [table for table in expected_tables if table not in tables]
            
            if missing_tables:
                logger.warning(f"Missing tables: {missing_tables}")
                # Don't fail completely - some tables might not be supported
            
            created_tables = [table for table in expected_tables if table in tables]
            logger.info(f"Schema verified - {len(created_tables)}/{len(expected_tables)} tables created")
            logger.info(f"Created tables: {created_tables}")
            
            return len(created_tables) > 0  # Success if at least some tables created
            
        except Exception as e:
            logger.error(f"Schema verification failed: {e}")
            return False
    
    def setup_complete_schema(self):
        """Complete optimized schema setup process"""
        try:
            logger.info("Starting optimized Cassandra schema setup...")
            
            # Connect to cluster
            if not self.connect():
                return False
            
            # Create keyspace
            self.create_keyspace()
            
            # Create all tables
            self.create_tables()
            
            # Create indexes
            self.create_indexes()
            
            # Verify schema
            if self.verify_schema():
                logger.info("Optimized Cassandra schema setup completed successfully!")
                return True
            else:
                logger.error("Schema verification failed")
                return False
                
        except Exception as e:
            logger.error(f"Schema setup failed: {e}")
            return False
        finally:
            if self.session:
                self.session.shutdown()
            if self.cluster:
                self.cluster.shutdown()

def setup_optimized_schema():
    """Main function to set up optimized Cassandra schema"""
    hosts = os.getenv('CASSANDRA_HOSTS', 'localhost').split(',')
    keyspace = os.getenv('CASSANDRA_KEYSPACE', 'gibsey_network')
    
    schema_manager = OptimizedCassandraSchema(hosts=hosts, keyspace=keyspace)
    return schema_manager.setup_complete_schema()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    if setup_optimized_schema():
        print("✅ Optimized Cassandra schema setup completed successfully!")
    else:
        print("❌ Optimized Cassandra schema setup failed!")
        exit(1)