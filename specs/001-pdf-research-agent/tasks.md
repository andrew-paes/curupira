---
description: "Task list for feature implementation"
---

# Tasks: Agente de Pesquisa em Artigos Científicos (PDF)

**Input**: Design documents from `specs/001-pdf-research-agent/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks included to satisfy plan.md "Testing" (pytest + FastAPI TestClient) and constitution Principle V (verifiable against criteria).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (Python + FastAPI)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure per plan.md (`src/`, `src/llm/`, `src/documents/`, `src/agent/`, `src/web/static/`, `tests/unit/`, `tests/integration/`)
- [ ] T002 Initialize Python project with dependencies in `requirements.txt` (fastapi, uvicorn, litellm, pymupdf, pytest, httpx)
- [ ] T003 [P] Create `.gitignore` and venv setup instructions in `README.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Implement configuration management in `src/config.py` (load provider, api_key, endpoint, model, directory from CLI args/env vars)
- [ ] T005 [P] Implement LLM provider abstraction in `src/llm/provider.py` (LiteLLM wrapper; configurable provider/endpoint/model)
- [ ] T006 [P] Implement document discovery + page-level text extraction in `src/documents/loader.py` (recursive subdirectory traversal; PyMuPDF per-page text; read-only — no write to the acervo; local directory only; flag pages with no extractable text instead of failing)
- [ ] T007 Implement FastAPI app skeleton + startup wiring in `src/main.py` (load config, serve static files, stub `POST /ask`)

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Perguntar em linguagem natural sobre o acervo (Priority: P1) 🎯 MVP

**Goal**: O usuário faz uma pergunta e recebe os artigos mais relevantes com evidência e justificativa de relevância.

**Independent Test**: Iniciar o serviço com um diretório de PDFs, enviar uma pergunta e verificar que a resposta lista artigos relevantes com `filename`, `excerpt` e `relevance`.

### Implementation for User Story 1

- [ ] T008 [P] [US1] Implement in-memory page index + lexical retrieval in `src/documents/index.py`
- [ ] T009 [US1] Implement answerer in `src/agent/answerer.py` (retrieve candidate pages, prompt LLM, return results with filename/excerpt/relevance) — depends on T008
- [ ] T010 [US1] Implement `POST /ask` endpoint in `src/main.py` per `contracts/query-api.md` — depends on T009
- [ ] T011 [US1] Implement simple web UI in `src/web/static/index.html` (submit question, render results)
- [ ] T021 [P] [US1] Integration test for `POST /ask` contract in `tests/integration/test_ask.py` — depends on T010
- [ ] T022 [P] [US1] Unit test for page index + lexical retrieval in `tests/unit/test_index.py` — depends on T008

---

## Phase 4: User Story 2 - Configurar a LLM e o diretório do acervo (Priority: P2)

**Goal**: Configuração da LLM (provider, chave, endpoint, modelo) e do diretório na inicialização, com independência de fornecedor.

**Independent Test**: Iniciar o serviço com configurações de providers distintos e verificar que o agente funciona em ambos sem alteração de código.

### Implementation for User Story 2

- [ ] T012 [US2] Add config validation + startup error handling in `src/config.py` (missing/invalid directory, missing API key, unknown provider)
- [ ] T013 [US2] Map LLM API failures to distinct user-facing messages per failure type (with raw provider detail) in `src/llm/provider.py` and `/ask` responses
- [ ] T014 [US2] Verify provider-agnostic behavior per `quickstart.md` (two providers via configuration only, no code change)

---

## Phase 5: User Story 3 - Verificar a evidência no PDF original (Priority: P3)

**Goal**: Cada resultado permite localizar e conferir a evidência no PDF (página, citação) e distingue fato de interpretação, sem fabricar evidências.

**Independent Test**: Para cada resultado, abrir o PDF na página indicada e confirmar a evidência; verificar a separação entre fatos e interpretação.

### Implementation for User Story 3

- [ ] T015 [P] [US3] Add page tracking to results (page number when determinable) in `src/agent/answerer.py` and response model
- [ ] T016 [P] [US3] Add facts vs interpretation separation to the response in `src/agent/answerer.py` (`facts` vs `interpretation`)
- [ ] T017 [US3] Add no-evidence handling in `src/agent/answerer.py` (report no sufficient evidence; list partial matches with low confidence) — depends on T015, T016
- [ ] T018 [US3] Add citation format + no-fabrication guardrails (prompt constraints) in `src/agent/answerer.py`
- [ ] T023 [P] [US3] Unit test for no-fabrication + facts/interpretation separation in `tests/unit/test_answerer.py` — depends on T015, T016, T018

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T019 [P] Run `quickstart.md` validation scenarios and fix issues
- [ ] T020 [P] Update `README.md` with usage instructions (install, startup, access)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational - builds on config/LLM provider (foundational); independent of US1/US3
- **User Story 3 (P3)**: Depends on US1 (enhances the answerer) - extends `src/agent/answerer.py`

### Within Each User Story

- Index before answerer (US1)
- Answerer before endpoint (US1)
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- US1 and US2 can proceed in parallel after Foundational (independent files)
- Utilities within a story marked [P] can run in parallel
- T015 and T016 (US3) are independent and can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch independent US1 tasks together:
Task: "Implement in-memory page index + lexical retrieval in src/documents/index.py"  # T008 [P]
# Then, after T008:
Task: "Implement answerer in src/agent/answerer.py"  # T009 (depends on T008)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Q&A loop)
   - Developer B: User Story 2 (config/provider)
3. US3 follows US1 (enhances the answerer)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

