import fitz
from pathlib import Path


def load_pdf(path: Path) -> list[dict]:
    """
    Returns list of pages with text + some metadata
    """
    doc = fitz.open(path)
    pages = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        if not text:
            continue

        pages.append(
            {
                "page_number": page_num,
                "text": text,
            }
        )

    return pages
