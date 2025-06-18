# **Mycelial Narrative Relay (MNR)**

A **subterranean data‑fungus** that diffuses meaning between distant story shards by modeling each shard as a nutrient node, transferring semantic “spores” across an evolving mycelial network.

---

## **1. Graph‑Schema**

### **1.1 Nutrient Nodes (Narrative Shards)**

* **Definition**: Each shard of text (or corpus snippet) is represented as a *node* containing “nutritional” value (semantic depth, community relevance, or creative potential).
* **Attributes**:

  * **Semantic Vector** (embedding)
  * **Narrative Themes** (tags: e.g., fantasy, sci‑fi, poetry)
  * **Nutrient Capacity** (score of how many “spores” it can host)
  * **State** (fresh, partially decayed, archived)

### **1.2 Weighted Edges (Mycelial Strands)**

* **Spores as Agents**: Edges carry “spores,” i.e., units of meaning or potential transformation that move between shards.
* **Connection Weight**: Reflects the **semantic similarity** between nodes, plus **reader interaction** metrics (frequent cross‑reading or referencing = stronger path).
* **Capacity & Flow**: Each edge has a maximum spore throughput, preventing “overloading” any single path.

### **1.3 Example Schema**

```yaml
nodes: [
  {
    id: "shard_1",
    themes: ["myth", "fungal"],
    semanticVector: [0.12, 0.88, ...],
    nutrientCapacity: 10,
    state: "fresh"
  },
  {
    id: "shard_2",
    themes: ["sci-fi", "hive-mind"],
    semanticVector: [0.95, 0.22, ...],
    nutrientCapacity: 8,
    state: "fresh"
  },
  ...
]

edges: [
  {
    source: "shard_1",
    target: "shard_2",
    weight: 0.7,      // measure of similarity + user interest
    capacity: 5       // max spores in transit at once
  },
  ...
]
```

---

## **2. Diffusion Algorithm**

To mimic fungal nutrient flow, the MNR uses a **hybrid of Fickian Diffusion** and **Preferential Attachment**:

1. **Fickian Flow**

   * Spores move along a gradient from higher concentration (crowded shards) to lower concentration (underfed shards).
   * Each time step, we calculate $\Delta c = D \times (\nabla^2 c)$, where:

     * $c$ = spore concentration at a node.
     * $D$ = diffusion coefficient (tuned by environmental factors like “reader interest”).

2. **Preferential Attachment**

   * Nodes with **high user engagement** or “story potential” attract more spores.
   * If node $n$ has popularity $p_n$, the probability of an incoming spore binding to $n$ is proportional to $p_n / \sum{p_k}$.
   * This ensures that popular shards become nutrient‑dense hubs but also risk oversaturation unless they’re well connected.

3. **Rebalancing via Reader Activity**

   * **Reader Impressions**: Each user read or comment increases local spore production in that shard.
   * If a shard’s spore count exceeds its nutrient capacity, spores automatically “diffuse out” to neighbors or decay, reflecting an organic limit.

---

## **3. Visualization Spec (D3 + WebGL)**

### **3.1 Overview**

A multi‑layer interactive interface:

1. **Macro View**: D3.js graph of nodes and edges. Nodes pulse or change color based on spore load. Edges thicken/thin with spore traffic.
2. **Micro View**: WebGL shader simulating “fungal filaments” crossing the edges. Spores appear as tiny glowing particles moving from node to node.

### **3.2 Real‑Time Growth & Decay**

* **Growth**: When a shard’s engagement triggers new connections, filaments visually branch out or intensify between nodes.
* **Decay**: Underused shards fade in color, edges become brittle or break. Spores draining out is shown as dimming along filaments.

### **3.3 User Interactions**

* **Hover for Data**: Hovering over a node reveals its narrative excerpt, user engagement stats, and current spore count.
* **Click to Expand**: Clicking a node transitions to a “shard detail” WebGL scene showing local fungal sub-structures.
* **Auto‑Recenter**: Force‑direct or manual layout options allow users to rearrange the network for clarity.

---

## **4. Governance Mechanic**

### **4.1 Custodianship with Magical Bonds (MB)**

* **Stake to Cultivate**: Community members lock up MB tokens to become “Mycelial Custodians” of specific regions (clusters of shards).
* **Maintenance Tasks**: Custodians prune stale edges, guide new connections, and ensure a healthy balance of spore diffusion.
* **Reward Mechanism**: Active custodians are periodically rewarded with additional MB for maintaining robust narrative health (e.g., high synergy, minimal spam).

### **4.2 TNAs for Cross‑Pollination Research**

* **Project Funding**: Larger, cross‑shard collaborations (e.g., bridging far-flung topics or languages) require **TNA** proposals.
* **Voting & Execution**: If a TNA-funded research quest is approved, participants gather data on new or underexplored shards, introducing fresh content or linking them.
* **Outcome Sharing**: When a cross‑pollination quest succeeds (proved by increased synergy or stable mycelial expansions), TNA dividends are distributed among participants.

---

## **5. Security & Resiliency**

### **5.1 “Blight” Attacks**

* **Malicious Content**: Attempted injection of harmful or misleading shards that disrupt the semantic ecosystem.
* **Spore Overload**: Attackers might flood popular nodes with junk connections, causing chaos in the network.

### **5.2 Decentralized Moderation Myco‑Agents**

* **Automated Detection**: Myco‑agents are scripts (or AI subroutines) that continuously scan for suspicious content or abnormally rapid spore multiplication.
* **Quarantine Zones**: Potentially infected shards get flagged, and spore flow is restricted until a human or community review occurs.
* **On-Chain Arbitration**: If a node is deemed malicious after review, its edges are severed or taxed. MB stakers can reclaim partial stake if they participated in early detection or remedial action.

### **5.3 Resiliency Strategies**

* **Redundant Pathways**: If one “super node” or cluster becomes compromised, spores can re‑route around it thanks to alternative connections.
* **Gradual Decay**: Unattended or suspicious shards gradually lose capacity, preventing indefinite accumulation of harmful content or unstoppable growth.

---

## **Conclusion**

The **Mycelial Narrative Relay (MNR)** envisions a dynamic, fungal‑like ecosystem for collaborative storytelling.

1. **Graph‑Schema**: Each shard is a nutrient node, with spores traveling weighted edges driven by semantic similarity and user interactions.
2. **Diffusion Algorithm**: Combines **Fickian** gradient flow with **preferential attachment**, ensuring that popular or thematically rich shards flourish while outliers still receive slow, life‑sustaining trickles.
3. **Visualization**: D3.js plus WebGL filaments offer an immersive view of real‑time growth, linking the textual realm to an organic, subterranean aesthetic.
4. **Governance**: Magical Bonds empower custodians to steward healthy clusters, while TNAs fund bridging initiatives across distant story terrains.
5. **Security**: Decentralized moderation myco‑agents guard against “blight” and preserve ecosystem integrity, ensuring the MNR remains a fertile ground for creative meaning‑making.