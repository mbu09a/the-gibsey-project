CREATE KEYSPACE IF NOT EXISTS gibsey WITH replication = {'class': 'SimpleStrategy','replication_factor': 1};
USE gibsey;

CREATE TABLE IF NOT EXISTS pages (
  page_id TEXT PRIMARY KEY,
  char_hex TINYINT,
  behavior TINYINT,
  symbol_code TINYINT,
  section INT,
  page_num INT,
  provenance TEXT,
  orientation TEXT,
  trajectory TEXT,
  return_to TEXT,
  text TEXT,
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS page_edges (
  page_id TEXT,
  edge_type TEXT,
  target_id TEXT,
  created_at TIMEUUID,
  PRIMARY KEY ((page_id), edge_type, created_at)
) WITH CLUSTERING ORDER BY (edge_type ASC, created_at ASC);

CREATE TABLE IF NOT EXISTS page_embeddings (
  page_id TEXT PRIMARY KEY,
  dim INT,
  vec BLOB
);

CREATE TABLE IF NOT EXISTS page_index_signals (
  page_id TEXT PRIMARY KEY,
  entities SET<TEXT>,
  motifs SET<TEXT>,
  unresolved_anchors SET<TEXT>,
  novelty DOUBLE,
  coherence DOUBLE
);

CREATE TABLE IF NOT EXISTS section_counters (
  section INT PRIMARY KEY,
  open_branches COUNTER,
  return_debt COUNTER
);

CREATE TABLE IF NOT EXISTS plans (
  plan_id TIMEUUID PRIMARY KEY,
  page_id TEXT,
  symbol_code TINYINT,
  trajectory TEXT,
  plan_json TEXT,
  created_at TIMESTAMP
);