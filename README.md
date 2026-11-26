# Handshake Lab

O projeto apresenta a validação didática de um handshake fictício por meio de um autômato de pilha (AP) de 9 estados e um autômato linearmente limitado (ALL) de 23 estados. A modelagem adotada verifica tanto o conteúdo quanto a ordem dos dados binários transmitidos.

## Executar a interface

Python 3.10 ou superior, com Tkinter (incluído normalmente no instalador oficial do Python para Windows e macOS). Em algumas distribuições Linux, é necessária a instalação do pacote `python3-tk` pelo gerenciador da distribuição. Não há dependências de pip.

Após a extração do ZIP, a aplicação pode ser executada na pasta `handshake_lab` com o comando:

```sh
python main.py
```

No Windows, também é possível utilizar `py main.py`. A execução sem janela de terminal pode ser feita com `pythonw main.py` ou pelo arquivo `iniciar.pyw`, caso a associação do Python esteja configurada.

A interface inicia com a cadeia válida e permite selecionar um dos três exemplos ou inserir uma cadeia sem espaços. É possível executar o fluxo completo ou cada autômato isoladamente. Após o acionamento de Iniciar, a execução pode ocorrer por meio das opções Próximo passo, Automático (com velocidade ajustável) ou Executar tudo. A opção Pausar interrompe a animação, enquanto Reiniciar restabelece a configuração inicial. Posições começam em zero. O destaque azul indica topo/cabeçote; x e y são bits já marcados. O histórico registra as transições reais, não uma simulação visual independente. O ALL só executa após o AP aceitar no fluxo completo.

## Testes

```sh
python testes.py
python gerar_rastreio.py
python testes_interface.py
```

Foram definidos, no arquivo `testes.py`, 8 casos de aceitação e 8 de rejeição para cada módulo, totalizando 32 cadeias principais distintas inclusive entre os módulos, todas com pelo menos 18 símbolos e descrições específicas da regra verificada. Seis das oito rejeições do ALL correspondem a cadeias aceitas pelo AP; as duas restantes verificam o reconhecimento independente do ALL. Além desses casos, foram incluídos a entrada vazia e a menor cadeia válida, de 8 caracteres, como casos-limite, 3 testes de integração e 1 teste de erro de alfabeto. O comportamento dos reconhecedores também é comparado com um oráculo externo mediante a enumeração de todos os campos de até 3 bits. As listas e tuplas utilizadas nos exemplos e no oráculo de teste não participam do reconhecimento. Os resultados obtidos encontram-se em `resultados_testes.txt`.

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

Os reconhecedores usam exclusivamente a configuração formal: estado, posição e pilha (string) no AP; estado, posição e fita fixa (bytearray) no ALL. A entrada do AP é somente leitura. Não usam regex, contadores de símbolos, listas de configurações, comparação global de campos, DFS ou conjuntos de visitados. As tuplas fixas são resultados das funções de transição. A decisão e a última regra são informações de saída. A GUI mantém histórico de texto, controles e contador de passos para apresentação; nenhum desses dados é lido para aceitar ou rejeitar. As operações físicas da implementação Python podem copiar strings ao alterar a pilha, mas conceitualmente cada transição manipula somente seu topo.

A proposta tem origem no tema de validação de handshake escolhido pela equipe. Foi utilizado o ChatGPT (OpenAI) como ferramenta de apoio à reformulação da linguagem, à construção do código dos autômatos, à interface gráfica, aos testes e à documentação. Os testes automatizados foram executados no ambiente de apoio, e a interface foi testada em Linux com display virtual. A reprodução dos testes pela equipe em ambiente local, o registro das verificações individuais e das contribuições dos integrantes, bem como a conferência da originalidade em relação aos exercícios de sala, permanecem pendentes de confirmação. O modelo é fictício e não constitui uma implementação do protocolo TCP ou de autenticação criptográfica real. As referências bibliográficas de apoio à fundamentação teórica encontram-se em `MODELAGEM.md`.
