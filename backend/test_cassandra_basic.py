#!/usr/bin/env python3
"""
Basic Cassandra database test without vector embeddings
Tests the core functionality first
"""

import asyncio
import logging
import uuid
from datetime import datetime, timezone

from app.cassandra_database_v2 import ProductionCassandraDatabase
from app.models import StoryPage, User, SessionData, PageType, AuthorType, SymbolRotation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_basic_operations():
    """Test basic Cassandra operations without vector embeddings"""
    
    logger.info("🧪 Testing basic Cassandra operations...")
    
    # Initialize database
    db = ProductionCassandraDatabase(hosts=['localhost'])
    
    try:
        # Connect to database
        logger.info("Connecting to Cassandra...")
        connected = await db.connect()
        
        if not connected:
            logger.error("❌ Failed to connect to Cassandra")
            return False
        
        logger.info("✅ Connected to Cassandra")
        
        # Test 1: Create a simple page (without embedding for now)
        logger.info("Testing page creation...")
        
        test_page = StoryPage(
            id=str(uuid.uuid4()),
            symbol_id="london-fox",
            text="Test page for London Fox - questioning reality through computational frameworks.",
            page_type=PageType.AI_RESPONSE,
            author=AuthorType.AI,
            rotation=SymbolRotation.NINETY,
            section=1,
            title="Test Page"
        )
        
        # Create with mock embedding to test the flow
        test_page.embedding = [0.1] * 384  # Mock embedding vector
        
        created_page = await db.create_page(test_page)
        logger.info(f"✅ Created page: {created_page.id}")
        
        # Test 2: Retrieve the page
        logger.info("Testing page retrieval...")
        retrieved_page = await db.get_page(test_page.id)
        
        if retrieved_page and retrieved_page.id == test_page.id:
            logger.info("✅ Page retrieval successful")
        else:
            logger.error("❌ Page retrieval failed")
            return False
        
        # Test 3: Get pages by symbol
        logger.info("Testing pages by symbol...")
        london_fox_pages = await db.get_pages_by_symbol("london-fox")
        
        if london_fox_pages and len(london_fox_pages) > 0:
            logger.info(f"✅ Found {len(london_fox_pages)} London Fox pages")
        else:
            logger.error("❌ Failed to get pages by symbol")
            return False
        
        # Test 4: Create a user
        logger.info("Testing user creation...")
        
        test_user = User(
            id=str(uuid.uuid4()),
            username=f"test_user_{int(datetime.now().timestamp())}",
            email="test@gibsey.network"
        )
        
        created_user = await db.create_user(test_user)
        logger.info(f"✅ Created user: {created_user.username}")
        
        # Test 5: Create a session
        logger.info("Testing session creation...")
        
        test_session = SessionData(
            id=str(uuid.uuid4()),
            user_id=test_user.id,
            current_page_index=0,
            furthest_page_index=5
        )
        
        created_session = await db.create_session(test_session)
        logger.info(f"✅ Created session: {created_session.id}")
        
        # Test 6: Get database stats
        logger.info("Testing database stats...")
        stats = await db.get_stats()
        logger.info(f"✅ Database stats: {stats}")
        
        logger.info("🎉 All basic tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        await db.disconnect()

if __name__ == "__main__":
    success = asyncio.run(test_basic_operations())
    print("✅ Basic Cassandra test completed successfully!" if success else "❌ Basic Cassandra test failed!")