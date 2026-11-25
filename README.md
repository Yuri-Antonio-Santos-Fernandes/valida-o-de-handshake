# Handshake Lab

Desenvolvemos uma aplicação didática para a validação de um handshake fictício, utilizando um autômato de pilha (AP) de 9 estados e um autômato linearmente limitado (ALL) de 23 estados. Nossa proposta verifica o conteúdo e a ordem dos dados binários transmitidos, além da estrutura das mensagens do protocolo.

## Executar a interface

Utilizamos Python 3.10 ou superior com Tkinter (normalmente incluído no instalador oficial do Python para Windows e macOS). Em algumas distribuições Linux, é necessária a instalação do pacote `python3-tk` pelo gerenciador de pacotes da distribuição. O projeto não possui dependências de pip.

Para executar a aplicação, é necessário extrair o ZIP, acessar a pasta `handshake_lab` e utilizar o comando:

```sh
python main.py
```

No Windows, o comando `py main.py` também pode ser utilizado. Para iniciar a interface sem uma janela de terminal, as alternativas são `pythonw main.py` ou a abertura do arquivo `iniciar.pyw`, desde que a associação com o Python esteja configurada.

A interface inicia com a cadeia válida. O usuário pode selecionar um dos três exemplos ou inserir uma cadeia sem espaços, escolher o fluxo completo ou a execução isolada do AP ou do ALL e acionar o botão Iniciar. Disponibilizamos três modos de execução: Próximo passo, Automático (com velocidade selecionável) e Executar tudo. O botão Pausar interrompe a animação e Reiniciar restaura a configuração inicial. Posições começam em zero. O destaque azul indica topo/cabeçote; x e y são bits já marcados. O histórico registra as transições reais, não uma simulação visual independente. O ALL só executa após o AP aceitar no fluxo completo.

## Testes

```sh
python testes.py
python gerar_rastreio.py
python testes_interface.py
```

`testes.py` possui 8 aceitas e 8 rejeitadas distintas para cada módulo, todas com no mínimo 18 símbolos, mais entrada vazia e menor cadeia válida de 8 caracteres (exceções deliberadas de caso-limite), 3 integrações e 1 erro de alfabeto. Também compara o comportamento com um oráculo externo por enumeração de todos os campos de até 3 bits. As listas/tuplas de exemplos e oráculos de teste NÃO são usadas pelos reconhecedores. Os resultados das execuções estão registrados em `resultados_testes.txt`.

| Entrada | AP | ALL no fluxo completo |
|---|---|---|
| `HC101100R001101K101100F` | Aceita | Aceita |
| `HC101100R101101K101100F` | Rejeita | Não executa |
| `HC101100R001101K101101F` | Aceita | Rejeita |

## Arquivos

- `ap_handshake.py`: δ(q,símbolo,topo), δ de ε, classe AP e execução.
- `all_handshake.py`: δ(p,símbolo), classe ALL e execução.
- `integracao.py`: encadeamento para testes/uso programático.
- `exemplos.py`: cadeias para demonstração, sem participação na decisão.
- `testes_interface.py` e `resultados_interface.txt`: teste reproduzível da GUI, requer tela gráfica.
- `main.py` e `iniciar.pyw`: interface Tkinter (lógica visual somente).
- `testes.py`, `resultados_testes.txt`, `gerar_rastreio.py`, `rastreio_exemplo.txt`: dados, resultados e rastreio.
- `MODELAGEM.md`: gramática, derivação, especificações, tabelas, provas e terminação.

## Restrições e origem

Na implementação dos reconhecedores, utilizamos exclusivamente a configuração formal: estado, posição e pilha (string) no AP; estado, posição e fita fixa (bytearray) no ALL. A entrada do AP é somente leitura. Não usam regex, contadores de símbolos, listas de configurações, comparação global de campos, DFS ou conjuntos de visitados. As tuplas fixas são resultados das funções de transição. A decisão e a última regra são informações de saída. A GUI mantém histórico de texto, controles e contador de passos para apresentação; nenhum desses dados é lido para aceitar ou rejeitar. As operações físicas da implementação Python podem copiar strings ao alterar a pilha, mas conceitualmente cada transição manipula somente seu topo.

Partimos da proposta de validação de handshake e adotamos um modelo de desafio e resposta baseado na correspondência de sequências binárias. Utilizamos o ChatGPT (OpenAI) como ferramenta de apoio à reformulação da linguagem, à construção do código dos autômatos, ao desenvolvimento da interface, aos testes e à documentação.

Os testes automatizados foram executados no ambiente de apoio, e a interface foi testada em ambiente Linux com display virtual. Nesta etapa, ainda estão pendentes a reprodução dos testes pela equipe em ambiente local, a conferência das transições e o registro das verificações e contribuições individuais no relatório técnico. A comparação com os exercícios realizados em sala também permanece pendente.

Nosso modelo é fictício e tem finalidade didática: não implementa o protocolo TCP nem autenticação criptográfica real. As referências bibliográficas indicadas em `MODELAGEM.md` constituem a base sugerida para aprofundamento teórico e conferência da modelagem.
