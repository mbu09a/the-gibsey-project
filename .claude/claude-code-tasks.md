# Claude Code Task List – Gibsey MCP Layer & Vault

> **Purpose** – Feed this checklist to Claude Code so it can open the repo, create the necessary branches/files, and begin shipping the MCP + Vault feature set. Each task is phrased as an actionable commit or PR.

---

## 0. Bootstrap Docs (Day 0)

1. **Create feature branch**

   * `git checkout -b feature/mcp-vault-docs`

2. **Add documentation files**

   ```bash
   mkdir -p docs
   printf "%s" "$ARCH_MD" > docs/architecture.md
   printf "%s" "$SPRINT_MD" > docs/SPRINT_PLAN.md
   printf "%s" "$QUESTIONS_MD" > docs/open-questions.md
   ```

   > Use the exact markdown blobs from Operator’s output.

3. **Push & open PR** – title: `docs: MCP & Vault architecture + sprint plan`.

---

## 1. Database & Seed (Day 1‑2)

4. **Drizzle migration – `vault` table**

   ```ts
   // migrations/20250604_add_vault.ts
   import { sql } from "drizzle-orm";
   export async function up(db) {
     await db.execute(sql`
       CREATE TABLE IF NOT EXISTS vault (
         id           INTEGER PRIMARY KEY AUTOINCREMENT,
         char_id      INTEGER NOT NULL REFERENCES characters(id),
         author       TEXT    NOT NULL CHECK(author IN ('reader','bot')),
         content      TEXT    NOT NULL,
         created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
       );
     `);
   }
   ```

5. **Add `embedding` column** *(future‑proofing for Beta)*

   * Type: `TEXT` (base64‑encoded float32 array) or use pgvector if we pivot.

6. **Seed 16‑row `characters` table**

   * Build `scripts/seed_characters.ts` importing the MCPConfig list (colors, symbols, etc.).

---

## 2. React Context & UI Shell (Day 3‑5)

7. **Create React Context** `ActiveCharacterContext` (id, name, color, symbolSVG).

8. **Skeleton `<MCPChatDrawer />` component**

   * Right‑side fixed drawer (Tailwind `w-96` on desktop, full‑height slide‑over on mobile).
   * Header shows `symbolSVG` + name, background `color`.
   * Body: placeholder message list.
   * Footer: `<textarea>` + “Send” button.

9. **Keyboard/Click hook** – clicking a Corpus symbol sets `activeCharacter`.

10. **Cypress test** – drawer opens & theme colors apply.

---

## 3. API Layer (Day 6‑8)

11. **`/api/mcp/[id]` Hono route**

    * Accept POST `{ message: string }`.
    * Build context prompt: page text + last 5 Vault snippets.
    * Stream GPT‑3.5 (temp 0.7) via OpenAI SSE; forward chunks.

12. **`/api/vault` routes**

    * `POST` → insert row (validate author field after basic profanity filter).
    * `GET` → pagination, `?character=` filter.

13. **Unit tests** – Bun test ensures inserts/query work.

---

## 4. Wire Up Front‑end (Day 9‑12)

14. **Hook `<MCPChatDrawer />` to `/api/mcp`**

    * Stream via `fetch`/`ReadableStream`.
    * On stream completion, auto‑POST bot reply to `/api/vault`.

15. **Manual Save Toggle** – reader messages have a "Save" checkbox; POST when checked.

16. **Vault Timeline Modal**

    * Route `/vault/:characterId` shows last 20 entries (lazy‑load older).

17. **E2E test** – send message, receive bot reply, both rows present in Vault.

---

## 5. Cleanup & PRs (Day 13‑14)

18. **ESLint / Prettier pass** – ensure no lint errors.

19. **Open final PR** – `feat: MCP chat + Vault` targeting `main`.

20. **Address open questions** – flag TODOs in code where decisions needed (LLM provider, rate limits, etc.).

---

## ENV / Secrets to Configure

* `OPENAI_API_KEY` (and optional `ANTHROPIC_API_KEY`).
* `DB_URL` – remains SQLite local for now.

---

> **DONE:** When all tasks green, tag release `v0.9-alpha`.