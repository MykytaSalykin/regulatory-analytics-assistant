CREATE EXTENSION IF NOT EXISTS vector;

CREATE SCHEMA IF NOT EXISTS meta;
CREATE SCHEMA IF NOT EXISTS finance;
CREATE SCHEMA IF NOT EXISTS rag;

CREATE TABLE IF NOT EXISTS meta.data_sources (
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

CREATE TABLE IF NOT EXISTS meta.ingestion_runs (
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

CREATE TABLE IF NOT EXISTS meta.quality_checks (
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

CREATE TABLE IF NOT EXISTS finance.institutions (
    institution_code VARCHAR(50) PRIMARY KEY,
    lei_code VARCHAR(20) UNIQUE,
    institution_name VARCHAR(500) NOT NULL,
    country_code VARCHAR(2),
    country_name VARCHAR(100),
    source_id INTEGER REFERENCES meta.data_sources(source_id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS finance.periods (
    period_code VARCHAR(20) PRIMARY KEY,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER,
    is_latest BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS finance.metrics (
    institution_code VARCHAR(50) NOT NULL REFERENCES finance.institutions(institution_code),
    period_code VARCHAR(20) NOT NULL REFERENCES finance.periods(period_code),
    metric_code VARCHAR(100) NOT NULL,
    metric_name VARCHAR(500),
    metric_category VARCHAR(100),
    value NUMERIC(20, 6),
    currency VARCHAR(3) DEFAULT 'EUR',
    unit VARCHAR(50),
    source_row VARCHAR(100),
    source_sheet VARCHAR(255),
    source_id INTEGER REFERENCES meta.data_sources(source_id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (institution_code, period_code, metric_code)
);

CREATE INDEX IF NOT EXISTS idx_metrics_institution ON finance.metrics(institution_code);
CREATE INDEX IF NOT EXISTS idx_metrics_period ON finance.metrics(period_code);
CREATE INDEX IF NOT EXISTS idx_metrics_category ON finance.metrics(metric_category);
CREATE INDEX IF NOT EXISTS idx_metrics_code ON finance.metrics(metric_code);

CREATE TABLE IF NOT EXISTS rag.documents (
    document_id BIGSERIAL PRIMARY KEY,
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

CREATE TABLE IF NOT EXISTS rag.chunks (
    chunk_id BIGSERIAL PRIMARY KEY,
    document_id BIGINT NOT NULL REFERENCES rag.documents(document_id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    page_number INTEGER,
    section_title VARCHAR(1000),
    text TEXT NOT NULL,
    embedding_model VARCHAR(100) NOT NULL,
    embedding vector(1536),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(document_id, chunk_index)
);

CREATE INDEX IF NOT EXISTS idx_chunks_document ON rag.chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_chunks_page ON rag.chunks(page_number);
