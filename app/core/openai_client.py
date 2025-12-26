from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    resp = client.embeddings.create(model=model, input=text)
    return resp.data[0].embedding


def chat(
    messages: list[dict], model: str = "gpt-4.1-mini", temperature: float = 0.0
) -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return resp.choices[0].message.content
