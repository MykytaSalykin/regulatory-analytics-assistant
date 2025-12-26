from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import traceback

from app.classification.query_classifier import classify_query
from app.analytics.handlers import profitability_expectations
from app.hybrid.hybrid_answer_generator import generate_hybrid_answer
from app.core.db import engine

app = FastAPI(
    title="Regulatory Analytics Assistant",
    description="Hybrid AI assistant for regulatory documents and financial analytics",
    version="0.1.0",
)


# Schemas
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


# Healthcheck
@app.get("/health")
def health():
    return {"status": "ok"}


# Main entrypoint
@app.post("/query", response_model=QueryResponse)
def query_assistant(request: QueryRequest):
    try:
        query = request.query.strip()

        if not query:
            raise HTTPException(status_code=400, detail="Query must not be empty")

        query_type = classify_query(query)

        if query_type == "analytics":
            rows = profitability_expectations(engine)

            if not rows:
                answer = "No analytical data found for this query."
            else:
                answer_lines = [
                    f"- {row['answer']}: {row['responses']} responses" for row in rows
                ]
                answer = "\n".join(answer_lines)

            return QueryResponse(
                query_type="analytics",
                answer=answer,
                sources=[],
            )

        # hybrid (analytics + RAG)
        result = generate_hybrid_answer(query)

        return QueryResponse(
            query_type="hybrid",
            answer=result["answer"],
            sources=[
                Source(
                    file=src.get("file"),
                    page=src.get("page"),
                    score=src.get("score"),
                )
                for src in result.get("sources", [])
            ],
        )

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing query",
        )
