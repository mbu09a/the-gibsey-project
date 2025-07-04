#!/usr/bin/env python3
"""
Database initialization script for Gibsey Mycelial Network
Sets up Cassandra schema and runs data migration
"""

import asyncio
import sys
import os
import time
import logging

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.cassandra_schema_v2 import setup_optimized_schema
from app.data_migration import run_migration
from app.vector_service import initialize_vector_service

async def wait_for_services(max_wait=300):
    """Wait for Cassandra and Stargate to be ready"""
    logger = logging.getLogger(__name__)
    
    logger.info("Waiting for Cassandra and Stargate services...")
    
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            # Try to connect to Cassandra directly
            from cassandra.cluster import Cluster
            cluster = Cluster(['cassandra'], port=9042)
            session = cluster.connect()
            session.shutdown()
            cluster.shutdown()
            
            logger.info("Cassandra is ready!")
            break
            
        except Exception as e:
            logger.debug(f"Cassandra not ready yet: {e}")
            await asyncio.sleep(5)
    else:
        logger.error("Cassandra did not become ready in time")
        return False
    
    # Wait a bit more for Stargate
    logger.info("Waiting for Stargate...")
    await asyncio.sleep(10)
    
    # Test Stargate connection
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get('http://stargate:8082/health') as response:
                    if response.status == 200:
                        logger.info("Stargate is ready!")
                        return True
        except Exception as e:
            logger.debug(f"Stargate not ready yet: {e}")
            await asyncio.sleep(5)
    
    logger.error("Stargate did not become ready in time")
    return False

async def initialize_database():
    """Complete database initialization process"""
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("🚀 Starting Gibsey database initialization...")
        
        # 1. Wait for services to be ready
        if not await wait_for_services():
            logger.error("Services not ready, aborting initialization")
            return False
        
        # 2. Initialize vector service
        logger.info("Initializing vector embedding service...")
        await initialize_vector_service()
        
        # 3. Setup optimized Cassandra schema
        logger.info("Setting up optimized Cassandra schema...")
        schema_success = setup_optimized_schema()
        
        if not schema_success:
            logger.error("Schema setup failed")
            return False
        
        # 4. Seed corpus data
        logger.info("Seeding corpus data...")
        import subprocess
        import sys
        
        try:
            # Import and run the seeding script directly
            sys.path.append('/app')
            from scripts.seed_embeddings import EmbeddingsSeeder
            
            seeder = EmbeddingsSeeder()
            seeding_success = seeder.run(incremental=False)
            
            if not seeding_success:
                logger.error("Corpus seeding failed")
                return False
            else:
                logger.info("Corpus seeding completed successfully")
                
        except Exception as e:
            logger.error(f"Error running corpus seeding: {e}")
            return False
        
        logger.info("✅ Database initialization completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(initialize_database())
    sys.exit(0 if success else 1)