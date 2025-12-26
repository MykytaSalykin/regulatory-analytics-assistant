from sqlalchemy import text
from app.core.db import engine
from app.core.openai_client import get_embedding

BATCH_SIZE = 50


def generate_embeddings():
    with engine.begin() as conn:
        rows = conn.execute(
            text("""
                SELECT chunk_id, content
                FROM rag.document_chunks_raw
                WHERE chunk_id NOT IN (
                    SELECT chunk_id FROM rag.document_embeddings
                )
                ORDER BY chunk_id
            """)
        ).fetchall()

        print(f"Generating embeddings for {len(rows)} chunks")

        for chunk_id, content in rows:
            embedding = get_embedding(content)

            conn.execute(
                text("""
                    INSERT INTO rag.document_embeddings (chunk_id, embedding)
                    VALUES (:chunk_id, :embedding)
                """),
                {"chunk_id": chunk_id, "embedding": embedding},
            )


if __name__ == "__main__":
    generate_embeddings()
