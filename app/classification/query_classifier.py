def classify_query(query: str) -> str:
    q = query.lower()

    analytics_keywords = [
        "profitability",
        "capital",
        "liquidity",
        "ratio",
        "metrics",
        "survey",
        "expectations",
    ]

    document_keywords = [
        "eba",
        "regulation",
        "regulatory",
        "guideline",
        "report",
        "article",
        "paragraph",
        "directive",
        "compliance",
        "mentioned",
    ]

    has_analytics = any(k in q for k in analytics_keywords)
    has_document = any(k in q for k in document_keywords)

    # Priority rule: explicit document intent wins
    if has_document and not has_analytics:
        return "document"

    if has_analytics and has_document:
        return "hybrid"

    if has_analytics:
        return "analytics"

    return "document"
