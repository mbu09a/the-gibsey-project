"""Symbol upload and embedding API endpoints."""
import os
import io
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Import SREC compiler functions
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from srec.compiler import compile_symbol, get_embedding_count, get_embedded_symbols

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/symbols", tags=["symbols"])

class SymbolUploadResponse(BaseModel):
    """Response for symbol upload."""
    symbol_id: str
    message: str
    embeddings_created: int
    total_embeddings: int

class SymbolStatusResponse(BaseModel):
    """Response for symbol status check."""
    total_symbols: int
    total_embeddings: int
    embedded_symbols: List[str]
    collection: str
    chroma_host: str
    chroma_port: int

class BatchUploadResponse(BaseModel):
    """Response for batch symbol upload."""
    processed: int
    failed: int
    total_embeddings: int
    errors: List[Dict[str, str]]

# Configuration from environment
ALLOWED_EXTENSIONS = {'.svg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
CORPUS_SYMBOLS_DIR = Path(os.getenv("CORPUS_SYMBOLS_DIR", "public/corpus-symbols"))

def validate_svg_file(file: UploadFile) -> None:
    """Validate uploaded SVG file."""
    # Check extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Only {ALLOWED_EXTENSIONS} files are allowed."
        )
    
    # Check content type
    if not file.content_type or 'svg' not in file.content_type.lower():
        raise HTTPException(
            status_code=400,
            detail="Invalid content type. File must be an SVG."
        )

@router.post("/upload", response_model=SymbolUploadResponse)
async def upload_symbol(
    file: UploadFile = File(...),
    save_to_corpus: bool = True
) -> SymbolUploadResponse:
    """
    Upload a single SVG file and create embeddings.
    
    Args:
        file: SVG file to upload
        save_to_corpus: Whether to save the file to corpus-symbols directory
    """
    validate_svg_file(file)
    
    # Read file content
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE} bytes."
        )
    
    # Extract symbol ID from filename
    symbol_id = Path(file.filename).stem
    
    try:
        # Save to corpus directory if requested
        if save_to_corpus:
            CORPUS_SYMBOLS_DIR.mkdir(parents=True, exist_ok=True)
            svg_path = CORPUS_SYMBOLS_DIR / file.filename
            with open(svg_path, 'wb') as f:
                f.write(content)
            logger.info(f"Saved SVG to {svg_path}")
        
        # Compile with SREC
        compile_symbol(symbol_id, content)
        
        # Get counts
        total_embeddings = get_embedding_count()
        
        return SymbolUploadResponse(
            symbol_id=symbol_id,
            message=f"Successfully compiled {symbol_id} with 4 rotation embeddings",
            embeddings_created=4,
            total_embeddings=total_embeddings
        )
        
    except Exception as e:
        logger.error(f"Failed to process symbol {symbol_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process symbol: {str(e)}"
        )

@router.post("/upload-batch", response_model=BatchUploadResponse)
async def upload_symbols_batch(
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
) -> BatchUploadResponse:
    """
    Upload multiple SVG files and create embeddings.
    
    Note: Large batches are processed in the background.
    """
    if len(files) > 100:
        raise HTTPException(
            status_code=400,
            detail="Too many files. Maximum 100 files per batch."
        )
    
    processed = 0
    failed = 0
    errors = []
    
    for file in files:
        try:
            validate_svg_file(file)
            content = await file.read()
            
            if len(content) > MAX_FILE_SIZE:
                errors.append({
                    "file": file.filename,
                    "error": "File too large"
                })
                failed += 1
                continue
            
            symbol_id = Path(file.filename).stem
            
            # For large batches, process in background
            if len(files) > 10:
                background_tasks.add_task(compile_symbol, symbol_id, content)
            else:
                compile_symbol(symbol_id, content)
            
            processed += 1
            
        except Exception as e:
            errors.append({
                "file": file.filename,
                "error": str(e)
            })
            failed += 1
    
    total_embeddings = get_embedding_count()
    
    return BatchUploadResponse(
        processed=processed,
        failed=failed,
        total_embeddings=total_embeddings,
        errors=errors
    )

@router.get("/status", response_model=SymbolStatusResponse)
async def get_symbol_status() -> SymbolStatusResponse:
    """Get current status of symbol embeddings."""
    try:
        embedded_symbols = get_embedded_symbols()
        total_embeddings = get_embedding_count()
        
        return SymbolStatusResponse(
            total_symbols=len(embedded_symbols),
            total_embeddings=total_embeddings,
            embedded_symbols=embedded_symbols,
            collection=os.getenv("SREC_COLLECTION", "corpus_symbols"),
            chroma_host=os.getenv("CHROMA_HOST", "localhost"),
            chroma_port=int(os.getenv("CHROMA_PORT", "8001"))
        )
    except Exception as e:
        logger.error(f"Failed to get symbol status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get status: {str(e)}"
        )

@router.delete("/symbol/{symbol_id}")
async def delete_symbol_embeddings(symbol_id: str) -> Dict[str, Any]:
    """Delete all embeddings for a specific symbol."""
    try:
        # This would need to be implemented in compiler.py
        # For now, return not implemented
        raise HTTPException(
            status_code=501,
            detail="Delete functionality not yet implemented"
        )
    except Exception as e:
        logger.error(f"Failed to delete symbol {symbol_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete symbol: {str(e)}"
        )

@router.post("/reprocess-all")
async def reprocess_all_symbols(
    background_tasks: BackgroundTasks,
    corpus_dir: Optional[str] = None
) -> Dict[str, Any]:
    """Reprocess all symbols in the corpus directory."""
    corpus_path = Path(corpus_dir or CORPUS_SYMBOLS_DIR)
    
    if not corpus_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Corpus directory not found: {corpus_path}"
        )
    
    svg_files = list(corpus_path.glob("**/*.svg"))
    
    if not svg_files:
        raise HTTPException(
            status_code=404,
            detail=f"No SVG files found in {corpus_path}"
        )
    
    # Process in background
    def process_all():
        for svg_file in svg_files:
            try:
                with open(svg_file, 'rb') as f:
                    compile_symbol(svg_file.stem, f.read())
            except Exception as e:
                logger.error(f"Failed to reprocess {svg_file}: {e}")
    
    background_tasks.add_task(process_all)
    
    return {
        "message": f"Started reprocessing {len(svg_files)} symbols in background",
        "corpus_dir": str(corpus_path),
        "svg_count": len(svg_files)
    }