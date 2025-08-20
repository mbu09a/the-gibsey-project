# Mini-Architecture- “Gibsey as an Event-Driven Play”

`┌──────────────────────────────────────────────────────────────────────┐ │                              FRONTEND (React)                        │ │  - Symbol Grid (16 chars × 16 sections)     - Orientation Dial (↻)  │ │  - Ask/Receive text panels                  - Vault timeline         │ │  Emits: SYMBOL.SELECTED, ORIENTATION.ROTATE, ASK.SUBMIT, VAULT.SAVE  │ └──────────────┬───────────────────────────────────────────────────────┘                │  (Kafka produce)                ▼ ┌──────────────────────────────────────────────────────────────────────┐ │                          EVENT BUS (Kafka)                           │ │  Topics (examples):                                                  │ │   gibsey.ui.symbol        gibsey.ui.orientation   gibsey.ask         │ │   gibsey.generate.page    gibsey.index.update     gibsey.vault       │ │   gibsey.snapshot         gibsey.audit            gibsey.dlq         │ │  Partitions keyed by: session_id (preserve user timeline order)      │ └──────────────┬───────────────────────────┬───────────────────────────┘                │                           │        (Faust/Kafka Streams)        (Consumers: DSPy & Services)                │                           │                ▼                           ▼ ┌──────────────────────────────────┐   ┌────────────────────────────────┐ │  STREAM PROCESSORS (Faust/KS)    │   │   DSPy ACTORS (skills/agents)  │ │  - debounce/aggregate UI bursts  │   │  - PageGenerator (RAG)         │ │  - route by character/section    │   │  - SymbolInterpreter            │ │  - enrich w/ session context     │   │  - Analyst/Commentary voices    │ └──────────────┬───────────────────┘   └──────────────┬─────────────────┘                │                                       │                │ (produce enriched events)             │ (produce results)                ▼                                       ▼       ┌─────────────────────┐                 ┌─────────────────────────┐       │   STARGATE → CASS   │                 │  STORAGE WRITERS        │       │  (Event Sourcing)   │◄───write───────►│  - Event Store (append) │       │  tables:            │                 │  - Snapshots (state)    │       │   events_log        │                 │  - Vault (curated)      │       │   state_snapshots   │                 └─────────────────────────┘       │   pages_index       │       └─────────┬───────────┘                 │  (read models / RAG)                 ▼       ┌─────────────────────┐       │   RAG INDEX (CASS)  │       │   - embeddings,     │       │     symbol ↔ text   │       └─────────┬───────────┘                 │                 ▼          ┌───────────────┐          │ OBSERVABILITY │          │ - Prometheus  │          │ - Grafana     │          │ - Kafka UI    │          └───────────────┘`

## How cues flow (like a show)

1. **User clicks a symbol** → frontend produces `gibsey.ui.symbol`.
    
2. **Faust** enriches with session, character, section; emits `gibsey.generate.page.request`.
    
3. **DSPy PageGenerator** consumes request → does RAG over Cassandra → emits `gibsey.generate.page.done` with text + metadata.
    
4. **Writers** append the event to `events_log`, update `pages_index`, optionally take a **snapshot** of UI state.
    
5. **Frontend** subscribes (websocket/HTTP poller on a gateway) and renders the new page; user can **VAULT.SAVE** (curation), which becomes another event.
    

---

## Minimal topic plan (copy/paste)

- `gibsey.ui.symbol` – {session_id, character_id, section_id, symbol_id}
    
- `gibsey.ui.orientation` – {session_id, symbol_id, orientation: [N,E,S,W]}
    
- `gibsey.ask` – {session_id, prompt, context.symbols[]}
    
- `gibsey.generate.page.request` – downstream cue for DSPy
    
- `gibsey.generate.page.done` – {page_id, text, embeddings_ref, provenance}
    
- `gibsey.index.update` – maintain fast read models (per character/section)
    
- `gibsey.vault` – user-curated saves + labels
    
- `gibsey.snapshot` – periodic state snapshot (for fast resume)
    
- `gibsey.audit` – minimal, append-only audit trail
    
- `gibsey.dlq` – dead-letter for poison messages
    

**Partition key:** `session_id` (ensures each user’s timeline is totally ordered).  
**Headers you’ll love:** `x-character`, `x-section`, `x-symbol`, `x-orientation`, `x-voice`.

---

## Event schema (tiny, but future-proof)

`{   "event_id": "uuid",   "type": "gibsey.ui.symbol",   "ts": "2025-08-18T19:41:00Z",   "session_id": "uuid",   "actor": "user|system|agent",   "payload": {     "character_id": "princhetta",     "section_id": 8,     "symbol_id": "S8-PR",     "orientation": "N"   },   "provenance": {     "client": "web",     "version": "ui-0.3.1"   } }`

---

## Cassandra (via Stargate) tables (event sourcing + queryable views)

**`events_log` (append-only)**

`PRIMARY KEY ((session_id), ts, event_id) columns: type, payload_json, headers_json`

**`state_snapshots`** (materialized every N events)

`PRIMARY KEY ((session_id), snapshot_ts) columns: ui_state_json, last_event_ts, cursor`

**`pages_index`** (read model for quick UI)

`PRIMARY KEY ((character_id, section_id), page_id) columns: session_id, title, excerpt, embeddings_ref, created_ts`

**`vault`** (curation)

`PRIMARY KEY ((session_id), saved_ts, page_id) columns: label, notes`

---

## Tiny DSPy actor shape (just to show contract)

`# purpose: one focused skill that turns a cue into a page class PageGenerator(Skill):     def __call__(self, character_id, section_id, orientation, ask=None):         # 1) fetch context chunks from pages_index/embeddings         # 2) compose prompt = symbol semantics + user ask + prior state         # 3) generate page text + metadata         return {"page_id": uuid4(), "text": text, "provenance": {...}}`

You wire this to the Kafka consumer for `gibsey.generate.page.request` and produce `gibsey.generate.page.done`.

---

## Naming & routing that will save you later

- **Topic prefix by domain**: `gibsey.ui.*` (human cues), `gibsey.generate.*` (agent work), `gibsey.state.*` (snapshots/index).
    
- **Idempotency**: carry `event_id`; writers upsert with `(session_id, event_id)` guard.
    
- **Replay**: to rebuild a session, consume `events_log` by `session_id` from the beginning; apply in order; hydrate UI or re-generate read models.
    
- **Backpressure**: Faust windowing for bursty UI (e.g., orientation dial spins).
    
- **Schema**: keep JSON in the log, but define a Pydantic/Marshmallow model in code to avoid drift.
    

---

## Tonight’s vibe-coding checklist (30–90 min, bite-size)

1. **Create topics**: `gibsey.ui.symbol`, `gibsey.generate.page.request`, `gibsey.generate.page.done`.
    
2. **Write a tiny gateway** (Node/Express or Python/FastAPI) with two endpoints:
    
    - `POST /event/ui/symbol` → produce to `gibsey.ui.symbol` (key=session_id).
        
    - `GET /events/stream?session_id=…` → simple SSE that tails `gibsey.generate.page.done`.
        
3. **Faust app**: consume `gibsey.ui.symbol` → enrich → produce `gibsey.generate.page.request`.
    
4. **Mock PageGenerator**: consume requests → return lorem text tagged with `character_id/section_id` → produce `...page.done`.
    
5. **Write to Cassandra**: on `...page.done`, append to `events_log` and `pages_index`.
    
6. **Frontend**: button click → `POST /event/ui/symbol`; subscribe to SSE → render page text.