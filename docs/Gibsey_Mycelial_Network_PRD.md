# Gibsey Mycelial Network: Product Requirements Document (PRD, Revised)

---

## 1. Project Overview

**Name:**
Gibsey Mycelial Network (“The Cluster That Dreams”)

**Summary:**
A first-of-its-kind, AI-powered, *vector-driven*, event-native narrative OS:

* **Every page, prompt, and user action is embedded, indexed, and searched semantically** via Cassandra and Stargate—*this is the living memory of the park*.
* **Every narrative event—page written, prompt selected, character response, motif migration—is an event in the system**, handled by a true event streaming backbone (Kafka).
* **All AI/LLM/agent responses are streamed token-by-token to the UI**, supporting “fake streaming” for fallback.
* **User and agent co-authorship is woven into a persistent, branching, hypertextual book**, navigable by meaning, motif, and symbol.

---

## 2. Tech Stack

**Frontend:**

* React 18, TypeScript, TailwindCSS, Next.js or Vite
* WebGL/Three.js (3D/graph visualization of Vault + Cluster)

**Backend/API:**

* FastAPI (Python) or Node.js (Express/Fastify) for API
* WebSockets/SSE for real-time streaming chat and updates
* Stargate (REST/GraphQL API for Cassandra)
* Kafka for all narrative/user/agent events

**AI/Agents:**

* Ollama (local LLMs), OpenAI/Claude API (cloud, fallback), vLLM (optional)
* DSPy (for agent orchestration, prompt pipelines, and context building)
* Sentence Transformers/SBERT or OpenAI embeddings (for vectorization of all content)
* RAG (Retrieval-Augmented Generation) pipeline for all agent responses

**Database:**

* **Cassandra (required, not optional!)**
* Stargate for REST/GraphQL
* Redis for session and cache

**Storage:**

* S3/Blob/local for media, cluster state, full text, versioned Vault exports

**Event Backbone:**

* **Kafka** (event streaming for page/prompt/user/agent/cluster events)

**Monitoring/Visualization:**

* Grafana, Prometheus, custom WebGL 3D UI

**Other:**

* n8n (optional: for automation/scheduled events/admin pipelines)
* Kubernetes (K8s) + Docker (required): everything runs as pods/services, scalable, resilient

---

## 3. User Flow (Vector-Driven)

1. **Onboarding:**

   * User logs in (Supabase/auth required for session history, permissions, author tracking).
   * UI fetches current Vault grid, user’s journey, available prompts.

2. **Page Rendering & Vault Navigation:**

   * Every **StoryPage** is fetched from Cassandra, with its text, metadata, symbol, rotation, vector, and canonical history.
   * Vault grid/tree shows both linear and branching paths—**color, symbol, and orientation are driven by metadata and vector context**.
   * All page and prompt lookups are **vector searches** for “nearest neighbors” (semantic recall).

3. **Prompt/Branching:**

   * Each page displays 3 (or more) prompts, each generated via a mix of (a) hardcoded options, (b) context-aware vector search (find the most semantically relevant next question or character), and (c) motif or user-initiated “search for next.”
   * User clicks a prompt—**this is published as a Kafka event**, triggering new page generation.

4. **AI/Character Generation (RAG-Driven, Streaming):**

   * When a new page or response is needed, the backend:

     1. **Builds a semantic context window:** (current page + vector neighbors + user history + relevant motifs)
     2. **Streams the prompt to the LLM (Ollama/OpenAI/Claude) with `"stream": true`**
     3. **UI receives tokens via WebSocket/SSE**, displays real-time.
     4. Once finished, result is embedded, stored as a new page in Cassandra, added to the Vault, and indexed.

5. **User Authorship & Interruption:**

   * Users can write their own page/fragments at any eligible node.
   * **User-generated content is embedded, indexed, and becomes canon or non-canon based on Vault rules** (limits per session, author permissions, etc.)

6. **Motif/Multi-Modal Navigation:**

   * User can “jump” via motifs/symbols (e.g. all “balcony” moments, or all Jacklyn-90° responses), using vector search or motif queries.
   * Motifs and recurring phrases/symbols are embedded and indexed for navigation and story logic.

7. **Cluster Visualization & Infra as Narrative:**

   * Cluster events (K8s pod scaling, failures, healing) are sent as Kafka events, visualized as part of the story (e.g., “Jacklyn-Variance’s consciousness flickered and revived...”)
   * Real-time Grafana/3D WebGL cluster view for meta-demo.

---

## 4. Core Features (AI/Vector/Event-Driven)

### A. **Semantic Memory & RAG Backbone**

* Every page, prompt, motif, user query, and AI response is embedded (vectorized).
* Cassandra stores both raw and embedded data; Stargate exposes fast search.
* **All navigation, prompt generation, and agent responses leverage vector search for context and recall.**

### B. **Event-Driven Narrative Logic**

* **Every action is an event in Kafka:**

  * New page, prompt selection, user/AI authorship, motif appearance, Vault update, cluster change.
* Agents (LLMs), Vault, UI, and cluster services are all event-driven and subscribe to relevant topics.

### C. **Streaming, Interruptible AI Responses**

* All LLM responses are streamed to UI token-by-token (true streaming or “fake streaming” fallback).
* User or agent can “interrupt,” “inject,” or “co-author” in real time (extendable for future collaborative demos).

### D. **Persistent, Versioned Vault & Story State**

* **Full versioned history of every page, prompt, and branch, with vector index, canonical/non-canonical tags, and author attribution.**
* Users can replay, fork, or “time travel” anywhere in the Vault.
* Every node (page, prompt, motif, author, agent) is a first-class object in Cassandra.

### E. **Motif, Symbol, and Multi-Modal Search**

* User and agents can search or navigate by motif, symbol, color, or semantic content—Vault is *not* just a tree, but a hypergraph.
* Special tokens and motif embeddings make non-text navigation possible.

### F. **User Auth, Security, and Limits**

* Full user authentication (Supabase or equivalent), session management, author attribution.
* Rate limits, write limits, and “non-canon chat” fallback to avoid spam or overload.

### G. **Cluster-Narrative Integration**

* All infra events (K8s, scaling, failures) are routed as Kafka events and narrativized into story updates.
* Cluster health, capacity, and operator interventions become “meta-plot” events.

### H. **Monitoring, Analytics, and Moderation**

* Grafana/Prometheus for infra, plus real-time dashboards for narrative analytics:

  * Prompt success rates, vector recall accuracy, LLM streaming performance, author engagement.

### I. **Automation, Orchestration, & Cron**

* n8n (optional) for scheduled events, admin tools, or motif propagation.
* Cluster/agent orchestration for multi-character “events” and interventions.

---

## 5. Backend Schema (Expanded for AI/Vector/Event)

### **StoryPage**

* id: string
* symbolId: string
* rotation: 0 | 90 | 180 | 270
* pageType: 'primary' | 'prompt' | 'user\_query' | 'ai\_response'
* parentId?: string
* promptType?: 'character\_prompt' | 'user\_prompt' | 'character\_response'
* text: string
* author: string ('user', 'AI', etc.)
* branchId?: string
* createdAt: datetime
* embedding: vector\[768+]  <!-- Required, always indexed -->
* canonical: bool
* version: string

### **PromptOption**

* id: string
* text: string
* rotation: 90 | 180 | 270
* targetSymbolId: string
* promptType: 'character\_prompt' | 'user\_prompt' | 'character\_response'
* embedding: vector\[768+]

### **Motif**

* id: string
* text: string
* embedding: vector\[768+]
* color: string
* symbol: string
* occurrences: \[StoryPage ids]

### **Branch**

* id: string
* rootPageId: string
* pages: StoryPage\[]
* userId: string

### **ClusterEvent**

* id: string
* eventType: string
* metadata: object
* relatedPageId?: string
* timestamp: datetime

### **User**

* id: string
* username: string
* history: \[StoryPage ids]
* authoredPages: \[StoryPage ids]
* sessionId: string
* permissions: object

---

## 6. Security Guidelines

* All user and AI content must be embedded, versioned, and auditable.
* All vector and event data must be secured, not just relational data.
* All streaming endpoints are authenticated and rate-limited.

---

## 7. Regulations & Compliance

* **GDPR/CCPA:**

  * If storing user data, provide clear privacy policy, user data export, and deletion mechanisms.
* **Open Source Licensing:**

  * All code, models, and narrative data must be properly licensed; use MIT, Apache 2.0, or custom license for narrative artifacts.
* **Accessibility:**

  * UI/UX should follow basic a11y standards (keyboard navigation, alt-text, color contrast).

---

## 8. Launch Plan & Demo

**Goal:**

* Minimal but real demo includes:

  * Linear and nonlinear Vault navigation (via vector/semantic recall)
  * Prompt selection and symbol rotation, with vector/context-aware branching
  * AI/user chat with *streaming LLM* (real or fake)
  * Real event streaming for Vault and cluster updates
  * Cluster visualization, with narrative-infra sync (pods/services light up as story progresses)
  * Analytics dashboard for core narrative/AI metrics

**Next Steps:**

* Implement vector embedding pipeline (Ollama/OpenAI/SBERT) for all objects
* Connect Cassandra + Stargate for persistent, indexed storage and search
* Plug Kafka into every narrative, prompt, and user/AI event
* Deploy streaming LLM backend and integrate with UI via WebSockets/SSE
* Extend UI for real-time Vault, motif, and graph navigation
* Instrument cluster for live narrative-infra sync
* **Push all code and docs to repo for transparent, versioned development**

---

**This is now a true product/technical spec for a generative, event-native, semantic memory-powered, scalable narrative OS—Gibsey as an AI park and literary engine.**