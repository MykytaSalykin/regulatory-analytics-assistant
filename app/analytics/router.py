from app.analytics.handlers import profitability_expectations
from app.core.db import engine
import logging

logger = logging.getLogger(__name__)


def handle_analytics_query(query: str) -> dict:
    """
    MVP analytics router.
    Decides which analytics handler to run based on query intent.
    Returns structured dict with summary, data, and source.
    """
    try:
        query_lower = query.lower()

        if "profitability" in query_lower:
            rows = profitability_expectations(engine)

            if not rows:
                return {
                    "summary": "No profitability data found in the survey metrics.",
                    "data": [],
                    "source": "EBA RAQ Survey 2025",
                }

            summary_lines = [
                f"- {row['answer']}: {row['responses']} responses" for row in rows[:10]
            ]

            summary = (
                "Based on the EBA RAQ survey, banks' profitability expectations "
                "are primarily driven by the following factors:\n"
                + "\n".join(summary_lines)
            )

            return {"summary": summary, "data": rows, "source": "EBA RAQ Survey 2025"}

        return {
            "summary": "No matching analytics logic found for this query. Try asking about profitability expectations.",
            "data": [],
            "source": "EBA RAQ Survey 2025",
        }

    except Exception as e:
        logger.error(f"Error in handle_analytics_query: {e}")
        return {
            "summary": "Error processing analytics query. Please try again.",
            "data": [],
            "source": "EBA RAQ Survey 2025",
        }
