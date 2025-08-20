# Gibsey QDPI/DSPy and Kafka- Repo‑Ready Implementation Plan for Claude Code

> **Purpose**: This is the single Markdown doc you can point **Claude Code** at tonight. It merges the GPT‑5 Pro repo‑audit plan **plus** a solid Kafka design (including “pages as topics” options) into a concrete, repo‑aligned game plan you can start implementing now.

---

## TL;DR

- Keep **Cassandra** as source of truth for pages + edges; add event‑sourcing tables for audit/state.
    
- Run the QDPI cycle (X→Y→A→Z) as **DSPy actors** behind a **Kafka** bus: UI emits cues → PageGenerator consumes → writes pages/edges → emits results → UI streams them.
    
- Use **topic‑per‑domain** as default; optionally add **topic‑per‑section** or **topic‑per‑page** for power‑users. Start simple tonight.
    
- Retain the existing FastAPI routes for direct calls, but add **event gateway endpoints** that produce to Kafka.
    

---

## 1) Repo Context Snapshot (what we assume exists)

- **Backend**: `backend/main.py` (FastAPI app), API routers under `backend/app/api/` (pages, prompts, qdpi, etc.).
    
- **DB**: Cassandra via Stargate or Python driver. Existing schemas for `story_pages` family; embeddings support via `vector_service.py` and local JSONL store.
    
- **LLM**: `backend/app/llm_wrapper.py` (Ollama first, OpenAI/Anthropic optional).
    
- **Canon**: 710 pages in `gibsey-canon/corpus/...` (or `src/assets/texts.json`).
    
- **Gaps**: explicit **edges** tables, **return‑debt/TTL** enforcement, and **Kafka** plumbing.
    

> If any file paths differ, adjust the references below; structure is modular.

---

## 2) Symbol System (concise)

- **256 symbols**: `symbol = (CHAR<<4)|B` where `CHAR ∈ 0..F` = 16 characters; `B ∈ 0..15` = 16 behaviors.
    
- **Behaviors** = 4 orientations × 4 provenances: `X/Y/A/Z` × `C/P/U/S` → `XC…ZS`.
    
- **Pages are instances** (e.g., `S01-P0007`), not new symbols.
    

---

## 3) Event‑Driven Architecture (tonight’s target)

```
Frontend → (POST) /event/ui → Kafka [ui.*] → Faust/Streams (enrich) → Kafka [generate.*]
→ DSPy PageGenerator (consumer) → Cassandra (pages, edges, index) → Kafka [generate.done]
→ Gateway SSE/WebSocket → Frontend renders page
```

**Why**: decouple UI, planning, and generation; get audit logs “for free”; scale DSPy workers later.

---

## 4) Kafka Topic Strategy

### 4.1 Core topics (start with these)

- `gibsey.ui.symbol` — user selected symbol (character/behavior).
    
- `gibsey.ask` — user ask/intent.
    
- `gibsey.generate.page.request` — enriched request to generate/continue.
    
- `gibsey.generate.page.done` — page generated (text + edges + metadata).
    
- `gibsey.index.update` — signal to update read‑models/embeddings (optional if done inline).
    
- `gibsey.audit` — append‑only pipeline events (optional first night).
    
- `gibsey.dlq` — dead‑letter queue.
    

**Partition key**: `session_id` (keeps each user’s timeline totally ordered).

**Headers** to set consistently: `x-character`, `x-section`, `x-symbol`, `x-orientation`, `x-provenance`, `x-trajectory`.

### 4.2 Pages as Topics — three patterns

1. **Keyed‑by‑page (recommended MVP)**  
    Single topic (e.g., `gibsey.page.events`), produce with `key=page_id`. Scales well; no topic explosion.
    
2. **Topic‑per‑section (balanced)**  
    16 topics: `gibsey.page.S01`, …, `gibsey.page.S16`. Use `key=page_id` to keep per‑page ordering.
    
3. **Topic‑per‑page (maximalism / research)**  
    710 canonical topics + branches: `gibsey.page.S01.P0007.events`. Great for isolation but heavy on ops. If you try this, enable auto‑create in dev and add a janitor to delete idle topics.
    

> **Tonight**: ship the **Keyed‑by‑page** pattern. Add toggles so you can move to per‑section later without refactors.

### 4.3 Minimal event schemas

```jsonc
// gibsey.ui.symbol
{
  "event_id": "uuid",
  "ts": "ISO-8601",
  "session_id": "uuid",
  "symbol_code": 0,              // 0..255
  "page_id": "S01-P0007",       // locus (optional for AU/ZU)
  "user_intent": ""             // optional
}

// gibsey.generate.page.request (post-enrichment)
{
  "event_id": "uuid",
  "ts": "ISO-8601",
  "session_id": "uuid",
  "char_hex": 0,                 // left nibble
  "behavior": 0,                 // right nibble
  "symbol_code": 0,
  "section": 1,
  "page_id": "S01-P0007",
  "trajectory_hint": "T0|T1|T2|T3",
  "user_intent": "",
  "context_ids": ["S01-P0006","S01-P0005"]
}

// gibsey.generate.page.done
{
  "event_id": "uuid",
  "ts": "ISO-8601",
  "session_id": "uuid",
  "page_id": "branch-uuid-or-canon",
  "character": "an author",
  "symbol_code": 0,
  "trajectory": "T0|T1|T2|T3",
  "text": "...",
  "edges": {"next_within": "S01-P0008", "loop_back_to": null, "forks": []},
  "validation": {"style_ok": true, "continuity_score": 1.0}
}
```

---

## 5) Cassandra Schema (merge of canon + events)

### 5.1 Pages/Edges/Index (QDPI core)

```sql
CREATE TABLE IF NOT EXISTS pages (
  page_id        TEXT PRIMARY KEY,   -- e.g. "S01-P0007" or UUID for branches
  char_hex       TINYINT,
  behavior       TINYINT,
  symbol_code    TINYINT,
  section        INT,
  page_num       INT,
  title          TEXT,
  orientation    TEXT,               -- X|Y|A|Z
  provenance     TEXT,               -- C|P|U|S
  trajectory     TEXT,               -- T0|T1|T2|T3
  return_to      TEXT,
  text           TEXT,
  created_at     TIMESTAMP,
  author         TEXT,
  version        TEXT
);

CREATE TABLE IF NOT EXISTS page_edges (
  page_id   TEXT,
  edge_type TEXT,                    -- NEXT|LOOP|FORK|MIRROR
  target_id TEXT,
  created_at TIMEUUID,
  PRIMARY KEY ((page_id), edge_type, created_at)
) WITH CLUSTERING ORDER BY (edge_type ASC, created_at ASC);

CREATE TABLE IF NOT EXISTS page_embeddings (
  page_id TEXT PRIMARY KEY,
  dim     INT,
  embedding BLOB
);

CREATE TABLE IF NOT EXISTS page_index_signals (
  page_id            TEXT PRIMARY KEY,
  entities           SET<TEXT>,
  motifs             SET<TEXT>,
  unresolved_anchors SET<TEXT>,
  novelty            DOUBLE,
  coherence          DOUBLE
);

CREATE TABLE IF NOT EXISTS section_counters (
  section INT PRIMARY KEY,
  open_branches COUNTER,
  return_debt   COUNTER
);
```

### 5.2 Event‑sourcing tables

```sql
CREATE TABLE IF NOT EXISTS events_log (
  session_id   TEXT,
  ts           TIMEUUID,
  event_id     TEXT,
  type         TEXT,
  payload_json TEXT,
  headers_json TEXT,
  PRIMARY KEY ((session_id), ts, event_id)
);

CREATE TABLE IF NOT EXISTS state_snapshots (
  session_id   TEXT,
  snapshot_ts  TIMEUUID,
  ui_state_json TEXT,
  last_event_ts TIMEUUID,
  cursor        TEXT,
  PRIMARY KEY ((session_id), snapshot_ts)
);

CREATE TABLE IF NOT EXISTS pages_index (
  character_id TEXT,
  section      INT,
  page_id      TEXT,
  title        TEXT,
  excerpt      TEXT,
  embeddings_ref TEXT,
  created_ts   TIMEUUID,
  PRIMARY KEY ((character_id, section), page_id)
);

CREATE TABLE IF NOT EXISTS vault (
  session_id TEXT,
  saved_ts   TIMEUUID,
  page_id    TEXT,
  label      TEXT,
  notes      TEXT,
  PRIMARY KEY ((session_id), saved_ts, page_id)
);
```

---

## 6) DSPy Program (Kafka‑aware)

Keep the signatures; add a light wrapper that binds to Kafka consumers.

```python
# qdpi/pipeline_signatures.py
import dspy

class ReadSignature(dspy.Signature):
    symbol_code: int
    render: str
    summary: str
    edges: dict
    context: dict

class IndexSignature(dspy.Signature):
    text: str
    entities: list
    motifs: list
    anchors: list
    scores: dict

class AskSignature(dspy.Signature):
    state: dict
    user_intent: str = ""
    trajectory: str
    voice: dict
    constraints: dict
    sources: list

class ReceiveSignature(dspy.Signature):
    plan: dict
    page_text: str
    edges: dict
    validation: dict
```

```python
# qdpi/program.py
import dspy
from qdpi.symbols import decode_symbol

class QDPIProgram(dspy.Module):
    def __init__(self):
        self.read = dspy.Predict(ReadSignature)
        self.index = dspy.Predict(IndexSignature)
        self.ask = dspy.Predict(AskSignature)
        self.receive = dspy.ChainOfThought(ReceiveSignature)
        self.select_traj = dspy.Select(options=["T0","T1","T2","T3"])  # policy gate

    def forward(self, symbol_code: int, user_intent: str = "", locus_page: str | None = None):
        x = self.read(symbol_code)
        y = self.index(x.render or "")
        plan = self.ask(state={"x": x, "y": y, "locus": locus_page}, user_intent=user_intent)
        # Simple gate; tighten with policy module
        plan.trajectory = plan.trajectory or self.select_traj(context={"scores": y.scores, "intent": user_intent})
        z = self.receive(plan)
        _ = self.index(z.page_text)  # re-index new text
        return z
```

---

## 7) Kafka Plumbing (gateway + actors)

### 7.1 FastAPI Gateway (produce + stream)

```python
# backend/app/api/events.py
from fastapi import APIRouter, Request
from aiokafka import AIOKafkaProducer
import json, os, uuid, asyncio

router = APIRouter(prefix="/api/v1/event", tags=["events"])
BROKERS = os.getenv("KAFKA_BROKERS", "localhost:9092")

async def get_producer():
    p = AIOKafkaProducer(bootstrap_servers=BROKERS)
    await p.start()
    return p

@router.post("/ui/symbol")
async def ui_symbol(body: dict):
    event = {
        "event_id": str(uuid.uuid4()),
        "ts": body.get("ts"),
        "session_id": body["session_id"],
        "symbol_code": body["symbol_code"],
        "page_id": body.get("page_id"),
        "user_intent": body.get("user_intent", "")
    }
    p = await get_producer()
    try:
        key = event["session_id"].encode()
        await p.send_and_wait("gibsey.ui.symbol", json.dumps(event).encode(), key=key)
    finally:
        await p.stop()
    return {"ok": True, "event_id": event["event_id"]}
```

> Add an SSE/WebSocket endpoint that tails `gibsey.generate.page.done` via a background consumer and forwards events to connected clients.

### 7.2 Enricher (Faust or simple consumer)

```python
# services/enricher.py (Faust recommended later; simple consumer tonight)
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio, json, os, uuid

BROKERS = os.getenv("KAFKA_BROKERS", "localhost:9092")

async def run():
    c = AIOKafkaConsumer("gibsey.ui.symbol", bootstrap_servers=BROKERS, group_id="enricher")
    p = AIOKafkaProducer(bootstrap_servers=BROKERS)
    await c.start(); await p.start()
    try:
        async for msg in c:
            ui = json.loads(msg.value)
            # TODO: decode symbol, attach char/behavior/section/locus
            enriched = {
                "event_id": str(uuid.uuid4()),
                "ts": ui.get("ts"),
                "session_id": ui["session_id"],
                "symbol_code": ui["symbol_code"],
                "char_hex": (ui["symbol_code"] >> 4) & 0xF,
                "behavior": ui["symbol_code"] & 0xF,
                "section": 1,  # TODO: look up from locus page
                "page_id": ui.get("page_id"),
                "trajectory_hint": "T0",
                "user_intent": ui.get("user_intent", "")
            }
            key = enriched["session_id"].encode()
            await p.send_and_wait("gibsey.generate.page.request", json.dumps(enriched).encode(), key=key)
    finally:
        await c.stop(); await p.stop()

if __name__ == "__main__":
    asyncio.run(run())
```

### 7.3 DSPy PageGenerator (consumer → Cassandra → done)

```python
# services/page_generator.py
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio, json, os, uuid, time
from qdpi.program import QDPIProgram

BROKERS = os.getenv("KAFKA_BROKERS", "localhost:9092")
prog = QDPIProgram()

async def run():
    c = AIOKafkaConsumer("gibsey.generate.page.request", bootstrap_servers=BROKERS, group_id="qdpi.pagegen")
    p = AIOKafkaProducer(bootstrap_servers=BROKERS)
    await c.start(); await p.start()
    try:
        async for msg in c:
            req = json.loads(msg.value)
            z = prog.forward(req["symbol_code"], user_intent=req.get("user_intent", ""), locus_page=req.get("page_id"))
            # TODO: persist z.page_text + edges into Cassandra here
            done = {
                "event_id": str(uuid.uuid4()),
                "ts": time.time(),
                "session_id": req["session_id"],
                "page_id": z.edges.get("new_page_id", str(uuid.uuid4())),
                "character": req.get("char_hex"),
                "symbol_code": req["symbol_code"],
                "trajectory": z.validation.get("trajectory", req.get("trajectory_hint", "T0")),
                "text": z.page_text,
                "edges": z.edges,
                "validation": z.validation
            }
            await p.send_and_wait("gibsey.generate.page.done", json.dumps(done).encode(), key=done["session_id"].encode())
    finally:
        await c.stop(); await p.stop()

if __name__ == "__main__":
    asyncio.run(run())
```

---

## 8) QDPI Core Library (symbols, schema, policy)

```python
# qdpi/symbols.py
CHARACTER_MAP = { 0:"an-author", 1:"london-fox", 2:"glyph-marrow", 3:"phillip-bafflemint", 4:"jacklyn-variance", 5:"oren-progresso", 6:"old-natalie-weissman", 7:"princhetta", 8:"cop-e-right", 9:"new-natalie-weissman", 10:"arieol-owlist", 11:"jack-parlance", 12:"manny-valentinas", 13:"shamrock-stillman", 14:"todd-fishbone", 15:"the-author" }
BEHAVIOR_MAP = { i: b for i, b in enumerate([
    {"orientation": "X", "provenance": "C"}, {"X":"P"}, {"X":"U"}, {"X":"S"},
    {"Y":"C"}, {"Y":"P"}, {"Y":"U"}, {"Y":"S"},
    {"A":"C"}, {"A":"P"}, {"A":"U"}, {"A":"S"},
    {"Z":"C"}, {"Z":"P"}, {"Z":"U"}, {"Z":"S"}
]) }

def encode_symbol(char_hex:int, behavior:int) -> int: return ((char_hex & 0xF) << 4) | (behavior & 0xF)

def decode_symbol(symbol_code:int) -> tuple[int,int]: return (symbol_code >> 4) & 0xF, symbol_code & 0xF
```

```python
# qdpi/page_schema.py (pydantic)
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List

class PageSchema(BaseModel):
    page_id: str
    symbol_code: int
    character: str
    orientation: str
    provenance: str
    trajectory: str
    voice_preset: Optional[str]
    inputs: Dict[str, Any] = Field(default_factory=dict)
    text: str
    edges: Dict[str, Any] = Field(default_factory=dict)
    validation: Dict[str, Any] = Field(default_factory=dict)
```

```python
# qdpi/policy.py
MAX_RETURN_DEBT = 2
MAX_BRANCH_DEPTH = 3

def allow_fork(open_branches:int, return_debt:int) -> bool:
    if return_debt > MAX_RETURN_DEBT: return False
    return open_branches < 2

def require_return(branch_length:int) -> bool:
    return branch_length >= MAX_BRANCH_DEPTH
```

---

## 9) API Surface (keep + add)

### Keep (direct pipeline calls)

- `POST /api/v1/pipeline/run/symbol/{code}` → run X→Y→A→Z synchronously (handy for tests).
    
- `GET /api/v1/page/{id}` → hydrate a page with edges/signals.
    
- `POST /api/v1/branch/{id}` → branch from a locus.
    
- `GET /api/v1/pipeline/stats/section/{id}` → counters.
    

### Add (event gateway)

- `POST /api/v1/event/ui/symbol` → produce `gibsey.ui.symbol`.
    
- `GET /api/v1/event/stream?session_id=...` → SSE that forwards `gibsey.generate.page.done`.
    

---

## 10) Ingestion & Scripts

- `scripts/ingest_canon.py` — insert 710 canon pages; write `NEXT` edges to complete the ring; set `symbol_code` to `XC` of the respective character; mark `provenance='C'`, `orientation='X'`, `trajectory='T0'`.
    
- `scripts/run_symbol.py` — CLI to run a symbol once (sync path) for quick smoke.
    
- `scripts/reindex_page.py` — recompute index signals for a page/all pages.
    
- `scripts/kafka_topics.py` — create core topics; (optional) create per‑section topics.
    

---

## 11) Tests

- **Unit**: symbol encode/decode (all 256); policy gates; basic index stubs.
    
- **Integration**: pipeline continuation (T0), loopback (T1), fork (T2), TTL return (T3→T1). Mock LLM.
    
- **Event‑flow**: produce `ui.symbol` → see `generate.request` → produce `generate.done` → page persisted.
    
- **DB**: ingest count = 710; each canon page has a `NEXT` edge; ring closes.
    

---

## 12) Runbook (dev)

### Env vars

```
CASSANDRA_HOSTS=localhost:9042
CASSANDRA_KEYSPACE=gibsey
KAFKA_BROKERS=localhost:9092
OLLAMA_BASE_URL=http://localhost:11434
OPENAI_API_KEY= # optional
```

### Start services (example: Redpanda + Cassandra)

```yaml
# docker-compose.yaml (dev-friendly)
services:
  cassandra:
    image: cassandra:4.1
    ports: ["9042:9042"]
  redpanda:
    image: redpandadata/redpanda:latest
    command: ["redpanda","start","--overprovisioned","--smp","1","--memory","1G","--reserve-memory","0M","--node-id","0","--check=false"]
    ports: ["9092:9092","9644:9644"]
```

### Initialize

```
# apply CQL (core + events)
cqlsh -f scripts/cassandra_init.cql

# ingest canon
python scripts/ingest_canon.py gibsey-canon/corpus/

# create topics
python scripts/kafka_topics.py

# run services
uvicorn backend.main:app --reload
python services/enricher.py
python services/page_generator.py
```

### Smoke test

```
curl -X POST http://localhost:8000/api/v1/event/ui/symbol \
  -H 'content-type: application/json' \
  -d '{"session_id": "00000000-0000-0000-0000-000000000001", "symbol_code": 0, "page_id": "S01-P0007"}'

# Watch SSE or logs; expect a `gibsey.generate.page.done` with text + edges
```

---

## 13) “Tonight” Checklist (1–3 hrs, phone‑friendly)

-  Create **pages/edges/index** and **events** tables (copy/paste CQL).
    
-  Ingest **first 16–32 canon pages** (you can finish the rest later).
    
-  Add `events.py` router (POST `/event/ui/symbol`).
    
-  Run `enricher.py` (simple consumer) + `page_generator.py` (DSPy stub).
    
-  Produce a `ui.symbol` and see a `generate.page.done` echo back.
    
-  Persist `done` into `pages` + `page_edges` (even if text is placeholder).
    

---

## 14) Definition of Done (MVP)

- `POST /event/ui/symbol` → **emits** request; pipeline **consumes**; **writes** a new page; emits **done**; UI (or SSE client) can **see** it.
    
- Canonical ring present; `NEXT` edges correct; **return‑debt/TTL** policy stubs wired.
    
- Unit + integration tests pass locally; CI green.
    

---

## 15) Risks & Mitigations

- **Topic sprawl** (if per‑page): start with **keyed‑by‑page**; add per‑section later.
    
- **LLM variance**: short generations, retry‑on‑low‑continuity, deterministic tests with monkeypatched LLM.
    
- **Partial writes**: commit edges/signals first; page last; add repair script; append to `events_log`.
    
- **Throughput**: keep actors lightweight; add Kafka only where needed tonight; scale with more consumers per group later.
    

---

## Appendix A — Behavior table (right nibble)

|B|Behavior|Meaning|
|---|---|---|
|0|XC|Read, Canon|
|1|XP|Read, Parallel|
|2|XU|Read, User‑driven|
|3|XS|Read, System‑guided|
|4|YC|Index, Canon|
|5|YP|Index, Parallel|
|6|YU|Index, User memory|
|7|YS|Index, System memory|
|8|AC|Ask, Canon constraints|
|9|AP|Ask, Parallel constraints|
|10|AU|Ask, User intent|
|11|AS|Ask, System plan|
|12|ZC|Receive, Canon‑bounded gen|
|13|ZP|Receive, Parallel gen|
|14|ZU|Receive, User‑prompted gen|
|15|ZS|Receive, System‑prompted gen|

## Appendix B — YAML frontmatter template

```yaml
page_id: S01-P0007
symbol_code: 0x00
character: an author
orientation: X
provenance: C
trajectory: T0
voice_preset: an_author.v1
inputs:
  seeds: []
  motifs: ["preface", "identity"]
  constraints: { tense: present, max_tokens: 800 }
text: |
  ...
edges:
  next_within: S01-P0008
  loop_back_to: null
  forks: []
validation:
  style_ok: true
  continuity_score: 1.0
```

## Appendix C — Tests (pytest outline)

```python
# tests/test_symbols.py
from qdpi.symbols import encode_symbol, decode_symbol

def test_roundtrip():
    for code in range(256):
        ch, b = decode_symbol(code)
        assert encode_symbol(ch, b) == code
```

```python
# tests/test_policy.py
from qdpi.policy import allow_fork, require_return

def test_policy():
    assert not allow_fork(open_branches=0, return_debt=9)
    assert allow_fork(open_branches=1, return_debt=0)
    assert require_return(3)
```

```python
# tests/test_event_flow.py (mock LLM + DB)
# 1) produce ui.symbol → enrich → request → generate → done
# 2) assert page persisted; edges present; done seen by stream client
```