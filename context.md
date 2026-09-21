# Context.md

## 1. Contexto

Quero construir um pequeno serviço que funcione como um agente de IA para
auxiliar a pesquisa acadêmica.

A ideia surgiu de uma necessidade real: tenho um diretório local contendo
diversos artigos científicos em PDF e gostaria de poder fazer perguntas sobre
esse conjunto de documentos sem precisar abrir os arquivos individualmente,
lembrar onde cada informação está ou fazer manualmente a busca em cada artigo.

Quero que o sistema funcione como uma espécie de mecanismo de pesquisa
semântico privado para o meu próprio acervo de artigos.

O sistema não deve ser um buscador geral da Internet. O seu universo de
conhecimento, para esta primeira versão, será um diretório local informado
pelo usuário contendo artigos científicos em PDF.

---

## 2. O que eu quero conseguir fazer

Quero iniciar o serviço informando as configurações necessárias para utilizar
uma LLM de minha escolha.

Entre essas configurações estão:

- minha chave de API;
- o provider da LLM;
- o endereço (endpoint/URL) da API;
- o modelo que será utilizado;
- o diretório local que contém meu acervo de artigos científicos.

Depois de iniciado, quero poder acessar o serviço por meio de uma interface
web no navegador.

Na interface, quero fazer perguntas em linguagem natural sobre os artigos
existentes no diretório.

Por exemplo:

> "Quais artigos do meu repositório apresentam estudos relacionados à
> qualidade de software?"

Ou:

> "Encontre estudos que relacionem especificação de software e uso de IA
> generativa."

Ou ainda:

> "Quais artigos discutem empiricamente os efeitos de ferramentas de IA
> sobre a produtividade de desenvolvedores?"

A expectativa é que o agente examine o meu acervo e apresente os artigos mais
relevantes para a pergunta.

---

## 3. O que espero receber como resposta

Não quero apenas uma lista de nomes de arquivos.

Quero uma resposta que permita localizar e verificar a informação no artigo
original.

Para cada resultado relevante, espero encontrar, quando possível:

- nome do arquivo PDF;
- identificação do artigo;
- trecho ou síntese da informação encontrada;
- indicação da página do PDF onde a evidência aparece;
- explicação de por que aquele artigo é relevante para a pergunta;
- referência/citação suficiente para que eu possa consultar o artigo original.

A resposta deve deixar clara a diferença entre:

1. aquilo que está efetivamente presente nos artigos;
2. aquilo que é uma interpretação ou síntese produzida pela IA.

O usuário deve conseguir voltar ao PDF e conferir a evidência apresentada.

---

## 4. Exemplo de uso

Imagino uma experiência parecida com esta:

Usuário:

> "No meu repositório de artigos científicos, encontre estudos
> relacionados à qualidade de software que utilizem IA generativa."

Agente:

> Encontrei 5 artigos potencialmente relevantes.
>
> 1. artigo_a.pdf
>    - Relevância: alta
>    - Evidência: o estudo investiga...
>    - Página: 7
>
> 2. artigo_b.pdf
>    - Relevância: alta
>    - Evidência: os autores analisam...
>    - Página: 12
>
> 3. artigo_c.pdf
>    - Relevância: média
>    - Evidência: ...
>    - Página: 4

A intenção não é apenas "conversar com uma IA", mas utilizar a IA para
navegar e pesquisar um conjunto delimitado de documentos científicos.

---

## 5. Comportamento esperado do agente

O agente deve ser capaz de:

- receber uma pergunta do usuário;
- consultar os documentos disponíveis no diretório configurado;
- identificar quais documentos podem ser relevantes;
- ler o conteúdo necessário dos documentos;
- comparar informações encontradas em diferentes artigos;
- produzir uma resposta sintetizada;
- apontar para os arquivos utilizados como evidência;
- informar a página da evidência quando ela puder ser determinada;
- evitar apresentar como fato algo que não esteja sustentado pelos documentos.

O agente deve trabalhar sobre o acervo fornecido pelo usuário e não deve
inventar artigos, páginas, citações ou evidências.

---

## 6. Ferramentas do agente

Quero que o agente tenha ferramentas para trabalhar com os documentos locais.

A primeira versão deve ser deliberadamente pequena e possuir somente as
ferramentas necessárias para investigar os arquivos.

A intenção atual é disponibilizar ferramentas para:

- descobrir os arquivos disponíveis no diretório;
- abrir/inspecionar um arquivo;
- ler o conteúdo necessário de um arquivo.

Não quero que o agente altere os artigos ou edite o conteúdo original do
acervo.

As decisões exatas sobre como essas ferramentas funcionarão devem ser
definidas posteriormente na especificação e no plano técnico, e não aqui.

---

## 7. Interface

Quero que o serviço possa ser acessado por um navegador web.

A interface inicial pode ser simples.

O objetivo principal da interface é permitir:

1. informar uma pergunta;
2. enviar a pergunta ao agente;
3. visualizar a resposta;
4. identificar quais arquivos foram utilizados;
5. localizar as páginas e evidências apresentadas.

A interface não precisa parecer um produto comercial.

Para este projeto, prefiro uma interface pequena e funcional, que permita
demonstrar claramente o comportamento do agente.

---

## 8. Configuração da LLM

Quero poder escolher a LLM utilizada pelo agente.

O serviço deve receber, no momento da inicialização, informações como:

- provider;
- API key;
- endpoint;
- modelo.

Não quero que o agente fique preso a um único fornecedor de LLM.

A intenção é que o mesmo agente possa funcionar com diferentes providers,
desde que eles possam ser utilizados através da configuração suportada pelo
serviço.

A forma exata de abstrair os providers será decidida posteriormente.

---

## 9. Limites e escopo inicial

Este projeto é um experimento acadêmico sobre desenvolvimento orientado por
especificação.

Portanto, não quero construir um sistema completo de gerenciamento de
referências ou uma plataforma acadêmica.

A primeira versão deve se concentrar no seguinte problema:

> Fazer perguntas em linguagem natural sobre um conjunto local de artigos
> científicos em PDF e retornar os documentos e evidências mais relevantes
> para responder à pergunta.

Ficam inicialmente fora do escopo:

- buscar novos artigos na Internet;
- fazer download automático de artigos;
- administrar referências bibliográficas completas;
- editar os PDFs;
- substituir um gerenciador bibliográfico;
- funcionar como um sistema de publicação científica;
- treinar uma LLM própria.

Esses itens podem ser considerados futuramente, mas não fazem parte do
primeiro experimento.

---

## 10. Dificuldades que eu já imagino

Não quero esconder as dificuldades do problema. Pelo contrário, gostaria que
elas fizessem parte do experimento.

Algumas questões que imagino que precisarão ser resolvidas:

### PDFs

Artigos científicos podem possuir:

- texto selecionável;
- texto mal estruturado;
- tabelas;
- figuras;
- notas de rodapé;
- múltiplas colunas;
- páginas digitalizadas;
- conteúdo que não pode ser extraído de maneira simples.

### Localização da evidência

Não basta encontrar uma informação.

Quero saber em qual artigo e, quando possível, em qual página ela aparece.

Isso exige que a relação entre resposta da IA e documento original seja
preservada.

### Relevância

Uma pergunta pode possuir diferentes interpretações.

Por exemplo, "qualidade de software" pode aparecer explicitamente em um
artigo ou pode ser tratada através de conceitos relacionados.

O sistema precisa lidar com essa diferença sem transformar qualquer ocorrência
de uma palavra em um resultado relevante.

### Alucinação

A LLM pode afirmar que determinada informação está em um artigo quando isso
não é verdade.

Quero que o projeto permita detectar e discutir esse tipo de problema.

### Acervo grande

Se houver muitos PDFs, pode não ser viável enviar todo o conteúdo de todos
os artigos para a LLM a cada pergunta.

Quero descobrir, durante o desenvolvimento, quais estratégias são adequadas
para pesquisar um conjunto de documentos maior sem tornar o sistema
desnecessariamente complexo para este experimento.

### Falhas externas

A API da LLM pode:

- estar indisponível;
- rejeitar a chave;
- retornar erro;
- atingir limites de uso;
- produzir uma resposta incompleta.

O comportamento esperado nesses casos precisa ser especificado.

---

## 11. O que não quero decidir ainda

Neste momento, não quero escolher antecipadamente todos os detalhes de
implementação.

Por exemplo, ainda não quero fixar:

- qual biblioteca será utilizada para processar PDFs;
- qual estratégia de busca será utilizada;
- se haverá embeddings;
- se haverá banco vetorial;
- como o conteúdo será indexado;
- qual framework web será utilizado;
- como exatamente cada provider será integrado.

Quero que essas decisões surjam na fase de planejamento, depois que os
requisitos estiverem claros.

---

## 12. Objetivo acadêmico do projeto

Além de produzir um software pequeno e útil, quero utilizar este projeto
para demonstrar o processo de Spec-Driven Development.

Quero conseguir mostrar que:

1. uma intenção inicialmente vaga pode ser transformada em uma especificação;
2. a especificação pode gerar um plano técnico;
3. o plano pode ser decomposto em tarefas;
4. cada tarefa pode ser implementada e verificada;
5. problemas encontrados durante a implementação podem levar à revisão da
   especificação;
6. o código final pode ser confrontado com critérios de aceitação explícitos.

O foco do trabalho não é construir o agente mais avançado possível.

O foco é demonstrar, através de um problema real e interessante, como a
especificação pode orientar o desenvolvimento assistido por IA.

---

## 13. Resultado que considero satisfatório

Ao final, quero conseguir abrir o serviço no navegador, fazer uma pergunta
sobre meu acervo de artigos e receber uma resposta que:

- identifique artigos potencialmente relevantes;
- explique por que são relevantes;
- apresente evidências;
- informe o arquivo de origem;
- informe a página quando possível;
- permita conferir a informação diretamente no PDF.

Mais importante, quero conseguir mostrar no repositório todo o caminho entre
a intenção inicial e a implementação:

`Context → Constitution → Specification → Plan → Tasks → Implementation → Verification`

---

## 14. Questões em aberto para a próxima etapa

Estas questões não devem ser respondidas por suposição no contexto inicial.
Devem ser esclarecidas durante a elaboração da especificação:

1. Como definir "artigo relevante"?
2. Quantos resultados devem ser retornados?
3. Como o agente deve se comportar quando não encontrar evidência suficiente?
4. Como informar incerteza?
5. O que fazer quando a página não puder ser determinada?
6. Como tratar PDFs sem texto extraível?
7. Qual tamanho máximo de arquivo deve ser suportado?
8. O agente pode ler subdiretórios?
9. Como restringir o acesso exclusivamente ao diretório autorizado?
10. Como evitar que a LLM invente citações ou páginas?
11. Qual formato deve ter a referência apresentada ao usuário?
12. O que deve acontecer quando a API configurada estiver indisponível?
13. Como medir se os resultados encontrados são realmente relevantes?
14. Quais critérios de aceitação permitirão verificar objetivamente cada
    comportamento?

Essas perguntas representam, intencionalmente, o ponto de partida para a
próxima fase do trabalho: transformar este contexto em uma especificação
precisa.
