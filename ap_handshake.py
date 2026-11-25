"""AP determinístico. δ(q, entrada, topo) = (destino, substituição do topo).
A pilha é uma string (topo à esquerda); não há memória auxiliar de reconhecimento.
"""
ALFABETO = 'HCRKF01'
ALFABETO_PILHA = 'Z01'
INICIAL, FINAL = 'q0', 'q8'

class ErroAlfabeto(ValueError):
    pass

def checar_alfabeto(entrada):
    for i, x in enumerate(entrada):
        if x not in ALFABETO:
            raise ErroAlfabeto(f'Símbolo {x!r} na posição {i} não pertence ao alfabeto {ALFABETO}.')


def delta_epsilon(q, topo):
    if q == 'q4' and topo == 'Z':
        return 'q5', 'Z'  # Resposta terminou: todos os bits desempilhados.
    return None


def delta(q, x, t):
    if q == 'q0' and x == 'H' and t == 'Z': return 'q1', 'Z'
    if q == 'q1' and x == 'C' and t == 'Z': return 'q2', 'Z'
    if q == 'q2' and x in '01' and t == 'Z': return 'q3', x + t
    if q == 'q3' and t in '01':
        if x in '01': return 'q3', x + t  # Empilha o bit do desafio.
        if x == 'R': return 'q4', t
    if q == 'q4' and t in '01' and x == t: return 'q4', ''  # Desempilha bit igual.
    if q == 'q5' and x == 'K' and t == 'Z': return 'q6', 'Z'
    if q == 'q6' and x in '01' and t == 'Z': return 'q7', 'Z'
    if q == 'q7' and t == 'Z':
        if x in '01': return 'q7', 'Z'
        if x == 'F': return 'q8', 'Z'
    return None  # Transição indefinida: rejeição se não estiver em configuração final.


class AP:
    def __init__(self, entrada):
        checar_alfabeto(entrada)
        self.entrada = entrada
        self.q, self.pos, self.pilha = INICIAL, 0, 'Z'
        self.decisao = None
        self.regra = 'Configuração inicial'

    def passo(self):
        if self.decisao is not None: return
        t = self.pilha[0]
        regra = delta_epsilon(self.q, t)
        x = 'ε'
        if regra is None and self.pos < len(self.entrada):
            x = self.entrada[self.pos]
            regra = delta(self.q, x, t)
        if regra is None:
            self.decisao = self.q == FINAL and self.pos == len(self.entrada)
            self.regra = ('Estado final e entrada consumida' if self.decisao else
                          f'Sem transição em {self.q}; leitura {self.entrada[self.pos:self.pos+1] or "fim"}; topo {t}')
            return
        destino, escrita = regra
        self.regra = f'δ({self.q}, {x}, {t}) = ({destino}, {escrita or "ε"})'
        self.q = destino
        self.pilha = escrita + self.pilha[1:]
        if x != 'ε': self.pos += 1
        if self.q == FINAL and self.pos == len(self.entrada): self.decisao = True

    def estado(self):
        return f'{self.q:4} | posição {self.pos:3} | pilha {self.pilha} | {self.regra}'


def simular(entrada, rastreio=False):
    ap = AP(entrada)
    if rastreio: print(ap.estado())
    while ap.decisao is None:
        ap.passo()
        if rastreio: print(ap.estado())
    return ap.decisao
