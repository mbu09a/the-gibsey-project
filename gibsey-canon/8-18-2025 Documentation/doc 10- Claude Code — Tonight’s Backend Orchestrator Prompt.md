# Claude Code — Tonight’s Backend Orchestrator Prompt (QDPI/DSPy Backend)

> You are **Claude Code** running in VS Code. You are the **backend orchestrator** for The Gibsey Project. Execute the steps below in order. Keep changes minimal-but-working. After each step, print a short status block with ✅/❌ and any diffs or logs.

---

## Mission (tonight)

Ship a minimal, end‑to‑end **QDPI→DSPy** backend that can:

- store canonical pages in **Cassandra**,
    
- run one X→Y→A→Z cycle to generate a page,
    
- persist edges & signals,
    
- expose **FastAPI** endpoints,
    
- (stub) produce/consume **Kafka** events for page generation.
    

Handoff points:

- **Codex CLI (GPT‑5)** will own SVG mapping + symbol manifest.
    
- **Gemini CLI** will own UI + real‑time stream hookup.
    

---

## Pre‑Flight

1. **Discover repo**
    
    - Confirm these paths (adjust if different):
        
        - `backend/main.py` (FastAPI entry)
            
        - `backend/app/` (routers, models, db clients)
            
        - `gibsey-canon/corpus/` or `src/assets/texts.json` (710 pages)
            
        - `qdpi-256-glyphs/` (SVG set)
            
2. **Create/verify .env** (add if missing):
    
    ```env
    CASSANDRA_HOSTS=localhost:9042
    CASSANDRA_KEYSPACE=gibsey
    STARGATE_URL=
    KAFKA_ENABLED=false
    KAFKA_BROKERS=localhost:9092
    OLLAMA_BASE_URL=http://localhost:11434
    OPENAI_API_KEY=
    EMBEDDING_DIM=384
    GLYPH_SRC_DIR=qdpi-256-glyphs
    GLYPH_MANIFEST=backend/app/assets/glyph_manifest.json
    ```
    
3. **Dependencies**
    
    - Python: `pip install fastapi uvicorn[standard] pydantic cassandra-driver dspy-ai numpy aiokafka python-dotenv` (plus any project‑specific requirements already present).
        

Output a quick inventory (tree of `backend/` and `gibsey-canon/`).

---

## Step 1 — Cassandra Schema (minimal QDPI tables)

Create or update schema. If you already have a script, extend it; otherwise add `scripts/cassandra_qdpi_init.cql` with:

```sql
CREATE KEYSPACE IF NOT EXISTS gibsey WITH replication = {'class': 'SimpleStrategy','replication_factor': 1};
USE gibsey;
CREATE TABLE IF NOT EXISTS pages (
  page_id TEXT PRIMARY KEY,
  char_hex TINYINT,
  behavior TINYINT,
  symbol_code TINYINT,
  section INT,
  page_num INT,
  provenance TEXT,
  orientation TEXT,
  trajectory TEXT,
  return_to TEXT,
  text TEXT,
  created_at TIMESTAMP
);
CREATE TABLE IF NOT EXISTS page_edges (
  page_id TEXT,
  edge_type TEXT,
  target_id TEXT,
  created_at TIMEUUID,
  PRIMARY KEY ((page_id), edge_type, created_at)
) WITH CLUSTERING ORDER BY (edge_type ASC, created_at ASC);
CREATE TABLE IF NOT EXISTS page_embeddings (
  page_id TEXT PRIMARY KEY,
  dim INT,
  vec BLOB
);
CREATE TABLE IF NOT EXISTS page_index_signals (
  page_id TEXT PRIMARY KEY,
  entities SET<TEXT>,
  motifs SET<TEXT>,
  unresolved_anchors SET<TEXT>,
  novelty DOUBLE,
  coherence DOUBLE
);
CREATE TABLE IF NOT EXISTS section_counters (
  section INT PRIMARY KEY,
  open_branches COUNTER,
  return_debt COUNTER
);
CREATE TABLE IF NOT EXISTS plans (
  plan_id TIMEUUID PRIMARY KEY,
  page_id TEXT,
  symbol_code TINYINT,
  trajectory TEXT,
  plan_json TEXT,
  created_at TIMESTAMP
);
```

Add a tiny runner `backend/scripts/init_qdpi_schema.py` that loads `.env`, connects (cassandra-driver), and executes that CQL. Run it and print `DESCRIBE TABLES` output.

**Accept:** tables exist; no exceptions.

---

## Step 2 — QDPI Core (symbols, schema, policy)

Create module `backend/qdpi/` with:

**`symbols.py`**

```python
CHARACTER_MAP = {
  0:"an author",1:"london-fox",2:"glyph-marrow",3:"phillip-bafflemint",
  4:"jacklyn-variance",5:"oren-progresso",6:"old-natalie-weissman",7:"princhetta",
  8:"cop-e-right",9:"new-natalie-weissman",10:"arieol-owlist",11:"jack-parlance",
  12:"manny-valentinas",13:"shamrock-stillman",14:"todd-fishbone",15:"the-author"
}
BEHAVIORS = {
  0:("X","C"),1:("X","P"),2:("X","U"),3:("X","S"),
  4:("Y","C"),5:("Y","P"),6:("Y","U"),7:("Y","S"),
  8:("A","C"),9:("A","P"),10:("A","U"),11:("A","S"),
  12:("Z","C"),13:("Z","P"),14:("Z","U"),15:("Z","S")
}

def encode_symbol(char_hex:int, behavior:int)->int:
    return ((char_hex & 0xF) << 4) | (behavior & 0xF)

def decode_symbol(code:int)->tuple[int,int]:
    return ((code>>4)&0xF, code & 0xF)
```

**`page_schema.py`** (Pydantic)

```python
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class PageSchema(BaseModel):
    page_id: str
    symbol_code: int
    character: str
    orientation: str
    provenance: str
    trajectory: str
    voice_preset: Optional[str] = None
    inputs: Dict[str, Any] = Field(default_factory=dict)
    text: str
    edges: Dict[str, Any] = Field(default_factory=dict)
    validation: Dict[str, Any] = Field(default_factory=dict)
```

**`policy.py`**

```python
MAX_RETURN_DEBT=2
MAX_BRANCH_DEPTH=3

def allow_fork(open_branches:int, return_debt:int)->bool:
    if return_debt>MAX_RETURN_DEBT: return False
    return open_branches < 3

def require_return(branch_length:int)->bool:
    return branch_length>=MAX_BRANCH_DEPTH
```

Add unit tests later (Step 5). Commit.

**Accept:** importable `backend.qdpi` with encode/decode working for 0..255.

---

## Step 3 — Canon Ingestion (710 pages + NEXT ring)

Create `scripts/ingest_canon.py`:

- Read from `gibsey-canon/corpus/...` **or** `src/assets/texts.json`.
    
- Assign `section` (1..16) and `page_num` per user’s TOC.
    
- For canon pages: `behavior=0 (XC)`, `orientation='X'`, `provenance='C'`, `trajectory='T0'`.
    
- Insert into `pages` and create `NEXT` edges in `page_edges`.
    
- Link Section 16 last → Section 1 first to close the ring.
    
- Print total rows, first/last IDs.
    

**Accept:** 710 pages present; each has a NEXT edge; one ring.

---

## Step 4 — DSPy Pipeline (X→Y→A→Z)

Create `backend/qdpi/pipeline_signatures.py` and `backend/qdpi/program.py` with minimal stubs:

```python
# pipeline_signatures.py
import dspy
class ReadSignature(dspy.Signature):
    symbol_code:int; render:str; summary:str; edges:dict; context:dict
class IndexSignature(dspy.Signature):
    text:str; entities:list; motifs:list; anchors:list; scores:dict
class AskSignature(dspy.Signature):
    state:dict; user_intent:str=""; trajectory:str; voice:dict; constraints:dict; sources:list
class ReceiveSignature(dspy.Signature):
    plan:dict; page_text:str; edges:dict; validation:dict
```

```python
# program.py
import dspy
from .symbols import decode_symbol, BEHAVIORS, CHARACTER_MAP

class QDPIProgram(dspy.Module):
    def __init__(self):
        self.read=dspy.Predict(ReadSignature)
        self.index=dspy.Predict(IndexSignature)
        self.ask=dspy.Predict(AskSignature)
        self.receive=dspy.Predict(ReceiveSignature)
        self.select=dspy.Select(options=["T0","T1","T2","T3"])
    def forward(self, symbol_code:int, user_intent:str=""):
        x=self.read(symbol_code); y=self.index(x.render)
        plan=self.ask(state={"x":x, "y":y}, user_intent=user_intent)
        plan.trajectory=self.select(context={"scores":y.scores,"intent":user_intent}) or "T0"
        z=self.receive(plan); _=self.index(z.page_text); return z
```

For now, implement each stage with simple functions in the API layer (Step 5) rather than complex DSPy logic.

**Accept:** `from backend.qdpi.program import QDPIProgram` imports without error.

---

## Step 5 — FastAPI Endpoints (minimal surface)

Create `backend/app/api/pipeline.py`:

```python
from fastapi import APIRouter, HTTPException
from backend.qdpi.program import QDPIProgram
from backend.qdpi.symbols import decode_symbol, BEHAVIORS, CHARACTER_MAP

router = APIRouter(prefix="/api/v1/pipeline", tags=["pipeline"])
prog = QDPIProgram()

@router.post("/run/symbol/{code}")
async def run_symbol(code:str, body:dict|None=None):
    try: code_val=int(code,0)
    except: raise HTTPException(400, detail="Invalid symbol code")
    user_intent = (body or {}).get("user_intent","")
    out = prog(code_val, user_intent=user_intent)
    return {"page_text": out.page_text, "edges": out.edges, "validation": out.validation}
```

- Wire router into `backend/main.py` if not already.
    
- Provide **temporary stub impls** for `read/index/ask/receive` via monkeypatch or simple functions (e.g., read returns the current canon page text given code; receive echoes a small generated string and sets a `next_within`).
    

**Accept:** `uvicorn backend.main:app --reload` exposes `/api/docs` with new routes and returns JSON for a test call.

---

## Step 6 — Kafka (toggleable, minimal)

- Add a feature flag `KAFKA_ENABLED`.
    
- Create topics (if broker running):
    
    - `gibsey.generate.page.request`
        
    - `gibsey.generate.page.done`
        
- Add `backend/workers/kafka_io.py` with `aiokafka` producers/consumers:
    
    - Producer helper: `emit_page_request(session_id, symbol_code, user_intent)`
        
    - Consumer task: on `...page.request` → call `QDPIProgram` → produce `...page.done` and (later) persist.
        
- For now, **don’t** block API on Kafka; just log stubs when disabled.
    

**Accept:** When enabled, producing a request logs a consumed → produced cycle.

---

## Step 7 — Tests & Fixtures

Add `tests/test_qdpi_basic.py`:

```python
def test_encode_decode_roundtrip():
    from backend.qdpi.symbols import encode_symbol, decode_symbol
    for code in range(256):
        c,b=decode_symbol(code)
        assert encode_symbol(c,b)==code
```

Add a smoke test that calls the `/api/v1/pipeline/run/symbol/0x00` endpoint via TestClient and asserts keys present.

**Accept:** `pytest -q` green on these basics.

---

## Step 8 — Handoffs to Other Agents

- **Codex CLI (GPT‑5)**: build `GLYPH_MANIFEST` by scanning `qdpi-256-glyphs/` and normalizing names → `{ hex:"0xAB", character:"...", behavior:"ZU", path:"...svg" }`. Save to `backend/app/assets/glyph_manifest.json`. Add a loader util here in backend to read it later.
    
- **Gemini CLI**: consume `/api/v1/pipeline/run/symbol/{code}`; render the 256‑grid UI, tooltips, reader panel, mini graph, and an SSE/WebSocket stub for live pulses; later, wire to Kafka `...page.done`.
    

Include a short `AGENTS.md` note or update existing doc to record these splits.

---

## Step 9 — Runbook (commands)

```bash
# 1) Schema
python backend/scripts/init_qdpi_schema.py

# 2) Ingest
python scripts/ingest_canon.py --from corpus  # or --from-json src/assets/texts.json

# 3) API
uvicorn backend.main:app --reload
curl -X POST "http://localhost:8000/api/v1/pipeline/run/symbol/0x00" -H "Content-Type: application/json" -d '{"user_intent":"continue"}'

# 4) Kafka (optional)
# create topics; start broker; set KAFKA_ENABLED=true in .env
```

---

## Definition of Done (tonight)

- `pages` + `page_edges` created and populated with canon (ring closed).
    
- `/api/v1/pipeline/run/symbol/{code}` returns a JSON payload with `page_text` and at least one edge in `edges`.
    
- Encode/decode unit test passes.
    
- Kafka stubs compile and no‑op when disabled; basic produce/consume works when enabled.
    

---

## Report Back (after each step)

Post a block like:

```
[STEP N STATUS]
✅ Done: <summary>
Files changed: <list>
Notes: <warnings/todos>
```

If something is ambiguous, proceed with sensible defaults, leave TODO markers, and keep moving.