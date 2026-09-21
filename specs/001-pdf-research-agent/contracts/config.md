# Contrato: Configuração (Startup)

Parâmetros informados na inicialização do serviço.

## Parâmetros

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| provider | string | sim | fornecedor da LLM |
| api_key | string | sim | chave de API |
| endpoint | string | sim | URL da API |
| model | string | sim | modelo a utilizar |
| directory | string | sim | diretório local do acervo (percorrido recursivamente) |

## Regras

- O acervo é lido recursivamente a partir de `directory` (inclui subdiretórios).
- A chave de API não é exposta na interface; é usada apenas nas chamadas à LLM.
- Provider-agnóstico: o mesmo agente funciona com providers diferentes alterando
  apenas a configuração, sem mudança de código.
