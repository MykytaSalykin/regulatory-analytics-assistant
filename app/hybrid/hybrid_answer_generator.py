from app.classification.query_classifier import classify_query
from app.analytics.router import handle_analytics_query
from app.rag.answer_generator import generate_rag_answer


def generate_hybrid_answer(query: str) -> str:
    query_type = classify_query(query)

    if query_type == "analytics":
        analytics_result = handle_analytics_query(query)
        return analytics_result["summary"]

    if query_type == "document":
        return generate_rag_answer(query)

    # Hникшв
    analytics_result = handle_analytics_query(query)
    rag_answer = generate_rag_answer(query)

    final_answer = f"""
ANALYTICAL INSIGHTS (Survey-based):
{analytics_result["summary"]}

REGULATORY CONTEXT (EBA Documents):
{rag_answer}
    """.strip()

    return final_answer
