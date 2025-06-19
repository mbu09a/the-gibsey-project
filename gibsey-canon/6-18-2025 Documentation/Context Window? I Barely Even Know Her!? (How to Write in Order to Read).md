Below is a **step‑by‑step engineering brief** that translates the insight you just articulated—_“Gibsey should write itself, not merely read itself”_—into concrete, immediately actionable development tasks. Everything is scoped so that you (or Claude Code) can tackle the work in small, focused commits while still moving decisively toward a **generative, symbol‑driven DSPy + QDPI pipeline**.

---

## 1 · Reframed Objective (one sentence)

> **Build a DSPy/QDPI pipeline that starts from compact Corpus symbols, retrieves _rich_ source fragments, and recombines them into new narrative text—thereby _expanding_ the material rather than summarising or compressing it.**

This flips the usual “RAG‑for‑reading” pattern into a **“RAG‑for‑writing”** pattern:

|Conventional RAG (reading)|Gibsey RAG‑X (writing)|
|---|---|
|1. User query → retrieve summaries → answer.|1. Symbol seeds → retrieve full‑fidelity fragments → **recombine & elaborate** → produce original text.|
|Goal: minimise tokens.|Goal: maximise _creative complexity per token_.|

---

## 2 · Minimal Generative Pipeline

```mermaid
flowchart LR
    A[Symbol Seed(s)] -->|DSPy Module 1| B(Fragment Retriever)
    B -->|Raw quotes, events, motifs| C(Recombiner / Composer)
    C -->|Draft Passage| D(Reflect‑Refine Loop) 
    D -->|Final Narrative| E(Vault Save + Metadata)
    E -->|Vectors & Embeds| F(Next‑gen Retrieval)
```

### Module responsibilities

|DSPy Module|What it DOES (creative role)|Key prompt/constraint|
|---|---|---|
|**SymbolSelector**|Choose 1‑N Corpus symbols (user‑picked or model‑picked) to seed writing.|“Return an array of up to _k_ symbols most thematically resonant with prompt X.”|
|**FragmentRetriever**|Pull _full‑fidelity_ passages, quotes, images, or research snippets linked to each symbol (no summaries).|“For each symbol, fetch _two_ diverse raw fragments (≤ 300 tokens each).”|
|**Recombiner / Composer**|Weave fragments into a new passage, adding connective tissue and original prose.|“Compose an original scene of 400‑600 words; keep quoted fragments verbatim.”|
|**Reflect‑Refine**|Self‑critique: continuity, voice, surprise. If weak, regenerate.|Use DSPy’s `Iterative` pattern with explicit acceptance criteria (voice match ≥ 8/10).|
|**MetadataWriter**|Tag the output: symbols used, new sub‑symbols minted, emotional tone.|Enables future retrieval by affect or motif.|

**Why this still scales cheaply:**  
Only the _fragments_ (max ≈ 1 k tokens total) plus the draft (< 1 k) are fed to the large model on each turn—_not_ your entire novel.

---

## 3 · Concrete Tasks & Claude‑Code Prompts

|#|Task (1‑2 h each)|File / Directory|Claude Code Prompt|
|---|---|---|---|
|**T1**|**Add a `SymbolSeed` endpoint** (`POST /symbols/expand`) that accepts one or more Corpus IDs and returns retrieved fragments (raw, not summarised).|`backend/routes/symbols.ts`|_“Create a Bun + Hono route `/symbols/expand`. Body: `{ symbols: string[], k?: number }`. Respond with JSON `{ symbol, fragments[] }` where each `fragment` has `text`, `sourcePageId`, `charStart`, `charEnd`. Use existing vector search to fetch full passages, not summaries.”_|
|**T2**|**Implement `FragmentRetriever` DSPy module** that calls the new route.|`ai/modules/fragment_retriever.py`|_“Write a DSPy module `FragmentRetriever(symbols: list[str], k: int) -> list[Fragment]`. Use `httpx` to call `/symbols/expand`, return list of `Fragment` dataclass objects.”_|
|**T3**|**Create `RecombinerComposer` module** that takes fragments and a style directive (e.g., “Princhetta voice”) and outputs a 400–600 word scene.|`ai/modules/recombiner_composer.py`|_“Implement DSPy `RecombinerComposer(fragments, style, target_len=500)` using an LLM with open‑ended generation. Keep quoted fragments verbatim (wrap in « »). Return draft text plus `used_symbol_ids`.”_|
|**T4**|**Add reflection loop** using DSPy’s `Iterative` wrapper with an acceptance function checking (a) voice similarity score from an embedding model, (b) novelty vs. source fragments.|`ai/pipelines/generative_writer.py`|_“Wrap `RecombinerComposer` in `Iterative` that re‑calls composer until `score_voice ≥ 0.8` and `novelty ≥ 0.4` (cosine distance between output embedding and average fragment embedding).”_|
|**T5**|**Expose a `/write` API route** that wires T1‑T4: client posts `{ symbols, styleHint }` and receives `finalNarrative`, `metadata`.|`backend/routes/write.ts`|_“Create Hono route `/write`. Body: `{ symbols: string[], styleHint?: string }`. Orchestrate FragmentRetriever → RecombinerComposer → ReflectLoop. Return full narrative plus metadata.”_|
|**T6**|**Add simple front‑end “Generative Pad”**: textarea to choose symbols (autocomplete), button “Write Passage”, output pane.|`frontend/components/GenerativePad.tsx`|_“Build a React component `GenerativePad`. Props: none. State: `selectedSymbols`, `style`, `draft`. Hit `/write` when user clicks **Generate**. Render result in a scrollable card; show which fragments were used (collapsible).”_|
|**T7**|**Unit‑test RecombinerComposer** with stubbed fragments to ensure fragments remain verbatim and length bounds respected.|`ai/tests/composer.test.py`|_“Use pytest (or Vitest if TS) to feed three fake fragments to `RecombinerComposer`; assert: (1) output contains all fragments verbatim, (2) 350 ≤ len(output.split()) ≤ 650.”_|

---

## 4 · Key Prompt Templates (copy‑paste ready)

### 4.1 Recombiner / Composer system prompt

```
You are “Gibsey‑Composer”, an author who expands symbol‑seed fragments into vivid, original scenes.
• Keep every quoted fragment verbatim, wrapped in « ».
• Blend fragments seamlessly; add connective prose and new details.
• Target length: {{target_len}} words (±15%).
• Maintain {{style}} voice and narrative tense.
```

### 4.2 Reflect‑Refine acceptance function (Python pseudocode)

```python
def accept(draft, fragments, voice_embed, min_voice=0.8, min_novel=0.4):
    emb_draft = embed(draft)
    score_voice = cosine(emb_draft, voice_embed)
    novelty = 1 - cosine(emb_draft, mean(embed(f.text) for f in fragments))
    return score_voice >= min_voice and novelty >= min_novel
```

---

## 5 · Avoiding “lossy” summarisation without blowing up cost

|Technique|Why it aligns with your principle|
|---|---|
|**Fragment caps (k & length)**|You retrieve _full_ passages, but you cap how many and how long—so richness is preserved yet bounded.|
|**Symbol pre‑filter**|Symbols are _already_ compressed meanings; selecting relevant ones focuses generation without discarding nuance inside the chosen fragments.|
|**Local inference**|Run the generative model locally (e.g., fine‑tuned Mixtral‑8x7B with LongRoPE). Token cost per 1 k ~ $0.0008; creative expansion stays cheap.|
|**Iterative acceptance loop**|Quality filter prevents “garbage expansion,” so every extra token spent adds genuine narrative value.|

---

## 6 · What to _de‑scope_ for this sprint

- Multi‑symbol “braiding” across ten chapters.
    
- Full gift‑ledger economy and QDPI four‑way handshake.
    
- Automated fine‑tuning of style adapters (run once later).
    

Focus on proving that **Symbol → Fragments → Novel Scene** loop works end‑to‑end.

---

### Bottom line

You don’t need to fight the context‑window ceiling by shrinking your text; you bypass it by **growing new text from compact symbolic seeds**. The seven tasks above—each with a Claude‑ready prompt—convert that philosophy into code this week. Once the loop is live, _Gibsey is no longer reading itself efficiently; it is writing itself creatively_—exactly as you envisioned.