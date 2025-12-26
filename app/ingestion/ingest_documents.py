from pathlib import Path
from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunker import chunk_text
from app.core.db import engine
import pandas as pd


RAW_DOCS_PATH = Path("data/raw/documents")


def ingest_pdf(pdf_path: Path):
    pages = load_pdf(pdf_path)

    records = []

    for page in pages:
        chunks = chunk_text(page["text"])

        for idx, chunk in enumerate(chunks):
            records.append(
                {
                    "file_name": pdf_path.name,
                    "page_number": page["page_number"],
                    "chunk_index": idx,
                    "content": chunk,
                }
            )

    return pd.DataFrame(records)


def main():
    all_chunks = []

    for pdf in RAW_DOCS_PATH.glob("*.pdf"):
        print(f"Ingesting {pdf.name}")
        df = ingest_pdf(pdf)
        all_chunks.append(df)

    df_chunks = pd.concat(all_chunks, ignore_index=True)

    df_chunks.to_sql(
        name="document_chunks_raw",
        schema="rag",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=500,
    )

    print(f"Inserted {len(df_chunks)} chunks")


if __name__ == "__main__":
    main()
