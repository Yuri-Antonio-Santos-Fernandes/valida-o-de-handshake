"""Dados e oráculos de teste externos aos autômatos; não participam da decisão."""
from ap_handshake import simular as ap, ErroAlfabeto
from all_handshake import simular as all_
from integracao import validar
from itertools import product

from exemplos import VALIDA, ERRO_AP, ERRO_ALL

def cadeia(w, r, k): return f'HC{w}R{r}K{k}F'


# Casos principais: 32 entradas distintas entre os dois reconhecedores.
AP_ACEITAS = (
    (VALIDA, 'estrutura completa; resposta invertida'),
    ('HC00000R00000K00000F', 'desafio composto apenas por zeros'),
    ('HC11111R11111K11111F', 'desafio composto apenas por uns'),
    ('HC01010R01010K01010F', 'desafio palíndromo iniciado em 0'),
    ('HC10101R10101K10101F', 'desafio palíndromo iniciado em 1'),
    ('HC11000R00011K11000F', 'inversão não palíndroma'),
    ('HC00111R11100K10101F', 'confirmação com conteúdo diferente'),
    ('HC100101R101001K0000000F', 'confirmação mais longa que o desafio'),
)
AP_REJEITADAS = (
    (ERRO_AP, 'bit da resposta incompatível com o topo'),
    ('HC101100R00110K101100F', 'resposta curta; restam bits acima de Z'),
    ('HC101100R0011011K101100F', 'resposta longa; esperava K'),
    ('HH101100R001101K101100F', 'C obrigatório após H'),
    ('HC101100K001101R101100F', 'ordem R/K incorreta'),
    ('HC101100R001101K101100', 'F obrigatório'),
    ('HC101100R001101K101100FF', 'símbolo após estado final'),
    ('HC101100R001101KF00000', 'confirmação não vazia; F final'),
)
ALL_ACEITAS = (
    ('HC00101R10100K00101F', 'desafio com zeros iniciais'),
    ('HC11011R11011K11011F', 'desafio palíndromo'),
    ('HC000000R000000K000000F', 'seis bits iguais a zero'),
    ('HC111111R111111K111111F', 'seis bits iguais a um'),
    ('HC010101R101010K010101F', 'alternância iniciada em 0'),
    ('HC101010R010101K101010F', 'alternância iniciada em 1'),
    ('HC01110R01110K01110F', 'bloco de uns entre zeros'),
    ('HC110001R100011K110001F', 'inversão e confirmação com bits mistos'),
)
ALL_REJEITADAS = (
    (ERRO_ALL, 'último bit da confirmação divergente'),
    ('HC101100R001101K10110F', 'confirmação mais curta'),
    ('HC101100R001101K1011000F', 'confirmação mais longa'),
    ('HC101100R001101K010011F', 'mesmas quantidades; ordem diferente'),
    ('HC01101R10110K11101F', 'primeiro bit da confirmação divergente'),
    ('HC11010R01011K11000F', 'bit interno da confirmação divergente'),
    ('HC00101R00100K00101F', 'resposta não corresponde à inversão'),
    ('HC110001R100011K110001', 'ausência do marcador final F'),
)


def executar():
    total = 0
    principais = AP_ACEITAS + AP_REJEITADAS + ALL_ACEITAS + ALL_REJEITADAS
    assert len(principais) == len({w for w, _ in principais}) == 32
    assert all(len(w) >= 18 and set(w) <= set('HCRKF01') for w, _ in principais)
    for nome, funcao, bons, ruins, minimo in (
        ('AP', ap, AP_ACEITAS, AP_REJEITADAS, 'HC0R0K0F'),
        ('ALL', all_, ALL_ACEITAS, ALL_REJEITADAS, 'HC1R1K1F'),
    ):
        print(f'\n=== {nome} ===')
        assert len(bons) == len(ruins) == 8
        casos = tuple((w, True, r) for w, r in bons) + tuple((w, False, r) for w, r in ruins)
        casos += ((minimo, True, 'menor entrada válida; exceção de caso-limite'), ('', False, 'entrada vazia; exceção de caso-limite'))
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
