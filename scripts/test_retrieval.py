from app.rag.retriever import retrieve_chunks

query = "What are the main risks identified by EBA for European banks?"

results = retrieve_chunks(query, top_k=5)

for r in results:
    print("=" * 80)
    print(f"{r.file_name} | page {r.page_number} | similarity={r.similarity:.3f}")
    print(r.content[:500])
