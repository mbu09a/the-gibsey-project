"""
Cassandra schema definition for the Gibsey Mycelial Network
Implements the data models from the PRD with vector support
"""

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import DCAwareRoundRobinPolicy
import os
import time
import logging

logger = logging.getLogger(__name__)

class CassandraSchemaManager:
    """Manages Cassandra keyspace and table creation"""
    
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
                # Create cluster connection
                self.cluster = Cluster(
                    self.hosts,
                    port=self.port,
                    load_balancing_policy=DCAwareRoundRobinPolicy()
                )
                
                # Connect to cluster (system keyspace first)
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
            
            # Switch to the new keyspace
            self.session.set_keyspace(self.keyspace)
            logger.info(f"Switched to keyspace: {self.keyspace}")
            
        except Exception as e:
            logger.error(f"Failed to create keyspace: {e}")
            raise
    
    def create_tables(self):
        """Create all tables for the Gibsey data model"""
        
        # 1. StoryPage table - main content storage
        story_page_table = """
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
            embedding list<float>  -- For vector storage
        )
        """
        
        # 2. Pages by symbol index - for character-based queries
        pages_by_symbol_table = """
        CREATE TABLE IF NOT EXISTS pages_by_symbol (
            symbol_id text,
            created_at timestamp,
            id text,
            PRIMARY KEY (symbol_id, created_at, id)
        ) WITH CLUSTERING ORDER BY (created_at DESC)
        """
        
        # 3. Pages by parent index - for tree navigation
        pages_by_parent_table = """
        CREATE TABLE IF NOT EXISTS pages_by_parent (
            parent_id text,
            created_at timestamp,
            id text,
            PRIMARY KEY (parent_id, created_at, id)
        ) WITH CLUSTERING ORDER BY (created_at DESC)
        """
        
        # 4. PromptOption table
        prompt_options_table = """
        CREATE TABLE IF NOT EXISTS prompt_options (
            id text PRIMARY KEY,
            text text,
            rotation int,
            target_symbol_id text,
            prompt_type text,
            description text,
            embedding list<float>
        )
        """
        
        # 5. Prompts by target symbol index
        prompts_by_symbol_table = """
        CREATE TABLE IF NOT EXISTS prompts_by_symbol (
            target_symbol_id text,
            prompt_type text,
            id text,
            PRIMARY KEY (target_symbol_id, prompt_type, id)
        )
        """
        
        # 6. User table
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id text PRIMARY KEY,
            username text,
            email text,
            created_at timestamp,
            last_active timestamp,
            history list<text>,
            authored_pages list<text>,
            session_id text,
            permissions map<text, text>
        )
        """
        
        # 7. Users by username index
        users_by_username_table = """
        CREATE TABLE IF NOT EXISTS users_by_username (
            username text PRIMARY KEY,
            user_id text
        )
        """
        
        # 8. Session table
        sessions_table = """
        CREATE TABLE IF NOT EXISTS sessions (
            id text PRIMARY KEY,
            user_id text,
            current_page_index int,
            furthest_page_index int,
            session_start timestamp,
            last_activity timestamp,
            metadata map<text, text>
        )
        """
        
        # 9. Branch table
        branches_table = """
        CREATE TABLE IF NOT EXISTS branches (
            id text PRIMARY KEY,
            root_page_id text,
            user_id text,
            created_at timestamp,
            pages list<text>
        )
        """
        
        # 10. Branches by user index
        branches_by_user_table = """
        CREATE TABLE IF NOT EXISTS branches_by_user (
            user_id text,
            created_at timestamp,
            id text,
            PRIMARY KEY (user_id, created_at, id)
        ) WITH CLUSTERING ORDER BY (created_at DESC)
        """
        
        # 11. Motif table
        motifs_table = """
        CREATE TABLE IF NOT EXISTS motifs (
            id text PRIMARY KEY,
            text text,
            color text,
            symbol text,
            occurrences list<text>,
            embedding list<float>
        )
        """
        
        # 12. Cluster events table
        cluster_events_table = """
        CREATE TABLE IF NOT EXISTS cluster_events (
            id text PRIMARY KEY,
            event_type text,
            timestamp timestamp,
            related_page_id text,
            metadata map<text, text>
        )
        """
        
        # 13. Events by type index
        events_by_type_table = """
        CREATE TABLE IF NOT EXISTS events_by_type (
            event_type text,
            timestamp timestamp,
            id text,
            PRIMARY KEY (event_type, timestamp, id)
        ) WITH CLUSTERING ORDER BY (timestamp DESC)
        """
        
        # Execute all table creation queries
        tables = [
            ("story_pages", story_page_table),
            ("pages_by_symbol", pages_by_symbol_table),
            ("pages_by_parent", pages_by_parent_table),
            ("prompt_options", prompt_options_table),
            ("prompts_by_symbol", prompts_by_symbol_table),
            ("users", users_table),
            ("users_by_username", users_by_username_table),
            ("sessions", sessions_table),
            ("branches", branches_table),
            ("branches_by_user", branches_by_user_table),
            ("motifs", motifs_table),
            ("cluster_events", cluster_events_table),
            ("events_by_type", events_by_type_table)
        ]
        
        for table_name, query in tables:
            try:
                self.session.execute(query)
                logger.info(f"Created table: {table_name}")
            except Exception as e:
                logger.error(f"Failed to create table {table_name}: {e}")
                raise
    
    def verify_schema(self):
        """Verify that all tables were created successfully"""
        try:
            # Query system tables to verify our tables exist
            tables_query = """
            SELECT table_name FROM system_schema.tables 
            WHERE keyspace_name = %s
            """
            
            result = self.session.execute(tables_query, [self.keyspace])
            tables = [row.table_name for row in result]
            
            expected_tables = [
                'story_pages', 'pages_by_symbol', 'pages_by_parent',
                'prompt_options', 'prompts_by_symbol',
                'users', 'users_by_username', 'sessions',
                'branches', 'branches_by_user',
                'motifs', 'cluster_events', 'events_by_type'
            ]
            
            missing_tables = [table for table in expected_tables if table not in tables]
            
            if missing_tables:
                logger.error(f"Missing tables: {missing_tables}")
                return False
            
            logger.info(f"Schema verified - all {len(expected_tables)} tables created")
            return True
            
        except Exception as e:
            logger.error(f"Schema verification failed: {e}")
            return False
    
    def setup_complete_schema(self):
        """Complete schema setup process"""
        try:
            logger.info("Starting Cassandra schema setup...")
            
            # Connect to cluster
            self.connect()
            
            # Create keyspace
            self.create_keyspace()
            
            # Create all tables
            self.create_tables()
            
            # Verify schema
            if self.verify_schema():
                logger.info("Cassandra schema setup completed successfully!")
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
    
    def drop_keyspace(self):
        """Drop the entire keyspace (for development/testing)"""
        try:
            drop_query = f"DROP KEYSPACE IF EXISTS {self.keyspace}"
            self.session.execute(drop_query)
            logger.info(f"Dropped keyspace: {self.keyspace}")
        except Exception as e:
            logger.error(f"Failed to drop keyspace: {e}")
            raise

def setup_cassandra_schema():
    """Main function to set up Cassandra schema"""
    # Get configuration from environment
    hosts = os.getenv('CASSANDRA_HOSTS', 'localhost').split(',')
    keyspace = os.getenv('CASSANDRA_KEYSPACE', 'gibsey_network')
    
    schema_manager = CassandraSchemaManager(hosts=hosts, keyspace=keyspace)
    return schema_manager.setup_complete_schema()

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Run schema setup
    if setup_cassandra_schema():
        print("✅ Cassandra schema setup completed successfully!")
    else:
        print("❌ Cassandra schema setup failed!")
        exit(1)