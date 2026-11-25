"""Teste de integração da GUI; requer display gráfico (ou Xvfb no Linux)."""
import tkinter as tk
from main import Aplicacao
from exemplos import VALIDA, ERRO_AP, ERRO_ALL

def executar():
    r = tk.Tk(); a = Aplicacao(r); r.update()
    try:
        for w, esperado in ((VALIDA,(True,True)),(ERRO_AP,(False,None)),(ERRO_ALL,(True,False))):
            a.exemplo(w); a.passo(); assert a.ap.pos == 1; a.executar_tudo()
            while a.fase is not None: r.update()
            obtido = (a.ap.decisao,a.all_.decisao if a.all_ else None)
            assert obtido == esperado
            print(f'GUI: {w} | esperado={esperado} | obtido={obtido}')
        for modo in ('Somente AP','Somente ALL'):
            a.modo.set(modo); a.exemplo(VALIDA); a.executar_tudo()
            while a.fase is not None: r.update()
            assert (a.ap or a.all_).decisao
            print(f'GUI: {modo} aceitou a cadeia válida.')
        a.var.set(VALIDA+'?'); a.iniciar()
        assert a.fase is None and 'ERRO:' in a.status['text']
        print('GUI: '+a.status['text'])
        a.modo.set('Fluxo completo'); a.exemplo(VALIDA); a.vel.set('Lenta'); a.auto(); a.pausar()
        assert a.job is None and a.ap.pos==1
        a.iniciar(); assert a.ap.pos==0
        print('GUI: execução automática, pausa e reinício verificados.')
    finally: r.destroy()

if __name__=='__main__': executar()
