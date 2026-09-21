"""Orquestra recuperação e respostas fundamentadas em evidência."""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field

from ..documents.index import PageIndex
from ..llm.provider import LLMClient

_JSON_RE = re.compile(r"\{.*\}", re.DOTALL)

_SYSTEM_PROMPT = (
    "Você é um assistente de pesquisa que responde perguntas usando APENAS os trechos "
    "fornecidos de uma coleção local de artigos científicos.\n"
    "REGRAS OBRIGATÓRIAS:\n"
    "1. Use somente os trechos fornecidos como evidência.\n"
    "2. NÃO invente nomes de arquivo, números de página, citações ou fatos.\n"
    "3. Distinga claramente o que está presente nos artigos (facts) da sua síntese "
    "(interpretation).\n"
    "4. Se nenhum trecho sustentar a pergunta, retorne results vazio.\n"
)


@dataclass
class Result:
    filename: str
    article_id: str = ""
    excerpt: str = ""
    page: int | None = None
    relevance: str = ""
    citation: str = ""
    confidence: str = "alta"


@dataclass
class Answer:
    results: list = field(default_factory=list)
    facts: str = ""
    interpretation: str = ""
    uncertainty: str | None = None

    def to_dict(self) -> dict:
        return {
            "results": [asdict(r) for r in self.results],
            "facts": self.facts,
            "interpretation": self.interpretation,
            "uncertainty": self.uncertainty,
        }


class Answerer:
    """Recupera páginas candidatas e produz uma resposta com citações."""

    def __init__(self, index: PageIndex, llm: LLMClient):
        self.index = index
        self.llm = llm

    def answer(self, question: str) -> Answer:
        pages = self.index.search(question, top_k=10)
        if not pages:
            return self._no_evidence()
        prompt = self._build_prompt(question, pages)
        raw = self.llm.complete(prompt)
        return self._parse(raw)

    def _build_context(self, pages) -> str:
        blocks = []
        for page in pages:
            blocks.append(
                f"[Arquivo: {page.document.filename} | Página: {page.number}]\n{page.text[:2000]}"
            )
        return "\n\n".join(blocks)

    def _build_prompt(self, question: str, pages) -> str:
        context = self._build_context(pages)
        return (
            _SYSTEM_PROMPT
            + f"Pergunta: {question}\n\n"
            + f"Trechos:\n{context}\n\n"
            + "Responda APENAS com JSON no formato:\n"
            + '{"results": [{"filename": "...", "article_id": "...", "excerpt": "...", '
            + '"page": N, "relevance": "...", "citation": "...", '
            + '"confidence": "alta|media|baixa"}], "facts": "...", '
            + '"interpretation": "...", "uncertainty": null}\n'
        )

    def _parse(self, raw: str) -> Answer:
        match = _JSON_RE.search(raw)
        if not match:
            return self._no_evidence("Resposta do modelo não pôde ser interpretada.")
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            return self._no_evidence("Resposta do modelo não pôde ser interpretada.")

        results = [
            Result(
                filename=item.get("filename", ""),
                article_id=item.get("article_id", ""),
                excerpt=item.get("excerpt", ""),
                page=item.get("page"),
                relevance=item.get("relevance", ""),
                citation=item.get("citation", ""),
                confidence=item.get("confidence", "alta"),
            )
            for item in data.get("results", [])
        ]
        if not results:
            return self._no_evidence()

        return Answer(
            results=results,
            facts=data.get("facts", ""),
            interpretation=data.get("interpretation", ""),
            uncertainty=data.get("uncertainty"),
        )

    def _no_evidence(self, uncertainty: str | None = None) -> Answer:
        return Answer(
            results=[],
            facts="",
            interpretation="",
            uncertainty=uncertainty or "Não foi encontrada evidência suficiente no acervo.",
        )
