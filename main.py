"""Interface Tkinter. Toda decisão vem de AP.passo() ou ALL.passo().
Histórico visual e relógio de animação são exclusivos da apresentação.
"""
import tkinter as tk
from tkinter import ttk
from ap_handshake import AP, ErroAlfabeto
from all_handshake import ALL
from exemplos import VALIDA, ERRO_AP, ERRO_ALL

BG='#eef3f9'; WHITE='#ffffff'; NAVY='#14233b'; MUTED='#536782'; BLUE='#2558c8'; GREEN='#127657'; RED='#b72b3a'; LINE='#d7e1ee'; TEAL='#e1f3ee'

class Aplicacao:
    def __init__(self, root):
        self.root=root; root.title('Handshake Lab | Autômatos'); root.geometry('1160x820'); root.minsize(800,690); root.configure(bg=BG)
        self.ap=None; self.all_=None; self.fase=None; self.job=None; self.entrada=''; self.numero=0
        self.var=tk.StringVar(value=VALIDA); self.modo=tk.StringVar(value='Fluxo completo'); self.vel=tk.StringVar(value='Rápida')
        style=ttk.Style(root); style.theme_use('clam'); style.configure('TCombobox', padding=5, font=('Arial',10))
        header=tk.Frame(root,bg=NAVY,padx=24,pady=15); header.pack(fill='x')
        tk.Label(header,text='HANDSHAKE LAB',bg=NAVY,fg='#a8c6ff',font=('Arial',10,'bold')).pack(anchor='w')
        tk.Label(header,text='Validador de desafio e resposta',bg=NAVY,fg=WHITE,font=('Arial',21,'bold')).pack(anchor='w')
        tk.Label(header,text='Linguagens formais • Autômato de pilha + Autômato linearmente limitado',bg=NAVY,fg='#c9d7eb',font=('Arial',10)).pack(anchor='w')
        body=tk.Frame(root,bg=BG,padx=20,pady=10); body.pack(fill='both',expand=True)
        inp=tk.Frame(body,bg=WHITE,padx=14,pady=9); inp.pack(fill='x')
        tk.Label(inp,text='01  ENTRADA DO PROTOCOLO',bg=WHITE,fg=MUTED,font=('Arial',10,'bold')).pack(anchor='w')
        row=tk.Frame(inp,bg=WHITE); row.pack(fill='x',pady=5)
        self.entry=tk.Entry(row,textvariable=self.var,font=('Consolas',15),bg='#f5f8fc',fg=NAVY,relief='flat',highlightthickness=1,highlightbackground=LINE,highlightcolor=BLUE); self.entry.pack(side='left',fill='x',expand=True,ipady=7)
        self.combo=ttk.Combobox(row,textvariable=self.modo,values=('Fluxo completo','Somente AP','Somente ALL'),state='readonly',width=17); self.combo.pack(side='left',padx=(10,0))
        self.button(row,'Iniciar',self.iniciar,True).pack(side='left',padx=(8,0))
        row=tk.Frame(inp,bg=WHITE); row.pack(fill='x',pady=(2,0))
        for nome,w in (('✓ Válido',VALIDA),('× Erro no AP',ERRO_AP),('× Erro no ALL',ERRO_ALL)):
            self.button(row,nome,lambda w=w:self.exemplo(w)).pack(side='left',padx=(0,6))
        tk.Label(row,text='H início  •  C desafio  •  R resposta  •  K confirmação  •  F fim',bg=WHITE,fg=MUTED,font=('Arial',9)).pack(side='right')
        self.status=tk.Label(body,text='Selecione um exemplo ou digite uma cadeia e clique em Iniciar.',bg=BG,fg=NAVY,font=('Arial',11,'bold'),anchor='w'); self.status.pack(fill='x',pady=8)
        panels=tk.Frame(body,bg=BG); panels.pack(fill='x'); panels.columnconfigure(0,weight=1,uniform='p'); panels.columnconfigure(1,weight=1,uniform='p')
        self.apcard,self.apstatus,self.apmeta,self.aprule,self.apcanvas=self.painel(panels,0,'02  AUTÔMATO DE PILHA','AP • resposta invertida')
        self.allcard,self.allstatus,self.allmeta,self.allrule,self.allcanvas=self.painel(panels,1,'03  FITA LINEARMENTE LIMITADA','ALL • confirmação exata')
        controls=tk.Frame(body,bg=BG); controls.pack(fill='x',pady=8)
        self.button(controls,'Próximo passo',self.passo,True).pack(side='left',padx=(0,6))
        self.button(controls,'▶ Automático',self.auto).pack(side='left',padx=(0,6))
        self.button(controls,'Pausar',self.pausar).pack(side='left',padx=(0,6))
        self.button(controls,'Executar tudo',self.executar_tudo).pack(side='left',padx=(0,6))
        self.button(controls,'Reiniciar',self.iniciar).pack(side='left',padx=(0,6))
        ttk.Combobox(controls,textvariable=self.vel,values=('Lenta','Normal','Rápida'),state='readonly',width=9).pack(side='right')
        tk.Label(controls,text='Velocidade',bg=BG,fg=MUTED,font=('Arial',9)).pack(side='right',padx=6)
        trace=tk.Frame(body,bg=WHITE,padx=12,pady=8); trace.pack(fill='both',expand=True)
        tk.Label(trace,text='04  RASTREAMENTO REAL DAS TRANSIÇÕES',bg=WHITE,fg=MUTED,font=('Arial',10,'bold')).pack(anchor='w')
        textframe=tk.Frame(trace,bg=WHITE); textframe.pack(fill='both',expand=True,pady=(5,0))
        sy=ttk.Scrollbar(textframe); sy.pack(side='right',fill='y')
        sx=ttk.Scrollbar(trace,orient='horizontal'); sx.pack(fill='x',side='bottom')
        self.log=tk.Text(textframe,font=('Consolas',10),height=7,bg='#f5f8fc',fg=NAVY,relief='flat',wrap='none',yscrollcommand=sy.set,xscrollcommand=sx.set,state='disabled'); self.log.pack(fill='both',expand=True)
        sy.config(command=self.log.yview); sx.config(command=self.log.xview)
        root.protocol('WM_DELETE_WINDOW',self.fechar)
        self.iniciar()

    def button(self,parent,text,command,primary=False):
        return tk.Button(parent,text=text,command=command,bg=BLUE if primary else '#e5edf8',fg=WHITE if primary else NAVY,activebackground='#1947a8' if primary else '#d4e3f6',activeforeground=WHITE if primary else NAVY,relief='flat',bd=0,padx=10,pady=7,font=('Arial',10,'bold'),cursor='hand2')

    def painel(self,parent,col,label,title):
        card=tk.Frame(parent,bg=WHITE,padx=12,pady=9); card.grid(row=0,column=col,sticky='nsew',padx=(0,5) if col==0 else (5,0))
        tk.Label(card,text=label,bg=WHITE,fg=MUTED,font=('Arial',9,'bold')).pack(anchor='w')
        tk.Label(card,text=title,bg=WHITE,fg=NAVY,font=('Arial',15,'bold')).pack(anchor='w')
        status=tk.Label(card,text='Aguardando',bg=WHITE,fg=MUTED,font=('Arial',10,'bold')); status.pack(anchor='w',pady=(3,0))
        meta=tk.Label(card,text='—',bg=WHITE,fg=NAVY,font=('Arial',10)); meta.pack(anchor='w')
        canvas=tk.Canvas(card,height=78,bg='#f5f8fc',highlightthickness=0); canvas.pack(fill='x',pady=(4,0))
        scroll=ttk.Scrollbar(card,orient='horizontal',command=canvas.xview); scroll.pack(fill='x'); canvas.config(xscrollcommand=scroll.set)
        rule=tk.Label(card,text='—',bg=WHITE,fg=MUTED,font=('Arial',9),anchor='w',justify='left',wraplength=480); rule.pack(fill='x',pady=(4,0))
        return card,status,meta,rule,canvas

    def exemplo(self,w):
        self.var.set(w); self.iniciar()

    def escrever(self,msg):
        self.log.configure(state='normal'); self.log.insert('end',msg+'\n'); self.log.see('end'); self.log.configure(state='disabled')

    def iniciar(self):
        self.pausar(); self.ap=None; self.all_=None; self.fase=None; self.numero=0; self.entrada=self.var.get(); self.modo_exec=self.modo.get()
        self.log.configure(state='normal'); self.log.delete('1.0','end'); self.log.configure(state='disabled')
        try:
            if self.modo_exec=='Somente ALL': self.all_=ALL(self.entrada); self.fase='ALL'
            else: self.ap=AP(self.entrada); self.fase='AP'
        except ErroAlfabeto as e:
            self.status.config(text=f'ERRO: {e}',fg=RED); self.escrever(f'ERRO: {e}'); self.atualizar(); return
        self.status.config(text=f'{self.fase} pronto • {len(self.entrada)} símbolos • posições começam em 0',fg=BLUE)
        self.escrever(f'000 | {self.fase} | '+self.maquina().estado()); self.atualizar()

    def maquina(self): return self.ap if self.fase=='AP' else self.all_

    def transicao(self):
        if self.fase is None: return
        m=self.maquina()
        if m.decisao is None:
            m.passo(); self.numero+=1; self.escrever(f'{self.numero:03} | {self.fase} | {m.estado()}')
        if m.decisao is not None:
            if self.fase=='AP' and m.decisao and self.modo_exec=='Fluxo completo':
                self.all_=ALL(self.entrada); self.fase='ALL'; self.escrever('--- AP aceitou; ALL recebe a cadeia inteira ---'); self.escrever(f'    | ALL | {self.all_.estado()}'); self.status.config(text='AP aceitou • ALL em execução',fg=BLUE)
            else:
                etapa=self.fase; resultado='ACEITO' if m.decisao else 'REJEITADO'; extra=' • ALL não executado' if etapa=='AP' and not m.decisao and self.modo_exec=='Fluxo completo' else ''
                self.status.config(text=f'{resultado} • decisão do {etapa}{extra}',fg=GREEN if m.decisao else RED); self.escrever(f'--- {resultado}{extra} ---'); self.fase=None

    def passo(self): self.pausar(); self.transicao(); self.atualizar()
    def auto(self):
        if self.job is None and self.fase is not None: self.tick()
    def tick(self):
        self.job=None; self.transicao(); self.atualizar()
        if self.fase is not None: self.job=self.root.after({'Lenta':500,'Normal':120,'Rápida':20}[self.vel.get()],self.tick)
    def executar_tudo(self):
        self.pausar(); self.lote()
    def lote(self):
        self.job=None
        for _ in range(80):
            if self.fase is None: break
            self.transicao()
        self.atualizar()
        if self.fase is not None: self.job=self.root.after(1,self.lote)
    def pausar(self):
        if self.job is not None: self.root.after_cancel(self.job); self.job=None
    def fechar(self): self.pausar(); self.root.destroy()

    def desenhar(self,cv,sequencia,indice,rotulo):
        cv.delete('all'); cv.create_text(8,10,text=rotulo,anchor='w',font=('Arial',9),fill=MUTED)
        passo=max(20,min(29,(cv.winfo_width()-16)//max(1,len(sequencia))))
        for i,x in enumerate(sequencia):
            left=8+i*passo; meio=left+(passo-3)/2; ativo=i==indice; marked=x in 'xy'
            cv.create_rectangle(left,25,left+passo-3,50,fill=TEAL if marked else ('#dce8fe' if ativo else WHITE),outline=BLUE if ativo else LINE,width=2 if ativo else 1)
            cv.create_text(meio,37,text=x,font=('Consolas',11,'bold'),fill=GREEN if marked else NAVY)
            cv.create_text(meio,60,text=str(i),font=('Arial',8),fill=MUTED)
            if ativo: cv.create_text(meio,19,text='▼',font=('Arial',8),fill=BLUE)
        largura=max(cv.winfo_width(),16+len(sequencia)*passo); cv.configure(scrollregion=(0,0,largura,78))
        if indice>=0 and largura>cv.winfo_width(): cv.xview_moveto(max(0,(8+indice*passo-cv.winfo_width()/2)/largura))
        else: cv.xview_moveto(0)

    def atualizar(self):
        for m,status,meta,rule,cv in ((self.ap,self.apstatus,self.apmeta,self.aprule,self.apcanvas),(self.all_,self.allstatus,self.allmeta,self.allrule,self.allcanvas)):
            if m is None:
                status.config(text='Não executado',fg=MUTED); meta.config(text='—'); rule.config(text='—'); cv.delete('all'); continue
            d=m.decisao; status.config(text='Em execução' if d is None else ('ACEITA' if d else 'REJEITA'),fg=BLUE if d is None else (GREEN if d else RED))
            rule.config(text=m.regra)
            if isinstance(m,AP):
                meta.config(text=f'Estado {m.q}  |  posição {m.pos}  |  leitura {m.entrada[m.pos:m.pos+1] or "fim"}')
                self.desenhar(cv,m.pilha,0,'Pilha • topo à esquerda')
            else:
                meta.config(text=f'Estado {m.q}  |  cabeça {m.cabeca}  |  {len(m.fita)-2} células graváveis')
                self.desenhar(cv,m.fita.decode(),m.cabeca,'Fita • x = 0 marcado, y = 1 marcado')

if __name__=='__main__':
    root=tk.Tk(); Aplicacao(root); root.mainloop()
