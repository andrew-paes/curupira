# Data Model: Agente de Pesquisa em Artigos Científicos (PDF)

## Entities

### Acervo
- **Descrição**: o conjunto de documentos no diretório local configurado (percorrido recursivamente).
- **Relações**: contém zero ou mais Documento.

### Documento (artigo em PDF)
- **Descrição**: um arquivo PDF do acervo.
- **Atributos**:
  - `path`: caminho do arquivo (identificador único)
  - `filename`: nome do arquivo
  - `pages`: lista de páginas com texto extraído
- **Regras**: identificado unicamente pelo caminho; conteúdo imutável (não é
  editado pelo sistema — FR-009).

### Página (Page)
- **Descrição**: uma página de um documento, com texto extraído.
- **Atributos**:
  - `document`: referência ao documento de origem
  - `number`: número da página (base 1)
  - `text`: texto extraído
- **Relações**: pertence a um Documento.

### Pergunta (Query)
- **Descrição**: texto em linguagem natural enviado pelo usuário.
- **Atributos**:
  - `text`: texto da pergunta

### Resultado (Result)
- **Descrição**: um artigo relevante apresentado na resposta.
- **Atributos**:
  - `filename`: nome do arquivo PDF
  - `article_id`: identificação do artigo (quando disponível)
  - `excerpt`: trecho ou síntese da evidência
  - `page`: número da página (quando determinável; ausente quando indeterminável)
  - `relevance`: explicação da relevância
  - `citation`: referência/citação para consulta ao original
  - `confidence`: nível de confiança (alta/média/baixa; baixa para correspondências parciais)

### Resposta (Answer)
- **Descrição**: resposta agregada do agente.
- **Atributos**:
  - `results`: lista de Resultado
  - `facts`: o que está efetivamente presente nos artigos
  - `interpretation`: síntese/interpretação produzida pela IA (separada)
  - `uncertainty`: indicação de incerteza (evidência insuficiente/página indeterminada)

### Configuração da LLM (LLMConfig)
- **Descrição**: parâmetros de inicialização do serviço.
- **Atributos**:
  - `provider`
  - `api_key`
  - `endpoint`
  - `model`
  - `directory`: diretório local do acervo (percorrido recursivamente)

## State transitions

- **Documento**: descoberto (descoberta recursiva) → indexado (texto extraído por
  página) → disponível para recuperação. Somente leitura; sem estado de mutação.
- **Pergunta → Resposta**: recebida → recuperação de páginas candidatas → resposta
  da LLM com citações → apresentação. Sem persistência entre sessões.

## Validation rules (derivadas dos requisitos)

- Todo Resultado DEVE conter `filename` e `citation` (FR-003).
- `page` DEVE ser preenchido quando determinável; ausente quando indeterminável
  (FR-011).
- A Resposta DEVE separar `facts` de `interpretation` (FR-004) e NÃO fabricar
  evidências (FR-005).
- Sem evidência suficiente → a resposta indica isso; correspondências parciais
  podem vir como Resultado com `confidence: "baixa"` (FR-010).
