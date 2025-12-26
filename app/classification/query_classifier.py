def classify_query(text: str) -> str:
    text_l = text.lower()

    analytics_keywords = [
        "how many",
        "percentage",
        "share",
        "trend",
        "increase",
        "decrease",
        "rank",
        "count",
        "distribution",
    ]

    document_keywords = [
        "eba",
        "regulation",
        "guideline",
        "according to",
        "risk assessment",
        "policy",
        "framework",
    ]

    is_analytics = any(k in text_l for k in analytics_keywords)
    is_document = any(k in text_l for k in document_keywords)

    if is_analytics and is_document:
        return "hybrid"
    if is_analytics:
        return "analytics"
    return "document"
