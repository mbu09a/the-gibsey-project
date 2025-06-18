# Gibsey MCP + Vault — Sprint Roadmap

*Baseline estimate: 36 days · Story‑points ≈ ½‑day each*

---

## 0 · Discovery  (3 days – 3 SP)

| Goal                                              | Exit Criteria                                                                                  |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Map current code paths; set up Storybook baseline | • `architecture.md` merged in `main`<br>• Storybook shows `<ReaderPane>` & `<TableOfContents>` |

---

## 0.5 · Proof of Concept  (5 days – 13 SP)

| Objective                                  | Key Tasks                                                                                    | Done‑When                                                                       |
| ------------------------------------------ | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Wire one character (London Fox) end‑to‑end | • `/api/mcp/london` route<br>• Skeleton `<MCPChatDrawer>`<br>• Manual “Save to Vault” button | • London Fox streams reply within 2 s<br>• Reader can save entry and see DB row |

---

## 0.9 · Alpha  (10 days – 21 SP)

| Objective                              | Key Tasks                                                                                                                            | Exit Gate                                                                                          |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| Full MCP set, auto‑save, Vault listing | • Seed 16 `characters` rows<br>• React Context for `activeCharacter` & theme<br>• `vault` table migration<br>• `/api/vault` GET/POST | • Chat for any character streams & auto‑saves<br>• `/vault/:character` modal lists last 20 entries |

---

## 1.0 · Beta  (10 days – 20 SP)

| Objective                                | Key Tasks                                                                                                             | Exit Gate                                                                                  |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Semantic Vault search + adaptive theming | • Add `embedding` column & pgvector FT<br>• Endpoint `/api/vault/search`<br>• Theme colors propagate to chat & header | • Search returns ranked matches ≤ 500 ms<br>• Drawer & page header match character palette |

---

## 1.1 · Launch  (8 days – 13 SP)

| Objective                                  | Key Tasks                                                                                | Exit Gate                                                   |
| ------------------------------------------ | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Harden for public release                  | • Supabase / Clerk auth<br>• `ratelimit` Bun middleware<br>• Shareable Vault snippet URL | • Anonymous read; login to chat<br>• Abuse‑safe rate limits |
| • `/vault/:id` link renders public snippet |                                                                                          |                                                             |

---

### Story‑Point Key

*1 SP ≈ 4 hrs effective engineering time.*

---

## Alpha Ticket Breakdown (sample)

| ID  | Title                   | Description                               | Acceptance              | SP |
| --- | ----------------------- | ----------------------------------------- | ----------------------- | -- |
| A‑1 | Characters seed         | Populate 16‑row MCPConfig                 | `drizzle seed` succeeds | 2  |
| A‑2 | ActiveCharacter context | Provide id, color, symbol to app          | Unit test passes        | 3  |
| A‑3 | `<MCPChatDrawer>` UI    | Right‑side drawer, md‑render, auto‑scroll | Cypress e2e passes      | 5  |
| A‑4 | `/api/mcp/[id]`         | Stream GPT‑3.5 completions                | SSE returns 200 ≤ 2 s   | 5  |
| A‑5 | Vault migration         | Create table, embed col                   | Migration idempotent    | 2  |
| A‑6 | Auto‑save bot replies   | POST to Vault after stream                | Row visible in DB       | 2  |
| A‑7 | Vault list modal        | Paginated list per char                   | Shows 20 entries        | 2  |

*Complete ticket list lives in `/docs/SPRINT_PLAN.md`.*

---

## Risk & Mitigation Quick‑Notes

1. **LLM cost blow‑up** — add cheap‑model fallback flag.
2. **SSE limits on Vercel Edge** — plan Fly.io backup.
3. **Schema creep** — freeze DB after Beta unless major bug.

---

**End of document**