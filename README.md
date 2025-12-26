# Regulatory Analytics Assistant

**Proof of Concept** — AI-powered analytics system for banking regulatory and risk analysis.

## Overview

This system combines:
- **Structured financial data analytics** (SQL-based queries on EBA survey data)
- **Retrieval-Augmented Generation (RAG)** over regulatory PDF documents
- **Intelligent query classification** to route requests appropriately

## Domain

EU banking regulation, specifically:
- EBA (European Banking Authority) risk analytics
- Transparency Exercise 2025 data
- Regulatory reports and guidelines

## Data Sources

### Structured Data
- EBA Transparency Exercise 2025 RAQ statistical annex (Excel)
- Statistical Data Dictionary (SDD)

### Unstructured Documents (PDF)
- EBA Risk Assessment Report (2025)
- RAQ Booklet (Autumn 2025)

## Tech Stack

- **Backend**: Python 3.11+, FastAPI
- **Database**: PostgreSQL 16 + pgvector
- **AI**: OpenAI API (embeddings & generation)
- **Data**: Pandas, SQLAlchemy
- **UI**: Streamlit
- **Deployment**: Docker Compose

## Project Structure

```
regulatory-analytics-assistant/
├── app/
│   ├── api/           # FastAPI endpoints
│   ├── analytics/     # SQL-based analytics handlers
│   ├── rag/           # RAG retrieval & answer generation
│   ├── classification/# Query classifier
│   ├── ingestion/     # Data ingestion pipelines
│   ├── core/          # Database & OpenAI clients
│   └── schemas/       # Pydantic models
├── data/
│   ├── raw/           # Original Excel & PDF files
│   └── processed/     # Transformed data
├── docker/
│   └── init.sql       # Database schema DDL
├── notebooks/         # Exploratory data analysis
├── ui/
│   └── streamlit_app.py  # Streamlit UI
└── docker-compose.yml
```

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- OpenAI API key

### 1. Start PostgreSQL

```bash
docker-compose up -d
```

This starts PostgreSQL with pgvector extension on port 5432.

### 2. Initialize Database

```bash
docker exec -i regulatory_analytics_db psql -U postgres -d regulatory_analytics < docker/init.sql
```

### 3. Set Environment Variables

Create a `.env` file:

```bash
OPENAI_API_KEY=your_openai_api_key_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=regulatory_analytics
DB_USER=postgres
DB_PASSWORD=postgres
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Data Ingestion (if needed)

```bash
# Ingest survey data (from notebook or script)
python -m app.ingestion.ingest_documents

# Generate embeddings
python -m app.rag.embedding_generator
```

### 6. Start FastAPI Backend

```bash
uvicorn app.api.main:app --reload --port 8000
```

API will be available at: `http://localhost:8000`

API docs: `http://localhost:8000/docs`

### 7. Start Streamlit UI

```bash
streamlit run ui/streamlit_app.py
```

UI will open in your browser at: `http://localhost:8501`

## Usage

### Query Types

The system automatically classifies queries into three types:

1. **Analytics** — Statistical queries on survey data
   - Example: "What are the main drivers of profitability expectations?"

2. **Document** — Questions about regulatory documents
   - Example: "What does EBA say about credit risk?"

3. **Hybrid** — Combines both analytics and document context
   - Example: "How many banks expect profitability to increase and what does EBA recommend?"

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Query
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the profitability expectations?"}'
```

Response format:
```json
{
  "query_type": "analytics",
  "answer": "Based on EBA RAQ survey...",
  "sources": [
    {
      "file": "eba_risk_assessment_report_2025-12.pdf",
      "page": 42,
      "score": 0.87
    }
  ]
}
```

## Engineering Principles

- ✅ Clear schema design (finance / rag / meta schemas)
- ✅ Reproducible data pipelines
- ✅ Emphasis on explainability and source attribution
- ✅ Production-style structure
- ✅ Proper error handling and logging

## Current Limitations (POC)

- Single-user, local deployment only
- No authentication/authorization
- Limited analytics handlers (profitability only)
- Simple character-based text chunking
- No caching layer
- Basic query classification (keyword-based)

## Future Enhancements

- [ ] More sophisticated query classifier (LLM-based)
- [ ] Advanced analytics handlers (capital ratios, liquidity, etc.)
- [ ] Multi-document reasoning
- [ ] Query history and feedback loop
- [ ] Better chunking strategies (semantic, sentence-based)
- [ ] Caching and performance optimization
- [ ] Multi-user support with authentication

## License

This is a Proof of Concept project for educational and demonstration purposes.

## Contact

For questions or feedback, please open an issue in the repository.
