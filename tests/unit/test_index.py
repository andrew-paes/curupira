"""Testes de unidade para o índice de páginas e a recuperação lexical."""
from pathlib import Path

from src.documents.index import PageIndex, tokenize
from src.documents.loader import Document, Page


def make_document(filename: str, pages: list) -> Document:
    doc = Document(path=Path(filename))
    for number, text in pages:
        doc.pages.append(Page(document=doc, number=number, text=text))
    return doc


def test_tokenize_lowercases_and_splits():
    assert tokenize("Qualidade de SOFTWARE") == ["qualidade", "de", "software"]


def test_search_returns_most_relevant_page():
    doc = make_document(
        "a.pdf",
        [(1, "estudo sobre qualidade de software"), (2, "tema não relacionado")],
    )
    index = PageIndex([doc])
    pages = index.search("qualidade de software")
    assert pages
    assert pages[0].number == 1


def test_search_empty_query_returns_nothing():
    index = PageIndex([])
    assert index.search("") == []
    assert index.is_empty
