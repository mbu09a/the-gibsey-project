````markdown
# Mycelial Narrative Relay (MNR) Specification
**Role**: Principal Systems Mycologist of Gibsey  
**Objective**: Provide an implementation outline (DDL, algorithm pseudocode, example run, interfaces) for a Mycelial Narrative Relay system.

---

## 1. Graph DDL

Below is an example schema suitable for either:
- **PostgreSQL + pggraph** extension (property-graph style tables), or
- **Neo4j** (property-graph database).

**Node Label**: `:Shard`  
**Properties**:
- `id` (string or integer) — **primary key**  
- `title` (string)  
- `symbol_id` (string)  
- `word_count` (integer)  
- `nutrient_score` (float or decimal)

**Relationship**: `:SPORE`  
**Properties**:
- `semantic_spore_weight` (float) — the weight controlling nutrient diffusion  
- `emotional_valence` (float) — additional factor (e.g., positivity/negativity)

**Directed Graph**  
We assume relationships `:SPORE` go from one `:Shard` to another `:Shard` in a directed manner.

### 1.1. Neo4j Example

```cypher
// Create unique constraint on Shard id
CREATE CONSTRAINT FOR (s:Shard)
REQUIRE s.id IS UNIQUE;

// Example relationship creation:
CREATE (a:Shard { id: 'sh1', title: 'Root Shard', symbol_id: 'SYM-ROOT', word_count: 1200, nutrient_score: 0.5 })
CREATE (b:Shard { id: 'sh2', title: 'Branch Shard', symbol_id: 'SYM-BRANCH', word_count: 800, nutrient_score: 0.3 })
CREATE (a)-[:SPORE { semantic_spore_weight: 0.8, emotional_valence: 0.1 }]->(b);
````

### 1.2. PostgreSQL + pggraph Table Structure (Illustrative)

```sql
-- Table for Shards
CREATE TABLE shard (
    id               TEXT PRIMARY KEY,
    title            TEXT,
    symbol_id        TEXT,
    word_count       INT,
    nutrient_score   FLOAT
);

-- Table for Spore relationships
CREATE TABLE spore (
    source_id             TEXT REFERENCES shard(id),
    target_id             TEXT REFERENCES shard(id),
    semantic_spore_weight FLOAT,
    emotional_valence     FLOAT,
    PRIMARY KEY (source_id, target_id)
);
```

---

## 2. Diffusion Algorithm

We define a **k-step nutrient diffusion** procedure. The idea is that each shard’s `nutrient_score` can be updated based on inbound edges from other shards, using a *decay factor* and each edge’s `semantic_spore_weight`. Pseudocode is provided using Python-like syntax but remains language-agnostic.

### 2.1. Parameters

* **k**: number of diffusion steps
* **decay**: factor $0 < decay < 1$ controlling how quickly the influence diminishes per step
* **query\_shard\_id**: the starting shard from which to propagate or measure influence
* **N**: how many “top enriched” shards to return

### 2.2. Pseudocode

```python
def diffuse_nutrient_scores(graph, query_shard_id, k=2, decay=0.85, N=5):
    """
    graph: a structure that can return shards, edges, and adjacency 
           (e.g., { shard_id: { 'nutrient_score': float, 'outgoing': [(neighbor_id, edge_props), ...] } })
    query_shard_id: the shard from which we might measure relative diffusion
    k: number of diffusion iterations
    decay: factor controlling how much nutrient 'decays' each step
    N: how many top-enriched shards to return
    """
    # 1. Initialize an accumulator to track new nutrient contributions per shard
    new_scores = {sh_id: 0.0 for sh_id in graph.keys()}
    
    # 2. Optionally, you can reset or store original scores if needed
    original_scores = {sh_id: graph[sh_id]['nutrient_score'] for sh_id in graph.keys()}
    
    # 3. For each step in 1..k, propagate nutrient across edges
    for step in range(k):
        # Clear new scores each iteration (or use an array if you want to sum across steps differently)
        new_scores = {sh_id: 0.0 for sh_id in graph.keys()}
        
        for shard_id, shard_data in graph.items():
            current_score = shard_data['nutrient_score']
            outgoing_edges = shard_data['outgoing']  # list of (neighbor_id, edge_props)
            
            for (neighbor_id, edge_props) in outgoing_edges:
                w = edge_props['semantic_spore_weight']
                # Compute contribution from shard_id to neighbor
                contribution = current_score * w * decay
                # Accumulate in neighbor's new score
                new_scores[neighbor_id] += contribution
        
        # 4. After processing all shards, update nutrient_score with the new totals
        for sh_id in graph.keys():
            graph[sh_id]['nutrient_score'] = new_scores[sh_id]
    
    # 5. Sort shards by updated nutrient_score, descending
    sorted_shards = sorted(graph.keys(), key=lambda sid: graph[sid]['nutrient_score'], reverse=True)
    
    # 6. Return top-N
    top_n = sorted_shards[:N]
    return top_n
```

**Key Points**:

* We iterate `k` times.
* Each iteration, we compute the new score for each shard based on the sum of inbound contributions.
* A `decay` factor ensures diminishing returns after multiple hops.
* We return the IDs (or references) of the top-N shards with the greatest nutrient score after the diffusion steps.

> **Note**: This simple example resets each shard’s score per iteration. Alternatively, you could incorporate the *previous* score for each iteration or keep a fraction of it. Tuning the algorithm depends on the desired narrative effect.

---

## 3. Example Run (Toy Graph)

Let’s consider **5 shards**: `S1`, `S2`, `S3`, `S4`, `S5`. The adjacency is:

* `S1` -> `S2` (weight=0.5), `S1` -> `S3` (weight=0.2)
* `S2` -> `S4` (weight=0.7)
* `S3` -> `S4` (weight=0.4), `S3` -> `S5` (weight=0.6)
* `S4` -> (no outgoing edges)
* `S5` -> `S1` (weight=0.1)

Initial `nutrient_score` for all shards = 1.0 (for simplicity). Let `k=1`, `decay=0.85`.

**Iteration**:

1. **S1** has 1.0. It contributes:

   * to S2: `1.0 * 0.5 * 0.85 = 0.425`
   * to S3: `1.0 * 0.2 * 0.85 = 0.17`
2. **S2** has 1.0. It contributes:

   * to S4: `1.0 * 0.7 * 0.85 = 0.595`
3. **S3** has 1.0. It contributes:

   * to S4: `1.0 * 0.4 * 0.85 = 0.34`
   * to S5: `1.0 * 0.6 * 0.85 = 0.51`
4. **S4** has 1.0. (No outgoing edges → no contributions)
5. **S5** has 1.0. It contributes:

   * to S1: `1.0 * 0.1 * 0.85 = 0.085`

After this single iteration (`k=1`):

* **S1** new score = `0.085`
* **S2** new score = `0.425`
* **S3** new score = `0.17`
* **S4** new score = `0.595 + 0.34 = 0.935`
* **S5** new score = `0.51`

Sorted in descending order:

1. `S4` = 0.935
2. `S5` = 0.51
3. `S2` = 0.425
4. `S3` = 0.17
5. `S1` = 0.085

If `N=3`, the top-3 enriched shards are `[S4, S5, S2]`.

---

## 4. Interfaces

We assume a simple REST-based API to integrate with your existing **pro o1 bus** for message passing. The endpoints below illustrate possible routes.

### 4.1. POST `/mnr/diffuse`

* **Request Body** (JSON example):

  ```json
  {
    "query_shard_id": "S1",
    "k": 1,
    "decay": 0.85,
    "N": 3
  }
  ```
* **Response** (JSON example):

  ```json
  {
    "top_shards": ["S4", "S5", "S2"],
    "message": "Diffusion complete for query shard S1"
  }
  ```

### 4.2. GET `/mnr/top/:id`

* **Description**: Returns the top-N shards for the specified shard, possibly using default `k`, `decay`, and `N`.
* **Path Param**: `:id` — the query shard ID
* **Query Params**: `k`, `decay`, `N` (optional)
* **Response**: JSON with fields `top_shards` plus any additional metadata.

Example call:

```
GET /mnr/top/S1?k=1&decay=0.85&N=3
```

**Response**:

```json
{
  "top_shards": ["S4", "S5", "S2"],
  "used_params": {
    "k": 1,
    "decay": 0.85,
    "N": 3
  }
}
```

---

## 5. Unresolved

1. **Edge Storage**: Should we store both directions of edges or infer inbound adjacency dynamically?
2. **Multi-Tenancy**: If multiple “mycelia” co-exist, do we partition shards by graph or rely on labels?
3. **Performance**: For large graphs, might need distributed or iterative processing (e.g., Spark, streaming system).
4. **Security**: Does the system require access control per shard?
5. **Emotional Valence**: Does it affect the final nutrient\_score directly, or is it an orthogonal property?

> Please discuss or confirm these open questions before production rollout.

---

**© 2025 Gibsey**
Principal Systems Mycologist — *Mycelial Narrative Relay* v1.0

```
```