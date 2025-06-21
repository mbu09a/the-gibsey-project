-- Cassandra initialization script for Gibsey Project
-- Creates keyspace and vector-enabled table for semantic search

-- Create keyspace with SimpleStrategy for single-node development
CREATE KEYSPACE IF NOT EXISTS gibsey 
WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

-- Use the gibsey keyspace
USE gibsey;

-- Create pages table with vector embedding support
CREATE TABLE IF NOT EXISTS pages (
    page_id text PRIMARY KEY,
    symbol_id text,
    title text,
    page_index int,
    tokens int,
    content text,
    embedding vector<float, 768>
);

-- Create secondary index on symbol_id for character-based queries
CREATE INDEX IF NOT EXISTS idx_pages_symbol_id ON pages (symbol_id);

-- Create secondary index on page_index for ordered retrieval
CREATE INDEX IF NOT EXISTS idx_pages_page_index ON pages (page_index);

-- Create vector index for semantic search (Cassandra 5.0 vector ANN)
CREATE CUSTOM INDEX IF NOT EXISTS idx_pages_embedding ON pages (embedding)
USING 'org.apache.cassandra.index.sai.StorageAttachedIndex';