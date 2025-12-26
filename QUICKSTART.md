# Quick Start Guide

## Prerequisites

1. **Docker & Docker Compose** installed
2. **Python 3.11+** installed
3. **OpenAI API Key** ready

## Step-by-Step Setup

### 1. Clone and Navigate

```bash
cd regulatory-analytics-assistant
```

### 2. Start PostgreSQL

```bash
docker-compose up -d
```

Wait a few seconds for PostgreSQL to be ready.

### 3. Initialize Database

```bash
docker exec -i regulatory_analytics_db psql -U postgres -d regulatory_analytics < docker/init.sql
```

### 4. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

### 5. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 6. Load Sample Data (Optional)

If you have the survey data ready:

```bash
jupyter notebook notebooks/eda.ipynb
```

Run the cells to load survey_metrics data into the database.

### 7. Ingest Documents (Optional)

If you want to use RAG functionality:

```bash
python -m app.ingestion.ingest_documents
python -m app.rag.embedding_generator
```

### 8. Start the Application

**Option A: Use the convenience script**

```bash
./run.sh
```

**Option B: Manual start**

Terminal 1 - Start FastAPI:
```bash
uvicorn app.api.main:app --reload --port 8000
```

Terminal 2 - Start Streamlit:
```bash
streamlit run ui/streamlit_app.py
```

### 9. Access the Application

- **Streamlit UI**: http://localhost:8501
- **FastAPI Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Quick Test

### Via UI
1. Open http://localhost:8501
2. Enter: "What are the main drivers of profitability expectations?"
3. Click "Ask"

### Via API
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the profitability expectations?"}'
```

## Troubleshooting

### PostgreSQL not starting
```bash
docker-compose down
docker-compose up -d
docker logs regulatory_analytics_db
```

### Database connection error
Check that PostgreSQL is running:
```bash
docker ps | grep regulatory_analytics_db
```

### No data returned
Make sure you've loaded the survey data from the notebook.

### OpenAI API errors
- Verify your API key in `.env`
- Check you have credits available
- Ensure you're using a valid model name

### Module not found errors
```bash
pip install -r requirements.txt
```

Make sure you're in the project root directory.

## Next Steps

1. **Load your data**: Follow the notebook in `notebooks/eda.ipynb`
2. **Ingest documents**: Run the document ingestion pipeline
3. **Try different queries**: Test analytics, document, and hybrid queries
4. **Explore the code**: Check out the modular structure in `app/`

## Support

For issues or questions, refer to the main README.md or check the code comments.
