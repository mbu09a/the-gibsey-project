# The Gibsey Project

*A CRT‑terminal‑style reader for **The Wonderful Worlds of Gibsey***

This app recreates the glow, scan‑lines, and keyboard feel of a late‑80s green‑phosphor monitor while letting you page through a sprawling, 16‑symbol corpus one scene at a time. Every chapter ("symbol") owns its own colour theme, SVG glyph, and JSON file, so you can expand or tweak the book piecemeal without ever touching the code.

---

## 🎨 Core Features

| Area                    | Highlights                                                                                                                                                             |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Retro CRT Aesthetic** | • Phosphor‑green text & bloom<br>• Subtle curvature + scan‑lines<br>• Bitmap font **VT323** (self‑hosted)                                                              |
| **Reader Navigation**   | • One page on screen at all times<br>• ← / → keys or on‑screen arrows<br>• Click any symbol in the vertical index to jump chapters                                     |
| **Symbol System**       | • 16 SVG glyphs, one per chapter<br>• Automatic theme swap (text + borders) via `colors.ts`                                                                            |
| **Incremental Loading** | • One JSON file *per story* in `src/stories/`<br>• Hot‑reload when you drop a new file<br>• Perfect for proofreading before flooding the reader with hundreds of pages |

---

## 📁 Project Layout

```
the-gibsey-project/
├── public/
│   ├── corpus-symbols/       # 16 SVGs (exact file‑names don't matter)
│   ├── fonts/                # VT323.ttf (loaded locally)
│   └── index.html            # Vite entry stub
├── src/
│   ├── assets/
│   │   └── colors.ts         # Symbol → colour map (single source of truth)
│   ├── stories/              # One `<slug>.json` per chapter
│   │   └── an-authors-preface.json
│   ├── components/
│   │   ├── CRTFrame.tsx      # Outer glow, curvature & scan‑lines
│   │   ├── PageViewer.tsx    # Renders paragraphs for the active page
│   │   ├── SymbolIndex.tsx   # Clickable vertical TOC
│   │   └── SymbolTag.tsx     # Shows current glyph + title
│   ├── context/
│   │   └── StoryContext.tsx  # Global state (active story, page, theme)
│   ├── styles/
│   │   ├── globals.css       # Tailwind base + custom CRT effects
│   │   └── typography.css    # Optional prose tweaks
│   ├── pages/
│   │   └── index.tsx         # App shell (if using Next) *or* main.tsx (Vite)
│   ├── types/
│   │   └── story.ts          # `Story` & `StoryPage` interfaces
│   └── utils/
│       └── storyLoader.ts    # Helper to merge all JSON files at build time
├── tailwind.config.ts
├── tsconfig.json
├── package.json              # Bun/NPM scripts live here
└── README.md (you are here)
```

---

## 🧾 Story JSON Schema

```ts
interface StoryPage {
  page: number;              // 1‑based index within the story
  paragraphs: string[];      // Each <p> rendered with spacing & indent
}

interface Story {
  storyId: string;           // slug‑safe identifier (folder‑friendly)
  title: string;             // Display title
  symbolId: string;          // Links to SVG + colour
  color?: string;            // Optional override; falls back to colors.ts
  order: number;             // 1‑16 in the master cycle
  pages: StoryPage[];
}
```

> **Tip:** Start with a single story file, load the app, fix spacing, commit. Repeat. You’ll spot formatting glitches while they’re still trivial.

---

## 🚀 Quick Start

### 1. Prerequisites

* Node ≥ 18
* **Bun** (optional) – ultra‑fast dev scripts (`bun install`, `bun run dev`)

### 2. Install deps

```bash
bun install         # or: npm install / pnpm install / yarn
```

### 3. Run dev server

```bash
bun run dev         # or: npm run dev
```

Visit [http://localhost:5173](http://localhost:5173) and bask in the green glow.

### 4. Add content

* Drop SVGs into **/public/corpus‑symbols**
* Drop your first story JSON into **/src/stories/**
* Tailwind hot‑reload will pick up colours & pages automatically

### 5. Build for prod

```bash
bun run build       # or: npm run build
```

---

## 🎮 Controls

* **← / →**   Previous / next page
* **Click glyph**   Jump to that chapter’s opening page
* **ESC**   (Planned) Quit to symbol index only

---

## 🛠 Tech Stack

* **React + Vite**
* **TypeScript**
* **TailwindCSS** (JIT mode)
* **Bun** scripts by default – switch to your favourite package manager if you like

---

## 📍 Roadmap

| Status | Feature                                   |
| ------ | ----------------------------------------- |
| ✅      | Per‑story JSON hot‑loading                |
| ⬜      | In‑app search (fuzzy)                     |
| ⬜      | Symbol hover tooltips (character bios)    |
| ⬜      | Optional dark amber CRT palette           |
| ⬜      | Static export to Netlify/Cloudflare Pages |

---

## 📝 Licence

© 2025 The Malt Gibsey Company. All rights reserved.

This repo contains **parody** references and original fiction; see `LICENSE` for distribution terms.