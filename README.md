# Multiplexadores (MUX) — Parte Prática

Trabalho em grupo de **Arquitetura e Organização de Computadores** — Grupo 2: Multiplexadores.

**Integrantes:** Renato Caresia, Kaio Henrique e Luiz Otavio

## O que é este projeto

Simulação em Python de multiplexadores construídos **apenas com portas lógicas** (AND, OR e NOT). Nenhum `if` e nenhum `lista[seleção]` decide qual entrada vai para a saída: quem faz a escolha são as portas. (Os `if` que existem no código só conferem se os valores recebidos são 0 ou 1, e os índices `i[0]` a `i[7]` no MUX 8:1 só fazem o papel dos fios que ligam cada entrada ao seu MUX 4:1.) A ideia é mostrar que o MUX é, de fato, um circuito combinacional: a saída depende só das entradas atuais (dados e seleção), e a seleção é feita pela lógica das portas.

Um multiplexador (MUX) tem várias entradas de dados, algumas entradas de seleção e uma única saída. Os bits de seleção escolhem qual entrada de dados é copiada para a saída.

| MUX | Entradas de dados | Bits de seleção | Equação |
|-----|-------------------|-----------------|---------|
| 2:1 | I0, I1 | S0 | `Y = I0·S0' + I1·S0` |
| 4:1 | I0 a I3 | S1, S0 | `Y = I0·S1'·S0' + I1·S1'·S0 + I2·S1·S0' + I3·S1·S0` |
| 8:1 | I0 a I7 | S2, S1, S0 | construído a partir de 2 × MUX 4:1 + 1 × MUX 2:1 |

## Requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa

## Estrutura dos arquivos

```
mux-trabalho/
├── README.md              # versão técnica (este arquivo)
├── README_para_leigos.md  # explicação simples, para quem nunca viu o assunto
├── mux.py                 # portas lógicas e multiplexadores (2:1, 4:1, 8:1)
├── demo_mux4.py           # demonstração base: MUX 4:1
└── exemplo1_mux8.py       # Exemplo 1: MUX 8:1 hierárquico
```

## Como executar

```bash
git clone https://github.com/RenatoCaresia/mux-trabalho.git
cd mux-trabalho

python demo_mux4.py
python exemplo1_mux8.py
```

Se o comando `python` não for encontrado, use `python3` (Mac/Linux) ou `py` (Windows).

Todos os scripts aceitam argumentos opcionais, úteis para testar valores diferentes durante a apresentação. Use `--help` para ver as opções.

---

## Demonstração base — MUX 4:1

```bash
python demo_mux4.py                          # usa os valores padrão: --dados 1001 --sel 10
python demo_mux4.py --dados 0110 --sel 01    # escolhe outros valores
```

- `--dados`: 4 bits, na ordem `I0 I1 I2 I3`
- `--sel`: 2 bits, na ordem `S1 S0`

**Entradas:** quatro bits de dados e dois bits de seleção.
**Processamento:** duas portas NOT (geram `S1'` e `S0'`), quatro portas AND de 3 entradas (uma por combinação de seleção) e uma porta OR que junta as saídas das ANDs. O programa mostra o sinal de cada AND, então dá para ver que só uma fica habilitada por vez.
**Saída:** `Y`, igual à entrada escolhida.

Exemplo de execução (valores padrão, `--dados 1001 --sel 10`):

```
Exemplo de execução
  Entradas de dados : I0=1 I1=0 I2=0 I3=1
  Seleção           : S1=1 S0=0  ->  endereço 2
  Processamento     : cada AND confere se S1 S0 é o endereço dela
    porta | endereço | seleção bate? | dado | saída da AND
    ------+----------+---------------+------+-------------
    AND0  |    00    |     0         | I0=1 |      0
    AND1  |    01    |     0         | I1=0 |      0
    AND2  |    10    |     1  <--    | I2=0 |      0
    AND3  |    11    |     0         | I3=1 |      0
    OR junta as 4 saídas: OR(0, 0, 0, 0) = 0
  Saída             : Y = 0  (igual a I2 = 0)
```

Repare que a AND2 está habilitada (a seleção bate), mas o dado dela é 0, então a saída é 0. A AND0 e a AND3 têm dado 1, mas estão desligadas pela seleção.

**Verificação:** no final, o script testa as **64 combinações possíveis** (16 combinações de dados × 4 seleções = 2⁶) e confere que a saída é sempre a entrada certa e que só uma AND fica habilitada em cada caso.

---

## Exemplo 1 — MUX 8:1 construído a partir de MUX 4:1 e 2:1

```bash
python exemplo1_mux8.py                    # varre as 8 seleções
python exemplo1_mux8.py --dados 01101001   # escolhe outros dados (I0..I7)
python exemplo1_mux8.py --sel 011          # uma execução (S2 S1 S0)
```

**Ideia:** um MUX grande pode ser montado com MUX menores (construção hierárquica).

```
   I0 I1 I2 I3 --> [ MUX 4:1  A ] --> YA --+
                      S1  S0                |
                                            +--> [ MUX 2:1 ] --> Y
   I4 I5 I6 I7 --> [ MUX 4:1  B ] --> YB --+        S2
                      S1  S0
```

- Os bits `S1 S0` vão para os **dois** MUX 4:1 ao mesmo tempo. Cada um escolhe uma entrada da sua metade.
- O bit `S2` vai para o MUX 2:1 e decide qual metade chega à saída.
- Assim, o endereço `S2 S1 S0` escolhe uma das 8 entradas.

**Entradas:** 8 bits de dados e 3 bits de seleção.
**Processamento:** dois MUX 4:1 em paralelo, seguidos de um MUX 2:1.
**Saída:** `Y`, mais os sinais intermediários `YA` e `YB`, para dar para ver o caminho dos dados.

Exemplo de execução (`--sel 011`, dados padrão `10110010`):

```
Exemplo de execução
  Seleção        : S2=0 S1=1 S0=1  ->  endereço 3
  Passo 1 (S1S0) : MUX A entrega YA=1 | MUX B entrega YB=0
  Passo 2 (S2)   : S2=0 escolhe a metade A (I0..I3)
  Saída          : Y = 1  (igual a I3 = 1)
```

**Verificação:** o script compara o circuito com a definição matemática `Y = I[endereço]` para as **2048 combinações possíveis** (256 combinações de dados × 8 seleções = 2¹¹, já que são 11 bits de entrada no total). O resultado esperado é `Divergências: 0`.

---

## Roteiro da demonstração (aprox. 3 minutos e meio)

A apresentação completa tem de 10 a 15 minutos; esta é a parte prática, com a mesma divisão dos slides. Todos devem saber explicar o código, mesmo a parte que não apresentam.

| Tempo | Quem | O que dizer | O que mostrar |
|-------|------|-------------|---------------|
| 0:00 – 0:30 | Kaio Henrique | **Como implementamos.** O MUX foi feito em Python só com portas AND, OR e NOT, sem `if` escolhendo a saída. O código de `mux4x1` é a equação do MUX 4:1 escrita em Python. | Slide "Como implementamos" ou `mux.py` aberto |
| 0:30 – 1:45 | Kaio Henrique | **MUX 4:1.** Cada porta AND confere se a seleção é o endereço dela, e a OR junta tudo. Mostrar na coluna "seleção bate?" que só uma AND fica habilitada por vez. Citar a verificação das 64 combinações. | `python demo_mux4.py` e depois um caso diferente, como `--dados 0110 --sel 01` |
| 1:45 – 3:00 | Luiz Otavio | **Exemplo 1: MUX 8:1.** S1 e S0 vão para os dois MUX 4:1, e S2 escolhe a metade. Mostrar na tabela as colunas YA e YB e como Y acompanha uma delas. Citar a verificação das 2048 combinações. | `python exemplo1_mux8.py` e depois `--sel 011` |
| 3:00 – 3:30 | Renato Caresia | **Conclusão.** O MUX é o seletor do computador: escolhe operandos, operações da ULA e registradores, e MUX pequenos formam MUX maiores. Dizer onde está o repositório. | Slide de conclusão |

**Dicas para a apresentação**

- Digitem um comando ao vivo, em vez de só mostrar o resultado pronto. O professor valoriza ver entrada, processamento e saída.
- Melhor ainda: peçam para o professor escolher os bits de `--dados` e `--sel` na hora. Isso mostra que a saída não foi preparada antes.
- Se o tempo apertar, cortem a leitura de código e fiquem na saída do terminal com a explicação da lógica.
- Tenham um plano B: um vídeo curto gravado da execução, caso o computador da sala dê problema.
- Todos devem conseguir explicar `mux.py`. As funções `mux4x1`, `mux4x1_passo_a_passo` (a mesma equação, guardando o sinal de cada porta para mostrar na tela) e `mux8x1_passo_a_passo` são os pontos mais prováveis de perguntas.

---

## Referências

- TOCCI, Ronald J.; WIDMER, Neal S.; MOSS, Gregory L. **Sistemas digitais**: princípios e aplicações. 12. ed. São Paulo: Pearson, 2019.
- STALLINGS, William. **Arquitetura e organização de computadores**. 10. ed. São Paulo: Pearson, 2017.
- TEXAS INSTRUMENTS. **SNx4HC151**: 8-line to 1-line data selectors/multiplexers. Datasheet SCLS110F. Dallas, 2022. Disponível em: <https://www.ti.com/lit/gpn/sn74hc151>. Acesso em: 23 nov. 2026.
- ENCYCLOPAEDIA BRITANNICA. **Telegraph**: development of the telegraph industry. Disponível em: <https://www.britannica.com/technology/telegraph/Development-of-the-telegraph-industry>. Acesso em: 23 nov. 2026.
- IEEE SPECTRUM. **Chip Hall of Fame**: Xilinx XC2064 FPGA. Disponível em: <https://spectrum.ieee.org/chip-hall-of-fame-xilinx-xc2064-fpga>. Acesso em: 23 nov. 2026.
- ALL ABOUT CIRCUITS. **Purpose and internal functionality of FPGA look-up tables**. Disponível em: <https://www.allaboutcircuits.com/technical-articles/purpose-and-internal-functionality-of-fpga-look-up-tables/>. Acesso em: 23 nov. 2026.
- PYTHON SOFTWARE FOUNDATION. **Documentação do Python 3**. Disponível em: <https://docs.python.org/3/>. Acesso em: 23 nov. 2026.
