
"""Symbol‑Rotation Embedding Compiler (SREC)."""
import os, io, sys, hashlib, logging, xxhash, json
from pathlib import Path
from PIL import Image
import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

MODEL_NAME = os.getenv("SREC_EMBED_MODEL", "sentence-transformers/clip-ViT-B-32")
COL = os.getenv("SREC_COLLECTION", "corpus_symbols")
CHOST = os.getenv("CHROMA_HOST", "localhost")
CPORT = int(os.getenv("CHROMA_PORT", "8000"))

log = logging.getLogger("srec")
logging.basicConfig(level=logging.INFO, format="%(message)s")

_model = None
_client = None
_coll = None

def _init():
    global _model, _client, _coll
    if _model is None:
        log.info(f"[SREC] loading model {MODEL_NAME}")
        _model = SentenceTransformer(MODEL_NAME)
    if _client is None:
        _client = chromadb.HttpClient(host=CHOST, port=CPORT)
        _coll = _client.get_or_create_collection(COL)

def svg_to_png_bytes(svg_bytes: bytes, rot: int) -> bytes:
    """Convert SVG to PNG with rotation. Requires Wand for production."""
    is_production = os.getenv("SREC_ENV", "dev") == "production"
    
    try:
        from wand.image import Image as WandImage
        from wand.color import Color
        
        # Production-ready SVG rendering with Wand
        with WandImage(blob=svg_bytes, format='svg', background=Color('white')) as img:
            # Ensure consistent size for embeddings
            img.resize(256, 256)
            img.format = 'png'
            img.rotate(rot, background=Color('white'))
            png_bytes = img.make_blob()
        return png_bytes
        
    except ImportError as e:
        if is_production:
            raise RuntimeError(
                "Wand is required for production SVG processing. "
                "Install with: pip install Wand\n"
                "Also ensure ImageMagick is installed:\n"
                "  - macOS: brew install imagemagick\n"
                "  - Ubuntu: apt-get install imagemagick\n"
                "  - Docker: See Dockerfile for setup"
            ) from e
        else:
            # Development fallback
            log.warning("⚠️  Wand not available - using placeholder embeddings (dev mode)")
            log.warning("   For real embeddings: pip install Wand")
            
            # Create placeholder with symbol indicator
            img = Image.new('RGB', (256, 256), color='lightgray')
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img)
            draw.text((10, 120), f"Placeholder\nRotation: {rot}°", fill='black')
            
            img = img.rotate(rot, expand=True, fillcolor='white')
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return buf.getvalue()

def compile_symbol(symbol_id: str, svg_bytes: bytes):
    _init()
    embeds, ids, metas = [], [], []
    for rot in (0, 90, 180, 270):
        h = xxhash.xxh128(svg_bytes + str(rot).encode()).hexdigest()
        png_bytes = svg_to_png_bytes(svg_bytes, rot)
        vec = _model.encode(Image.open(io.BytesIO(png_bytes)))
        embeds.append(vec.tolist())
        ids.append(h)
        metas.append({"symbol": symbol_id, "rot": rot})
    _coll.upsert(ids=ids, embeddings=embeds, metadatas=metas)
    log.info(f"[SREC] {symbol_id} compiled")

def _walk_svg(path: Path):
    for p in path.glob("**/*.svg"):
        yield p

def get_embedding_count():
    """Get total number of embeddings in the collection."""
    _init()
    return _coll.count()

def get_embedded_symbols():
    """Get list of unique symbols that have been embedded."""
    _init()
    results = _coll.get()
    if not results or 'metadatas' not in results:
        return []
    symbols = set()
    for meta in results['metadatas']:
        if meta and 'symbol' in meta:
            symbols.add(meta['symbol'])
    return sorted(list(symbols))

def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print("usage: python -m srec.compiler <svg_dir>")
        sys.exit(1)
    svg_dir = Path(argv[0])
    
    files = list(_walk_svg(svg_dir))
    log.info(f"🔍 Found {len(files)} SVG files to process")
    
    processed = 0
    for f in tqdm(files, desc="Processing SVGs"):
        try:
            compile_symbol(f.stem, f.read_bytes())
            processed += 1
        except Exception as e:
            log.error(f"❌ Failed to process {f.name}: {e}")
    
    # Summary
    total_embeddings = get_embedding_count()
    log.info(f"\n✅ Successfully processed {processed}/{len(files)} SVGs")
    log.info(f"📊 Total embeddings in ChromaDB: {total_embeddings}")
    log.info(f"💾 Collection: {COL} on {CHOST}:{CPORT}")

if __name__ == "__main__":
    main()
