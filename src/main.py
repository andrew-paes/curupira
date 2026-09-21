"""Ponto de entrada da aplicação FastAPI do Curupira."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .agent.answerer import Answerer
from .config import Config, ConfigError
from .documents.index import PageIndex
from .documents.loader import load_acervo
from .llm.provider import LLMClient, LLMConfig, LLMError

STATIC_DIR = Path(__file__).resolve().parent / "web" / "static"

_LLM_FAILURE_STATUS = {
    "invalid_key": 401,
    "rate_limit": 429,
    "unavailable": 503,
    "incomplete": 502,
    "error": 500,
}


class AskRequest(BaseModel):
    question: str


def build_app(config: Config, answerer: Answerer | None = None) -> FastAPI:
    """Constrói a aplicação; `answerer` pode ser injetado para testes."""
    if answerer is None:
        llm = LLMClient(LLMConfig(config.provider, config.api_key, config.endpoint, config.model))
        documents = load_acervo(config.directory_path)
        index = PageIndex(documents)
        answerer = Answerer(index, llm)

    app = FastAPI(title="Curupira - Agente de Pesquisa em Artigos Científicos")

    @app.post("/ask")
    def ask(request: AskRequest):
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Pergunta vazia.")
        try:
            answer = answerer.answer(request.question)
        except LLMError as exc:
            status = _LLM_FAILURE_STATUS.get(exc.kind, 500)
            return JSONResponse(
                status_code=status,
                content={"error": exc.kind, "message": exc.message, "raw": exc.raw},
            )
        return answer.to_dict()

    @app.get("/")
    def index():
        return FileResponse(STATIC_DIR / "index.html")

    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    return app


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Curupira - agente de pesquisa em PDFs")
    parser.add_argument("--provider", default=os.environ.get("CURUPIRA_PROVIDER", ""))
    parser.add_argument("--api-key", default=os.environ.get("CURUPIRA_API_KEY", ""))
    parser.add_argument("--endpoint", default=os.environ.get("CURUPIRA_ENDPOINT", ""))
    parser.add_argument("--model", default=os.environ.get("CURUPIRA_MODEL", ""))
    parser.add_argument("--directory", default=os.environ.get("CURUPIRA_DIRECTORY", ""))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = Config(
        provider=args.provider,
        api_key=args.api_key,
        endpoint=args.endpoint,
        model=args.model,
        directory=args.directory,
    )
    try:
        config.validate()
    except ConfigError as exc:
        raise SystemExit(f"Erro de configuração: {exc}") from exc

    import uvicorn

    app = build_app(config)
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
