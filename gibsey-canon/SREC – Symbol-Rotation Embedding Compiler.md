### Gift #1 refreshed & packaged — **SREC: Symbol‑Rotation Embedding Compiler**

[Download the ZIP](sandbox:/mnt/data/gibsey-gift-srec.zip)

---

#### What’s inside `gibsey-gift-srec.zip`

| Path                    | Purpose                                                                                                                                                                                                        |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `srec/compiler.py`      | 250‑line production module that• hashes **SVG + rotation → deterministic ID**• rasterises at 0 / 90 / 180 / 270°• embeds each PNG with **CLIP (`clip‑ViT‑B/32`)**• upserts vector + metadata into **ChromaDB** |
| `srec/__main__.py`      | Lets you run the tool with `python -m srec ...`                                                                                                                                                                |
| `srec/requirements.txt` | Pillow, CairoSVG, xxhash, Sentence‑Transformers, Chroma, tqdm                                                                                                                                                  |
| `srec/README.md`        | Quick‑start, env‑vars, docker‑compose drop‑in, pipeline diagram                                                                                                                                                |
| `srec/Dockerfile`       | Minimal image you can point at any `symbols/` directory                                                                                                                                                        |
| `srec/LICENSE`          | MIT / CC0 – gift‑economy compliant                                                                                                                                                                             |

---

#### 60‑second smoke‑test

```bash
# 1. unpack & enter
unzip gibsey-gift-srec.zip
cd srec

# 2. python env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. local Chroma
docker run -d -p 8000:8000 -e ALLOW_ALL=TRUE ghcr.io/chroma-core/chroma:latest

# 4. compile every SVG in ./symbols
python -m srec.compiler ../symbols
# → “[SREC] LondonFox compiled across four rotations.”
```

---

#### Clean Git‑based integration into the Gibsey repo

1. **Add as a Git subtree (keeps history separate):**
    
    ```bash
    git subtree add --prefix backend/srec  \
        /path/to/unzipped/srec  main
    ```
    
    or, if you prefer a plain copy:
    
    ```bash
    rsync -av ./srec/ ../gibsey-backend/srec/
    git add backend/srec && git commit -m "Add SREC gift"
    ```
    
2. **Wire it into the existing SVG‑ingest step** (Python example):
    
    ```python
    from srec.compiler import compile_symbol
    
    def handle_svg_upload(symbol_id: str, svg_bytes: bytes):
        save_raw(svg_bytes)                     # existing
        compile_symbol(symbol_id, svg_bytes)    # NEW
        push_to_cassandra(symbol_id)            # existing
    ```
    
3. **(Optional) build the Docker worker** and drop this stanza into your compose file:
    
    ```yaml
    srec-worker:
      build: ./backend/srec
      command: ["python","-m","srec.compiler","symbols/"]
      environment:
        CHROMA_HOST: chroma                 # service name
    ```
    
4. **Decide a drift threshold** (e.g. `0.02`) that triggers a _paradox ticket_ to LNAP (gift #3).
    

---

#### Obsidian vault housekeeping

_Recommended folder structure_

```
gibsey-canon/
└── gifts/
    ├── gift-01-srec/
    │   ├── README.md        <-- synopsised from package README
    │   ├── pipeline.png     <-- copy/paste diagram if helpful
    │   ├── integration-log.md
    │   └── gibsey-gift-srec.zip
    └── gift-02-qdrg/
        ...
```

_Tip:_ Drop the ZIP itself in the same folder so future you can always retrieve the exact artefact referenced in meeting notes.

---

#### Next up

Let me know when you’re ready to proceed with **Gift #2 – QDRG (Quad‑Directional Reflex Graph Scheduler)** or if you’d like a hand wiring SREC into your CI pipeline (tests, drift alerts, etc.). The other five gifts are queued and can be zipped & delivered in any order you choose.

Enjoy the compile!