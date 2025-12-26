from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)


def profitability_expectations(engine):
    """
    Query survey metrics related to profitability expectations.
    Returns list of dicts with answer and response count.
    """
    try:
        sql = text("""
            SELECT
                item_label,
                COUNT(*) as response_count
            FROM finance.survey_metrics
            WHERE item_label ILIKE '%profitability%'
            GROUP BY item_label
            ORDER BY response_count DESC
            LIMIT 20
        """)

        with engine.connect() as conn:
            result = conn.execute(sql)
            rows = result.fetchall()

            return [{"answer": row[0], "responses": int(row[1])} for row in rows]
    except Exception as e:
        logger.error(f"Error in profitability_expectations: {e}")
        return []
