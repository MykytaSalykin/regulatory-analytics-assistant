from app.classification.query_classifier import classify_query
from app.analytics.router import route_analytics
from app.analytics.handlers import profitability_expectations
from app.core.db import engine

query = "How many banks expect an increase in profitability?"

qtype = classify_query(query)
print("Query type:", qtype)

if qtype == "analytics":
    handler = route_analytics(query)
    if handler == "profitability_expectations":
        result = profitability_expectations(engine)
        print(result)
