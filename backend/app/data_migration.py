"""
Data migration script to transfer existing JSON data to Cassandra
Migrates story pages from frontend JSON to the new database schema
"""

import json
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

from app.models import StoryPage, PageType, AuthorType, SymbolRotation
from app.stargate_client import StargateClient
from app.cassandra_schema import setup_cassandra_schema

logger = logging.getLogger(__name__)

class DataMigrator:
    """Handles migration of existing data to Cassandra"""
    
    def __init__(self, stargate_client: StargateClient):
        self.client = stargate_client
        self.migration_stats = {
            'pages_migrated': 0,
            'pages_failed': 0,
            'total_pages': 0
        }
    
    async def load_json_data(self, json_path: str) -> Dict[str, Any]:
        """Load data from frontend JSON file"""
        try:
            json_file = Path(json_path)
            if not json_file.exists():
                # Try relative path from backend
                json_file = Path(__file__).parent.parent.parent / "src" / "assets" / "texts.json"
            
            if not json_file.exists():
                raise FileNotFoundError(f"Could not find JSON data file at {json_path} or relative path")
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"Loaded JSON data from {json_file}")
            return data
            
        except Exception as e:
            logger.error(f"Error loading JSON data: {e}")
            raise
    
    def convert_json_page_to_model(self, page_data: Dict[str, Any], index: int) -> StoryPage:
        """Convert JSON page data to StoryPage model"""
        try:
            # Map JSON fields to model fields
            story_page = StoryPage(
                id=page_data.get('id', f"page_{index}"),
                symbol_id=page_data.get('symbolId', 'unknown'),
                rotation=SymbolRotation(page_data.get('rotation', 0)),
                page_type=PageType.PRIMARY,  # All existing pages are primary story
                text=page_data.get('text', ''),
                author=AuthorType.SYSTEM,  # Existing content is system-generated
                title=page_data.get('title'),
                section=page_data.get('section'),
                child_ids=page_data.get('childIds', []),
                branches=page_data.get('branches', []),
                prompts=page_data.get('prompts', []),
                created_at=datetime.utcnow(),  # Use current time for migration
                canonical=True,
                version="1.0"
            )
            
            return story_page
            
        except Exception as e:
            logger.error(f"Error converting page {index}: {e}")
            raise
    
    async def migrate_pages(self, pages_data: List[Dict[str, Any]]) -> bool:
        """Migrate all pages to Cassandra"""
        self.migration_stats['total_pages'] = len(pages_data)
        
        logger.info(f"Starting migration of {len(pages_data)} pages...")
        
        for index, page_data in enumerate(pages_data):
            try:
                # Convert to StoryPage model
                story_page = self.convert_json_page_to_model(page_data, index)
                
                # Insert into Cassandra
                await self.client.create_page(story_page)
                
                self.migration_stats['pages_migrated'] += 1
                
                if (index + 1) % 10 == 0:
                    logger.info(f"Migrated {index + 1}/{len(pages_data)} pages...")
                
            except Exception as e:
                logger.error(f"Failed to migrate page {index}: {e}")
                self.migration_stats['pages_failed'] += 1
                
                # Continue with other pages instead of failing completely
                continue
        
        # Log final stats
        logger.info(f"Migration completed:")
        logger.info(f"  Total pages: {self.migration_stats['total_pages']}")
        logger.info(f"  Successfully migrated: {self.migration_stats['pages_migrated']}")
        logger.info(f"  Failed: {self.migration_stats['pages_failed']}")
        
        return self.migration_stats['pages_failed'] == 0
    
    async def verify_migration(self) -> bool:
        """Verify that migration was successful"""
        try:
            # Get all pages from Cassandra
            migrated_pages = await self.client.get_pages(page_size=1000)
            
            logger.info(f"Verification: Found {len(migrated_pages)} pages in Cassandra")
            
            # Check if we have the expected number of pages
            expected_count = self.migration_stats['pages_migrated']
            actual_count = len(migrated_pages)
            
            if actual_count != expected_count:
                logger.warning(f"Page count mismatch: expected {expected_count}, found {actual_count}")
                return False
            
            # Verify some basic data integrity
            for page in migrated_pages[:5]:  # Check first 5 pages
                if not page.id or not page.symbol_id or not page.text:
                    logger.error(f"Data integrity issue in page {page.id}")
                    return False
            
            logger.info("Migration verification passed!")
            return True
            
        except Exception as e:
            logger.error(f"Migration verification failed: {e}")
            return False
    
    async def run_full_migration(self, json_path: str = None) -> bool:
        """Run the complete migration process"""
        try:
            logger.info("Starting full data migration...")
            
            # 1. Load JSON data
            if not json_path:
                json_path = "../src/assets/texts.json"
            
            json_data = await self.load_json_data(json_path)
            pages_data = json_data.get('pages', [])
            
            if not pages_data:
                logger.warning("No pages found in JSON data")
                return True
            
            # 2. Migrate pages
            migration_success = await self.migrate_pages(pages_data)
            
            # 3. Verify migration
            if migration_success:
                verification_success = await self.verify_migration()
                return verification_success
            else:
                logger.error("Migration failed, skipping verification")
                return False
                
        except Exception as e:
            logger.error(f"Full migration failed: {e}")
            return False

async def run_migration():
    """Main migration function"""
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        logger.info("🚀 Starting Gibsey data migration...")
        
        # 1. Setup Cassandra schema
        logger.info("Setting up Cassandra schema...")
        schema_success = setup_cassandra_schema()
        
        if not schema_success:
            logger.error("Schema setup failed, aborting migration")
            return False
        
        # 2. Initialize Stargate client
        logger.info("Connecting to Stargate...")
        async with StargateClient() as client:
            # Wait a moment for Stargate to be ready
            await asyncio.sleep(2)
            
            # 3. Run migration
            migrator = DataMigrator(client)
            success = await migrator.run_full_migration()
            
            if success:
                logger.info("✅ Migration completed successfully!")
                return True
            else:
                logger.error("❌ Migration failed!")
                return False
                
    except Exception as e:
        logger.error(f"Migration process failed: {e}")
        return False

if __name__ == "__main__":
    # Run the migration
    success = asyncio.run(run_migration())
    exit(0 if success else 1)