# Original Prompt for GPT‑5 Pro — Repo Audit to QDPI/DSPy Game Plan

> **You are GPT‑5 Pro.** Your task is to inspect my current repo and produce a single, copy‑pastable **Markdown game plan** to implement a minimal, working QDPI→DSPy pipeline with my 256‑symbol scheme. Assume I want to start **today**. If something is unknown (e.g., missing env vars), explicitly list the assumptions and what you need from me next.

---

## Goals (what to deliver in your answer)

1. A **concise repo audit** (current structure, services, env, gaps).
    
2. A **step‑by‑step implementation plan** (today → this week) with checkboxes.
    
3. Concrete **Cassandra schema (CQL)**, **encoder/decoder stub**, **page YAML schema**, **DSPy signatures**, **FastAPI endpoints**, and a **test plan**.
    
4. **Definition of Done** and a short **risk/mitigation** section.
    
5. Keep all code in your response minimal but runnable; favor stubs over walls of code.
    

---

## Context you need to use

### A) The 256‑symbol addressing scheme (type, not instance)

- **Characters (16)** → hex `0..F` (left nibble). Use this mapping:
    
    - `0` an author
        
    - `1` London Fox
        
    - `2` Glyph Marrow
        
    - `3` Phillip Bafflemint
        
    - `4` Jacklyn Variance
        
    - `5` Oren Progresso
        
    - `6` Old Natalie Weissman
        
    - `7` Princhetta
        
    - `8` Cop‑E‑Right
        
    - `9` New Natalie Weissman
        
    - `A` Arieol Owlist
        
    - `B` Jack Parlance
        
    - `C` Manny Valentinas
        
    - `D` Shamrock Stillman
        
    - `E` Todd Fishbone
        
    - `F` The Author
        
- **Behaviors (16 per character)** → right nibble `B ∈ [0..15]` = **4 orientations × 4 provenances**:
    
    - Orientations: **X/Y/A/Z = Read / Index / Ask / Receive**
        
    - Provenances: **C/P/U/S = Canon / Parallel / User / System**
        
    
    **Behavior table (right nibble):**
    
    |B|Behavior|Meaning|
    |---|---|---|
    |0|XC|Read, Canon|
    |1|XP|Read, Parallel|
    |2|XU|Read, User‑driven view|
    |3|XS|Read, System‑guided view|
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
    
- **Encoding (1 byte):** `symbol = (CHAR << 4) | B` ⇒ **16 × 16 = 256 types**.
    
- **Important:** A symbol is a **type**; a **page instance** is identified by `page_id` (e.g., `S01-P0007`). Reading pages 1–8 of Section 1 reuses **the same type** `0x00` (CHAR=0, B=XC) eight times on different instances.
    

### B) Page pipeline responsibilities (the 15 duties)

- **X: Read** → render, summarize, expose edges/hooks.
    
- **Y: Index** → entities/motifs, embedding, link neighbors, anchors, scores (novelty/coherence).
    
- **A: Ask** → route intent (T0/T1/T2/T3), constrain voice, assemble sources, write a gen spec.
    
- **Z: Receive** → generate text, bind edges (continue/loop/fork/mirror), validate style & continuity, commit, and trigger re‑index.
    

> Treat duties as _what each run does_, not separate symbol slots.

### C) Trajectories (runtime policy; not part of the 256)

- **T0 ContinueWithin** — go to canonical next in same section.
    
- **T1 LoopBackBridge** — generate a bridge then return to canonical next.
    
- **T2 ForkToSection{ID}** — start a new thread in target section.
    
- **T3 PureGenerativeDrift** — free exploration; TTL must close back to canon.
    

### D) Grounding invariants (departures must return)

1. **Canonical ring**: all 710 pages form a directed ring via `NEXT` edges.
    
2. Every non‑canonical Z must set `return_to = canonical_next(current)`, or another explicit canonical waypoint.
    
3. **Return‑debt counter** per section; block new forks when debt exceeds a threshold until a bridge returns.
    
4. **TTL for branches** (e.g., max 3 generated pages before forced return).
    
5. **Continuity‑first**: if unresolved anchors exist, force a T1 before allowing T2/T3.
    
6. **One‑edge guarantee**: Z must output at least one of `next_within`, `loop_back_to`, or `forks` (with a bridge‑back plan).
    

### E) Minimal architecture (today)

- **Cassandra 4.x** (OK to store vectors as BLOB for now; migrate later).
    
- Optional: **Stargate** for REST/GraphQL; otherwise use Python driver.
    
- **One Python service** (DSPy + FastAPI) implementing the 4 signatures and gating policies.
    
- **LLM + embedding** functions.
    
- **Kafka** is _optional_ for MVP; add later for background workers/audit.
    

### F) Minimal Cassandra schema (CQL)

```sql
CREATE TABLE pages (
  page_id TEXT PRIMARY KEY,
  char_hex TINYINT,          -- 0..15
  behavior TINYINT,          -- 0..15 (XC..ZS)
  symbol_code TINYINT,       -- (char<<4)|behavior
  section INT,               -- 1..16
  page_num INT,              -- nullable for generated pages
  provenance TEXT,           -- C/P/U/S
  orientation TEXT,          -- X/Y/A/Z
  trajectory TEXT,           -- T0/T1/T2/T3
  return_to TEXT,            -- canonical anchor id
  text TEXT,
  created_at TIMESTAMP
);

CREATE TABLE page_edges (
  page_id TEXT,
  edge_type TEXT,            -- NEXT | LOOP | FORK | MIRROR
  target_id TEXT,
  created_at TIMEUUID,
  PRIMARY KEY ((page_id), edge_type, created_at)
);

CREATE TABLE page_embeddings (
  page_id TEXT PRIMARY KEY,
  dim INT,
  vec BLOB
);

CREATE TABLE page_index_signals (
  page_id TEXT PRIMARY KEY,
  entities SET<TEXT>,
  motifs SET<TEXT>,
  unresolved_anchors SET<TEXT>,
  novelty DOUBLE,
  coherence DOUBLE
);

CREATE TABLE section_counters (
  section INT PRIMARY KEY,
  open_branches COUNTER,
  return_debt COUNTER
);

CREATE TABLE plans (
  plan_id TIMEUUID PRIMARY KEY,
  page_id TEXT,
  symbol_code TINYINT,
  trajectory TEXT,
  plan_json TEXT,
  created_at TIMESTAMP
);
```

### G) Page frontmatter schema (YAML)

```yaml
page_id: S01-P0007
symbol_code: 0x00          # CHAR=0 (an author), B=0 (XC)
character: an author
orientation: X             # Read
provenance: C              # Canon
trajectory: T0             # runtime policy decision
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

### H) DSPy signatures + skeleton

```python
import dspy

class ReadSignature(dspy.Signature):
    """Render and summarize a page."""
    symbol_code: int  # (char<<4)|B
    # outputs
    render: str
    summary: str
    edges: dict
    context: dict

class IndexSignature(dspy.Signature):
    """Index a text: entities, motifs, embedding, anchors, scores."""
    text: str
    entities: list
    motifs: list
    anchors: list
    scores: dict

class AskSignature(dspy.Signature):
    """Plan next move given state and optional user intent."""
    state: dict
    user_intent: str = ""
    trajectory: str
    voice: dict
    constraints: dict
    sources: list

class ReceiveSignature(dspy.Signature):
    """Generate a new page per plan; bind edges; validate."""
    plan: dict
    page_text: str
    edges: dict
    validation: dict

class QDPIProgram(dspy.Module):
    def __init__(self):
        self.read = dspy.Predict(ReadSignature)
        self.index = dspy.Predict(IndexSignature)
        self.ask = dspy.Predict(AskSignature)
        self.receive = dspy.ChainOfThought(ReceiveSignature)
        self.select_traj = dspy.Select(options=["T0","T1","T2","T3"])  # policy gate

    def forward(self, symbol_code: int, user_intent: str = ""):
        x = self.read(symbol_code)
        y = self.index(x.render)
        plan = self.ask(state={"x": x, "y": y}, user_intent=user_intent)
        plan.trajectory = self.select_traj(context={"scores": y.scores, "intent": user_intent})
        z = self.receive(plan)
        _ = self.index(z.page_text)  # re-index
        return z
```

### I) Encoder/decoder (spec)

- **Encode:** `code = (char_hex << 4) | behavior`
    
- **Decode:** `char_hex = code >> 4` ; `behavior = code & 0xF`
    
- Provide a table/map for behaviors 0..15 → {orientation, provenance}.
    

### J) Minimal FastAPI endpoints

- `POST /run/symbol/{code}` → runs X→Y→A→Z once (with optional `user_intent`).
    
- `GET /page/{page_id}` → returns stored page + edges + signals.
    
- `POST /branch/{page_id}` → run A→Z from a given locus.
    
- `GET /stats/section/{id}` → counters, debts, open branches.
    

---

## What to inspect in the repo (please do this first)

1. **Project layout** (monorepo? services? infra?).
    
2. **Cassandra integration** (driver vs Stargate; keyspace; migrations).
    
3. **Existing schemas** (pages, embeddings, anything vector‑ish).
    
4. **Embedding pipeline** (lib, dim, storage).
    
5. **LLM wrapper** (provider, config, rate limits).
    
6. **API framework** (FastAPI? Flask? None?).
    
7. **Any Kafka wiring** (topics, producers/consumers), even if we’ll ignore for MVP.
    
8. **Env/config** (dotenv, pydantic settings, docker compose).
    
9. **Tests/CICD** (pytest, pre‑commit).
    
10. **Docs/scripts** (`Makefile`, `scripts/`, `README`, `docs/`).
    

Output a short **Repo Audit** section summarizing these with file paths.

---

## Today → This Week: expected plan shape

Your Markdown plan should include these headings and checklists:

### 0) Assumptions & inputs needed

### 1) Data model bring‑up

### 2) Core library

### 3) DSPy program

### 4) API surface (FastAPI)

### 5) Tests & fixtures

### 6) CLI & scripts (DX)

### 7) Optional Kafka (later)

### 8) Definition of Done

- End‑to‑end: can run `POST /run/symbol/0x00` and get a generated page with **edges** and **return_to** populated; data persists; counters update; tests green.
    

### 9) Risks & mitigations

- Vector storage limits → use BLOB now; migrate to vector type later.
    
- LLM variance → add retry‑with‑constraints; keep max tokens modest.
    
- Policy bugs → property‑based tests around return‑debt/TTL.
    

---

## Output format (please follow)

Produce **one** Markdown file with:

1. **Repo Audit** (bulleted, with file paths)
    
2. **Implementation Plan** (checklists as above)
    
3. **CQL** (in a code block)
    
4. **Python stubs** (symbols, schema, DSPy skeleton, FastAPI endpoints; short)
    
5. **Test plan** (pytest outline)
    
6. **Runbook** (commands to ingest canon, run one symbol, inspect results)
    
7. **Definition of Done** and **Risks**
    

If anything is unclear, begin your answer with a 3–5 item **Clarifications Needed** list, then continue with your best‑effort plan.