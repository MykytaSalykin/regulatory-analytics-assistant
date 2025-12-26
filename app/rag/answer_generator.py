from app.core.openai_client import chat
from app.rag.retriever import retrieve_chunks
import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a Regulatory Analytics Assistant.
Use ONLY the provided sources. If the answer is not in the sources, say you don't know.
Cite sources as: (file, p.X). Be concise and factual.
"""


def _format_sources(chunks: list[dict]) -> str:
    parts = []
    for i, c in enumerate(chunks, start=1):
        parts.append(
            f"[{i}] file={c['file_name']} page={c['page_number']} score={c.get('similarity', 0):.3f}\n"
            f"{c['content']}"
        )
    return "\n\n".join(parts)


def answer_with_rag(query: str, top_k: int = 5) -> dict:
    """
    Core RAG logic.
    Returns answer text + retrieved chunks.
    """
    try:
        chunks = retrieve_chunks(query, top_k=top_k)

        if not chunks:
            return {
                "answer": "No relevant documents found for this query.",
                "chunks": [],
                "sources": [],
            }

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
            model="gpt-4o-mini",
            temperature=0.0,
        )

        sources = [
            {
                "file": c["file_name"],
                "page": c.get("page_number"),
                "score": c.get("similarity", 0),
            }
            for c in chunks
        ]

        return {"answer": answer, "chunks": chunks, "sources": sources}

    except Exception as e:
        logger.error(f"Error in answer_with_rag: {e}")
        return {
            "answer": "Error generating RAG answer. Please try again.",
            "chunks": [],
            "sources": [],
        }


def generate_rag_answer(query: str, top_k: int = 5) -> dict:
    """
    Public interface for RAG answering.
    Returns structured dict with answer and sources.
    """
    return answer_with_rag(query, top_k=top_k)
