"""O ALL recebe a mesma cadeia inteira, somente após aceitação do AP."""
from ap_handshake import simular as ap
from all_handshake import simular as all_

def validar(entrada, rastreio=False):
    a = ap(entrada, rastreio)
    return (a, all_(entrada, rastreio) if a else None)
