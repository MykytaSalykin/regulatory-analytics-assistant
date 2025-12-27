from app.rag.retriever import retrieve_chunks

EVAL_QUERIES = [
    {
        "query": "What are the main risks for EU banks according to EBA?",
        "relevant_pages": [55, 63, 77],
    },
    {
        "query": "What are the drivers of operational risk?",
        "relevant_pages": [55],
    },
]


def recall_at_k(top_k: int = 5) -> float:
    hits = 0

    for item in EVAL_QUERIES:
        results = retrieve_chunks(item["query"], top_k=top_k)
        retrieved_pages = {r["page_number"] for r in results}

        if retrieved_pages.intersection(item["relevant_pages"]):
            hits += 1

    return hits / len(EVAL_QUERIES)


if __name__ == "__main__":
    score = recall_at_k(top_k=5)
    print(f"Recall@5: {score:.2f}")
