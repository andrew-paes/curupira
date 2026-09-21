# Contrato: API de Pergunta (Query API)

O serviço expõe uma interface HTTP para enviar perguntas e receber respostas
fundamentadas em evidência.

## Endpoint

`POST /ask`

### Request

```json
{
  "question": "Quais artigos tratam de qualidade de software?"
}
```

### Response (200 OK)

```json
{
  "results": [
    {
      "filename": "artigo_a.pdf",
      "article_id": "identificação (quando disponível)",
      "excerpt": "trecho ou síntese da evidência",
      "page": 7,
      "relevance": "por que este artigo é relevante",
      "citation": "referência para consulta ao original",
      "confidence": "alta"
    }
  ],
  "facts": "o que está efetivamente presente nos artigos",
  "interpretation": "síntese/interpretação produzida pela IA (separada)",
  "uncertainty": null
}
```

## Sem evidência suficiente

- `results` vazio (ou lista de correspondências parciais com `confidence: "baixa"`
  e `page` possivelmente ausente) e `uncertainty`/`facts` indicando claramente que
  não há evidência suficiente.

## Erros (falha da LLM)

- Códigos HTTP 4xx/5xx com mensagens distintas por tipo de falha (chave inválida,
  serviço indisponível, limite de uso, erro interno, resposta incompleta),
  incluindo o detalhe do erro retornado pelo provedor.

## Regras

- A busca é restrita ao diretório configurado; nenhuma busca na Internet.
- A resposta nunca inventa arquivo, página ou citação.
