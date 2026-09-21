# Research: Agente de Pesquisa em Artigos Científicos (PDF)

## Decision Log

### Linguagem / runtime
- **Decision**: Python 3.11+
- **Rationale**: ecossistema maduro para PDF, LLM e web; ampla documentação e
  ferramentas de teste.
- **Alternatives considered**: TypeScript/Node (ecossistema web forte, mas menos
  bibliotecas maduras de extração de PDF com granularidade por página); Go
  (desempenho, mas menos bibliotecas de IA).

### Framework web
- **Decision**: FastAPI + uvicorn
- **Rationale**: leve, assíncrono, serve tanto a API quanto arquivos estáticos
  (interface simples); tipagem e documentação automática de contrato.
- **Alternatives considered**: Flask (mais simples, porém menos assíncrono e sem
  validação tipada); Django (pesado demais para este experimento).

### Abstração de provider LLM
- **Decision**: LiteLLM
- **Rationale**: interface unificada para múltiplos providers (OpenAI, Anthropic,
  Ollama, etc.), atendendo "independência de provider" com configuração por
  provider/API key/endpoint/modelo.
- **Alternatives considered**: SDKs individuais por provider (acopla o agente a um
  fornecedor — viola Princípio III); abstração própria (reinventa a roda).

### Extração de texto de PDF
- **Decision**: PyMuPDF (fitz)
- **Rationale**: extração confiável de texto com granularidade por página,
  necessária para rastrear a evidência (arquivo + página — Princípio I).
- **Alternatives considered**: pdfplumber (bom para tabelas/layout, porém mais
  lento); pypdf (funcionalidade básica).

### Estratégia de recuperação
- **Decision**: índice em memória por página; recuperação lexical (sobreposição de
  termos) das páginas mais relevantes; a LLM responde com citações obrigatórias
  (arquivo + página).
- **Rationale**: ~35 PDFs cabem em memória; evita banco vetorial prematuro
  (Princípio IV); índice por página preserva rastreabilidade (Princípio I).
- **Alternatives considered**: embeddings + banco vetorial (adiado — complexidade
  desnecessária para v1); enviar todo o texto à LLM (pode estourar a janela de
  contexto e perde a granularidade por página).

### Armazenamento
- **Decision**: N/A — arquivos em disco; índice em memória (reconstruído no
  startup).
- **Rationale**: simplicidade; nenhum estado persistente além dos próprios PDFs.
- **Alternatives considered**: banco de dados / vector store (adiado).

### Interface web
- **Decision**: página HTML/JS única servida pelo FastAPI (estática).
- **Rationale**: atende "interface simples e funcional" sem frontend separado.
- **Alternatives considered**: SPA com framework frontend (desnecessário para v1).

### Testes
- **Decision**: pytest + FastAPI TestClient
- **Rationale**: padrão Python; TestClient valida o contrato HTTP sem servidor
  real, adequado a testes unitários e de integração.
- **Alternatives considered**: unittest (padrão, porém menos expressivo).
