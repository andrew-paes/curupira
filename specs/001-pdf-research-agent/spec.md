# Feature Specification: Agente de Pesquisa em Artigos Científicos (PDF)

**Feature Branch**: `001-pdf-research-agent`

**Created**: 2026-09-20

**Status**: Draft

**Input**: User description: "Serviço de agente de IA para pesquisa semântica sobre um diretório local de artigos científicos em PDF (conforme context.md)."

## Clarifications

### Session 2026-09-20

- Q: Approximately how many PDF documents should the first version be expected to handle while still returning useful, evidence-grounded results? → A: Up to ~35 PDFs.
- Q: When the agent finds no article with sufficient evidence to answer the question, what should it do? → A: Report that no sufficient evidence was found, and optionally list partial matches separately (flagged as low-confidence).
- Q: When the LLM API fails (unavailable, rejected key, error, rate limit, or incomplete response), what should the user see? → A: Distinct messages per failure type with actionable guidance, plus the raw provider error detail (mix of B and D).
- Q: Should the agent also include PDFs located in subdirectories of the configured directory, or only files directly inside that directory? → A: Include subdirectories recursively (search the entire tree under the configured directory).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Perguntar em linguagem natural sobre o acervo (Priority: P1)

O usuário inicia o serviço, acessa a interface web e faz uma pergunta em linguagem natural sobre o conteúdo dos artigos do diretório configurado. O agente examina o acervo e apresenta os artigos mais relevantes, cada um com evidência e justificativa de relevância.

**Why this priority**: É a funcionalidade central que entrega o valor principal do produto — substituir a busca manual em cada PDF por uma pergunta única.

**Independent Test**: Pode ser testado de forma independente iniciando o serviço com um diretório de PDFs, enviando uma pergunta e verificando se a resposta lista artigos relevantes com evidências rastreáveis.

**Acceptance Scenarios**:

1. **Given** o serviço iniciado com um diretório contendo PDFs, **When** o usuário pergunta "Quais artigos tratam de qualidade de software?", **Then** o agente retorna uma lista de artigos relevantes, cada um com nome de arquivo, trecho/síntese e justificativa de relevância.
2. **Given** o mesmo acervo, **When** o usuário pergunta "Há estudos que relacionem especificação de software e IA generativa?", **Then** o agente identifica os artigos que abordam esses temas e explica por que são relevantes.

---

### User Story 2 - Configurar a LLM e o diretório do acervo (Priority: P2)

No momento da inicialização, o usuário informa a configuração da LLM (provider, chave de API, endpoint, modelo) e o diretório local que contém os artigos em PDF. O agente passa a operar sobre esse acervo e com essa LLM, sem ficar preso a um único fornecedor.

**Why this priority**: Sem essa configuração o serviço não pode iniciar; porém, isoladamente, ela apenas prepara o ambiente para a funcionalidade principal (P1).

**Independent Test**: Pode ser testado iniciando o serviço com configurações de providers distintos e verificando que o agente funciona em ambos sem alteração de código.

**Acceptance Scenarios**:

1. **Given** um conjunto de configurações de LLM (provider, chave, endpoint, modelo), **When** o usuário inicia o serviço, **Then** o agente usa a LLM configurada.
2. **Given** um diretório local com PDFs, **When** o usuário inicia o serviço informando esse diretório, **Then** o agente restringe sua busca exclusivamente a esse diretório.

---

### User Story 3 - Verificar a evidência no PDF original (Priority: P3)

Para cada resultado relevante, o usuário consegue localizar e conferir a informação diretamente no artigo original: nome do arquivo, página (quando determinável), trecho/síntese e referência/citação suficiente. A resposta deixa clara a diferença entre o que está efetivamente presente nos artigos e o que é interpretação/síntese da IA.

**Why this priority**: Reforça a confiança nas respostas (princípio não negociável de evidência fundamentada), mas depende da funcionalidade central de busca (P1).

**Independent Test**: Pode ser testado conferindo, para cada resultado, se a evidência apontada existe de fato no arquivo e na página indicada, e se fatos e interpretações estão claramente separados.

**Acceptance Scenarios**:

1. **Given** um resultado relevante, **When** o usuário abre o arquivo indicado na página informada, **Then** encontra a evidência correspondente à resposta.
2. **Given** uma resposta que contém interpretação da IA, **When** o usuário lê a resposta, **Then** consegue distinguir o que está presente no artigo do que é síntese produzida pela IA.

---

### Edge Cases

- Como o sistema informa incerteza quando a página da evidência não pode ser determinada?
- Como são tratados PDFs sem texto extraível (digitalizados ou com conteúdo não selecionável)?
- O que ocorre quando a API da LLM está indisponível, rejeita a chave, retorna erro, atinge limite de uso ou produz resposta incompleta?
- O que acontece quando o acervo é grande demais para enviar todo o conteúdo a cada pergunta?
- Como o sistema impede a LLM de inventar artigos, citações ou páginas?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema DEVE aceitar perguntas em linguagem natural por meio de uma interface web.
- **FR-002**: O sistema DEVE buscar exclusivamente dentro do diretório local configurado; NÃO DEVE buscar na Internet nem baixar artigos automaticamente.
- **FR-003**: Para cada resultado relevante, o sistema DEVE apresentar, quando possível: nome do arquivo PDF, identificação do artigo, trecho ou síntese da informação, página da evidência (quando determinável), explicação da relevância e referência/citação suficiente para consulta ao original.
- **FR-004**: O sistema DEVE distinguir claramente o que está efetivamente presente nos artigos daquilo que é interpretação ou síntese produzida pela IA.
- **FR-005**: O sistema NÃO DEVE inventar artigos, páginas, citações ou evidências; toda afirmação apresentada como fato DEVE ser sustentada pelo conteúdo dos documentos.
- **FR-006**: O sistema DEVE permitir configurar, no momento da inicialização: provider da LLM, chave de API, endpoint e modelo.
- **FR-007**: O sistema DEVE ser independente de fornecedor de LLM, funcionando com diferentes providers sem alteração de código.
- **FR-008**: O sistema DEVE permitir configurar o diretório local que contém o acervo de artigos em PDF e DEVE incluir recursivamente os PDFs localizados em subdiretórios desse diretório.
- **FR-009**: O sistema NÃO DEVE alterar os artigos nem editar o conteúdo original do acervo.
- **FR-010**: O sistema DEVE, quando não houver evidência suficiente para responder, informar claramente que não encontrou evidência suficiente e, opcionalmente, listar separadamente artigos parcialmente relevantes sinalizados como correspondência parcial (baixa confiança).
- **FR-011**: O sistema DEVE informar incerteza quando a página da evidência não puder ser determinada.
- **FR-012**: O sistema DEVE tratar falhas externas da API da LLM (indisponível, chave rejeitada, erro, limite de uso, resposta incompleta) com mensagens distintas por tipo de falha, incluindo orientação sobre como proceder e o detalhe do erro retornado pelo provedor.
- **FR-013**: O sistema DEVE tratar PDFs sem texto extraível (páginas digitalizadas) sem falhar, sinalizando páginas sem texto e prosseguindo com o restante do acervo.

### Key Entities *(include if feature involves data)*

- **Documento (artigo em PDF)**: representa um artigo do acervo; atributos relevantes incluem nome de arquivo, identificação, conteúdo e páginas.
- **Acervo**: o conjunto de documentos no diretório local configurado; delimita o universo de conhecimento do agente.
- **Página**: uma página de um documento, com o texto extraído; unidade de rastreamento da evidência (página).
- **Pergunta**: texto em linguagem natural enviado pelo usuário ao agente.
- **Resultado (evidência)**: referência a um documento e, quando possível, a uma página, acompanhada de trecho/síntese, explicação de relevância e citação; vincula a resposta da IA ao documento original.
- **Resposta**: a resposta agregada do agente, separando fatos de interpretação e indicando incerteza.
- **Configuração da LLM**: parâmetros de inicialização (provider, chave de API, endpoint, modelo) que definem a LLM utilizada.

**Glossário**: "documento", "artigo" e "PDF" referem-se ao mesmo conceito (um arquivo do acervo); usa-se "documento" como termo canônico.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: O usuário consegue enviar uma pergunta e receber uma resposta que lista artigos relevantes com evidências rastreáveis em uma única sessão de uso.
- **SC-002**: 100% das evidências/fatos apresentados são rastreáveis a um documento real do acervo (nenhuma citação, página ou artigo inventado).
- **SC-003**: Para os resultados em que a página é determinável, a resposta informa a página da evidência.
- **SC-004**: O usuário consegue, para cada resultado, abrir o PDF original e conferir a evidência apresentada sem ambiguidade.
- **SC-005**: O serviço funciona com pelo menos dois providers de LLM distintos alterando apenas a configuração, sem mudança de código.

## Assumptions

- O usuário-alvo é um pesquisador acadêmico com um acervo local de PDFs e familiaridade com configuração de chave de API de LLM.
- "Artigo relevante" é interpretado, nesta fase, como um artigo semanticamente relacionado à pergunta (menções explícitas ou conceitos correlatos), sem transformar qualquer ocorrência literal de palavra em resultado relevante; a estratégia exata de busca/relevância será definida no plano técnico.
- O número de resultados retornados segue um padrão pequeno e legível (ex.: 5 artigos); o valor exato pode ser ajustado na especificação detalhada ou no plano.
- Suporte a dispositivos móveis está fora do escopo da primeira versão.
- A interface web é simples e funcional, sem aparência de produto comercial.
- A forma de abstrair providers, a biblioteca de PDF, embeddings, banco vetorial e framework web são decisões adiadas para o plano técnico (conforme constituição, princípio IV).
- O acervo é restrito ao diretório autorizado informado pelo usuário; acesso a outros diretórios não é permitido.
- O acervo esperado para a primeira versão é de até ~35 PDFs; a viabilidade de acervos muito maiores é adiada para além desta versão.
- A identificação do artigo (`article_id`) é derivada, quando possível, dos metadados do PDF (título/autores); na ausência deles, usa-se o nome do arquivo como identificação.

