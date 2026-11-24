"""
mux.py - Multiplexadores construídos apenas com portas lógicas (AND, OR, NOT).

Todos os sinais são bits: 0 ou 1.
Convenção de nomes:
    I0, I1, ...  entradas de dados
    S0, S1, ...  entradas de seleção (S0 é o bit menos significativo)
    Y            saída
"""


# ---------------------------------------------------------------------------
# Portas lógicas básicas
# ---------------------------------------------------------------------------
def _bit(x):
    """Garante que o sinal é um bit válido (0 ou 1)."""
    if x not in (0, 1):
        raise ValueError(f"valor inválido: {x!r} (use apenas 0 ou 1)")
    return int(x)


def NOT(a):
    return 1 - _bit(a)


def AND(*entradas):
    resultado = 1
    for e in entradas:
        resultado &= _bit(e)
    return resultado


def OR(*entradas):
    resultado = 0
    for e in entradas:
        resultado |= _bit(e)
    return resultado


# ---------------------------------------------------------------------------
# MUX 2:1  ->  Y = I0·S0' + I1·S0
# ---------------------------------------------------------------------------
def mux2x1(i0, i1, s0):
    return OR(AND(i0, NOT(s0)),
              AND(i1, s0))


# ---------------------------------------------------------------------------
# MUX 4:1  ->  Y = I0·S1'·S0' + I1·S1'·S0 + I2·S1·S0' + I3·S1·S0
# ---------------------------------------------------------------------------
def mux4x1(i0, i1, i2, i3, s1, s0):
    return OR(AND(i0, NOT(s1), NOT(s0)),
              AND(i1, NOT(s1), s0),
              AND(i2, s1, NOT(s0)),
              AND(i3, s1, s0))


def mux4x1_passo_a_passo(i0, i1, i2, i3, s1, s0):
    """
    Mesmo circuito de mux4x1, mas guardando os sinais internos para mostrar na tela.

    Retorna um dicionário com:
        selecao  4 bits: a parte de seleção de cada AND (S1'·S0', S1'·S0, S1·S0', S1·S0).
                 Só uma vale 1: a da AND cujo endereço é igual a S1 S0.
        ands     4 bits: a saída de cada porta AND de 3 entradas (dado · seleção)
        saida    saída final Y (OR das 4 ANDs)
    """
    ns1, ns0 = NOT(s1), NOT(s0)
    selecao = [AND(ns1, ns0), AND(ns1, s0), AND(s1, ns0), AND(s1, s0)]
    ands = [AND(i0, ns1, ns0),
            AND(i1, ns1, s0),
            AND(i2, s1, ns0),
            AND(i3, s1, s0)]
    return {"selecao": selecao, "ands": ands, "saida": OR(*ands)}


# ---------------------------------------------------------------------------
# MUX 8:1 construído de forma hierárquica:
#   2 x MUX 4:1  (escolhem dentro de cada metade, usando S1 e S0)
#   1 x MUX 2:1  (escolhe entre as metades, usando S2)
# ---------------------------------------------------------------------------
def mux8x1_passo_a_passo(i, s2, s1, s0):
    """
    Executa o MUX 8:1 e devolve também os sinais intermediários.

    i: sequência com 8 bits, na ordem I0..I7.
    Retorna um dicionário com:
        ya    saída do MUX 4:1 "A" (entradas I0..I3)
        yb    saída do MUX 4:1 "B" (entradas I4..I7)
        saida saída final Y
    """
    if len(i) != 8:
        raise ValueError("o MUX 8:1 precisa de exatamente 8 entradas de dados")

    ya = mux4x1(i[0], i[1], i[2], i[3], s1, s0)  # metade baixa
    yb = mux4x1(i[4], i[5], i[6], i[7], s1, s0)  # metade alta
    y = mux2x1(ya, yb, s2)                       # S2 escolhe a metade
    return {"ya": ya, "yb": yb, "saida": y}


def mux8x1(i, s2, s1, s0):
    return mux8x1_passo_a_passo(i, s2, s1, s0)["saida"]
