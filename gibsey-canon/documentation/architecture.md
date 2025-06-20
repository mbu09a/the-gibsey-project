# The Gibsey Project – MCP & Vault Architecture

*Last updated:  04 Jun 2025*

---

## 1 · Current MVP Snapshot

| Layer         | Stack / Tooling                    | Purpose & Notes                                                                                                             |
| ------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Front‑end** | React 18 + Vite                    | Single‑page reader at `/`                                                                                                   |
| **State**     | `useState` / `useReducer`          | Tracks current page, corpus metadata, keyboard nav                                                                          |
| **Styling**   | Tailwind CSS + custom neon palette | Key selectors:<br>  • `.toc‑panel` – left sidebar<br>  • `.reader‑pane` – page viewport<br>  • `.corpus‑header` – title bar |
| **Runtime**   | Bun (edge server)                  | Serves static build; hosts Hono API                                                                                         |
| **API**       | Hono (Bun) under `/api/*`          | Currently exposes `GET /api/page?id=`                                                                                       |
| **Database**  | Drizzle ⇢ SQLite (file)            | Tables: `pages`, `corpus`, `characters`                                                                                     |

### Component Tree (ASCII)

```
<App>
  └─ <Layout>
       ├─ <CorpusHeader/>
       ├─ <TableOfContents/>   ← keyboard navigation
       └─ <ReaderPane/>        ← page text + nav buttons
```

---

## 2 · Planned Extensions

### 2.1 MCP (Minor Character Protocol) Layer

| Aspect                                             | Spec                                                                       |
| -------------------------------------------------- | -------------------------------------------------------------------------- |
| **Endpoint**                                       | `GET /api/mcp/:id` · Streams LLM completions (SSE)                         |
| **Context**                                        | (1) Current page text · (2) Last *N* Vault snippets for that `characterId` |
| **Config**                                         | \`\`\`ts                                                                   |
| interface MCPConfig {                              |                                                                            |
| id: number;                                        |                                                                            |
| name: string;                                      |                                                                            |
| color: string;        // Tailwind or HEX           |                                                                            |
| symbolSVG: string;    // inlined asset             |                                                                            |
| embedNamespace: string; // vector DB bucket        |                                                                            |
| systemPrompt: string; // seed prompt per character |                                                                            |
| }                                                  |                                                                            |

```|

### 2.2 UI / UX Injection
```

<Layout>
  ├─ …
  └─ <MCPChatDrawer/>  ← right‑side slide‑over or modal
```
*Drawer inherits `color` & `symbolSVG` from **React Context**: `ActiveCharacterContext`.*
*Features: markdown rendering, auto‑scroll, 2 msgs/10 s spam guard.*

### 2.3 Gibsey Vault

```ts
// drizzle schema
export const vault = table("vault", {
  id          : serial("id").primaryKey(),
  characterId : integer("char_id").references(() => characters.id),
  authorType  : text("author").checkIn(["reader", "bot"]),
  content     : text("content"),
  createdAt   : timestamp("created_at").defaultNow(),
  embedding   : text("embedding")  // reserved for pgvector / FTS5
});
```

*REST surface*

* `POST /api/vault` – persist entry
* `GET  /api/vault?character=…&page=…` – paginated history

### 2.4 Data‑Flow Diagram

```
Reader ─▶ MCPChatDrawer ──POST──▶ /api/mcp/:id
  ▲                                  │
  │                                  ▼
  │                      LLM stream (SSE)
  │                                  │
  │   auto‑save bot replies          ▼
  └─────────────POST /api/vault◀─────●
```

---

## 3 · Character Registry (excerpt)

| #                                                          | ID               | Display Name                | Palette   | Symbol       |
| ---------------------------------------------------------- | ---------------- | --------------------------- | --------- | ------------ |
| 1                                                          | `an‑author‑open` | An Author’s Preface         | `#00FF88` | `author.svg` |
| 2                                                          | `london‑fox`     | London Fox                  | `#FF0044` | `fox.svg`    |
| 3                                                          | `glyph‑narrow‑1` | An Unexpected Disappearance | `#00D4FF` | `glyph.svg`  |
| …                                                          | …                | …                           | …         | …            |
| 16                                                         | `author‑close`   | The Author’s Preface (End)  | `#00FF88` | `author.svg` |
| *Full 16‑item list lives in `/config/mcp.ts` seed script.* |                  |                             |           |              |

---

## 4 · Branching & CI Guardrails

1. **Feature branch** – all work in `feature/mcp‑vault`.
2. **Migrations** – destructive ops gated behind `--confirm` prompt.
3. **CI** – Bun tests · ESLint · Drizzle migration lint.
4. **PR Checks** – Cypress e2e passes; Lighthouse accessibility ≥ 85.

---

## 5 · Milestone Roadmap (snapshot)

| Phase      | Goal                                     | Key Exit Criteria                         |
| ---------- | ---------------------------------------- | ----------------------------------------- |
| 0.5 POC    | One MCP (London Fox) + manual Vault save | `/api/mcp/london` streams; drawer renders |
| 0.9 Alpha  | 16 MCPs, auto‑save, Vault list view      | Drizzle `vault` table live; list modal    |
| 1.0 Beta   | Vector search + adaptive theming         | Embeddings stored; semantic `GET` query   |
| 1.1 Launch | Auth, rate‑limit, shareable snippets     | Supabase/Clerk login; rate limiter        |

*Story‑points and ticket breakdown live in `SPRINT_PLAN.md`.*

---

## 6 · Open Questions

1. LLM provider & spend ceiling
2. Canon vs. reader‑authored pages policy
3. Vector store tech (SQLite FTS vs pgvector)
4. Moderation & rate‑limit rules

---

**End of document**