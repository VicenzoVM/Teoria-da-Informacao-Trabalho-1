# Como Usar — Interface Gráfica de Teoria da Informação

Execute `python main.py` para abrir a janela. Ela possui três abas.

---

## Aba 1 — TP1: Codificação / Decodificação

### Campo "Texto / Número(s)"

É a entrada principal. O que você digitar aqui define o que será codificado.

| O que digitar | Interpretação |
|---|---|
| `hello` | Texto — cada letra é um símbolo |
| `abracadabra` | Texto — cada letra é um símbolo |
| `65 66 67` | Números separados por espaço — cada número é um símbolo |
| `3,5,7,3` | Números separados por vírgula — cada número é um símbolo |
| `104` | Número único — tratado como texto (cada dígito é símbolo) |

> Para Golomb, Elias-Gamma e Fibonacci: se você digitar **texto**, ele é convertido automaticamente para ASCII antes de codificar. Se digitar **números**, eles são usados diretamente.

---

### Método: Golomb

Requer o **parâmetro M** (inteiro positivo ≥ 1). Campo extra aparece ao selecionar.

**Exemplos de entrada:**

| Campo "Texto / Número(s)" | M | Resultado esperado |
|---|---|---|
| `13` | `4` | `111001` |
| `0` | `4` | `0` |
| `7` | `2` | `11100` |
| `A` | `4` | Converte `A` → ASCII 65, codifica 65 |
| `hi` | `3` | Converte `h`→104, `i`→105, codifica cada um |

**Para decodificar:** cole o codeword no campo **"Codeword atual"** e clique em **Decodificar**. Se o codeword tiver vários números, separe por espaço: `111001 0 11100`.

---

### Método: Elias-Gamma

Aceita apenas inteiros positivos (≥ 1). Texto é convertido para ASCII automaticamente.

**Exemplos de entrada:**

| Campo "Texto / Número(s)" | Codeword gerado |
|---|---|
| `1` | `1` |
| `2` | `010` |
| `10` | `0001010` |
| `A` | Converte `A` → 65 → `00000001000001` |
| `hi` | Converte `h`→104 e `i`→105, exibe ambos |

**Para decodificar:** cole os bits no campo **"Codeword atual"**. Se houver múltiplos, separe por espaço.

---

### Método: Fibonacci / Zeckendorf

Aceita inteiros positivos (≥ 1). Texto vira ASCII automaticamente.

**Exemplos de entrada:**

| Campo "Texto / Número(s)" | Codeword gerado |
|---|---|
| `1` | `11` |
| `4` | `1011` |
| `13` | `1000001` |
| `A` | Converte `A` → 65 → `...` |
| `hi` | Converte `h`→104 e `i`→105 |

**Para decodificar:** cole os bits (com stop-bit `1` ao final) no campo **"Codeword atual"**.

---

### Método: Huffman

Aceita **texto** (cada caractere é símbolo) **ou números separados por espaço/vírgula** (cada número é símbolo).

**Exemplos de entrada:**

| Campo "Texto / Número(s)" | Modo detectado | O que acontece |
|---|---|---|
| `hello` | Texto | Codifica h, e, l, o como símbolos |
| `abracadabra` | Texto | Calcula frequências: a=5, b=2, r=2, c=1, d=1 |
| `65 66 67 65` | Numérico | Símbolos são "65", "66", "67" |
| `3,5,7,3` | Numérico | Símbolos são "3", "5", "7" |
| `aabc` | Texto | a=2, b=1, c=1 |

> Huffman exige **ao menos 2 símbolos distintos** na entrada. `aaaa` dará erro.

**Para decodificar:** cole o **JSON completo** gerado pelo codificador no campo **"Codeword atual"**. Exemplo:
```
{"codes": {"l": "0", "h": "100", "e": "101", "o": "11"}, "data": "100101000011", "mode": "text"}
```

---

### Inserção de Erro (Bit Flip)

Após codificar, o codeword aparece automaticamente no campo **"Codeword atual"**.

1. Digite uma posição no campo **"Posição do bit (0-based)"**
2. Clique **"Inserir Erro"**
3. O bit naquela posição é invertido (0→1 ou 1→0)
4. Você pode então clicar **"Decodificar"** para ver o efeito do erro

**Exemplos:**

| Codeword | Posição | Resultado |
|---|---|---|
| `111001` | `0` | `011001` (1º bit invertido) |
| `111001` | `5` | `111000` (último bit invertido) |
| `0001010` | `3` | `0000010` |

---

## Aba 2 — TP2: Detecção e Correção de Erro

### Método: CRC-4

Polinômio gerador fixo: **G(x) = x⁴ + x + 1 → `10011`**

**Campo "Bits":** qualquer sequência de 0s e 1s.

**Exemplos de codificação:**

| Entrada | Bits de CRC | Codeword final |
|---|---|---|
| `1101` | `0100` | `11010100` |
| `1010` | `1110` | `10101110` |
| `11001010` | `0110` | `110010100110` |
| `0` | calculado | `0` + 4 bits CRC |

**Para verificar:** cole o codeword (dados + CRC) no campo **"Codeword"** e clique **"Verificar / Decodificar"**.
- Se resto = `0000` → sem erros
- Se resto ≠ `0000` → erro detectado

---

### Método: Hamming (7,4)

**Para codificar:** exatamente **4 bits** no campo "Bits".

| Entrada (4 bits) | Codeword (7 bits) |
|---|---|
| `1011` | `0110011` |
| `0000` | `0000000` |
| `1111` | `1111111` |
| `1010` | `1110100` |
| `0101` | `0001101` |

**Para decodificar/corrigir:** cole os **7 bits** no campo **"Codeword"** e clique **"Verificar / Decodificar"**.
- Exibe a posição do erro (1 a 7) se houver
- Mostra o codeword corrigido e os 4 bits de dados recuperados

---

### Método: Repetição Ri

**Campo "R":** inteiro ímpar ≥ 1 (ex: 3, 5, 7). Ímpar é obrigatório para votação majoritária funcionar.

**Para codificar:** qualquer sequência de bits.

| Entrada | R | Codeword gerado |
|---|---|---|
| `101` | `3` | `111000111` |
| `10` | `5` | `1111100000` |
| `1101` | `3` | `111111000111` |
| `0` | `3` | `000` |

**Para decodificar:** cole o codeword no campo **"Codeword"** com o mesmo valor de R e clique **"Verificar / Decodificar"**.
- Aplica votação majoritária em cada grupo de R bits
- Informa quais grupos tinham votos discordantes (posição 0-based)

---

### Inserção de Erro Manual (Aba 2)

1. Codifique uma mensagem (clique **"Codificar"** — o codeword vai para o campo **"Codeword"**)
2. Digite a posição do bit a inverter em **"Posição (0-based)"**
3. Clique **"Inserir Erro"**
4. Clique **"Verificar / Decodificar"** para ver a detecção/correção em ação

**Exemplo prático com Hamming:**
```
Dados:     1011
Codeword:  0110011   (posições: p1 p2 d1 p4 d2 d3 d4)
Erro pos 4 → 0110111
Decodificar → detecta erro na posição 4, corrige para 0110011, dados = 1011
```

---

## Aba 3 — TP2: Comunicação Socket

### Passo a passo

1. **Clique em "Iniciar Servidor"**
   - O status muda para `● Rodando` (verde)
   - O servidor TCP fica escutando em `localhost:65432`
   - Você pode iniciar e parar quantas vezes quiser

2. **Preencha o campo "Mensagem (bits)"**
   - Deve conter apenas `0` e `1`

3. **Selecione o método de erro**

4. **Opcional — marque "Sim, posição:" para inserir um erro antes de enviar**
   - O bit na posição informada será invertido antes da transmissão

5. **Clique em "Enviar (Cliente)"**
   - O cliente codifica, (opcionalmente corrompe) e envia ao servidor
   - O servidor verifica/corrige e responde
   - Tudo aparece no Log em tempo real

---

### Exemplos por método

#### Hamming (7,4)
| Campo "Mensagem" | O que acontece |
|---|---|
| `1011` | Codifica → `0110011`, envia ao servidor, servidor decodifica → `1011` |
| `0000` | Codifica → `0000000`, envia, servidor confirma sem erros |
| `1111` | Codifica → `1111111`, envia, servidor decodifica → `1111` |

> Hamming exige **exatamente 4 bits**. Entrada `10` ou `10110` dará erro.

#### CRC-4
| Campo "Mensagem" | O que acontece |
|---|---|
| `1101` | Calcula CRC → `11010100`, envia, servidor verifica resto = 0000 |
| `10101010` | Qualquer tamanho funciona |

#### Repetição (R=3)
| Campo "Mensagem" | O que acontece |
|---|---|
| `101` | Codifica → `111000111`, envia, servidor vota e decodifica → `101` |
| `11` | Codifica → `111111`, envia, servidor decodifica → `11` |

---

### Exemplo com erro deliberado

**Cenário:** testar se o Hamming detecta e corrige 1 bit errado.

1. Mensagem: `1011`
2. Método: Hamming
3. Marcar "Sim, posição: `4`"
4. Clicar **"Enviar (Cliente)"**

**O log mostrará:**
```
[Cliente] Dados originais : 1011
[Cliente] Método          : hamming
[Cliente] Codeword enviado: 0110011
[Cliente] ⚠ Erro inserido na posição 4: 0110111
[Servidor] Recebido   : 0110111
[Servidor] Erro?       : Sim
[Servidor] Corrigido  : 0110011
[Servidor] Decodificado: 1011
[Servidor] Mensagem    : Erro corrigido na posição 5
```

---

## Resumo rápido de entradas válidas

| Método | Campo | Exemplo válido | Inválido |
|---|---|---|---|
| Golomb | Texto/Nº | `13` ou `hello` | negativo |
| Elias-Gamma | Texto/Nº | `10` ou `AB` | `0` ou negativo |
| Fibonacci | Texto/Nº | `13` ou `hi` | `0` ou negativo |
| Huffman | Texto/Nº | `hello` / `3 5 7` | único símbolo (`aaaa`) |
| CRC-4 | Bits | `1101` | `abc` ou `1 0 1` |
| Hamming encode | Bits | `1011` | menos ou mais de 4 bits |
| Hamming decode | Bits | `0110011` | menos ou mais de 7 bits |
| Repetição | Bits | `101` com R=`3` | R par (ex: 2, 4) |
| Socket Hamming | Bits | `1011` (4 bits) | qualquer outro tamanho |
| Socket CRC | Bits | `11001010` | letras ou espaços |
| Socket Repetição | Bits | `1011` com R ímpar | R par |
