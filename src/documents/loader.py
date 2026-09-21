"""Descoberta de PDFs e extração de texto por página."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pymupdf as fitz  # PyMuPDF


@dataclass
class Page:
    """Uma página de um documento, com o texto extraído."""

    document: "Document"
    number: int
    text: str


@dataclass
class Document:
    """Um arquivo PDF do acervo (somente leitura)."""

    path: Path
    title: str = ""
    author: str = ""
    pages: list = field(default_factory=list)
    text_extractable: bool = True

    @property
    def filename(self) -> str:
        return self.path.name

    @property
    def article_id(self) -> str:
        return self.title or self.filename


def discover_pdfs(directory: Path) -> list[Path]:
    """Descobre recursivamente todos os PDFs sob `directory`."""
    return sorted(directory.rglob("*.pdf"))


def load_document(path: Path) -> Document:
    """Extrai texto por página; sinaliza páginas sem texto extraível em vez de falhar."""
    doc = Document(path=path)
    try:
        with fitz.open(path) as pdf:
            meta = pdf.metadata or {}
            doc.title = (meta.get("title") or "").strip()
            doc.author = (meta.get("author") or "").strip()
            for number, page in enumerate(pdf, start=1):
                text = (page.get_text() or "").strip()
                if text:
                    doc.pages.append(Page(document=doc, number=number, text=text))
        doc.text_extractable = bool(doc.pages)
    except Exception:
        doc.text_extractable = False
        doc.pages = []
    return doc


def load_acervo(directory: Path) -> list[Document]:
    """Carrega todos os PDFs do diretório (somente leitura)."""
    return [load_document(path) for path in discover_pdfs(directory)]
