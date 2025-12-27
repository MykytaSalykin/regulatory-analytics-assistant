import pytest


@pytest.fixture(autouse=True)
def mock_openai_embedding(monkeypatch):
    def fake_embedding(text, model=None):
        return [0.0] * 1536

    monkeypatch.setattr(
        "app.core.openai_client.get_embedding",
        fake_embedding,
    )
