"""Teste de integração do contrato POST /ask."""
from fastapi.testclient import TestClient

from src.agent.answerer import Answer, Result
from src.config import Config
from src.main import build_app


class StubAnswerer:
    def answer(self, question: str) -> Answer:
        return Answer(
            results=[
                Result(
                    filename="a.pdf",
                    excerpt="trecho",
                    page=1,
                    relevance="relevante",
                    citation="a.pdf, p. 1",
                    confidence="alta",
                )
            ],
            facts="fato",
            interpretation="interpretação",
        )


def make_config() -> Config:
    return Config(provider="x", api_key="x", endpoint="x", model="x", directory=".")


def test_ask_returns_results():
    app = build_app(make_config(), answerer=StubAnswerer())
    client = TestClient(app)
    resp = client.post("/ask", json={"question": "teste"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["results"]
    assert data["facts"] == "fato"
    assert data["interpretation"] == "interpretação"


def test_ask_empty_question_returns_400():
    app = build_app(make_config(), answerer=StubAnswerer())
    client = TestClient(app)
    resp = client.post("/ask", json={"question": "   "})
    assert resp.status_code == 400
