# Open Questions for Brennan / Stakeholders

1. **LLM Provider & Budget**  
   * OpenAI GPT‑4o vs Anthropic Haiku? 16 simultaneous MCP streams could be costly.

2. **Auth Scope**  
   * Is anonymous session OK for Alpha, or do we require user accounts before launch?

3. **Vector Store**  
   * Stick with Drizzle + SQLite FTS5, or integrate pgvector / Supabase?

4. **Rate Limiting Rules**  
   * Per‑IP? Per‑user? Hard caps per day?

5. **Narrative Canon vs Reader Edits**  
   * Should reader‑authored pages ever overwrite canonical text, or live only in Vault?

6. **Content Moderation**  
   * Do we need an abuse filter for reader input before saving to Vault / sending to LLM?

7. **Deployment**  
   * Keep on Vercel edge functions (Hono) or move to Bun‑server on Fly.io for SSE stability?

8. **Accessibility**  
   * Any WCAG targets for neon color palette?

9. **Legal**  
   * GDPR/CCPA data retention for Vault entries (they may contain user‑generated content).

10. **Offline / Export**  
    * Requirement for exporting a user’s entire Vault as Markdown/JSON?