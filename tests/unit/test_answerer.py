"""Testes de unidade para o answerer: separação fato/interpretação e sem fabricação."""
import json
from pathlib import Path

from src.agent.answerer import Answerer
from src.documents.index import PageIndex
from src.documents.loader import Document, Page


class FakeLLM:
    def __init__(self, response: str):
        self._response = response

    def complete(self, prompt: str) -> str:
        return self._response


def make_index() -> PageIndex:
    doc = Document(path=Path("a.pdf"))
    doc.pages.append(Page(document=doc, number=1, text="estudo sobre qualidade de software"))
    return PageIndex([doc])


def test_answer_separates_facts_and_interpretation():
    payload = {
        "results": [
            {
                "filename": "a.pdf",
                "article_id": "a.pdf",
                "excerpt": "o estudo investiga qualidade de software",
                "page": 1,
                "relevance": "aborda diretamente a pergunta",
                "citation": "a.pdf, p. 1",
                "confidence": "alta",
            }
        ],
        "facts": "O artigo investiga qualidade de software.",
        "interpretation": "Há forte relação com a pergunta.",
        "uncertainty": None,
    }
    answerer = Answerer(make_index(), FakeLLM(json.dumps(payload)))
    answer = answerer.answer("qualidade de software")
    assert answer.facts
    assert answer.interpretation
    assert len(answer.results) == 1
    assert answer.results[0].filename == "a.pdf"


def test_answer_no_evidence_when_index_empty():
    answerer = Answerer(PageIndex([]), FakeLLM("{}"))
    answer = answerer.answer("qualquer coisa")
    assert answer.results == []
    assert answer.uncertainty


def test_answer_no_fabrication_when_model_returns_empty():
    payload = {"results": [], "facts": "", "interpretation": "", "uncertainty": "sem evidência"}
    answerer = Answerer(make_index(), FakeLLM(json.dumps(payload)))
    answer = answerer.answer("tema inexistente")
    assert answer.results == []
    assert answer.uncertainty
