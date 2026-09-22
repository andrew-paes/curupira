# Minha experiência com Spec-Driven Development

Já utilizo práticas de **Spec-Driven Development (SDD)** há algum tempo e, para este trabalho, a principal percepção que quero compartilhar é que o valor do método não está simplesmente em gerar código a partir de uma especificação. O maior ganho está em **reduzir a quantidade de decisões que a IA precisa inventar durante o desenvolvimento**.

A disciplina apresenta o SDD como um processo em fases, passando por constituição, especificação, planejamento, tarefas e implementação. Na prática, percebi que esse fluxo fica ainda mais eficiente quando acrescento algumas etapas e hábitos.

## 1. Antes do Spec Kit, eu escrevo um `Context.md`

Minha principal boa prática é começar antes mesmo de executar os comandos do Spec Kit.

Eu crio um `Context.md` como se fosse um documento produzido por uma equipe formada por **arquiteto de software, analista de sistemas e analista de requisitos**, depois de uma entrevista detalhada com o cliente.

Nesse arquivo registro, em linguagem natural:

* qual é o problema;
* quem são os usuários;
* o que se espera do sistema;
* exemplos de utilização;
* restrições;
* preocupações;
* hipóteses;
* dúvidas;
* coisas que ainda não sei.

Não tento transformar tudo imediatamente em requisitos formais. A intenção é capturar o máximo possível da **intenção humana antes que a IA comece a tomar decisões de implementação**.

Depois, uso esse contexto como matéria-prima para a constituição e para a especificação.

## 2. `Clarify` é uma etapa que considero essencial

Uma das coisas que mais percebi usando SDD é que a primeira especificação quase nunca está suficientemente clara.

Por isso, uma prática que adotei é executar o **`Clarify` logo após o planejamento** e responder todas as perguntas levantadas pela ferramenta.

Essas perguntas são importantes porque muitas vezes revelam decisões que estavam implícitas na minha cabeça, mas nunca tinham sido escritas.

O interessante é que, depois de responder às primeiras perguntas, ainda costumo executar o `Clarify` novamente antes da implementação. Na segunda rodada normalmente aparecem questões menores, muitas vezes de baixo risco, mas que ajudam a eliminar ambiguidades.

Para mim, isso é um dos melhores exemplos de colaboração entre humano e IA: a IA não está apenas escrevendo código; ela também está funcionando como uma espécie de **revisora de requisitos**.

## 3. Não gosto de tratar uma grande demanda como uma única feature

Outra prática que considero importante é orientar o planejamento para **separar o problema em features bem definidas**.

Quando uma solicitação contém várias funcionalidades, não gosto de deixar o planejamento tratar tudo como uma única grande unidade de trabalho.

Prefiro que ele pense como um analista de requisitos:

> “Quais são as grandes capacidades que compõem este sistema?”

Depois, cada capacidade pode ter seu próprio planejamento, requisitos, tarefas e critérios de validação.

Isso melhora a rastreabilidade e reduz a chance de uma tarefa gigantesca esconder várias decisões diferentes.

## 4. `Analyze` antes de implementar

Outra etapa que passei a valorizar é a **análise dos artefatos antes da implementação**.

Depois que especificação, planejamento e tarefas estão preparados, gosto de pedir uma análise crítica procurando:

* inconsistências;
* ambiguidades;
* requisitos faltantes;
* conflitos entre requisitos;
* tarefas que não correspondem claramente à especificação;
* decisões técnicas sem justificativa.

Esse momento é importante porque ainda estamos em um ponto barato do processo para corrigir problemas. A disciplina reforça que uma boa especificação deve possuir critérios de aceitação observáveis, requisitos não funcionais, casos extremos e nenhuma ambiguidade que dependa apenas do conhecimento de uma pessoa.

## 5. Checklist antes do código

Outra prática que considero muito útil é pedir que a IA gere um **checklist de verificação antes de começar a implementação**.

Esse checklist funciona como uma ponte entre a especificação e a validação.

Antes de escrever código, quero conseguir responder:

> “Como vou saber que esta feature está realmente pronta?”

Isso muda bastante a forma de pensar o desenvolvimento. Em vez de implementar primeiro e descobrir depois se funcionou, eu já tenho definido o que precisa ser verificado.

Cada tarefa deve ser pequena o suficiente para ser conferida contra os critérios de aceitação, e a implementação deve ser testada contra a especificação, e não apenas julgada pela impressão de que “parece funcionar”.

## 6. Durante a implementação, a especificação continua viva

Talvez essa seja a maior mudança de mentalidade que percebi.

Quando descubro durante a implementação que alguma coisa foi mal definida ou que uma decisão precisa mudar, tento não fazer simplesmente um “patch” no código.

Primeiro volto para o artefato correto: solicito alteração no **contexto**, então só depois vou para **especificação, plano ou tarefas**. Depois ajusto a implementação.

Isso mantém os artefatos sincronizados com o sistema real e evita que a documentação passe a contar uma história diferente daquilo que o software realmente faz.

## 7. O que eu aprendi usando SDD

Minha principal conclusão é que **SDD não significa escrever muita documentação antes de programar**.

Significa tornar explícitas as decisões que, em um desenvolvimento assistido por IA, seriam tomadas silenciosamente pelo modelo.

Cada lacuna deixada na especificação vira uma oportunidade para a IA escolher um comportamento por conta própria.

Por isso, para mim, o papel do desenvolvedor muda: ele passa menos tempo apenas dizendo *“escreva este código”* e mais tempo dizendo:

> **“Isto é o que o sistema deve fazer. Estas são as restrições. Estas são as decisões. Agora prove que a implementação está de acordo com isso.”**

Esse é o principal motivo pelo qual considero o SDD especialmente interessante no desenvolvimento com IA. A IA ajuda a gerar planos, decompor tarefas, analisar artefatos e produzir código, mas **a direção e a validação continuam sendo responsabilidades humanas**.

## 8. O que eu quero demonstrar neste trabalho

Meu objetivo não é demonstrar que consigo construir um software grande usando IA.

Quero demonstrar algo mais interessante: **como um problema inicialmente informal pode ser transformado, passo a passo, em intenção, especificação, planejamento, tarefas, implementação e verificação**.

Por isso escolhi construir um pequeno agente de pesquisa sobre artigos científicos. O sistema é apenas o veículo para demonstrar o processo.

Para mim, a pergunta mais importante do SDD é:

> **“Onde está escrita a intenção do sistema quando o código começa a mudar?”**

No SDD, a resposta deve estar no repositório — e não apenas na cabeça do desenvolvedor ou no histórico de uma conversa com a IA.
