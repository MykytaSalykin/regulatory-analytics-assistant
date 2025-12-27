def test_rag_answer_structure(monkeypatch):
    from app.rag.answer_generator import answer_with_rag

    def fake_retrieve(*args, **kwargs):
        return [
            {
                "file_name": "doc.pdf",
                "page_number": 1,
                "similarity": 0.9,
                "content": "test content",
            }
        ]

    monkeypatch.setattr("app.rag.answer_generator.retrieve_chunks", fake_retrieve)

    monkeypatch.setattr("app.rag.answer_generator.chat", lambda **kwargs: "test answer")

    result = answer_with_rag("test query")
    assert "answer" in result
    assert "chunks" in result
