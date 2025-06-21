Below is a concise **progress audit** of steps 1-2 _based on the public contents of_ `github.com/mbu09a/the-gibsey-project`, followed by a **precise implementation brief** Claude Code can follow to ship **Step 3 – Retrieval API (Read & Index)**.

---

## 1 · Canonical Data Cut — status

|Item|Evidence|Result|
|---|---|---|
|**710 pages split** into one file each|Project now contains a `gibsey-canon/` folder (root listing shows it) ([github.com](https://github.com/mbu09a/the-gibsey-project "GitHub - mbu09a/the-gibsey-project: A novel AI OS"))|**Partial** – presence confirmed, but the README still advertises _“one JSON per story in /src/stories/”_ ([github.com](https://github.com/mbu09a/the-gibsey-project "GitHub - mbu09a/the-gibsey-project: A novel AI OS")), so the page-level split may not be complete.|
|**Flattened MCP / symbols**|`gibsey-canon` exists; a `tokenizer/` and `public/corpus-symbols/` are still present outside it. Need to verify SVGs & colour map copied inside canon.|**Likely incomplete**.|
|**Repo tag `corpus-v1.0`**|The repo shows **one tag** in the UI ([github.com](https://github.com/mbu09a/the-gibsey-project "GitHub - mbu09a/the-gibsey-project: A novel AI OS")), but its name isn’t visible from the limited view.|**Probably done**, but confirm the tag name.|
|**CI for lint/diff**|`.github/workflows/` folder now exists ([github.com](https://github.com/mbu09a/the-gibsey-project "GitHub - mbu09a/the-gibsey-project: A novel AI OS")). Open the YAML manually to confirm UTF-8 + diff checks; most likely added.|**Looks present** but **review the checks**.|

**Action for Claude Code**

- Run a quick script to count Markdown files in `gibsey-canon/corpus/pages/`.
    
    - If < 710, finish splitting `src/stories/*.json` into page-files and regenerate `pages.json` / `index.json`.
        
- Copy any stray SVGs (`public/corpus-symbols/*.svg`) and the colour map (`src/assets/colors.ts`) into `gibsey-canon/corpus/characters/…/symbol.svg` and `info.json`.
    
- Verify the tag is literally **`corpus-v1.0`**; rename or retag if not.
    
- Confirm the CI job actually (a) attempts a UTF-8 decode of every page file and (b) diffs `pages.json` ↔ directory listing.
    

---

## 2 · House Tokenizer — status

|Item|Evidence|Result|
|---|---|---|
|**`tokenizer/` directory**|Exists in root listing ([github.com](https://github.com/mbu09a/the-gibsey-project "GitHub - mbu09a/the-gibsey-project: A novel AI OS"))|**Present**.|
|**Model files** (`gibsey_bpe.model`, `.vocab` or `.json`)|Can’t be viewed in raw on the public mirror (GitHub now blocks large binaries). Nevertheless the folder’s existence suggests Claude Code generated them.|**Assume done – but verify** size (~2-3 MB) & `user_defined_symbols` list.|
|**Backend loads tokenizer**|Need to inspect `backend/app/…` (rag_service.py) but raw fetch blocked.|**Unknown**.|
|**Bun/TS loads tokenizer**|Need to open `src/utils/` or `scripts/`; unseen from limited crawl.|**Unknown**.|
|**CLI `bun run token-viz`**|`scripts/` folder exists ([github.com](https://github.com/mbu09a/the-gibsey-project "GitHub - mbu09a/the-gibsey-project: A novel AI OS")). Check `package.json` for a `token-viz` script.|**Probably added**, but confirm.|

**Action for Claude Code**

1. Open `tokenizer/gibsey_bpe.vocab` and confirm the first 20 lines include  
    the four QDPI tokens and **all** current glyph IDs (`london-fox`, `jacklyn-variance`, etc.).
    
2. Add unit tests in `tests/test_tokenizer.py` and `tests/test_token_viz.ts` that:
    
    - encode `"Princhetta <X_READ> glyph london-fox"` and assert the special tokens stay whole.
        
3. In the Bun layer (`src/utils/`), export `countTokens` and call it from one endpoint so we know runtime loading works.
    

---

## 3 · Retrieval API (Read & Index) — implementation brief for Claude Code

> **Goal:** expose two FastAPI endpoints backed by Cassandra-vector search.  
> **Deadline suggestion:** 3-4 working days including test coverage.

### 3.1 Prepare the Vector Store

|Step|Details|
|---|---|
|**Schema**|Keyspace `gibsey`, table `pages`: `page_id text PRIMARY KEY`, `symbol_id text`, `title text`, `page_index int`, `tokens int`, `embedding vector<float, 768>`|
|**Embedding model**|Use `text-embedding-3-small` (OpenAI) or, if offline, `instructor-xl` from Hugging Face. Parameterise via `EMBED_MODEL` env var.|
|**Seeder script** (`scripts/seed_embeddings.py`)|* For every Markdown file under `gibsey-canon/corpus/pages/`: * read text * compute `tokens = len(sp.encode(text))` with **gibsey_bpe** * call embedding model * `INSERT INTO pages (…) VALUES (…)` via Cassandra driver. * Skip if `page_id` already present to allow incremental runs.|
|**Docker-Compose**|If not already in repo, add `docker-compose.cassandra.yml` with a single-node Cassandra + `cassandra:5.0` image and open port 9042.|

### 3.2 FastAPI Service (`backend/app/api.py`)

|Route|Input|Behaviour|
|---|---|---|
|`POST /read/{page_id}`|path param `page_id`|Fetch row by PK, return JSON: `title, text, symbol_id, tokens`.|
|`POST /index`|JSON body `{ "q": "string", "top_k": 5 }`|* Embed `q` with same model. * Do cosine ≥ `1 - 1e-6` search via Cassandra 5 vector index (`embedding ANN`). * Return array of `{page_id, title, preview, score}` where `preview` = first 300 custom tokens decoded.|

### 3.3 Wiring the Custom Tokenizer

- Import the SentencePiece model once at app start (singleton).
    
- Use it for:
    
    1. truncating previews (`preview = sp.decode(ids[:300])`)
        
    2. counting tokens for the TNA ledger (if ledger already exists)
        
    3. validating user query length (e.g., hard-cap 200 custom tokens).
        

### 3.4 Unit & Integration Tests

|Test file|Purpose|
|---|---|
|`tests/test_read_endpoint.py`|Insert a mock page row, call `/read/<id>`, assert status 200 and fields present.|
|`tests/test_semantic_index.py`|Seed two tiny pages, query `/index?q=…`, expect highest-scoring `page_id` to be correct.|

### 3.5 CI/CD

- Extend existing GitHub Actions workflow to run `scripts/seed_embeddings.py` **only** when corpus changes (path filter `gibsey-canon/corpus/pages/**`).
    
- Run `pytest` to execute the new test suite.
    
- Cache the `.sentencepiece` model and Hugging Face embeddings between jobs for speed.
    

### 3.6 Front-end Hook (nice-to-have)

- In the Bun API layer, add proxy functions `readPage(pageId)` and `searchPages(query)` that hit the new FastAPI routes.
    
- Display search results in a modal list; clicking an item triggers the existing page viewer.
    

---

### “Definition of Done” for Step 3

1. **Seed script** embeds all pages and inserts ≥ 710 rows in Cassandra.
    
2. `POST /read/{page_id}` returns a full page in < 50 ms on local dev.
    
3. `POST /index` returns top-k semantic matches with cosine scores.
    
4. All new tests pass in CI, and the workflow caches model files.
    
5. README section **“Retrieval API”** explains env vars (`OPENAI_KEY`, `CASSANDRA_HOST`, etc.) and seed procedure.
    

Once Claude Code completes and merges this branch, step 3 is green and you can move on to multi-voice agents or Vault write-back.

Good luck—Gibsey is getting close to becoming a fully searchable, chat-ready world!