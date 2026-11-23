import sys

# Definição formal
ALFABETO = set("()[]#saf")                       # Σ (alfabeto de entrada)
ALFABETO_PILHA = {"Z", "P", "C"}                 # Γ (alfabeto da pilha)
ESTADOS = ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "qf"]
INICIAL = "q0"
FINAIS = {"qf"}
FUNDO = "Z"

DELTA = {}


def _t(q, lido, topo, p, empilha):
    DELTA.setdefault((q, lido, topo), []).append((p, empilha))


# q0: exige abrir algo (estrutura não vazia)
_t("q0", "(", FUNDO, "q1", "P" + FUNDO)
_t("q0", "[", FUNDO, "q1", "C" + FUNDO)

# q1: dentro de um aninhamento (topo P ou C)
for topo in ("P", "C"):
    _t("q1", "(", topo, "q1", "P" + topo)        # empilha P
    _t("q1", "[", topo, "q1", "C" + topo)        # empilha C
_t("q1", ")", "P", "q1", "")                     # desempilha P
_t("q1", "]", "C", "q1", "")                     # desempilha C
_t("q1", "", FUNDO, "q2", FUNDO)                 # ε: pilha voltou ao fundo -> balanceado

# q2: balanceado. Pode abrir outro bloco ou ler '#'
_t("q2", "(", FUNDO, "q1", "P" + FUNDO)
_t("q2", "[", FUNDO, "q1", "C" + FUNDO)
_t("q2", "#", FUNDO, "q3", FUNDO)

# q3 - q6: blocos s, a, f (cada um não vazio, nessa ordem)
_t("q3", "s", FUNDO, "q4", FUNDO)                
_t("q4", "s", FUNDO, "q4", FUNDO)
_t("q4", "a", FUNDO, "q5", FUNDO)    
_t("q5", "a", FUNDO, "q5", FUNDO)
_t("q5", "f", FUNDO, "q6", FUNDO)            
_t("q6", "f", FUNDO, "q6", FUNDO)
_t("q6", "", FUNDO, "qf", FUNDO)                 # ε: encerra (só valido se a entrada acabou)


class ErroAlfabeto(ValueError):
    """Símbolo fora do alfabeto de entrada."""


def checar_alfabeto(entrada):
    for i, c in enumerate(entrada):
        if c not in ALFABETO:
            raise ErroAlfabeto(
                f"símbolo {c!r} na posição {i} não pertence ao alfabeto "
                f"{{{', '.join(sorted(ALFABETO))}}}"
            )


# Simulador
def simular(entrada):
    """Retorna (aceita, caminho, motivo).
    caminho = lista de (estado, pos, pilha, regra_aplicada)."""
    checar_alfabeto(entrada)

    inicial = (INICIAL, 0, FUNDO, "configuração inicial")
    a_explorar = [[inicial]]                     # pilha de caminhos (DFS)
    visitadas = set()
    melhor = [inicial]                           # ramo que foi mais longe (para explicar rejeição)

    while a_explorar:
        caminho = a_explorar.pop()
        q, pos, pilha, _ = caminho[-1]
        if (q, pos, pilha) in visitadas:
            continue
        visitadas.add((q, pos, pilha))

        if (pos, len(caminho)) >= (melhor[-1][1], len(melhor)):
            melhor = caminho

        if q in FINAIS and pos == len(entrada):
            return True, caminho, "estado final com entrada consumida"

        topo = pilha[0]
        opcoes = []
        if pos < len(entrada):                   # transições que leem símbolo
            for p, emp in DELTA.get((q, entrada[pos], topo), []):
                regra = f"δ({q}, {entrada[pos]}, {topo}) = ({p}, {emp or 'ε'})"
                opcoes.append((p, pos + 1, emp + pilha[1:], regra))
        for p, emp in DELTA.get((q, "", topo), []):   # transições ε
            regra = f"δ({q}, ε, {topo}) = ({p}, {emp or 'ε'})"
            opcoes.append((p, pos, emp + pilha[1:], regra))
        for cfg in reversed(opcoes):
            a_explorar.append(caminho + [cfg])

    q, pos, pilha, _ = melhor[-1]
    if pos == len(entrada):
        motivo = f"entrada consumida, mas o estado {q} não é final"
    else:
        motivo = (f"sem transição em {q} para o símbolo {entrada[pos]!r} "
                  f"(posição {pos}) com topo {pilha[0]}")
    return False, melhor, motivo


def imprimir_rastreio(entrada, caminho):
    print(f"  {'passo':<5} {'estado':<6} {'pos':<4} {'restante':<22} {'pilha(topo→)':<14} regra")
    for i, (q, pos, pilha, regra) in enumerate(caminho):
        restante = entrada[pos:] or "ε"
        print(f"  {i:<5} {q:<6} {pos:<4} {restante:<22} {pilha:<14} {regra}")


def validar(entrada, rastreio=True):
    print(f"Entrada: {entrada!r} (tamanho {len(entrada)})")
    try:
        aceita, caminho, motivo = simular(entrada)
    except ErroAlfabeto as e:
        print(f"  ERRO: {e}. A entrada não foi processada pelo AP.")
        return None
    if rastreio:
        imprimir_rastreio(entrada, caminho)
    print(f"  Decisão do AP: {'ACEITA' if aceita else 'REJEITA'} ({motivo})")
    return aceita


# Testes
# (entrada, esperado, regra verificada)
ACEITAS = [
    ("([])[()]#sssaaafff",         "estrutura balanceada + blocos s,a,f (3,3,3)"),
    ("(()())[[]]#ssaafff",         "aninhamento misto + quantidades diferentes (2,2,3)"),
    ("[()[]]#sssssaaaaaffff",      "bloco único misto + quantidades (5,5,4)"),
    ("((((()))))#sssaaafff",       "aninhamento profundo (5 níveis)"),
    ("()()()()()#ssaaaff",         "cinco blocos sequenciais ()"),
    ("[[[]]][[]]#sssaaaaf",        "colchetes aninhados + quantidades (3,4,1)"),
    ("([()])([()])#saaaffff",      "dois blocos mistos + quantidades (1,3,4)"),
    ("[]([])[()]#ssssaaaafff",     "três blocos de tipos diferentes + (4,4,3)"),
    ("()#saf",                     "CASO-LIMITE: menor cadeia aceita"),
]
REJEITADAS = [
    ("((())[[]]#sssaaafff",        "estrutura com parêntese aberto sem fechar"),
    ("([)](())#sssaaafff",         "fechamento de tipo errado (')' com topo C)"),
    ("(())))[[]]#sssaaafff",       "fecha mais do que abriu"),
    ("([])[()]sssaaaffff",         "falta o separador #"),
    ("([])[()]#fffaaasss",         "blocos fora de ordem (f antes de s)"),
    ("([])[()]#sssfffffff",        "bloco a vazio"),
    ("#sssssaaaaaffffffff",        "estrutura vazia antes do #"),
    ("([])[()]#sssaaafffsss",      "símbolos depois do bloco f"),
    ("",                           "CASO-LIMITE: entrada vazia"),
]
FORA_DO_ALFABETO = "([])[()]#sssaaaxfff"


def rodar_testes(mostrar_rastreio=False):
    todos = [(e, True, r) for e, r in ACEITAS] + [(e, False, r) for e, r in REJEITADAS]
    assert len({e for e, _, _ in todos}) == len(todos), "cadeias de teste devem ser distintas"
    assert all(set(e) <= ALFABETO for e, _, _ in todos), "só símbolos do alfabeto"

    print(f"{'entrada':<26} {'esperado':<9} {'obtido':<9} {'ok':<4} regra verificada")
    falhas = 0
    for entrada, esperado, regra in todos:
        aceita, caminho, _ = simular(entrada)
        ok = aceita == esperado
        falhas += not ok
        nome = lambda b: "ACEITA" if b else "REJEITA"
        print(f"{entrada!r:<26} {nome(esperado):<9} {nome(aceita):<9} "
              f"{'OK' if ok else 'FALHA':<4} {regra}")
        if mostrar_rastreio:
            imprimir_rastreio(entrada, caminho)
    print(f"\n{len(todos) - falhas}/{len(todos)} testes OK "
          f"({len(ACEITAS)} aceitas, {len(REJEITADAS)} rejeitadas)")

    print("\nTeste de símbolo fora do alfabeto:")
    validar(FORA_DO_ALFABETO)
    return falhas == 0


def main(argv):
    if "--testes" in argv:
        return 0 if rodar_testes("--rastreio" in argv) else 1
    if argv:
        validar(argv[0])
        return 0
    print("Modo interativo. Digite uma cadeia (ENTER = cadeia vazia, 'sair' encerra).")
    while True:
        try:
            linha = input("> ").strip()
        except EOFError:
            break
        if linha.lower() == "sair":
            break
        validar(linha)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
