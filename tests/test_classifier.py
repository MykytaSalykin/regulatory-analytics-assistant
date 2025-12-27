from app.classification.query_classifier import classify_query


def test_classify_analytics_query():
    assert classify_query("profitability of banks") == "analytics"


def test_classify_document_query():
    assert classify_query("what are the key risks mentioned by EBA") == "document"


def test_classify_hybrid_query():
    assert classify_query("profitability and regulatory risks") == "hybrid"
