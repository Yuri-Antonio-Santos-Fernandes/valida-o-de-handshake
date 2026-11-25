"""ALL determinístico. δ(p, símbolo) = (destino, escrita, direção).
A fita tem exatamente n+2 células: n graváveis e duas bordas fixas.
A memória do bit procurado está nos estados p11_0/p11_1 etc., não em variável auxiliar.
"""
from ap_handshake import ALFABETO, checar_alfabeto
ALFABETO_FITA = '<>HCRKF01xy'
INICIAL, ACEITA, REJEITA = 'p0', 'pa', 'pr'


def delta(q, x):
    # Fase 1 — validação sintática independente: HC[01]+R[01]+K[01]+F.
    if q == 'p0' and x == '<': return 'p1', x, 'D'
    if q == 'p1' and x == 'H': return 'p2', x, 'D'
    if q == 'p2' and x == 'C': return 'p3', x, 'D'
    if q == 'p3' and x in '01': return 'p4', x, 'D'
    if q == 'p4':
        if x in '01': return 'p4', x, 'D'
        if x == 'R': return 'p5', x, 'D'
    if q == 'p5' and x in '01': return 'p6', x, 'D'
    if q == 'p6':
        if x in '01': return 'p6', x, 'D'
        if x == 'K': return 'p7', x, 'D'
    if q == 'p7' and x in '01': return 'p8', x, 'D'
    if q == 'p8':
        if x in '01': return 'p8', x, 'D'
        if x == 'F': return 'p9', x, 'D'
    if q == 'p9' and x == '>': return 'p10', x, 'E'
    # Fase 2 — retorna ao início e escolhe o primeiro bit não marcado do desafio.
    if q == 'p10':
        if x in 'HCRKF01xy': return 'p10', x, 'E'
        if x == '<': return 'p11', x, 'D'
    if q == 'p11':
        if x in 'HCxy': return 'p11', x, 'D'
        if x == '0': return 'p12_0', 'x', 'D'
        if x == '1': return 'p12_1', 'y', 'D'
        if x == 'R': return 'p16', x, 'D'
    # Fase 3 — caminha até K, então lê a resposta da direita para a esquerda.
    if q == 'p12_0':
        if x in '01Rxy': return 'p12_0', x, 'D'
        if x == 'K': return 'p13_0', x, 'E'
    if q == 'p12_1':
        if x in '01Rxy': return 'p12_1', x, 'D'
        if x == 'K': return 'p13_1', x, 'E'
    if q == 'p13_0':
        if x in 'xy': return 'p13_0', x, 'E'
        if x == '0': return 'p14_0', 'x', 'D'
    if q == 'p13_1':
        if x in 'xy': return 'p13_1', x, 'E'
        if x == '1': return 'p14_1', 'y', 'D'
    # Fase 4 — volta a K e lê a confirmação da esquerda para a direita.
    if q == 'p14_0':
        if x in 'xy': return 'p14_0', x, 'D'
        if x == 'K': return 'p15_0', x, 'D'
    if q == 'p14_1':
        if x in 'xy': return 'p14_1', x, 'D'
        if x == 'K': return 'p15_1', x, 'D'
    if q == 'p15_0':
        if x in 'xy': return 'p15_0', x, 'D'
        if x == '0': return 'p10', 'x', 'E'
    if q == 'p15_1':
        if x in 'xy': return 'p15_1', x, 'D'
        if x == '1': return 'p10', 'y', 'E'
    # Fase 5 — sem bits pendentes no desafio, verifica sobras na resposta/confirm.
    if q == 'p16':
        if x in 'xyKF': return 'p16', x, 'D'
        if x == '>': return ACEITA, x, 'P'
    return REJEITA, x, 'P'  # P = parada, preserva a célula.


class ALL:
    def __init__(self, entrada):
        checar_alfabeto(entrada)
        self.fita = bytearray('<' + entrada + '>', 'ascii')
        self.q, self.cabeca = INICIAL, 0
        self.decisao = None
        self.regra = 'Configuração inicial'

    def passo(self):
        if self.decisao is not None: return
        x = chr(self.fita[self.cabeca])
        destino, escrita, movimento = delta(self.q, x)
        self.regra = f'δ({self.q}, {x}) = ({destino}, {escrita}, {movimento})'
        if self.cabeca == 0 or self.cabeca == len(self.fita)-1:
            assert x == escrita, 'Borda fixa'
        else:
            assert escrita not in '<>', 'Marcador dentro da fita'
            self.fita[self.cabeca] = ord(escrita)
        if movimento == 'D': self.cabeca += 1
        elif movimento == 'E': self.cabeca -= 1
        assert 0 <= self.cabeca < len(self.fita), 'Cabeçote fora da fita'
        self.q = destino
        if self.q == ACEITA: self.decisao = True
        elif self.q == REJEITA: self.decisao = False

    def estado(self):
        return f'{self.q:6} | cabeça {self.cabeca:3} | fita {self.fita.decode()} | {self.regra}'


def simular(entrada, rastreio=False):
    all_ = ALL(entrada)
    if rastreio: print(all_.estado())
    while all_.decisao is None:
        all_.passo()
        if rastreio: print(all_.estado())
    return all_.decisao
