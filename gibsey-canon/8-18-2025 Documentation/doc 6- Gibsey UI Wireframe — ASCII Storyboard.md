# Gibsey UI Wireframe — ASCII Storyboard

_Sketching the end‑to‑end experience from symbol click → page generation → holographic views. Use this as a visual guide while wiring Kafka/DSPy tonight._

---

## Legend

- **Characters (16):** an author, London Fox, Glyph Marrow, Phillip Bafflemint, Jacklyn Variance, Oren Progresso, Old Natalie Weissman, Princhetta, Cop‑E‑Right, New Natalie Weissman, Arieol Owlist, Jack Parlance, Manny Valentinas, Shamrock Stillman, Todd Fishbone, The Author.
    
- **Orientations:** X=Read, Y=Index, A=Ask, Z=Receive.
    
- **Provenance:** C=Canon, P=Parallel, U=User, S=System.
    
- **Trajectories:** T0 Continue, T1 LoopBackBridge, T2 ForkToSection, T3 PureDrift.
    
- **Edges:** NEXT (→), LOOP (⤺), FORK (↗/↘), MIRROR (⟂).
    

> Tip: in UI, hue = character; shade/pattern = provenance; small corner icon = orientation.

---

## Frame 1 — Entrance Grid (Home)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ SYMBOL GRID (16×16)                           │ ORIENTATION DIAL  │ VAULT ▼ │
│                                                                                    │
│  [0x00] an author  [0x10] London Fox  [0x20] Glyph Marrow  ... [0xF0] The Author   │
│  [··] cells show current orientation (X/Y/A/Z) and provenance (C/P/U/S overlay)    │
│                                                                                    │
│  [Rotate ↻]   [Filter: Character ▾]  [Filter: Orientation ▾]  [Search 🔍]          │
└──────────────────────────────────────────────────────────────────────────────┘
Vault Timeline: (empty)
```

**Interaction:** user clicks `Princhetta` (CHAR=7) in **XC**.  
**Event path:**

```
[UI] click S=0x70+B=0 (XC)
   │
   ▼
(gibsey.ui.symbol){session_id, char=7, B=0, orientation=X, provenance=C}
   │
   ├─▶ (Faust/Enricher) add context (section, last_page, cursor)
   ▼
(gibsey.generate.page.request)
```

---

## Frame 2 — Page Reveal (Reader Panel)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ SYMBOLS (left)             │ READER PANEL (center)                 │ INSPECT │
│ [S07 XC] Princhetta        │  Title: Princhetta Who Thinks…        │ ┌──────┐│
│ …                          │  Meta: [7:XC:C]  page_id=S08-P0381    │ │Edges ││
│                            │  ───────────────────────────────────  │ │NEXT →││
│                            │  Text…                                 │ │LOOP ⤺││
│                            │                                         │ │FORK ↗││
│                            │  [Ask ▸] [Save to Vault ★]             │ └──────┘│
└──────────────────────────────────────────────────────────────────────────────┘
Vault Timeline:  [● S08-P0381]
```

---

## Frame 3 — Ask & Branch (User Intent → T2/T3)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ ASK BOX: “What if Princhetta refuses to perform?” [Submit]                   │
└──────────────────────────────────────────────────────────────────────────────┘
Event flow:
[UI] gibsey.ask  →  (enricher)  →  gibsey.generate.page.request  →  DSPy.PageGenerator
                                                           └─▶ gibsey.generate.page.done
UI update:
┌────────────────────────────┬──────────────────────────────────────────────────┐
│ READER (canon)             │  BRANCH CARD (tinted = U provenance)            │
│ S08-P0381 (XC:C)           │  S08-BR1 (ZU:U)                                 │
│ text…                      │  “Princhetta turns away from the stage…”        │
│                            │  [Return plan: T1 to S08-P0382]                 │
└────────────────────────────┴──────────────────────────────────────────────────┘
Vault Timeline:  [● P0381]───↗[○ BR1]
```

---

## Frame 4 — LoopBack Enforcement (Return Debt)

```
Branch grows (TTL=3) → policy requires return.

Vault Timeline:  [● P0381]───↗[○ BR1]──[○ BR2]──[○ BR3]⤺
                                        │              │
                                        └──────────────┘ (snap-back)
Reader shows BR3 (bridge text) then auto-navigates to NEXT canon page P0382.
```

---

## Frame 5 — Graph View (2D)

```
┌──────────────────────────── Graph (2D) ──────────────────────────────────────┐
│                                                                              │
│             ○ ○ ○ ○ ○ ○ ○ ○  (Canonical Ring: 710 beads by section)         │
│         ○                               ○                                   │
│      ○                                     ○                                │
│     ○      ── NEXT → arrows along ring      ○                               │
│      ○                                     ○                                │
│         ○                               ○                                   │
│             ○ ○ ○ ○ ○ ○ ○ ○                                                   │
│                                                                              │
│   Branches: ↗ fronds in character hue; LOOP arcs curve back to ring          │
│   Hover bead → tooltip (page_id, [char:orientation:prov], excerpt)           │
└──────────────────────────────────────────────────────────────────────────────┘
```

Controls: `[Show: Canon | Branches | Drift]` `[Color: Character | Provenance]` `[Labels ▾]` `[Replay ▶]`

---

## Frame 6 — Holographic Field (3D)

```
Perspective view (Three.js):

             ↗  drift
            ○
         /        
   ○──○──○──○──○──○   (ring)       ○
        \\  ↗  \\               ↘
          ○      ○───────○   fork branch

Edges are elastic filaments. Vault saves crystallize nodes (◆).
Camera: orbit, pan, zoom; focus on session path.
```

---

## Frame 7 — 4D Playback (Temporal Hyper‑Object)

```
Controls: [⏮] [⏯] [⏭]  Speed: ▓▓▓▓  Trail Length: ▓▓▓

Event frames (Kafka replay):
 t0: ring only
 t1: +P0381 ●
 t2: +BR1 ○ (tinted U)
 t3: +BR2 ○
 t4: +BR3 ○
 t5: LOOP ⤺ snap → highlight P0382 ●

Result: shimmering jellyfish-like afterimage of session path.
```

---

## Event → UI Cheat Sheet

```
ui.symbol                → highlight grid cell; load canon page; add bead to Vault
ui.orientation           → rotate cell viz; update inspector badge
ask                      → open plan preview; send request downstream
generate.page.request    → (no UI) spinner on Ask box
generate.page.done       → insert branch card; bead in Vault; animate edge
index.update             → update tooltips/motifs; enable anchors overlay
vault.save               → solidify node (◆), pin in timeline, add label
snapshot                 → (no UI) replay cursor checkpoint
```

---

## Screen Structure (Components Map)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Sidebar: Symbols/Filters  │ Reader Panel            │ Inspector / Graph Mini │
│ ├─ SymbolGrid             │ ├─ PageHeader           │ ├─ EdgesList           │
│ ├─ OrientationDial        │ ├─ PageBody             │ ├─ Anchors/Motifs      │
│ └─ Filters/Search         │ ├─ AskBox               │ └─ Actions             │
│                           │ └─ BranchCards (stack)  │                         │
│ ───────────────────────────────────────────────────────────────────────────  │
│ Vault Timeline (bottom): Session beads/labels (scrollable mini‑map)          │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Optional Overlays (debug/toggles)

- **Policy HUD:** show return‑debt, TTL, open branches per section.
    
- **Anchors heatmap:** underline unresolved anchors in Reader.
    
- **Latency bars:** UI→Kafka→DSPy→done timings on each page card.
    
- **Color keys:** 16 chips (characters), provenance patterns.
    

---

## Minimal Keyboard / Click Map

- `g` = Graph view, `h` = Holographic 3D, `r` = Reader, `v` = Vault focus.
    
- `1..16` = jump to character; `x/y/a/z` = set orientation.
    
- `s` = Save to Vault; `space` = Replay toggle.
    

---

## Where this plugs into code tonight

- **Producer endpoints:** `POST /event/ui/symbol`, `POST /event/ask`.
    
- **Consumer:** PageGenerator → produce `generate.page.done`.
    
- **Reader:** `/api/v1/page/{page_id}` hydrates Inspector + Graph tooltips.
    
- **Vault:** `/api/v1/vault/save` (append; idempotent on `event_id`).
    

---

## Notes for future polish

- Session color blending on nodes; depth-of-field in 3D.
    
- Bead size = novelty; filament thickness = coherence.
    
- Cross‑session supergraph: toggle to see _everyone’s_ coral reef.