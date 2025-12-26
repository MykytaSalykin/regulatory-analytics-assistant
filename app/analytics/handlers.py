from sqlalchemy import text


def profitability_expectations(engine):
    sql = text("""
        SELECT
            sm.item_label AS answer,
            COUNT(*) AS responses
        FROM finance.survey_metrics sm
        JOIN finance.survey_items si ON sm.item_id = si.item_id
        WHERE si.item_label ILIKE '%profitability%'
        GROUP BY sm.item_label
        ORDER BY responses DESC
    """)

    with engine.begin() as conn:
        result = conn.execute(sql)
        return [
            {
                "answer": row._mapping["answer"],
                "responses": row._mapping["responses"],
            }
            for row in result
        ]
