<!--
Sync Impact Report
==================
Version change: (none) → 1.0.0
- Initial adoption: constitution created from context.md
Modified principles: none (initial creation)
Added sections:
  - Core Principles (5 principles)
  - Restrições Não Funcionais e Fora de Escopo
  - Fluxo de Desenvolvimento
  - Governance
Removed sections: none
Follow-up TODOs:
  - RATIFICATION_DATE assumed as 2026-09-20 (no explicit adoption date in repo);
    confirm or correct if a different date is intended.
  - 14 open questions from context.md §14 deferred to the specification phase (not answered here).
-->

# Curupira Constitution

## Core Principles

### I. Evidência Fundamentada (NON-NEGOTIABLE)

Toda resposta do agente DEVE ser rastreável até um documento real do acervo e,
quando possível, até a página de origem. O agente DEVE distinguir claramente
entre:

1. aquilo que está efetivamente presente nos artigos; e
2. aquilo que é interpretação ou síntese produzida pela IA.

O agente NÃO DEVE inventar artigos, páginas, citações ou evidências. Toda
alegação apresentada como fato DEVE ser sustentada pelo conteúdo dos documentos.

Rationale: o valor do serviço depende da confiança de que cada resposta pode ser
verificada diretamente no PDF original; respostas não rastreáveis ou alucinadas
invalidam o propósito do sistema.

### II. Escopo Local e Delimitado

O universo de conhecimento do agente é EXCLUSIVAMENTE o diretório local informado
pelo usuário, contendo artigos científicos em PDF. O sistema NÃO É um buscador
geral da Internet e NÃO DEVE buscar ou baixar novos artigos automaticamente.

Estão fora do escopo da primeira versão: busca na Internet, download automático
de artigos, administração completa de referências, edição de PDFs, substituição
de um gerenciador bibliográfico e funcionamento como sistema de publicação
científica.

Rationale: restringir o universo de conhecimento mantém o experimento pequeno,
verificável e previsível, além de evitar que respostas se misturem a fontes não
controladas.

### III. Independência de Provedor de LLM

O agente DEVE ser configurável quanto à LLM utilizada e NÃO DEVE ficar preso a um
único fornecedor. No momento da inicialização, o serviço DEVE receber: provider,
API key, endpoint e modelo.

A forma exata de abstrair os providers será definida na especificação e no plano
técnico, e não aqui.

Rationale: a capacidade de trocar de provedor sem reescrever o agente é um
requisito explícito do projeto e mantém o experimento portável entre LLMs.

### IV. Simplicidade Deliberada (YAGNI)

A primeira versão DEVE ser deliberadamente pequena e conter somente as
ferramentas necessárias para investigar os arquivos do acervo. Decisões de
implementação (biblioteca de PDF, estratégia de busca, embeddings, banco
vetorial, indexação, framework web e integração de cada provider) NÃO DEVEM ser
fixadas nesta constituição; DEVEM surgir na fase de planejamento, após os
requisitos estarem claros.

Rationale: o projeto é um experimento acadêmico, e complexidade prematura
comprometeria tanto a demonstração do método quanto a clareza do resultado.

### V. Desenvolvimento Orientado a Especificação

Todo o trabalho DEVE seguir o encadeamento:

`Context → Constitution → Specification → Plan → Tasks → Implementation → Verification`

Cada requisito DEVE ser rastreável até uma especificação e confrontável com
critérios de aceitação explícitos. Problemas encontrados durante a implementação
PODEM levar à revisão da especificação, e o código final DEVE ser verificável
contra os critérios definidos.

Rationale: o objetivo acadêmico central do projeto é demonstrar que uma intenção
inicialmente vaga pode ser transformada em especificação, plano, tarefas e
verificação objetiva.

## Restrições Não Funcionais e Fora de Escopo

O agente DEVE preservar a relação entre a resposta da IA e o documento original,
informando: nome do arquivo PDF, identificação do artigo, trecho ou síntese da
informação, página da evidência quando possível, explicação da relevância e
referência/citação suficiente para consulta ao original.

Dificuldades reconhecidas como parte do experimento (e a serem tratadas na
especificação, sem resposta por suposição aqui):

- PDFs com texto não selecionável, mal estruturado, tabelas, figuras, notas de
  rodapé, múltiplas colunas ou páginas digitalizadas;
- localização precisa da evidência (artigo e página);
- distinção entre ocorrência literal e relevância semântica de termos;
- detecção e discussão de alucinação da LLM;
- viabilidade de busca em acervo grande sem enviar todo o conteúdo a cada
  pergunta;
- falhas externas da API da LLM (indisponível, chave rejeitada, erro, limite de
  uso, resposta incompleta).

A interface de acesso DEVE ser uma interface web no navegador, simples e
funcional, que permita enviar uma pergunta, visualizar a resposta e identificar
arquivos, páginas e evidências utilizados.

## Fluxo de Desenvolvimento

As decisões de implementação NÃO DEVEM ser antecipadas nesta constituição; DEVEM
emergir durante as fases de especificação e planejamento. As ferramentas do
agente para a primeira versão são restritas a: descobrir os arquivos do
diretório, abrir/inspecionar um arquivo e ler o conteúdo necessário.

O agente NÃO DEVE alterar os artigos nem editar o conteúdo original do acervo.

As questões em aberto listadas no contexto (§14) — definição de "artigo
relevante", número de resultados, comportamento sem evidência suficiente,
tratamento de incerteza, página indeterminada, PDFs sem texto extraível, tamanho
máximo de arquivo, subdiretórios, restrição de acesso ao diretório autorizado,
prevenção de invenção de citações/páginas, formato da referência, comportamento
em indisponibilidade da API, medição de relevância e critérios de aceitação —
DEVEM ser esclarecidas durante a elaboração da especificação, e não respondidas
por suposição nesta constituição.

## Governance

Esta constituição tem precedência sobre práticas ad-hoc de desenvolvimento.
Qualquer alteração DEVE ser documentada, aprovada e, quando aplicável, acompanhada
de um plano de migração.

- **Procedimento de emenda**: alterações DEVEM passar por revisão e serem
  registradas no relatório de impacto (Sync Impact Report) no topo deste arquivo.
- **Política de versionamento**: `CONSTITUTION_VERSION` segue versionamento
  semântico — MAJOR para remoções/redefinições incompatíveis de princípios,
  MINOR para novos princípios ou expansão material de orientação, PATCH para
  esclarecimentos e correções não semânticas.
- **Revisão de conformidade**: toda especificação, plano e implementação DEVEM
  ser confrontados com os princípios desta constituição; desvios DEVEM ser
  justificados explicitamente.

**Version**: 1.0.0 | **Ratified**: 2026-09-20 | **Last Amended**: 2026-09-20

