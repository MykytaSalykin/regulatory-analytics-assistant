from app.analytics.handlers import profitability_expectations
from app.core.db import engine


def handle_analytics_query(query: str) -> dict:
    """
    MVP analytics router.
    Decides which analytics handler to run based on query intent.
    """

    query_lower = query.lower()

    if "profitability" in query_lower:
        rows = profitability_expectations(engine)

        summary_lines = [f"- {answer}: {count} responses" for answer, count in rows]

        summary = (
            "Based on the EBA RAQ survey, banks profitability expectations "
            "are primarily driven by the following factors:\n"
            + "\n".join(summary_lines)
        )

        return {"summary": summary, "data": rows, "source": "EBA RAQ Survey 2025"}

    return {
        "summary": "No matching analytics logic found for this query.",
        "data": [],
        "source": "EBA RAQ Survey 2025",
    }
