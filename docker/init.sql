CREATE EXTENSION IF NOT EXISTS vector;

CREATE SCHEMA IF NOT EXISTS meta;
CREATE SCHEMA IF NOT EXISTS finance;
CREATE SCHEMA IF NOT EXISTS rag;

CREATE TABLE meta.data_sources (
    source_id SERIAL PRIMARY KEY,
    source_name VARCHAR(255) NOT NULL UNIQUE,
    source_type VARCHAR(50) NOT NULL,
    file_path TEXT,
    description TEXT,
    version VARCHAR(100),
    publication_date DATE,
    ingested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    checksum VARCHAR(64),
    metadata JSONB
);

CREATE TABLE meta.ingestion_runs (
    run_id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES meta.data_sources(source_id),
    target_schema VARCHAR(50) NOT NULL,
    target_table VARCHAR(100) NOT NULL,
    rows_inserted INTEGER DEFAULT 0,
    rows_updated INTEGER DEFAULT 0,
    rows_failed INTEGER DEFAULT 0,
    status VARCHAR(20) NOT NULL,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    error_message TEXT
);

CREATE TABLE meta.quality_checks (
    check_id SERIAL PRIMARY KEY,
    run_id INTEGER REFERENCES meta.ingestion_runs(run_id),
    check_name VARCHAR(255) NOT NULL,
    check_type VARCHAR(100) NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    column_name VARCHAR(100),
    expected_value TEXT,
    actual_value TEXT,
    status VARCHAR(20) NOT NULL,
    executed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT
);

CREATE TABLE finance.institutions (
    institution_code VARCHAR(50) PRIMARY KEY,
    lei_code VARCHAR(20) UNIQUE,
    institution_name VARCHAR(500) NOT NULL,
    country_code VARCHAR(2),
    country_name VARCHAR(100),
    source_id INTEGER REFERENCES meta.data_sources(source_id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE finance.periods (
    period_code VARCHAR(20) PRIMARY KEY,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER,
    is_latest BOOLEAN DEFAULT FALSE
);

CREATE TABLE finance.metrics (
    institution_code VARCHAR(50) NOT NULL REFERENCES finance.institutions(institution_code),
    period_code VARCHAR(20) NOT NULL REFERENCES finance.periods(period_code),
    metric_code VARCHAR(100) NOT NULL,
    metric_name VARCHAR(500),
    metric_category VARCHAR(100),
    value NUMERIC(20, 2),
    currency VARCHAR(3) DEFAULT 'EUR',
    unit VARCHAR(50),
    source_row VARCHAR(100),
    source_sheet VARCHAR(255),
    source_id INTEGER REFERENCES meta.data_sources(source_id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (institution_code, period_code, metric_code)
);

CREATE INDEX idx_metrics_institution ON finance.metrics(institution_code);
CREATE INDEX idx_metrics_period ON finance.metrics(period_code);
CREATE INDEX idx_metrics_category ON finance.metrics(metric_category);

CREATE TABLE rag.documents (
    document_id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES meta.data_sources(source_id),
    title VARCHAR(1000) NOT NULL,
    document_type VARCHAR(50),
    file_path TEXT NOT NULL,
    file_name VARCHAR(500) NOT NULL,
    publication_date DATE,
    author VARCHAR(500),
    page_count INTEGER,
    checksum VARCHAR(64),
    metadata JSONB,
    ingested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE rag.chunks (
    chunk_id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES rag.documents(document_id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    page_number INTEGER,
    section_title VARCHAR(1000),
    text TEXT NOT NULL,
    embedding_model VARCHAR(100) NOT NULL,
    embedding vector(1536),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(document_id, chunk_index)
);

CREATE INDEX idx_chunks_document ON rag.chunks(document_id);
CREATE INDEX idx_chunks_embedding ON rag.chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE TABLE finance.survey_metrics (
    metric_id SERIAL PRIMARY KEY,
    exercise VARCHAR(100) NOT NULL,
    period VARCHAR(50) NOT NULL,
    item_code VARCHAR(50) NOT NULL,
    item_label TEXT NOT NULL,
    value NUMERIC(20, 2),
    answer_rank INTEGER,
    source VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_survey_metrics_period ON finance.survey_metrics(period);
CREATE INDEX idx_survey_metrics_item_code ON finance.survey_metrics(item_code);

CREATE TABLE rag.document_chunks_raw (
    chunk_id SERIAL PRIMARY KEY,
    file_name VARCHAR(500) NOT NULL,
    page_number INTEGER,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rag.document_embeddings (
    embedding_id SERIAL PRIMARY KEY,
    chunk_id INTEGER NOT NULL REFERENCES rag.document_chunks_raw(chunk_id) ON DELETE CASCADE,
    embedding vector(1536) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(chunk_id)
);

CREATE INDEX idx_document_embeddings_vector ON rag.document_embeddings 
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE OR REPLACE FUNCTION rag.search_chunks(
    query_embedding vector(1536),
    match_count integer DEFAULT 5
)
RETURNS TABLE (
    chunk_id integer,
    file_name varchar(500),
    page_number integer,
    content text,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        dcr.chunk_id,
        dcr.file_name,
        dcr.page_number,
        dcr.content,
        1 - (de.embedding <=> query_embedding) as similarity
    FROM rag.document_chunks_raw dcr
    JOIN rag.document_embeddings de ON dcr.chunk_id = de.chunk_id
    ORDER BY de.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
