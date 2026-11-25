from ap_handshake import simular as ap
from all_handshake import simular as all_
from exemplos import VALIDA
from contextlib import redirect_stdout
with open('rastreio_exemplo.txt','w',encoding='utf-8') as f, redirect_stdout(f):
    print('Entrada:', VALIDA, '\nAP:')
    print('Decisão AP:', ap(VALIDA, True))
    print('\nALL:')
    print('Decisão ALL:', all_(VALIDA, True))
