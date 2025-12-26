def chunk_text(
    text: str,
    max_chars: int = 800,
    overlap: int = 100,
) -> list[str]:
    """
    Simple character-based chunking with overlapping
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + max_chars
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end - overlap

    return chunks
