# Implementation Plan: Agente de Pesquisa em Artigos Científicos (PDF)

**Branch**: `001-pdf-research-agent` | **Date**: 2026-09-20 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-pdf-research-agent/spec.md`

## Summary

Serviço local acessível via navegador que permite fazer perguntas em linguagem
natural sobre um acervo local de artigos científicos em PDF e receber respostas
fundamentadas em evidência (arquivo + página + trecho + justificativa de
relevância + citação). A LLM é configurável por provider (provider, chave de API,
endpoint, modelo) e a busca é restrita ao diretório local, percorrido
recursivamente. Implementação em Python com FastAPI, extração de texto por página
via PyMuPDF, abstração de provider via LiteLLM e interface web simples.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: FastAPI + uvicorn (web), LiteLLM (abstração de provider
LLM), PyMuPDF/fitz (extração de texto de PDF por página)

**Storage**: N/A (arquivos em disco; índice em memória reconstruído no startup)

**Testing**: pytest + FastAPI TestClient (unitários e de integração)

**Target Platform**: Desktop local (Windows/macOS/Linux), acessado via navegador
em `localhost`

**Project Type**: web-service (backend + interface web simples)

**Performance Goals**: resposta a uma pergunta em tempo razoável para um único
usuário (latência dominada pela LLM; sem meta rígida para v1)

**Constraints**: busca restrita ao diretório local; sem busca na Internet; sem
mutação dos PDFs; provider-agnóstico; single-user

**Scale/Scope**: único usuário; acervo de até ~35 PDFs

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Evidência Fundamentada (NON-NEGOTIABLE)** — PASS: o design indexa texto por
  página e exige citação de arquivo + página; a LLM é instruída a nunca inventar
  fontes, e a resposta separa fatos de interpretação.
- **II. Escopo Local e Delimitado** — PASS: descoberta/leitura restrita ao
  diretório configurado (recursivo), sem acesso à Internet ou download.
- **III. Independência de Provedor de LLM** — PASS: abstração via LiteLLM;
  provider/API key/endpoint/modelo configuráveis no startup.
- **IV. Simplicidade Deliberada (YAGNI)** — PASS: índice em memória, sem banco
  vetorial e sem embeddings em v1 (adiados); sem frontend separado.
- **V. Desenvolvimento Orientado a Especificação** — PASS: este plano deriva
  diretamente da especificação; requisitos rastreáveis aos FRs.

## Project Structure

### Documentation (this feature)

```text
specs/001-pdf-research-agent/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
│   ├── query-api.md
│   └── config.md
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created here)
```

### Source Code (repository root)

```text
src/
├── main.py              # Aplicação FastAPI + inicialização
├── config.py            # Configuração (provider/API key/endpoint/modelo/diretório)
├── llm/
│   └── provider.py      # Cliente LLM agnóstico (LiteLLM)
├── documents/
│   ├── loader.py        # Descoberta recursiva + extração por página (PyMuPDF)
│   └── index.py         # Índice em memória + recuperação de páginas candidatas
├── agent/
│   └── answerer.py      # Orquestra recuperação + resposta com citações
└── web/
    └── static/          # Interface web simples (HTML/JS)

tests/
├── unit/
└── integration/
```

**Structure Decision**: Projeto único em Python (web-service). Backend FastAPI
servindo também a interface web estática. Sem banco de dados e sem frontend
separado (simplicidade — Princípio IV).

## Complexity Tracking

> Nenhuma violação da constituição a justificar.
