#!/usr/bin/env python
"""
SVG file watcher for automatic SREC compilation.
Monitors a directory for new/modified SVG files and processes them automatically.
"""
import os
import sys
import time
import logging
from pathlib import Path
from typing import Set

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent

# Add parent directory to path for SREC imports
sys.path.append(str(Path(__file__).parent.parent))
from srec.compiler import compile_symbol, get_embedded_symbols

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class SVGHandler(FileSystemEventHandler):
    """Handle SVG file system events."""
    
    def __init__(self, processed_files: Set[str]):
        self.processed_files = processed_files
        self._processing = set()  # Track files being processed
        
    def is_svg_file(self, path: str) -> bool:
        """Check if file is an SVG."""
        return Path(path).suffix.lower() == '.svg'
    
    def process_svg(self, file_path: str) -> None:
        """Process a single SVG file."""
        path = Path(file_path)
        
        # Skip if already processing or recently processed
        if file_path in self._processing:
            return
            
        # Check if file has changed since last processing
        try:
            mtime = path.stat().st_mtime
            if file_path in self.processed_files:
                # Skip if file hasn't been modified
                return
                
            self._processing.add(file_path)
            
            logger.info(f"🔄 Processing new/modified SVG: {path.name}")
            
            # Read and compile the SVG
            with open(path, 'rb') as f:
                svg_content = f.read()
            
            symbol_id = path.stem
            compile_symbol(symbol_id, svg_content)
            
            # Mark as processed
            self.processed_files.add(file_path)
            logger.info(f"✅ Successfully compiled: {symbol_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to process {path.name}: {e}")
        finally:
            self._processing.discard(file_path)
    
    def on_created(self, event: FileCreatedEvent) -> None:
        """Handle file creation."""
        if not event.is_directory and self.is_svg_file(event.src_path):
            # Wait a moment for file to be fully written
            time.sleep(0.5)
            self.process_svg(event.src_path)
    
    def on_modified(self, event: FileModifiedEvent) -> None:
        """Handle file modification."""
        if not event.is_directory and self.is_svg_file(event.src_path):
            # Wait a moment for file to be fully written
            time.sleep(0.5)
            self.process_svg(event.src_path)

def get_existing_svgs(directory: Path) -> Set[str]:
    """Get all existing SVG files in directory."""
    return {str(p) for p in directory.glob("**/*.svg")}

def process_initial_files(directory: Path, processed_files: Set[str]) -> None:
    """Process any existing files that haven't been embedded yet."""
    logger.info("🔍 Checking for unprocessed SVG files...")
    
    # Get already embedded symbols
    embedded_symbols = set(get_embedded_symbols())
    
    # Find all SVG files
    svg_files = list(directory.glob("**/*.svg"))
    unprocessed = []
    
    for svg_file in svg_files:
        symbol_id = svg_file.stem
        if symbol_id not in embedded_symbols:
            unprocessed.append(svg_file)
    
    if unprocessed:
        logger.info(f"📦 Found {len(unprocessed)} unprocessed SVG files")
        handler = SVGHandler(processed_files)
        
        for svg_file in unprocessed:
            handler.process_svg(str(svg_file))
    else:
        logger.info("✅ All SVG files are already processed")

def watch_directory(path: str, process_existing: bool = True) -> None:
    """
    Watch a directory for SVG file changes.
    
    Args:
        path: Directory path to watch
        process_existing: Whether to process existing files on startup
    """
    directory = Path(path)
    if not directory.exists():
        logger.error(f"Directory not found: {directory}")
        sys.exit(1)
    
    logger.info(f"👁️  Starting SVG watcher for: {directory}")
    logger.info(f"🔗 ChromaDB: {os.getenv('CHROMA_HOST', 'localhost')}:{os.getenv('CHROMA_PORT', '8001')}")
    
    # Track processed files to avoid duplicates
    processed_files = set()
    
    # Process existing files if requested
    if process_existing:
        process_initial_files(directory, processed_files)
        # Mark all existing files as processed to avoid reprocessing
        processed_files.update(get_existing_svgs(directory))
    
    # Set up file watcher
    event_handler = SVGHandler(processed_files)
    observer = Observer()
    observer.schedule(event_handler, str(directory), recursive=True)
    
    # Start watching
    observer.start()
    logger.info("🚀 Watcher started. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("🛑 Watcher stopped")
    
    observer.join()

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Watch directory for SVG files and auto-compile with SREC")
    parser.add_argument("directory", help="Directory to watch for SVG files")
    parser.add_argument("--skip-existing", action="store_true", 
                       help="Skip processing existing files on startup")
    parser.add_argument("--chroma-host", default="localhost",
                       help="ChromaDB host (default: localhost)")
    parser.add_argument("--chroma-port", default="8001",
                       help="ChromaDB port (default: 8001)")
    
    args = parser.parse_args()
    
    # Set environment variables
    os.environ["CHROMA_HOST"] = args.chroma_host
    os.environ["CHROMA_PORT"] = args.chroma_port
    
    # Start watching
    watch_directory(args.directory, process_existing=not args.skip_existing)

if __name__ == "__main__":
    main()