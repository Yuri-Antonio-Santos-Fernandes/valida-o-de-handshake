"""Dados e oráculos de teste externos aos autômatos; não participam da decisão."""
from ap_handshake import simular as ap, ErroAlfabeto
from all_handshake import simular as all_
from integracao import validar
from itertools import product

from exemplos import VALIDA, ERRO_AP, ERRO_ALL

def cadeia(w, r, k): return f'HC{w}R{r}K{k}F'


def executar():
    comuns = tuple(cadeia(w, w[::-1], w) for w in ('101100','00000','11111','01010','10101','11000','00111','100101'))
    # O AP não compara o conteúdo da confirmação: casos aceitos, inclusive com diferença.
    ap_bons = comuns[:6] + ('HC00111R11100K10101F', 'HC100101R101001K0000000F')
    ruins_ap = (
        (ERRO_AP, 'bit da resposta incompatível com topo'),
        ('HC101100R00110K101100F', 'resposta curta; pilha não esvaziou'),
        ('HC101100R0011011K101100F', 'resposta longa; esperava K'),
        ('HH101100R001101K101100F', 'C obrigatório após H'),
        ('HC101100K001101R101100F', 'ordem R/K incorreta'),
        ('HC101100R001101K101100', 'F obrigatório'),
        ('HC101100R001101K101100FF', 'símbolo após estado final'),
        ('HC101100R001101KF00000', 'confirmação não vazia e F final'),
    )
    ruins_all = (
        (ERRO_ALL, 'bit diferente na confirmação'),
        (ERRO_AP, 'bit diferente na resposta'),
        ('HC101100R001101K10110F', 'confirmação curta'),
        ('HC101100R001101K1011000F', 'sobra na confirmação'),
        ('HC101100R00110K101100F', 'resposta curta'),
        ('HC101100R0011010K101100F', 'sobra na resposta'),
        ('HC101100R001101K101100FF', 'F deve ser último'),
        ('HC101100R001101K010011F', 'mesmo tamanho, conteúdo diferente'),
    )
    total = 0
    for nome, funcao, bons, ruins in (('AP', ap, ap_bons, ruins_ap), ('ALL', all_, comuns, ruins_all)):
        print(f'\n=== {nome} ===')
        casos = tuple((w, True, 'estrutura e resposta inversa' if nome == 'AP' else 'correspondência exata nos três campos') for w in bons) + tuple((w, False, r) for w,r in ruins)
        assert len({w for w,_,_ in casos}) == 16
        assert all(len(w) >= 18 for w,_,_ in casos)
        casos += (('HC0R0K0F', True, 'menor entrada válida; exceção de caso-limite'), ('', False, 'entrada vazia; exceção de caso-limite'))
        for w, esperado, regra in casos:
            obtido = funcao(w)
            assert obtido == esperado, (nome,w,esperado,obtido)
            total += 1
            print(f'{w or "ε"} ({len(w)}) | esperado={esperado} | obtido={obtido} | {regra}')
    print('\n=== INTEGRAÇÃO ===')
    for w, esperado, regra in ((VALIDA,(True,True),'válido'),(ERRO_AP,(False,None),'ALL não executado'),(ERRO_ALL,(True,False),'confirmação incorreta')):
        obtido = validar(w); assert obtido == esperado
        total += 1
        print(f'{w} | esperado={esperado} | obtido={obtido} | {regra}')
    try: validar(VALIDA+'?')
    except ErroAlfabeto as e:
        total += 1
        print(f'\n{VALIDA}? | esperado=erro de alfabeto | obtido={e}')
    else: raise AssertionError('Símbolo fora do alfabeto não detectado')
    print(f'\n{total}/40 verificações obrigatórias e casos-limite passaram.')
    # Verificação adicional por enumeração de todos os campos binários de 0 a 3 bits.
    campos = tuple(''.join(t) for n in range(4) for t in product('01', repeat=n))
    n = 0
    for w,r,k in product(campos,repeat=3):
        entrada = cadeia(w,r,k)
        a = bool(w and r and k and r == w[::-1]); b = a and w == k
        assert ap(entrada) == a, entrada
        assert all_(entrada) == b, entrada
        n += 2
    print(f'{n} verificações adicionais por enumeração de campos binários (oráculo externo).')

if __name__ == '__main__': executar()
