# Handshake Lab — modelagem formal

## 1. Problema e escopo

Propomos um protocolo fictício de estabelecimento de conexão por desafio e resposta. O cliente envia `H` (Hello); o servidor envia `C` e um desafio binário não vazio; o cliente envia `R` e a resposta (desafio invertido); o servidor envia `K` e uma confirmação (cópia do desafio); o cliente envia `F` (Finish). O registro contém todos os eventos em ordem. A inversão é didática: não proporciona segurança criptográfica, não é TCP e não representa tráfego real.

Alfabeto de ambos: Σ = {H,C,R,K,F,0,1}. O AP recebe toda a entrada, e, apenas se aceitar, o ALL recebe **a mesma cadeia inteira**. O ALL também pode ser executado independentemente, por isso repete a validação de formato e de conteúdo da resposta. A dependência adicional do fluxo é a igualdade exata entre desafio e confirmação, não só seus tamanhos.

## 2. Linguagem do AP e gramática

L_AP = { HC w R w^rev K v F | w,v ∈ {0,1}+ }, em que w^rev é w invertida.

Definimos a GLC G = (V, Σ, P, S), com V = {S,B,A}, símbolo inicial S e as seguintes produções:

```text
S → H C B K A F
B → 0 B 0 | 1 B 1 | 0 R 0 | 1 R 1
A → 0 A | 1 A | 0 | 1
```

B gera um desafio não vazio e sua inversão em torno de R. A gera uma confirmação binária não vazia arbitrária. Apresentamos a derivação à esquerda da cadeia selecionada para a demonstração (23 caracteres):

```text
S ⇒ HCBKAF
  ⇒ HC1B1KAF
  ⇒ HC10B01KAF
  ⇒ HC101B101KAF
  ⇒ HC1011B1101KAF
  ⇒ HC10110B01101KAF
  ⇒ HC101100R001101KAF
  ⇒ HC101100R001101K1AF
  ⇒ HC101100R001101K10AF
  ⇒ HC101100R001101K101AF
  ⇒ HC101100R001101K1011AF
  ⇒ HC101100R001101K10110AF
  ⇒ HC101100R001101K101100F
```

**Não regular:** supomos, por contradição, que L_AP seja regular e denotamos por p o comprimento de bombeamento. Escolhemos `HC` seguido de p zeros, `R`, p zeros, `K0F`. Para qualquer decomposição xyz com |xy|≤p e |y|>0, y está antes de R. Bombeando y duas vezes, ou duplicamos H/C (formato inválido), ou aumentamos a quantidade de zeros do desafio sem alterar a resposta. Em ambos os casos saímos da linguagem. Contradição com o lema do bombeamento regular. A GLC acima prova que L_AP é livre de contexto.

## 3. Especificação do AP (9 estados)

M = (Q, Σ, Γ, δ, q0, Z, {q8}); Q = {q0,q1,q2,q3,q4,q5,q6,q7,q8}; Γ = {Z,0,1}; Z fundo da pilha. Configuração inicial (q0, posição 0, pilha Z). Topo à esquerda. Aceitação por estado final q8 **e consumo integral da entrada**. Não há transições de q8; qualquer sufixo extra rejeita. Transição indefinida em configuração não final rejeita. A única transição ε é disjunta das transições de leitura no mesmo estado/topo, portanto determinístico.

| Estado | Significado |
|---|---|
| q0 | Espera Hello |
| q1 | Espera Challenge |
| q2 | Exige primeiro bit do desafio |
| q3 | Empilha bits até Response |
| q4 | Compara resposta com topo e desempilha |
| q5 | Pilha retornou a Z; espera K |
| q6 | Exige primeiro bit da confirmação |
| q7 | Lê confirmação até F |
| q8 | Estado final |

Tabela δ(q, leitura, topo) = (destino, substituição do topo). b,t ∈ {0,1}; ε é cadeia vazia. b e t são metavariáveis, não registradores.

| Origem | Leitura | Topo | Destino | Substituição |
|---|---|---|---|---|
| q0 | H | Z | q1 | Z |
| q1 | C | Z | q2 | Z |
| q2 | b | Z | q3 | bZ |
| q3 | b | t | q3 | bt |
| q3 | R | t | q4 | t |
| q4 | b | b | q4 | ε |
| q4 | ε | Z | q5 | Z |
| q5 | K | Z | q6 | Z |
| q6 | b | Z | q7 | Z |
| q7 | b | Z | q7 | Z |
| q7 | F | Z | q8 | Z |

**Correspondência GLC/AP:** após ler w, a pilha contém w^rev Z. A transição em R não modifica a pilha. A cada bit de resposta, só é possível desempilhar um bit igual ao topo. K só é permitido quando a pilha retorna a Z, logo a resposta deve ser exatamente w^rev. Os estados q6/q7 verificam a confirmação não vazia, e q8 exige F final. Toda cadeia da GLC satisfaz essas operações, e toda cadeia aceita tem essa forma. O AP termina porque cada transição consome um símbolo, exceto q4→q5, que pode ocorrer no máximo uma vez; no máximo n+1 transições bem-sucedidas.

## 4. Linguagem sensível ao contexto

L_ALL = { HC w R w^rev K w F | w ∈ {0,1}+ }. O ALL exige correspondência bit a bit, inclusive quando todos os campos têm a mesma quantidade de símbolos. L_ALL é subconjunto próprio de L_AP: `HC101100R001101K101101F` pertence apenas a L_AP.

**Não livre de contexto:** supomos, por contradição, que L_ALL seja livre de contexto e denotamos por p o comprimento do lema do bombeamento para LLC. Consideramos a cadeia `HC 0^p R 0^p K 0^p F` (espaços apenas ilustrativos). Para toda decomposição uvxyz com |vxy|≤p e |vy|>0, bombeamos v e y com expoente 2. Se v ou y contiver um marcador H,C,R,K,F, o marcador será duplicado, invalidando o formato. Caso contrário, v e y contêm somente zeros. A janela vxy não pode alcançar simultaneamente os primeiro e terceiro blocos, pois o bloco intermediário já tem p zeros, além dos separadores. Assim ao menos um dos três blocos não muda, enquanto pelo menos um cresce. A cadeia resultante não pertence a L_ALL. Isso contradiz o lema. A existência do ALL determinístico limitado abaixo prova que L_ALL é sensível ao contexto (caracterização por autômatos linearmente limitados).

## 5. Especificação do ALL (23 estados)

Q = {p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12_0,p12_1,p13_0,p13_1,p14_0,p14_1,p15_0,p15_1,p16,pa,pr}. Σ igual ao AP. Γ = Σ ∪ {x,y,<,>}; x representa 0 já verificado, y representa 1 já verificado. Inicial p0, cabeça na posição 0 (borda esquerda), fita `<entrada>`. Estados terminais pa (aceitação) e pr (rejeição). Movimentos D = direita, E = esquerda, P = parada (apenas terminal). Para n símbolos, n células graváveis e 2 bordas fixas, total n+2. Não há expansão, sobrescrita das bordas, nem acesso fora dos limites. Não há armazenamento externo para recordar o bit: ele é codificado nas variantes de estado com sufixo _0 ou _1.

### Estados e transições

Tabela δ(p, leitura) = (destino, escrita, movimento). `=` significa preservar símbolo lido. b ∈ {0,1}; m(0)=x; m(1)=y. As linhas com b são duas regras distintas, uma por bit, explicitadas no código. Todas as demais combinações em estados não terminais vão para pr, preservando o símbolo e parando (P). pa/pr não têm transições.

| Estado | Significado | Leitura | Destino | Escrita | Movimento |
|---|---|---|---|---|---|
| p0 | Borda inicial | < | p1 | = | D |
| p1 | Hello | H | p2 | = | D |
| p2 | Challenge | C | p3 | = | D |
| p3 | Primeiro bit do desafio | 0,1 | p4 | = | D |
| p4 | Restante do desafio | 0,1 | p4 | = | D |
| p4 | Separador da resposta | R | p5 | = | D |
| p5 | Primeiro bit da resposta | 0,1 | p6 | = | D |
| p6 | Restante da resposta | 0,1 | p6 | = | D |
| p6 | Separador da confirmação | K | p7 | = | D |
| p7 | Primeiro bit da confirmação | 0,1 | p8 | = | D |
| p8 | Restante da confirmação | 0,1 | p8 | = | D |
| p8 | Finish | F | p9 | = | D |
| p9 | Exige fim da entrada | > | p10 | = | E |
| p10 | Retorna à borda esquerda | H,C,R,K,F,0,1,x,y | p10 | = | E |
| p10 | Recomeça rodada | < | p11 | = | D |
| p11 | Ignora cabeçalho e bits marcados | H,C,x,y | p11 | = | D |
| p11 | Marca primeiro bit pendente | b | p12_b | m(b) | D |
| p11 | Não há mais desafio pendente | R | p16 | = | D |
| p12_b | Procura K | 0,1,R,x,y | p12_b | = | D |
| p12_b | Entra na resposta pela direita | K | p13_b | = | E |
| p13_b | Ignora resposta marcada | x,y | p13_b | = | E |
| p13_b | Confere e marca resposta | b | p14_b | m(b) | D |
| p14_b | Volta até K | x,y | p14_b | = | D |
| p14_b | Entra na confirmação pela esquerda | K | p15_b | = | D |
| p15_b | Ignora confirmação marcada | x,y | p15_b | = | D |
| p15_b | Confere e marca confirmação | b | p10 | m(b) | E |
| p16 | Verifica que não sobraram bits | x,y,K,F | p16 | = | D |
| p16 | Fim com todos os bits marcados | > | pa | = | P |

**Invariante:** após i rodadas concluídas, os primeiros i bits do desafio, os últimos i bits da resposta (em ordem inversa) e os primeiros i da confirmação foram marcados. Os bits correspondentes são iguais. Marcadores conservam o valor original. A próxima rodada marca o primeiro bit pendente do desafio, guarda seu valor no controle finito, encontra o último bit pendente da resposta e o primeiro bit pendente da confirmação. Se faltar bit ou houver divergência, a regra padrão rejeita. Se o desafio terminar, p16 rejeita qualquer bit não marcado restante. Logo aceitar equivale exatamente à regra de L_ALL. A validação sintática inicial garante que a interpretação dos delimitadores é única, mesmo no modo independente.

**Terminação:** a fase sintática percorre a fita para a direita uma vez. Cada rodada bem-sucedida marca mais um bit do desafio, nunca desmarca, e realiza um número constante de varreduras delimitadas pelas bordas ou por K. No máximo n rodadas; p16 realiza uma varredura final. Toda transição indefinida rejeita imediatamente. Tempo O(n²) em transições, espaço de trabalho do modelo exatamente n células graváveis. O histórico na GUI não é consultado por nenhum autômato; impressão/animação têm custos adicionais. O AP também é determinístico; não há exploração de caminhos alternativos.

## 6. Demonstração e justificativas

- Válido (23): `HC101100R001101K101100F`.
- AP rejeita (23): `HC101100R101101K101100F`. Após R, topo 0; primeiro bit lido 1, sem transição.
- ALL rejeita (23): `HC101100R001101K101101F`. AP aceita porque K é binária e não vazia. Na sexta rodada, p15_0 encontra 1 (em vez de 0) e transita para pr. Todos os campos têm o mesmo comprimento.

Uma rodada do ALL para a entrada válida: fita inicial `<HC101100R001101K101100F>`; após marcar a primeira trinca e antes da próxima rodada: `<HCy01100R00110yKy01100F>`. O bit 1 foi guardado em p12_1, p13_1, p14_1, p15_1. No final, `<HCyxyyxxRxxyyxyKyxyyxxF>`. O arquivo `rastreio_exemplo.txt` registra a execução das transições reais e permite acompanhar esse processo integralmente.

**Limitação:** reconhecemos que a inversão não constitui uma autenticação segura; a aplicação não implementa rede, temporização nem integridade criptográfica. As varreduras tornam o ALL quadrático em transições. A interface também retém texto de rastreamento para fins didáticos, sem servir de memória de decisão do ALL.

## 7. Fontes teóricas para estudo

- Sipser, Michael. *Introduction to the Theory of Computation*. 3ª ed., Cengage, 2013. Capítulos 1 (linguagens regulares e bombeamento), 2 (GLC, AP e bombeamento de LLC) e 3 (máquinas de Turing, variantes).
- Hopcroft, John E.; Motwani, Rajeev; Ullman, Jeffrey D. *Introduction to Automata Theory, Languages, and Computation*. 3ª ed., Pearson, 2006. Autômatos de pilha, máquinas de Turing e linguagens sensíveis ao contexto.

As referências bibliográficas acima são indicadas para fundamentação e aprofundamento dos conceitos utilizados. A consulta a páginas específicas e a conferência bibliográfica pela equipe permanecem pendentes. As demonstrações apresentadas foram desenvolvidas para as linguagens definidas neste projeto. A verificação de possíveis semelhanças com os exercícios realizados em sala também permanece pendente.
