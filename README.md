# Teoria da Informação — Trabalho Prático 1

Ferramenta de linha de comando para codificação e decodificação de dados, implementando os principais algoritmos estudados em Teoria da Informação.

---

## Sumário

- [Algoritmos implementados](#algoritmos-implementados)
- [Instalação](#instalação)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Como usar a CLI](#como-usar-a-cli)
  - [encode](#encode)
  - [decode](#decode)
  - [bit-flip](#bit-flip)
- [Referência rápida](#referência-rápida)
- [Executar testes](#executar-testes)

---

## Algoritmos implementados

| Algoritmo | Encoder | Decoder | Observação |
|---|---|---|---|
| Golomb | ✅ | ✅ | Requer parâmetro `m` |
| Elias-Gamma | ✅ | ✅ | Apenas inteiros positivos |
| Fibonacci/Zeckendorf | ✅ | ✅ | Representação de Zeckendorf com stop-bit |
| Huffman | ✅ | ✅ | Saída/entrada em JSON |
| Bit-flip (inserção de erro) | ✅ | — | Suporta semente para reprodutibilidade |

---

## Instalação

Requisito: **Python 3.9 ou superior**.

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
```

Após instalar, o comando `cripto-da-galera` fica disponível globalmente no ambiente virtual.

```bash
cripto-da-galera --help
```

---

## Estrutura do projeto

```
.
├── src/
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py         # Entry point da CLI empacotada
│   │   └── cli.py          # Definição de todos os subcomandos da CLI
│   ├── encoders/
│   │   ├── __init__.py
│   │   └── encoders.py     # Golomb, Elias-Gamma, Fibonacci, Huffman, bit_flip
│   └── decoders/
│       ├── __init__.py
│       └── decoders.py     # Golomb, Elias-Gamma, Fibonacci, Huffman
├── tests/
│   ├── conftest.py
│   ├── test_algoritmos.py
│   ├── test_carga.py
│   └── test_cli.py
├── main.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Como usar a CLI

A CLI é organizada em dois comandos principais — `encode` e `decode` — cada um com subcomandos para cada algoritmo.

```
cripto-da-galera <comando> <subcomando> [argumentos]
```

---

### encode

#### Golomb

Codifica um inteiro não-negativo usando o código de Golomb com parâmetro `m`.

```bash
cripto-da-galera encode golomb <m> <n>
```

| Argumento | Tipo | Descrição |
|---|---|---|
| `m` | inteiro positivo | Parâmetro divisor do código de Golomb |
| `n` | inteiro ≥ 0 | Valor a codificar |

```bash
# Exemplo
cripto-da-galera encode golomb 4 13
# Saída: 111001
```

---

#### Elias-Gamma

Codifica um inteiro positivo usando o código Elias-Gamma.

```bash
cripto-da-galera encode elias-gamma <n>
```

| Argumento | Tipo | Descrição |
|---|---|---|
| `n` | inteiro > 0 | Valor a codificar |

```bash
# Exemplo
cripto-da-galera encode elias-gamma 10
# Saída: 0001010
```

---

#### Fibonacci / Zeckendorf

Codifica um inteiro positivo na representação de Zeckendorf (soma de Fibonacci não consecutivos), com stop-bit ao final.

```bash
cripto-da-galera encode fibonacci <n>
```

| Argumento | Tipo | Descrição |
|---|---|---|
| `n` | inteiro > 0 | Valor a codificar |

```bash
# Exemplo
cripto-da-galera encode fibonacci 66
# Saída: 1000101001
```

Entradas inválidas como `0`, negativos ou valores não inteiros são rejeitadas.

---

#### Huffman

Codifica um texto arbitrário usando o código de Huffman. A saída é um JSON contendo o mapa de códigos (`codes`) e os bits resultantes (`data`). Guarde essa saída para decodificar depois.

```bash
cripto-da-galera encode huffman "<texto>"
```

| Argumento | Tipo | Descrição |
|---|---|---|
| `texto` | string | Texto a codificar |

```bash
# Exemplo
cripto-da-galera encode huffman "hello"
# Saída: {"codes": {"h": "00", "e": "01", "o": "10", "l": "11"}, "data": "0001111110"}
```

---

#### Bit-flip (inserção de erro)

Aplica erros aleatórios (inversão de bits) a uma string binária com uma dada probabilidade. Útil para simular ruído em canal de comunicação.

```bash
cripto-da-galera encode bit-flip <bits> <probabilidade> [--seed <N>]
```

| Argumento | Tipo | Descrição |
|---|---|---|
| `bits` | string binária | Ex: `10110011` |
| `probabilidade` | float 0.0–1.0 | Chance de cada bit ser invertido |
| `--seed` | inteiro (opcional) | Semente para resultado reproduzível |

```bash
# Exemplo sem seed (resultado aleatório a cada execução)
cripto-da-galera encode bit-flip 10101010 0.3

# Exemplo com seed (resultado sempre igual)
cripto-da-galera encode bit-flip 10101010 0.5 --seed 42
# Saída: 11011011
```

---

### decode

#### Golomb

Decodifica bits gerados pelo encoder Golomb.

```bash
cripto-da-galera decode golomb <m> <bits>
```

```bash
# Exemplo
cripto-da-galera decode golomb 4 111001
# Saída: 13
```

---

#### Elias-Gamma

Decodifica bits gerados pelo encoder Elias-Gamma.

```bash
cripto-da-galera decode elias-gamma <bits>
```

```bash
# Exemplo
cripto-da-galera decode elias-gamma 0001010
# Saída: 10
```

---

#### Fibonacci / Zeckendorf

Decodifica bits gerados pelo encoder Fibonacci.

```bash
cripto-da-galera decode fibonacci <bits>
```

```bash
# Exemplo
cripto-da-galera decode fibonacci 1000101001
# Saída: 66
```

O decoder valida que a entrada:
- contém apenas `0` e `1`
- termina com stop-bit
- não possui representação inválida antes do stop-bit

---

#### Huffman

Decodifica uma mensagem Huffman. A entrada deve ser o JSON completo gerado pelo encoder (com `codes` e `data`).

```bash
cripto-da-galera decode huffman '<json>'
```

```bash
# Exemplo (use aspas simples para proteger o JSON no terminal)
cripto-da-galera decode huffman '{"codes": {"h": "00", "e": "01", "o": "10", "l": "11"}, "data": "0001111110"}'
# Saída: hello
```

> **Dica:** Em um script, você pode encadear encode e decode salvando o JSON em uma variável:
> ```bash
> encoded=$(cripto-da-galera encode huffman "minha mensagem")
> cripto-da-galera decode huffman "$encoded"
> ```

---

## Referência rápida

```bash
# Encode
cripto-da-galera encode golomb      <m> <n>
cripto-da-galera encode elias-gamma <n>
cripto-da-galera encode fibonacci   <n>
cripto-da-galera encode huffman     "<texto>"
cripto-da-galera encode bit-flip    <bits> <prob> [--seed N]

# Decode
cripto-da-galera decode golomb      <m> <bits>
cripto-da-galera decode elias-gamma <bits>
cripto-da-galera decode fibonacci   <bits>
cripto-da-galera decode huffman     '<json>'

# Outros
cripto-da-galera hello
cripto-da-galera legend
cripto-da-galera --version
cripto-da-galera --help
```

---

## Executar testes

```bash
# Rodar toda a suíte
pytest

# Rodar apenas os testes da CLI
pytest tests/test_cli.py -v

# Rodar apenas os testes dos algoritmos
pytest tests/test_algoritmos.py -v
```

Para rodar com cobertura, instale o plugin opcional `pytest-cov` e execute:

```bash
pip install pytest-cov
pytest --cov=src
```
