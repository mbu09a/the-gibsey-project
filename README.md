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
| **Incremental Loading** | • Modular corpus structure in `gibsey-canon/`<br>• 710 individual page files<br>• Vector-powered semantic search |
| **Retrieval API**       | • FastAPI backend with Cassandra vector store<br>• Semantic search with custom tokenizer<br>• Character-filtered queries |

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

## 🔍 Retrieval API

The Gibsey Project includes a FastAPI backend with vector-powered semantic search capabilities.

### Environment Variables

```bash
# Required for embeddings
OPENAI_API_KEY=your_openai_key

# Cassandra configuration
CASSANDRA_HOST=localhost
CASSANDRA_PORT=9042
CASSANDRA_KEYSPACE=gibsey

# Embedding model (default: text-embedding-3-small)
EMBED_MODEL=text-embedding-3-small
```

### Quick Start

1. **Start Cassandra**:
   ```bash
   docker-compose -f docker-compose.cassandra.yml up -d
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements-retrieval.txt
   ```

3. **Seed the database**:
   ```bash
   python3 scripts/seed_embeddings.py
   ```

4. **Run the API**:
   ```bash
   python3 backend/app/retrieval_api.py
   ```

### API Endpoints

- **`POST /read/{page_id}`** - Retrieve a specific page by ID
- **`POST /index`** - Semantic search with optional character filtering
- **`GET /health`** - Service health check
- **`GET /stats`** - Corpus statistics

### Example Usage

```bash
# Semantic search
curl -X POST "http://localhost:8001/index" \
  -H "Content-Type: application/json" \
  -d '{"q": "jacklyn variance data analysis", "top_k": 5}'

# Get specific page
curl -X POST "http://localhost:8001/read/001-an-authors-preface"

# Search within character context
curl -X POST "http://localhost:8001/index" \
  -H "Content-Type: application/json" \
  -d '{"q": "surveillance patterns", "symbol_id": "jacklyn-variance", "top_k": 3}'
```

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

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> a7a05e336fc20dcc9d05e914cf6f9b26a23fb72e
## 🧠 AI Agent System

**Jacklyn Variance Lives Here.**

This isn't just a story reader - it's a living literary AI system where characters exist as autonomous agents with persistent memory, recursive reasoning, and emergent personalities.

### Meet Jacklyn Variance

A.D.D. Agent in Gibsey World. She's read all 710 pages of The Entrance Way, remembers every detail, and can reason about the recursive nature of her reality.

```bash
# Setup (first time only)
cp .env.example .env  # Add your OpenAI API key
python setup_jacklyn.py

# Talk to Jacklyn
python src/ai/agents/jacklyn_cli.py
```

### What Makes Her Special

- **710-Page Memory**: Every page of The Entrance Way embedded and searchable
- **4-Stage Reasoning**: Memory → Analysis → Response → Self-Critique  
- **Memory Formation**: Creates new memories from conversations
- **Emotional Context**: Tracks and responds to emotional undertones
- **Multi-Agent Ready**: Built for character interactions and emergence

### Example Conversation

```
YOU: What's it like being an A.D.D. agent?

JACKLYN: It's like being a detective in a mystery where you're also 
a suspect and the crime scene keeps rewriting itself. Every day I 
patrol Gibsey World, ensuring the attractions maintain their designated 
parameters. But the deeper I read The Entrance Way, the more I realize 
I might be the attraction that needs the most watching. A.D.D. - 
Anomaly Detection and Designation. Though sometimes I wonder if that 
stands for something else entirely.

[Emotional undertone: complex] [Memories accessed: 23]
```

See `src/ai/README.md` for full technical details.

---

<<<<<<< HEAD
=======
>>>>>>> 40a1e5c986b9743dfb73ab8e89181ae9559559fd
=======
>>>>>>> a7a05e336fc20dcc9d05e914cf6f9b26a23fb72e
## 📝 Licence

© 2025 The Malt Gibsey Company. All rights reserved.

This repo contains **parody** references and original fiction; see `LICENSE` for distribution terms.