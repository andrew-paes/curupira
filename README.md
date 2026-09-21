# Curupira

## AGL11091 - Tendências Em Engenharia De Software - Turma U (26/2)

Aula - Spec Driven Development

---

## O que é

Agente de IA que responde perguntas em linguagem natural sobre um acervo local de
artigos científicos em PDF, com respostas fundamentadas em evidência (arquivo +
página + trecho + relevância + citação). A LLM é configurável por provider e a
busca é restrita ao diretório local, percorrido recursivamente.

## Como usar

### Pré-requisitos

- Python 3.11+
- Uma LLM acessível por API (provider + chave + endpoint + modelo)
- Um diretório com artigos científicos em PDF (até ~35 para esta versão)

### Instalação

```bash
python -m venv .venv
.venv/Scripts/activate        # Windows; use source .venv/bin/activate no macOS/Linux
pip install -r requirements.txt
```

### Inicialização

```bash
python -m src.main --provider <provider> --api-key <key> --endpoint <url> --model <model> --directory <path>
```

(Alternativamente via variáveis de ambiente `CURUPIRA_PROVIDER`,
`CURUPIRA_API_KEY`, `CURUPIRA_ENDPOINT`, `CURUPIRA_MODEL`, `CURUPIRA_DIRECTORY`.)

### Acesso

Abra `http://localhost:8000` no navegador e faça uma pergunta.

### Testes

```bash
pytest
```

### Documentação do processo

- Especificação, plano, tarefas e design: `specs/001-pdf-research-agent/`


