from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

from app.classification.query_classifier import classify_query
from app.analytics.router import handle_analytics_query
from app.rag.answer_generator import generate_rag_answer
from app.hybrid.hybrid_answer_generator import generate_hybrid_answer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Regulatory Analytics Assistant",
    description="Hybrid AI assistant for regulatory documents and financial analytics",
    version="0.1.0",
)


class QueryRequest(BaseModel):
    query: str


class Source(BaseModel):
    file: str
    page: int | None = None
    score: float | None = None


class QueryResponse(BaseModel):
    query_type: str
    answer: str
    sources: list[Source]


@app.get("/health")
def health():
    """Healthcheck endpoint"""
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query_assistant(request: QueryRequest):
    """
    Main query endpoint.
    Classifies query and returns appropriate response.
    """
    try:
        query = request.query.strip()

        if not query:
            raise HTTPException(status_code=400, detail="Query must not be empty")

        logger.info(f"Processing query: {query[:100]}")

        query_type = classify_query(query)
        logger.info(f"Query classified as: {query_type}")

        if query_type == "analytics":
            analytics_result = handle_analytics_query(query)

            return QueryResponse(
                query_type="analytics", answer=analytics_result["summary"], sources=[]
            )

        elif query_type == "document":
            rag_result = generate_rag_answer(query)

            return QueryResponse(
                query_type="document",
                answer=rag_result["answer"],
                sources=[
                    Source(
                        file=src.get("file", ""),
                        page=src.get("page"),
                        score=src.get("score"),
                    )
                    for src in rag_result.get("sources", [])
                ],
            )

        else:  # hybrid
            hybrid_result = generate_hybrid_answer(query)

            return QueryResponse(
                query_type="hybrid",
                answer=hybrid_result["answer"],
                sources=[
                    Source(
                        file=src.get("file", ""),
                        page=src.get("page"),
                        score=src.get("score"),
                    )
                    for src in hybrid_result.get("sources", [])
                ],
            )

    except HTTPException:
        raise

    except Exception:
        logger.exception("Unexpected error processing query")
        raise HTTPException(
            status_code=500, detail="Internal server error while processing query"
        )
