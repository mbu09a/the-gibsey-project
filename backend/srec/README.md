# SREC – Symbol‑Rotation Embedding Compiler

Deterministically embeds every **Corpus SVG** at four canonical rotations,
producing stable vector anchors for downstream search.

```
svg ─► rasterise (0/90/180/270) ─► CLIP embed ─► ChromaDB
                     ▲
           hash(svg+rot) → id
```

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# run against local Chroma
docker run -d -p 8000:8000 -e ALLOW_ALL=TRUE ghcr.io/chroma-core/chroma:latest
python -m srec.compiler ../symbols/
```

## Environment variables

| Var                | Default          | Purpose |
|--------------------|------------------|---------|
| `CHROMA_HOST`      | `localhost`      | Chroma endpoint |
| `CHROMA_PORT`      | `8000`           | — |
| `SREC_COLLECTION`  | `corpus_symbols` | Collection name |
| `SREC_EMBED_MODEL` | `clip-ViT-B/32`  | Any Sentence‑Transformers model |

## Docker‑compose snippet

See `README.md` in parent doc.

MIT/CC0 – gift‑economy compliant.
