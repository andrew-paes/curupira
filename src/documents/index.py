"""Índice em memória por página com recuperação lexical."""
from __future__ import annotations

import re
from dataclasses import dataclass

from .loader import Document, Page

_TOKEN_RE = re.compile(r"[a-zA-Z0-9à-úÀ-Úâêôãõç]+", re.UNICODE)


def tokenize(text: str) -> list[str]:
    """Divide texto em tokens normalizados (minúsculas)."""
    return [t.lower() for t in _TOKEN_RE.findall(text)]


@dataclass
class SearchHit:
    page: Page
    score: int


class PageIndex:
    """Índice simples em memória: sobreposição lexical de tokens por página."""

    def __init__(self, documents: list[Document]):
        self.documents = documents
        self._pages = [page for doc in documents for page in doc.pages]
        self._tokens = [set(tokenize(page.text)) for page in self._pages]

    @property
    def is_empty(self) -> bool:
        return not self._pages

    def search(self, query: str, top_k: int = 10) -> list[Page]:
        """Retorna as páginas mais relevantes por sobreposição de tokens."""
        query_tokens = set(tokenize(query))
        if not query_tokens:
            return []
        scored: list[SearchHit] = []
        for page, tokens in zip(self._pages, self._tokens):
            overlap = len(query_tokens & tokens)
            if overlap > 0:
                scored.append(SearchHit(page=page, score=overlap))
        scored.sort(key=lambda hit: hit.score, reverse=True)
        return [hit.page for hit in scored[:top_k]]
