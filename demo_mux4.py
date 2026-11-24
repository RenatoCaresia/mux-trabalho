"""
demo_mux4.py - Demonstração base: MUX 4:1 feito com portas lógicas.

Mostra:
  1) a tabela de seleção (qual entrada vai para a saída);
  2) um exemplo de execução com entradas escolhidas pelo usuário,
     incluindo os sinais dentro do circuito (as 4 portas AND e a OR);
  3) a verificação de todas as combinações possíveis.

Uso:
    python demo_mux4.py
    python demo_mux4.py --dados 0110 --sel 01
        (dados na ordem I0 I1 I2 I3; sel na ordem S1 S0)
"""
import argparse
from itertools import product

from mux import mux4x1, mux4x1_passo_a_passo


def ler_bits(texto, tamanho, nome):
    if len(texto) != tamanho or any(c not in "01" for c in texto):
        raise SystemExit(f"Erro: --{nome} deve ter exatamente {tamanho} bits (0 ou 1).")
    return [int(c) for c in texto]


def tabela_selecao(dados):
    print("\nTabela de seleção (para os dados informados)")
    print("  S1 S0 | entrada escolhida | valor | Y")
    print("  ------+-------------------+-------+---")
    for indice in range(4):
        s1, s0 = (indice >> 1) & 1, indice & 1
        y = mux4x1(*dados, s1, s0)
        print(f"   {s1}  {s0} |        I{indice}         |   {dados[indice]}   | {y}")


def execucao_unica(dados, sel):
    s1, s0 = sel
    indice = (s1 << 1) | s0
    r = mux4x1_passo_a_passo(*dados, s1, s0)
    print("\nExemplo de execução")
    print(f"  Entradas de dados : I0={dados[0]} I1={dados[1]} I2={dados[2]} I3={dados[3]}")
    print(f"  Seleção           : S1={s1} S0={s0}  ->  endereço {indice}")
    print("  Processamento     : cada AND confere se S1 S0 é o endereço dela")
    print("    porta | endereço | seleção bate? | dado | saída da AND")
    print("    ------+----------+---------------+------+-------------")
    for k in range(4):
        seta = "<--" if r["selecao"][k] else "   "
        print(f"    AND{k}  |    {k:02b}    |     {r['selecao'][k]}  {seta}    |"
              f" I{k}={dados[k]} |      {r['ands'][k]}")
    saidas = ", ".join(str(a) for a in r["ands"])
    print(f"    OR junta as 4 saídas: OR({saidas}) = {r['saida']}")
    print(f"  Saída             : Y = {r['saida']}  (igual a I{indice} = {dados[indice]})")


def verificacao_exaustiva():
    """Compara o circuito com a definição matemática Y = I[endereço]
    para TODAS as combinações possíveis (4 dados + 2 seleções = 2^6 = 64)."""
    total = 0
    divergencias = 0
    for dados in product((0, 1), repeat=4):
        for indice in range(4):
            s1, s0 = (indice >> 1) & 1, indice & 1
            r = mux4x1_passo_a_passo(*dados, s1, s0)
            total += 1
            certo = (mux4x1(*dados, s1, s0) == dados[indice]  # a equação
                     and r["saida"] == dados[indice]          # a versão passo a passo
                     and sum(r["selecao"]) == 1)              # só uma AND habilitada
            if not certo:
                divergencias += 1
    print("\nVerificação exaustiva")
    print(f"  Combinações testadas : {total}")
    print(f"  Divergências         : {divergencias}")
    print("  Resultado            : " + ("MUX 4:1 correto! (sempre só uma AND habilitada)"
                                         if divergencias == 0 else "FALHOU"))


def main():
    parser = argparse.ArgumentParser(description="Demonstração do MUX 4:1")
    parser.add_argument("--dados", default="1001", help="4 bits na ordem I0 I1 I2 I3")
    parser.add_argument("--sel", default="10", help="2 bits na ordem S1 S0")
    args = parser.parse_args()

    dados = ler_bits(args.dados, 4, "dados")
    sel = ler_bits(args.sel, 2, "sel")

    print("=" * 52)
    print(" MUX 4:1 - construído com portas AND, OR e NOT")
    print("=" * 52)
    tabela_selecao(dados)
    execucao_unica(dados, sel)
    verificacao_exaustiva()


if __name__ == "__main__":
    main()
