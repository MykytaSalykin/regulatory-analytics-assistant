from app.rag.answer_generator import answer_with_rag

query = "What are the main risks and vulnerabilities highlighted for EU/EEA banks?"
result = answer_with_rag(query, top_k=5)

print(result["answer"])
