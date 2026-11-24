"""
exemplo1_mux8.py - Exemplo 1: MUX 8:1 construído a partir de MUX 4:1 e MUX 2:1.

Ideia (construção hierárquica):
    - dois MUX 4:1 escolhem uma entrada dentro de cada metade (I0-I3 e I4-I7),
      usando S1 e S0;
    - um MUX 2:1 escolhe qual metade segue para a saída, usando S2.

Uso:
    python exemplo1_mux8.py                         # varre as 8 seleções
    python exemplo1_mux8.py --dados 01101001        # dados na ordem I0..I7
    python exemplo1_mux8.py --sel 101               # uma execução (S2 S1 S0)
"""
import argparse
from itertools import product

from mux import mux8x1, mux8x1_passo_a_passo

DIAGRAMA = """
   I0 I1 I2 I3 --> [ MUX 4:1  A ] --> YA --+
                      S1  S0                |
                                            +--> [ MUX 2:1 ] --> Y
   I4 I5 I6 I7 --> [ MUX 4:1  B ] --> YB --+        S2
                      S1  S0
"""


def ler_bits(texto, tamanho, nome):
    if len(texto) != tamanho or any(c not in "01" for c in texto):
        raise SystemExit(f"Erro: --{nome} deve ter exatamente {tamanho} bits (0 ou 1).")
    return [int(c) for c in texto]


def separar_selecao(indice):
    return (indice >> 2) & 1, (indice >> 1) & 1, indice & 1


def mostrar_dados(dados):
    print("Entradas de dados:")
    print("   " + "  ".join(f"I{k}" for k in range(8)))
    print("   " + "  ".join(f" {b}" for b in dados))


def varredura(dados):
    """Testa as 8 combinações de seleção e mostra os sinais intermediários."""
    print("\nVarredura das seleções")
    print("  S2 S1 S0 | índice | YA YB | Y | esperado | ok")
    print("  ---------+--------+-------+---+----------+----")
    for indice in range(8):
        s2, s1, s0 = separar_selecao(indice)
        r = mux8x1_passo_a_passo(dados, s2, s1, s0)
        esperado = dados[indice]
        ok = "ok" if r["saida"] == esperado else "ERRO"
        print(f"   {s2}  {s1}  {s0} |   {indice}    |  {r['ya']}  {r['yb']} | {r['saida']} |"
              f"    {esperado}     | {ok}")


def execucao_unica(dados, sel):
    s2, s1, s0 = sel
    indice = (s2 << 2) | (s1 << 1) | s0
    r = mux8x1_passo_a_passo(dados, s2, s1, s0)
    metade = "B (I4..I7)" if s2 else "A (I0..I3)"
    print("\nExemplo de execução")
    print(f"  Seleção        : S2={s2} S1={s1} S0={s0}  ->  endereço {indice}")
    print(f"  Passo 1 (S1S0) : MUX A entrega YA={r['ya']} | MUX B entrega YB={r['yb']}")
    print(f"  Passo 2 (S2)   : S2={s2} escolhe a metade {metade}")
    print(f"  Saída          : Y = {r['saida']}  (igual a I{indice} = {dados[indice]})")


def verificacao_exaustiva():
    """Compara o circuito com a definição matemática Y = I[endereço]
    para TODAS as combinações possíveis (8 dados + 3 seleções = 2^11)."""
    total = 0
    divergencias = 0
    for dados in product((0, 1), repeat=8):
        for indice in range(8):
            s2, s1, s0 = separar_selecao(indice)
            total += 1
            if mux8x1(dados, s2, s1, s0) != dados[indice]:
                divergencias += 1
    print("\nVerificação exaustiva")
    print(f"  Combinações testadas : {total}")
    print(f"  Divergências         : {divergencias}")
    print("  Resultado            : " + ("MUX 8:1 correto!" if divergencias == 0 else "FALHOU"))


def main():
    parser = argparse.ArgumentParser(description="Exemplo 1: MUX 8:1 hierárquico")
    parser.add_argument("--dados", default="10110010", help="8 bits na ordem I0..I7")
    parser.add_argument("--sel", default=None, help="3 bits na ordem S2 S1 S0")
    args = parser.parse_args()

    # valida tudo antes de imprimir, para o erro não aparecer no meio da saída
    dados = ler_bits(args.dados, 8, "dados")
    sel = None if args.sel is None else ler_bits(args.sel, 3, "sel")

    print("=" * 60)
    print(" Exemplo 1 - MUX 8:1 feito com 2 x MUX 4:1 + 1 x MUX 2:1")
    print("=" * 60)
    print(DIAGRAMA)
    mostrar_dados(dados)

    if sel is None:
        varredura(dados)
    else:
        execucao_unica(dados, sel)

    verificacao_exaustiva()


if __name__ == "__main__":
    main()
