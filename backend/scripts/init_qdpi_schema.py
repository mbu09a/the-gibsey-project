#!/usr/bin/env python3
"""Initialize QDPI schema in Cassandra"""

import os
import sys
from pathlib import Path
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / ".env")

def init_qdpi_schema():
    """Initialize QDPI tables in Cassandra"""
    
    # Connect to Cassandra
    hosts = os.getenv("CASSANDRA_HOSTS", "localhost:9042").split(",")
    hosts = [h.split(":")[0] for h in hosts]  # Extract host without port
    keyspace = os.getenv("CASSANDRA_KEYSPACE", "gibsey")
    
    print(f"Connecting to Cassandra hosts: {hosts}")
    
    try:
        cluster = Cluster(hosts)
        session = cluster.connect()
        
        # Read and execute CQL script
        cql_path = Path(__file__).parent.parent.parent / "scripts" / "cassandra_qdpi_init.cql"
        with open(cql_path, 'r') as f:
            statements = f.read().split(';')
            
        for stmt in statements:
            stmt = stmt.strip()
            if stmt:
                print(f"Executing: {stmt[:50]}...")
                try:
                    session.execute(stmt)
                except Exception as e:
                    print(f"Warning: {e}")
        
        # Verify tables were created
        session.execute(f"USE {keyspace}")
        result = session.execute("DESCRIBE TABLES")
        tables = [row[0] for row in result]
        
        print(f"\nTables in keyspace '{keyspace}':")
        for table in sorted(tables):
            print(f"  - {table}")
        
        print(f"\n✅ QDPI schema initialized successfully!")
        
        cluster.shutdown()
        
    except Exception as e:
        print(f"❌ Error initializing schema: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_qdpi_schema()