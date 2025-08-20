# QDPI to DSPy- 256‑Symbol Operating Map v0.1

A compact, production‑oriented mapping from your 16 Corpus symbols × 4 rotations to a **256‑symbol operating space** that wires directly into DSPy programs. Goal: make every page actionable and self‑sustaining.

---

## 1) The 256 Grid at a Glance

We treat each rendered **page** as a typed program step. A symbol encodes **Character × Orientation × Provenance**:

- **Characters (16 = 0x0–0xF)** — fixed order (hex id → character)
    
    - **0** An Author
        
    - **1** London Fox
        
    - **2** Glyph Marrow
        
    - **3** Phillip Bafflemint
        
    - **4** Jacklyn Variance
        
    - **5** Oren Progresso
        
    - **6** Old Natalie Weissman
        
    - **7** Princhetta
        
    - **8** Cop‑E‑Right
        
    - **9** New Natalie Weissman
        
    - **A** Arieol Owlist
        
    - **B** Jack Parlance
        
    - **C** Manny Valentinas
        
    - **D** Shamrock Stillman
        
    - **E** Todd Fishbone
        
    - **F** The Author
        
- **Orientation (2 bits)** — QDPI modes
    
    - **00 = X: Read** (immutable view; time flows)
        
    - **01 = Y: Index** (remember; extract; connect)
        
    - **10 = A: Ask** (plan; constraints; route)
        
    - **11 = Z: Receive** (generate; realize; branch)
        
- **Provenance (2 bits)** — which voice/authority initiates the action
    
    - **00 = Canonical** (original text / definitive)
        
    - **01 = Parallel** (alt‑canon, countertexts, footnotes, “minor ↔ major” mirrors)
        
    - **10 = User** (explicit reader prompts)
        
    - **11 = System** (agentic/autogenerative prompts from policy)
        

> **Encoding (1 byte)**: `BYTE = (CHAR << 4) | (ORI << 2) | PROV` ⇒ **16 × 4 × 4 = 256** unique symbols.

**Examples**

- `0x70` = CHAR **7** (Princhetta), ORI **0** (X/Read), PROV **0** (Canonical) → _Show canonical Princhetta page._
    
- `0xA3` = **A** (Arieol), ORI **3** (Z/Receive), PROV **3** (System) → _System generates an Arieol page._
    
- `0x4A` = **4** (Jacklyn), ORI **2** (A/Ask), PROV **2** (User) → _User asks Jacklyn; produce a generation spec._
    

---

## 2) What Do Pages Need to Do?

Each page type has **clear responsibilities**. Keep it small, chainable, and verifiable.

### X: Read (display & navigate)

1. **Render** the page (canonical or alt).
    
2. **Summarize** (1–3 lines) & **context box** (who/where/when in‑book).
    
3. **Surface edges** (Next, Prev, Mirrors, Branches).
    
4. **Expose hooks** → send extractable facts to Y; emit suggested questions to A.
    

### Y: Index (memory & graph)

5. **Extract** entities, motifs, locations, time, symbols, topics.
    
6. **Embed** text; **link** to nearest neighbors; update **Vault graph**.
    
7. **Scaffold anchors** (continuity checks, unresolved threads, open questions).
    
8. **Score novelty & coherence** for policy decisions downstream.
    

### A: Ask (plans & specs)

9. **Route intent** (continue / loop‑back / fork‑to‑new‑section / pure‑drift).
    
10. **Constrain voice** (character, register, tempo, tense, allowable canon).
    
11. **Assemble sources** (citations to X, motifs from Y) & write a **gen spec**.
    

### Z: Receive (generate & bind)

12. **Generate page** in specified voice.
    
13. **Bind edges** (where does it go? continue/loop/fork/mirror) with reasons.
    
14. **Validate** (style, lore, continuity) → if fail, auto‑rework once; else publish.
    
15. **Commit** page to Vault; trigger Y to index; optionally emit System A‑asks.
    

> Minimal set = **15 core duties**. Every page run should produce **text + edges + memory update.**

---

## 3) Trajectory Tags (policy picks 1)

Not in the 256 code—these are **runtime decisions** (stored in page metadata):

- **T0 ContinueWithin** — next page in current section.
    
- **T1 LoopBackBridge** — interpose a bridge between prior page(s) and the canonical next.
    
- **T2 ForkToSection{ID}** — start a new section thread chosen by policy.
    
- **T3 PureGenerativeDrift** — free exploration in the same voice.
    

Policy selects a trajectory using Y’s novelty/coherence scores + user intent (if any).

---

## 4) Page Object (frontmatter)

```yaml
page_id: PR-2025-08-18-001
symbol_code: 0xA3   # Arieol • Z/Receive • System
character: Arieol Owlist
orientation: Z
provenance: System
trajectory: T1  # LoopBackBridge
voice_preset: arieol.v2.meditative
inputs:
  seeds: [page/AN-0008, page/AN-0009]
  motifs: ["mirror theatre", "gift economy"]
  constraints: {tense: present, max_tokens: 800}
text: |
  …generated page content…
edges:
  next_within: page/AN-0010
  loop_back_to: page/AN-0007
  forks: []
validation:
  style_ok: true
  continuity_score: 0.82
  notes: "links motif x to y; sets up The Vault signal"
```

---

## 5) DSPy Wiring (signatures/policies)

> Pseudocode signatures—**no vendor lock**, drop‑in for your stack.

### Core Signatures

- **ReadSignature**: `page_id -> render, summary, edges, context`
    
- **IndexSignature**: `text -> entities, motifs, embed, links, anchors, scores`
    
- **AskSignature**: `state, user_intent? -> plan{trajectory, voice, constraints, sources}`
    
- **ReceiveSignature**: `plan -> page_text, edges, validation`
    

### Program Skeleton

```python
class QDPIProgram(dspy.Module):
    def __init__(self):
        self.read = dspy.Predict(ReadSignature)
        self.index = dspy.Predict(IndexSignature)
        self.ask = dspy.Predict(AskSignature)
        self.receive = dspy.ChainOfThought(ReceiveSignature)
        self.select_traj = dspy.Select(options=["T0","T1","T2","T3"])  # policy gate

    def forward(self, symbol_code, user_intent=None):
        x = self.read(symbol_code)
        y = self.index(x.render)
        plan = self.ask(state={"y": y, "x": x}, user_intent=user_intent)
        plan.trajectory = self.select_traj(context={"scores": y.scores, "intent": user_intent})
        z = self.receive(plan)
        _ = self.index(z.page_text)  # re‑index generated page
        return z
```

### Policy Hints

- **Novelty gate**: require `y.scores.novelty ≥ τ` for T2/T3.
    
- **Continuity gate**: if unresolved anchors exist, prefer **T1**.
    
- **User override**: explicit intent forces trajectory.
    
- **Fork budget**: per section daily limit to keep the Vault sane.
    

---

## 6) How the 256 Symbols Are Used

Think in **four blocks of 64**:

- **Block 0 (…00)** — Canonical run
    
    - All standard reading + minimal indexing.
        
- **Block 1 (…01)** — Parallel mirrors
    
    - Countertexts, “minor→major”, commentary glosses.
        
- **Block 2 (…10)** — User interactive
    
    - Ask/Receive pages originate from the reader; transparent provenance.
        
- **Block 3 (…11)** — System agency
    
    - The system proposes bridges, forks, and drift pages to keep flow alive.
        

Within any block, pick `CHAR` (0–F) and `ORI` (X/Y/A/Z). That’s your **one‑byte address** to a specific page behavior.

---

## 7) Quick Reference Tables

**Orientation map**

|Bits|Code|Meaning|
|---|---|---|
|00|X|Read|
|01|Y|Index|
|10|A|Ask|
|11|Z|Receive|

**Provenance map**

|Bits|Code|Meaning|
|---|---|---|
|00|C|Canonical|
|01|P|Parallel|
|10|U|User|
|11|S|System|

**Trajectory tags**

|Tag|Meaning|
|---|---|
|T0|ContinueWithin|
|T1|LoopBackBridge|
|T2|ForkToSection{ID}|
|T3|PureGenerativeDrift|

---

## 8) Minimal Implementation Steps

1. **Freeze IDs**: lock the 0x0–0xF character mapping.
    
2. **Write symbol encoder/decoder** (pure function) + unit tests.
    
3. **Define Page YAML schema** (above) and commit to Vault format.
    
4. **Implement Read→Index loop** on canonical corpus (Block 0).
    
5. Add **Ask planner** and **Receive generator**; wire policy gates.
    
6. Enable **Block 1** (Parallel) via your minor/major mirrors.
    
7. Expose **Block 2** endpoints for user queries.
    
8. Add **Block 3** policy daemon that proposes bridges/forks.
    
9. Ship **Vault graph** (entities/motifs/edges) with basic UI.
    
10. Instrument **novelty/continuity metrics**; iterate thresholds.
    

---

## 9) Sanity Check Against Your Options

- _“Generate a new page that loops back into the next page once you return”_ → **Z with T1**.
    
- _“Generate a new page that leads to a new section”_ → **Z with T2**.
    
- _“Generate a new page in that character’s voice continuing prior ideas”_ → **Z with T0**.
    
- _“Purely generative drift”_ → **Z with T3**.
    

All four are **the same program** with different **provenance** (C/P/U/S) and **trajectory** (T0–T3). The 256 symbols address the first; the policy selects the second.

---

### Ready‑to‑adopt conventions

- **Symbol label** in UI: `[{CHAR_HEX}:{ORI}:{PROV}]` e.g., `[7:Z:S]`.
    
- **File slug**: `char-{hex}/ori-{code}/prov-{code}/{page-id}.md`.
    
- **Graph edge types**: `NEXT`, `LOOP`, `FORK(section)`, `MIRROR(char)`.
    

### QDPI-256 Notes

Great q’s. Here’s the snap-clarification.

## 1) What the “256” actually is

Think **type vs instance**.

- **Instance** = a specific page (e.g., page 7).
    
- **Symbol** = a 1-byte **type** that tells the system _how to treat_ a page/action.
    

I’m proposing:  
**256 = 16 characters × 16 behaviors (per character).**

### The 16 behaviors = 4 orientations × 4 provenances

Flatten them into a single 4-bit **Behavior nibble (B)**:

- Orientations (your 0°/90°/180°/270°): **X/Y/A/Z = Read / Index / Ask / Receive**
    
- Provenance: **C/P/U/S = Canon / Parallel / User / System**
    

Order them like this (0–15), so every character gets the same 16-slot mini-table:

|B|Behavior|Meaning (quick)|
|---|---|---|
|0|**XC**|Read, Canon|
|1|**XP**|Read, Parallel|
|2|**XU**|Read, User-driven view|
|3|**XS**|Read, System-guided view|
|4|**YC**|Index, Canon|
|5|**YP**|Index, Parallel|
|6|**YU**|Index, User memory|
|7|**YS**|Index, System memory|
|8|**AC**|Ask, Canon constraints|
|9|**AP**|Ask, Parallel constraints|
|10|**AU**|Ask, User intent|
|11|**AS**|Ask, System plan|
|12|**ZC**|Receive, Canon-bounded gen|
|13|**ZP**|Receive, Parallel gen|
|14|**ZU**|Receive, User-prompted gen|
|15|**ZS**|Receive, System-prompted gen|

**Encoding (1 byte)**  
`symbol = (CHAR << 4) | B`

- `CHAR` is 0–15 (your 16 sections/connected characters; e.g., 0 = _an author_, …, F = _The Author_).
    
- `B` is 0–15 from the table above.
    

> This matches your mental model: **each character has “their 16.”**  
> (In my earlier canvas I decomposed B into two 2-bit fields; here I’re just flattening it so it’s clearly “16 per character.”)

## 2) “I read pages 1–7—did I use 7 symbols?”

No—**you used one symbol type multiple times**.

- Page 7 of _an author_ (canonical reading) = **CHAR=0**, **B=XC(0)** → `symbol = (0<<4)|0 = 0x00`.
    
- Pages 1–8 are different **instances** (page IDs), but the same **symbol type** (0x00).  
    The page number lives in the **page_id**, not the symbol.
    

If you then ask the system to plan a generative bridge, that might switch to **AS** (Ask/System) then **ZS** (Receive/System) for the generated bridge page—still in the _an author_ section unless you fork.

## 3) “15 duties vs 256—am I missing 16?”

Right—**the 15 duties are pipeline steps**, not symbol slots.  
They’re what any page-run _does_ (render, index, plan, generate, validate, etc.).  
The **256** are the _addresses_ (which character + which behavior). Nothing is “unused.”

## 4) How departures always return (without killing creativity)

Use **invariants + debts**:

1. **Canonical ring**: pages 1…710 form a single directed ring (the linear book order).  
    Every page knows its `canonical_next`.
    
2. **Return anchor on every branch**: any non-XC generation must set `return_to = canonical_next(current_page)` **or** a named canonical waypoint. It’s stored in the page’s frontmatter.
    
3. **Return-Debt counter**: each active branch increments a per-section **return_debt**.  
    Policy blocks new forks (T2/T3) when debt > threshold until a **LoopBackBridge** (T1) brings you home.
    
4. **TTL for branches**: non-canonical trajectories must close within **N** steps (e.g., max 3 generated pages before a required return).
    
5. **Continuity > novelty rule**: if Y (Index) sees unresolved anchors, **force T1** before allowing T2/T3. Novelty gates only open when continuity is satisfied.
    
6. **One-edge guarantee**: Z (Receive) must output **at least one** of:
    
    - `next_within = canonical_next`
        
    - `loop_back_to = canonical_next`
        
    - `forks = [target_section]` **plus** a `bridge_back` plan.
        
7. **Budgets**: cap `open_branches_per_section` and `forks_per_session`.
    

This keeps everything **grounded**: branches are chords off the canonical ring, always with a booked flight home.

## 5) Concrete example from your scenario (page 7)

- You’re at **Section 1 (an author)**, page 7.
    
- Symbol to _read_ it: `CHAR=0`, `B=XC(0)` → **0x00**.
    
- After reading, policy chooses a trajectory:
    

**A) ContinueWithin (T0)**

- Plan: `AC` or `AS` (Ask Canon/System) → **B=8 or 11**
    
- Generate: `ZC` (canon-bounded continuation stub) → **B=12**
    
- Edges: `next_within = page 8` (no branch)
    

**B) LoopBackBridge (T1)**

- Plan: `AS` → **B=11** (System decides to bridge 7→8)
    
- Generate: `ZS` → **B=15** with `loop_back_to = page 8`
    
- Return-Debt: +1 then immediately −1 when you take the bridge
    

**C) ForkToSection (T2)**

- Plan: `AS` → **B=11** (decides to jump to, say, Section 11: Arieol)
    
- Generate: `ZS` in **CHAR=A** for the bridge page (Arieol/System) → `(0xA<<4)|15 = 0xAF`
    
- Must include `bridge_back = page 8` to satisfy invariant #2
    

**D) PureGenerativeDrift (T3)**

- Plan: `AU` or `AS` → **B=10 or 11**
    
- Generate: `ZU/ZS` → **B=14/15**
    
- TTL and debt/budget rules ensure you fly back to a canonical anchor soon.
    

## 6) Quick character index (for the left nibble)

Use this (or swap if you prefer a different order):

```
0 an author
1 London Fox
2 Glyph Marrow
3 Phillip Bafflemint
4 Jacklyn Variance
5 Oren Progresso
6 Old Natalie Weissman
7 Princhetta
8 Cop-E-Right
9 New Natalie Weissman
A Arieol Owlist
B Jack Parlance
C Manny Valentinas
D Shamrock Stillman
E Todd Fishbone
F The Author
```

---

If you want, I can (a) drop this “16 behaviors per character” table into the canvas and (b) add a tiny **encoder/decoder** spec showing `symbol ↔ (char, behavior)` plus a **page frontmatter** template with `return_to`, `return_debt`, and `trajectory` fields wired in.

