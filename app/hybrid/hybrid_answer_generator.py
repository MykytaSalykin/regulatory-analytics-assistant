from app.classification.query_classifier import classify_query
from app.analytics.router import handle_analytics_query
from app.rag.answer_generator import generate_rag_answer
import logging

logger = logging.getLogger(__name__)


def generate_hybrid_answer(query: str) -> dict:
    """
    Generate hybrid answer combining analytics and RAG.
    Returns structured dict with answer and sources.
    """
    try:
        query_type = classify_query(query)

        if query_type == "analytics":
            analytics_result = handle_analytics_query(query)
            return {"answer": analytics_result["summary"], "sources": []}

        if query_type == "document":
            rag_result = generate_rag_answer(query)
            return {
                "answer": rag_result["answer"],
                "sources": rag_result.get("sources", []),
            }

        # Hybrid: combine both
        analytics_result = handle_analytics_query(query)
        rag_result = generate_rag_answer(query)

        final_answer = f"""ANALYTICAL INSIGHTS (Survey-based):
{analytics_result["summary"]}

REGULATORY CONTEXT (EBA Documents):
{rag_result["answer"]}""".strip()

        return {"answer": final_answer, "sources": rag_result.get("sources", [])}

    except Exception as e:
        logger.error(f"Error in generate_hybrid_answer: {e}")
        return {
            "answer": "Error processing your query. Please try again.",
            "sources": [],
        }
