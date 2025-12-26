from sqlalchemy import text
from app.core.db import engine
from app.core.openai_client import get_embedding


def retrieve_chunks(query: str, top_k: int = 5) -> list[dict]:
    query_embedding = get_embedding(query)

    with engine.connect() as conn:
        rows = (
            conn.execute(
                text("""
                SELECT chunk_id, file_name, page_number, content, similarity
                FROM rag.search_chunks(
                    CAST(:embedding AS vector),
                    :top_k
                )
            """),
                {"embedding": query_embedding, "top_k": top_k},
            )
            .mappings()
            .all()
        )

    return [dict(r) for r in rows]
