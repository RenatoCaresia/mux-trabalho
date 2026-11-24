# Multiplexador: explicado para quem nunca viu isso na vida

> Esta é a versão **simples** do projeto. Se você quer a versão técnica, com equações e roteiro da apresentação, veja o [README.md](README.md).

---

## 1. Primeiro: o computador só conhece 0 e 1

Pense em uma lâmpada. Ela só tem dois jeitos de estar: **acesa** ou **apagada**.

- Lâmpada acesa = **1**
- Lâmpada apagada = **0**

Tudo dentro de um computador (fotos, músicas, jogos, vídeos) é feito de um montão de "lâmpadas" que ficam acesas ou apagadas. Cada uma delas se chama **bit**.

---

## 2. O que é um multiplexador?

O nome é complicado, mas a ideia é simples: **um multiplexador é um seletor**. Ele escolhe uma coisa entre várias.

Pense no **controle remoto da TV**:

- A TV recebe **vários canais** ao mesmo tempo.
- Mas só mostra **um** por vez na tela.
- Você aperta o botão e **escolhe** qual canal quer ver.

O multiplexador (chamamos de **MUX**, para abreviar) funciona igual:

| Na TV | No MUX |
|-------|--------|
| Os canais | As **entradas** (`I0`, `I1`, `I2`...) |
| O botão que você aperta | A **seleção** (`S0`, `S1`...) |
| O que aparece na tela | A **saída** (`Y`) |

**Para que serve?** O computador precisa escolher coisas o tempo todo: qual número usar numa conta, de qual lugar da memória ler uma informação, qual operação fazer. Quem faz essa escolha é o multiplexador.

---

## 3. Como "digitar" o número do canal só com 0 e 1?

Como o computador só tem 0 e 1, o número do canal também é escrito com lâmpadas.

Com **2 lâmpadas** de seleção dá para formar 4 códigos diferentes, ou seja, **4 canais**:

| Código (S1 S0) | Canal escolhido |
|:-------------:|:---------------:|
| 0 0 | canal 0 (`I0`) |
| 0 1 | canal 1 (`I1`) |
| 1 0 | canal 2 (`I2`) |
| 1 1 | canal 3 (`I3`) |

Com **3 lâmpadas** dá para formar 8 códigos, ou seja, **8 canais**. Cada lâmpada a mais **dobra** o número de canais.

---

## 4. As três peças que usamos para construir o MUX

Construímos o MUX usando só três peças muito simples, chamadas **portas lógicas**:

**NOT ("não")**: vira o sinal ao contrário. Se entra 0, sai 1. Se entra 1, sai 0. É como um botão de "inverter".

**AND ("e")**: só deixa passar se **todas** as entradas forem 1. É como uma porta com duas fechaduras: você precisa das **duas** chaves para abrir.

**OR ("ou")**: deixa passar se **pelo menos uma** entrada for 1. É como a campainha de uma casa com duas portas: toca se alguém apertar a da frente **ou** a dos fundos.

---

## 5. Como o MUX 4:1 funciona por dentro

"4:1" quer dizer "4 entradas, 1 saída".

Imagine **4 salas**, cada uma com um **porteiro**. Dentro de cada sala tem um bilhete com 0 ou 1.

- Cada porteiro conhece **um código secreto** só dele: o da sala 0 conhece "00", o da sala 1 conhece "01", o da sala 2 conhece "10" e o da sala 3 conhece "11".
- Você diz o código para todos os porteiros ao mesmo tempo.
- **Só um porteiro abre a porta**: aquele cujo código bate. Os outros continuam de braços cruzados e entregam "0".
- Todos os corredores se juntam em um só, por onde sai o bilhete do porteiro que abriu a porta. Essa junção é a porta **OR**.

Cada porteiro é uma porta **AND**: ele só libera o bilhete se o código estiver certo. E a porta **NOT** ajuda a conferir os zeros do código.

### Exemplo

As salas têm estes bilhetes: sala 0 = **1**, sala 1 = **0**, sala 2 = **0**, sala 3 = **1**.

Você diz o código **11**. Só o porteiro da sala 3 abre a porta, e o bilhete dele (1) sai pela saída.

### Rode e veja

```bash
python demo_mux4.py --dados 1001 --sel 11
```

O programa mostra:

```
Exemplo de execução
  Entradas de dados : I0=1 I1=0 I2=0 I3=1
  Seleção           : S1=1 S0=1  ->  endereço 3
  Processamento     : cada AND confere se S1 S0 é o endereço dela
    porta | endereço | seleção bate? | dado | saída da AND
    ------+----------+---------------+------+-------------
    AND0  |    00    |     0         | I0=1 |      0
    AND1  |    01    |     0         | I1=0 |      0
    AND2  |    10    |     0         | I2=0 |      0
    AND3  |    11    |     1  <--    | I3=1 |      1
    OR junta as 4 saídas: OR(0, 0, 0, 1) = 1
  Saída             : Y = 1  (igual a I3 = 1)
```

Em português:

- **Entradas de dados:** os bilhetes das 4 salas.
- **Seleção:** o código que você disse (11, que é o endereço 3).
- **Processamento:** cada linha `AND` é um porteiro. A coluna "endereço" é o código secreto dele, e "seleção bate?" diz se ele abriu a porta. Só o porteiro da sala 3 abriu (a setinha `<--`), então só ele entrega o bilhete de verdade; os outros entregam 0.
- **Saída:** a porta OR junta tudo, e o bilhete da sala 3 sai. Ele valia 1.

O programa também confere, no final, **todas as 64 situações possíveis** do MUX 4:1 e mostra se acertou todas.

---

## 6. E se eu precisar de mais canais? O MUX 8:1

Agora imagine **8 salas**. Em vez de inventar uma peça gigante e nova, a gente **junta peças pequenas** que já temos. É como montar uma construção grande com blocos de montar.

Dividimos as 8 salas em **dois salões** de 4 salas cada:

- **Salão A:** salas 0, 1, 2 e 3
- **Salão B:** salas 4, 5, 6 e 7

O código agora tem **3 números**. Eles trabalham em duas etapas:

1. **Os dois últimos números do código** vão para os dois salões ao mesmo tempo. Cada salão tem seu MUX 4:1 e entrega o bilhete de uma sala.
2. **O primeiro número do código** vai para um MUX final, que só precisa decidir entre dois: o bilhete do salão A ou o do salão B?

É como um endereço de apartamento: uma parte diz **qual prédio** (o salão, escolhido pelo primeiro número) e a outra diz **qual apartamento dentro dele** (a sala, escolhida pelos dois últimos números).

### Exemplo

Os bilhetes das 8 salas são `1 0 1 1 0 0 1 0`. Você diz o código **011**, que é o endereço 3.

- O salão A entrega o bilhete da sala 3 dele: **1**
- O salão B entrega o bilhete da sala 3 dele (a sala 7): **0**
- O primeiro número do código é 0, que significa "fico com o salão A".
- Resultado: **1**

### Rode e veja

```bash
python exemplo1_mux8.py --sel 011
```

```
Exemplo de execução
  Seleção        : S2=0 S1=1 S0=1  ->  endereço 3
  Passo 1 (S1S0) : MUX A entrega YA=1 | MUX B entrega YB=0
  Passo 2 (S2)   : S2=0 escolhe a metade A (I0..I3)
  Saída          : Y = 1  (igual a I3 = 1)
```

`YA` e `YB` são os bilhetes que saíram dos dois salões. `S2` é o primeiro número do código, e ele escolhe qual dos dois vale.

O programa também mostra o seguinte no final:

```
Verificação exaustiva
  Combinações testadas : 2048
  Divergências         : 0
  Resultado            : MUX 8:1 correto!
```

Isso quer dizer que o programa testou **todas as 2048 situações possíveis** e acertou **todas**. É como um professor corrigindo 2048 contas e não achando nenhum erro.

---

## 7. Como rodar no seu computador (passo a passo)

**1. Instale o Python.** Baixe em [python.org](https://www.python.org/downloads/) e instale. É grátis. No Windows, se o instalador mostrar a opção "Add python.exe to PATH", marque antes de clicar em instalar.

**2. Baixe a pasta do projeto.** Na página do projeto no GitHub, clique no botão verde **Code** e depois em **Download ZIP**. O arquivo vem compactado: clique com o botão direito nele e escolha **Extrair tudo** (Windows) ou dê dois cliques (Mac). Guarde a pasta extraída em um lugar fácil de achar (por exemplo, na Área de Trabalho).

**3. Abra o terminal dentro da pasta.** O terminal é aquela janela onde a gente digita comandos em vez de clicar.
- *Windows:* abra a pasta, clique na barra de endereço no topo, apague o que estiver lá, digite `cmd` e aperte Enter.
- *Mac:* abra o aplicativo **Terminal**, digite `cd ` (com um espaço no final), arraste a pasta do projeto para dentro da janela e aperte Enter.
- *Linux:* clique com o botão direito dentro da pasta e escolha "Abrir no Terminal".

**4. Digite um comando e aperte Enter:**

```bash
python demo_mux4.py
python exemplo1_mux8.py
```

Se aparecer uma mensagem de erro dizendo que `python` não foi encontrado, tente `py` (Windows) ou `python3` (Mac/Linux) no lugar.

**5. Brinque!** Você pode mudar os bilhetes e o código:

```bash
python demo_mux4.py --dados 0110 --sel 01
python exemplo1_mux8.py --dados 11110000 --sel 101
```

- `--dados` são os bilhetes das salas, escritos em ordem (primeiro a sala 0, depois a 1, e assim por diante).
- `--sel` é o código dos porteiros.

---

## 8. Mini dicionário

| Palavra | O que significa |
|---------|-----------------|
| **Bit** | Uma "lâmpada" que pode ser 0 (apagada) ou 1 (acesa) |
| **Multiplexador (MUX)** | Um seletor: escolhe uma entre várias entradas |
| **Entrada de dados** | Os "canais" que chegam ao MUX |
| **Seleção** | O "botão" que escolhe qual canal passa |
| **Saída** | O que sai do MUX, o canal escolhido |
| **Porta lógica** | Peça simples que faz uma pequena decisão com 0 e 1 (NOT, AND, OR) |
| **Circuito** | Várias peças ligadas juntas para fazer uma tarefa |
| **Terminal** | A janela onde digitamos comandos no computador |
