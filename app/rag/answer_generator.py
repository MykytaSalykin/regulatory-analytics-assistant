from app.core.openai_client import chat
from app.rag.retriever import retrieve_chunks


SYSTEM_PROMPT = """You are a Regulatory Analytics Assistant.
Use ONLY the provided sources. If the answer is not in the sources, say you don't know.
Cite sources as: (file, p.X). Be concise and factual.
"""


def _format_sources(chunks: list[dict]) -> str:
    parts = []
    for i, c in enumerate(chunks, start=1):
        parts.append(
            f"[{i}] file={c['file_name']} page={c['page_number']} score={c['similarity']:.3f}\n"
            f"{c['content']}"
        )
    return "\n\n".join(parts)


def answer_with_rag(query: str, top_k: int = 5) -> dict:
    """
    Core RAG logic.
    Returns answer text + retrieved chunks.
    """
    chunks = retrieve_chunks(query, top_k=top_k)

    sources_text = _format_sources(chunks)

    user_prompt = f"""Question:
{query}

Sources:
{sources_text}

Task:
Answer the question using ONLY the sources. Provide 2-5 bullet points, then a short "Sources used" list with citations.
"""

    answer = chat(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        model="gpt-4.1-mini",
        temperature=0.0,
    )

    return {"answer": answer, "chunks": chunks}


# PUBLIC INTERFACE FOR HYBRID / API / UI
def generate_rag_answer(query: str, top_k: int = 5) -> str:
    """
    Thin wrapper used by hybrid answering and future FastAPI/UI layers.
    Returns ONLY answer text.
    """
    result = answer_with_rag(query, top_k=top_k)
    return result["answer"]
