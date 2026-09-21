# Quickstart / Guia de Validação

## Pré-requisitos

- Python 3.11+
- Uma LLM acessível por API (provider + chave + endpoint + modelo)
- Um diretório local com até ~35 PDFs de artigos científicos

## Instalação

```bash
python -m venv .venv
.venv/Scripts/activate        # Windows; use source .venv/bin/activate no macOS/Linux
pip install -r requirements.txt
```

## Inicialização

```bash
python -m src.main --provider <provider> --api-key <key> --endpoint <url> --model <model> --directory <path>
```

(Alternativamente via variáveis de ambiente ou arquivo de configuração, conforme
o contrato de configuração em `contracts/config.md`.)

## Acesso

Abra `http://localhost:8000` no navegador.

## Cenários de validação (end-to-end)

1. **Pergunta com resultados**: digite "Quais artigos tratam de qualidade de
   software?" → a resposta lista artigos com `filename`, `excerpt`, `page` (quando
   possível), `relevance` e `citation`.
2. **Verificação de evidência**: abra um PDF listado na página indicada e confirme
   que a evidência existe (conferência no original).
3. **Sem evidência**: faça uma pergunta sem correspondência no acervo → a resposta
   informa que não há evidência suficiente (e, opcionalmente, lista correspondências
   parciais com baixa confiança).
4. **Falha da LLM**: inicie com chave inválida → a interface mostra mensagem
   específica de chave inválida + detalhe do provedor.
5. **Subdiretórios**: inclua PDFs em subpastas → o agente os encontra (descoberta
   recursiva).
6. **Provider diferente**: reinicie com outro provider → o agente funciona sem
   mudança de código.

## Critérios de sucesso verificáveis

- **SC-002**: nenhuma evidência fabricada — todo fato é rastreável a um PDF real.
- **SC-004**: cada resultado pode ser conferido diretamente no PDF original.
- **SC-005**: funciona com pelo menos dois providers trocando apenas a configuração.
