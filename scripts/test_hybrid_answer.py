from app.hybrid.hybrid_answer_generator import generate_hybrid_answer

query = "What are the main risks identified by banks and how do they align with EBA's assessment?"

answer = generate_hybrid_answer(query)
print(answer)
