#!/usr/bin/env python
"""
SREC startup script - ensures all symbols are compiled on backend launch.
Idempotent: only processes symbols that aren't already in ChromaDB.
"""
import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from srec.compiler import compile_symbol, get_embedded_symbols, get_embedding_count

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def find_svg_directories() -> List[Path]:
    """Find potential SVG directories in the project."""
    project_root = Path(__file__).parent.parent.parent  # backend/srec -> project root
    potential_dirs = [
        project_root / "public" / "corpus-symbols",
        project_root / "assets" / "symbols",
        project_root / "static" / "symbols",
        Path(os.getenv("CORPUS_SYMBOLS_DIR", ""))
    ]
    
    existing_dirs = [d for d in potential_dirs if d.exists() and d.is_dir()]
    return existing_dirs

def get_unprocessed_symbols(svg_dir: Path) -> List[Path]:
    """Get SVG files that haven't been processed yet."""
    # Get already embedded symbols
    embedded_symbols = set(get_embedded_symbols())
    
    # Find all SVG files
    svg_files = list(svg_dir.glob("**/*.svg"))
    unprocessed = []
    
    for svg_file in svg_files:
        symbol_id = svg_file.stem
        if symbol_id not in embedded_symbols:
            unprocessed.append(svg_file)
    
    return unprocessed

def process_symbols(svg_files: List[Path]) -> Dict[str, Any]:
    """Process a list of SVG files and return results."""
    results = {
        "processed": 0,
        "failed": 0,
        "errors": []
    }
    
    for svg_file in svg_files:
        try:
            logger.info(f"Processing: {svg_file.name}")
            with open(svg_file, 'rb') as f:
                compile_symbol(svg_file.stem, f.read())
            results["processed"] += 1
        except Exception as e:
            logger.error(f"Failed to process {svg_file.name}: {e}")
            results["failed"] += 1
            results["errors"].append({
                "file": str(svg_file),
                "error": str(e)
            })
    
    return results

def ensure_all_symbols_compiled() -> Dict[str, Any]:
    """
    Ensure all symbols in known directories are compiled.
    This is idempotent - only processes new/missing symbols.
    """
    logger.info("🚀 SREC Startup: Checking symbol embeddings...")
    
    # Get initial counts
    initial_count = get_embedding_count()
    initial_symbols = get_embedded_symbols()
    
    logger.info(f"📊 Current state: {len(initial_symbols)} symbols, {initial_count} embeddings")
    
    # Find SVG directories
    svg_dirs = find_svg_directories()
    if not svg_dirs:
        logger.warning("⚠️  No SVG directories found")
        return {
            "status": "no_directories",
            "message": "No SVG directories found",
            "initial_embeddings": initial_count
        }
    
    logger.info(f"📁 Found {len(svg_dirs)} SVG directories:")
    for d in svg_dirs:
        logger.info(f"   - {d}")
    
    # Process each directory
    total_results = {
        "processed": 0,
        "failed": 0,
        "errors": [],
        "directories": {}
    }
    
    for svg_dir in svg_dirs:
        logger.info(f"\n🔍 Checking directory: {svg_dir}")
        unprocessed = get_unprocessed_symbols(svg_dir)
        
        if unprocessed:
            logger.info(f"📦 Found {len(unprocessed)} unprocessed symbols")
            results = process_symbols(unprocessed)
            
            total_results["processed"] += results["processed"]
            total_results["failed"] += results["failed"]
            total_results["errors"].extend(results["errors"])
            total_results["directories"][str(svg_dir)] = results
        else:
            logger.info("✅ All symbols already processed")
            total_results["directories"][str(svg_dir)] = {
                "processed": 0,
                "failed": 0,
                "status": "up_to_date"
            }
    
    # Get final counts
    final_count = get_embedding_count()
    final_symbols = get_embedded_symbols()
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("📊 SREC Startup Summary:")
    logger.info(f"   Initial: {len(initial_symbols)} symbols, {initial_count} embeddings")
    logger.info(f"   Final: {len(final_symbols)} symbols, {final_count} embeddings")
    logger.info(f"   Processed: {total_results['processed']} new symbols")
    if total_results['failed'] > 0:
        logger.warning(f"   Failed: {total_results['failed']} symbols")
    logger.info("="*50 + "\n")
    
    return {
        "status": "success",
        "initial_embeddings": initial_count,
        "final_embeddings": final_count,
        "new_symbols": total_results["processed"],
        "failed_symbols": total_results["failed"],
        "errors": total_results["errors"],
        "directories": total_results["directories"]
    }

def main():
    """Main entry point for standalone execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description="SREC startup - ensure all symbols are embedded")
    parser.add_argument("--chroma-host", default="localhost",
                       help="ChromaDB host (default: localhost)")
    parser.add_argument("--chroma-port", default="8001",
                       help="ChromaDB port (default: 8001)")
    parser.add_argument("--corpus-dir", 
                       help="Additional corpus directory to check")
    
    args = parser.parse_args()
    
    # Set environment variables
    os.environ["CHROMA_HOST"] = args.chroma_host
    os.environ["CHROMA_PORT"] = args.chroma_port
    if args.corpus_dir:
        os.environ["CORPUS_SYMBOLS_DIR"] = args.corpus_dir
    
    # Run startup check
    results = ensure_all_symbols_compiled()
    
    # Exit with error if any failures
    if results.get("failed_symbols", 0) > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()

# This can also be imported and called from your FastAPI startup
# Example in main.py:
# from srec.startup import ensure_all_symbols_compiled
# 
# @app.on_event("startup")
# async def startup_event():
#     ensure_all_symbols_compiled()