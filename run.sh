#!/bin/bash

echo "🚀 Starting Regulatory Analytics Assistant"
echo ""

# Check if PostgreSQL is running
if ! docker ps | grep -q regulatory_analytics_db; then
    echo "⚠️  PostgreSQL container not running. Starting it now..."
    docker-compose up -d
    echo "⏳ Waiting for PostgreSQL to be ready..."
    sleep 5
fi

# Check if database is initialized
if docker exec regulatory_analytics_db psql -U postgres -d regulatory_analytics -c "\dt finance.survey_metrics" 2>/dev/null | grep -q "survey_metrics"; then
    echo "✅ Database is initialized"
else
    echo "⚠️  Database not initialized. Run: docker exec -i regulatory_analytics_db psql -U postgres -d regulatory_analytics < docker/init.sql"
fi

echo ""
echo "📊 Starting FastAPI backend..."
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo ""

# Start FastAPI in background
uvicorn app.api.main:app --reload --port 8000 &
FASTAPI_PID=$!

# Wait a bit for FastAPI to start
sleep 3

echo ""
echo "🎨 Starting Streamlit UI..."
echo "   UI: http://localhost:8501"
echo ""

# Start Streamlit (this will block)
streamlit run ui/streamlit_app.py

# When Streamlit exits, kill FastAPI
kill $FASTAPI_PID 2>/dev/null
