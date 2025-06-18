#!/usr/bin/env python3
"""
Direct Cassandra test - bypassing Stargate for now
Tests the core functionality with native Cassandra driver
"""

import asyncio
import logging
import uuid
from datetime import datetime, timezone

from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_direct_cassandra():
    """Test direct Cassandra connection and basic operations"""
    
    logger.info("🧪 Testing direct Cassandra connection...")
    
    try:
        # Connect to Cassandra with correct protocol version
        cluster = Cluster(
            ['localhost'],
            port=9042,
            protocol_version=4  # Use protocol version 4 for Cassandra 3.11
        )
        
        # Get session in thread pool
        loop = asyncio.get_event_loop()
        session = await loop.run_in_executor(
            None, 
            lambda: cluster.connect('gibsey_network')
        )
        
        logger.info("✅ Connected to Cassandra")
        
        # Test 1: Check tables exist
        logger.info("Testing table existence...")
        
        tables_query = "SELECT table_name FROM system_schema.tables WHERE keyspace_name = 'gibsey_network'"
        result = await loop.run_in_executor(None, session.execute, tables_query)
        
        tables = [row.table_name for row in result]
        logger.info(f"Found tables: {tables}")
        
        if 'story_pages' in tables:
            logger.info("✅ story_pages table exists")
        else:
            logger.error("❌ story_pages table not found")
            return False
        
        # Test 2: Insert a test page
        logger.info("Testing page insertion...")
        
        page_id = str(uuid.uuid4())
        
        # Use prepared statement
        insert_query = """
        INSERT INTO story_pages (
            id, symbol_id, rotation, page_type, text, author, 
            created_at, canonical, version, embedding, embedding_model
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        prepared = await loop.run_in_executor(None, session.prepare, insert_query)
        
        values = [
            page_id,
            'london-fox',
            90,
            'ai_response',
            'Test page for direct Cassandra insertion',
            'AI',
            int(datetime.now(timezone.utc).timestamp() * 1000),
            True,
            '1.0',
            [0.1] * 384,  # Mock embedding
            'mock'
        ]
        
        await loop.run_in_executor(None, session.execute, prepared, values)
        logger.info(f"✅ Inserted page with ID: {page_id}")
        
        # Test 3: Retrieve the page
        logger.info("Testing page retrieval...")
        
        select_query = "SELECT id, symbol_id, text FROM story_pages WHERE id = ?"
        select_prepared = await loop.run_in_executor(None, session.prepare, select_query)
        result = await loop.run_in_executor(None, session.execute, select_prepared, [page_id])
        
        rows = list(result)
        if rows:
            row = rows[0]
            logger.info(f"✅ Retrieved page: {row.id} - {row.symbol_id} - {row.text[:50]}...")
        else:
            logger.error("❌ Failed to retrieve page")
            return False
        
        # Test 4: Test index table
        logger.info("Testing index table insertion...")
        
        index_query = """
        INSERT INTO pages_by_symbol (symbol_id, page_type, created_at, id, text, rotation)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        index_prepared = await loop.run_in_executor(None, session.prepare, index_query)
        
        index_values = [
            'london-fox',
            'ai_response', 
            int(datetime.now(timezone.utc).timestamp() * 1000),
            page_id,
            'Test page for direct Cassandra insertion',
            90
        ]
        
        await loop.run_in_executor(None, session.execute, index_prepared, index_values)
        logger.info("✅ Inserted into index table")
        
        # Test 5: Query by symbol
        logger.info("Testing symbol-based query...")
        
        symbol_query = "SELECT id, text FROM pages_by_symbol WHERE symbol_id = ? AND page_type = ?"
        symbol_prepared = await loop.run_in_executor(None, session.prepare, symbol_query)
        result = await loop.run_in_executor(None, session.execute, symbol_prepared, ['london-fox', 'ai_response'])
        
        symbol_rows = list(result)
        if symbol_rows:
            logger.info(f"✅ Found {len(symbol_rows)} pages for london-fox")
        else:
            logger.error("❌ No pages found for london-fox")
            return False
        
        logger.info("🎉 All direct Cassandra tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        try:
            if 'session' in locals():
                await loop.run_in_executor(None, session.shutdown)
            if 'cluster' in locals():
                await loop.run_in_executor(None, cluster.shutdown)
        except:
            pass

if __name__ == "__main__":
    success = asyncio.run(test_direct_cassandra())
    print("✅ Direct Cassandra test completed successfully!" if success else "❌ Direct Cassandra test failed!")