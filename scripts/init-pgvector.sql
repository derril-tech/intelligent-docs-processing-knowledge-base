-- Initialize pgvector extension for DocuMind™
-- This script runs when the PostgreSQL container starts

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create vector dimensions for different embedding models
-- OpenAI text-embedding-3-large: 3072 dimensions
-- OpenAI text-embedding-ada-002: 1536 dimensions
-- BGE embeddings: 768 dimensions

-- Create a function to get embedding dimensions based on model
CREATE OR REPLACE FUNCTION get_embedding_dimensions(model_name TEXT)
RETURNS INTEGER AS $$
BEGIN
    CASE model_name
        WHEN 'text-embedding-3-large' THEN RETURN 3072;
        WHEN 'text-embedding-ada-002' THEN RETURN 1536;
        WHEN 'bge-large-en-v1.5' THEN RETURN 1024;
        WHEN 'bge-base-en-v1.5' THEN RETURN 768;
        ELSE RETURN 1536; -- Default to ada-002 dimensions
    END CASE;
END;
$$ LANGUAGE plpgsql;

-- Create indexes for vector similarity search
-- These will be created when the tables are created via Alembic migrations

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO user;
GRANT CREATE ON SCHEMA public TO user;
