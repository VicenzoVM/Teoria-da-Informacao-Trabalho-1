# Teoria da Informação — Trabalho Prático 1

Projeto de linha de comando para estudo de codificação e compressão em Teoria da Informação.

## Objetivo

Implementar codificação e decodificação para os métodos:

- Golomb
- Elias-Gamma
- Fibonacci/Zeckendorf
- Huffman

Também há suporte planejado para inserção de erro em bits para testes de robustez.

## Instalação

### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
```

## Como usar

Após instalar, o comando da CLI fica disponível como:

```bash
cripto-da-galera --help
```

Comando atualmente exposto na CLI:

```bash
cripto-da-galera decode golomb <m> <message>
```

Exemplo:

```bash
cripto-da-galera decode golomb 4 101001
```

## Status atual do projeto

- Fibonacci/Zeckendorf: encoder e decoder implementados no núcleo.
- Golomb, Elias-Gamma e Huffman: implementação em andamento.
- CLI: estrutura de subcomandos criada e evoluindo.

## Executar testes

```bash
python -m tests.encoder_test
python -m tests.decoder_test
python -m tests.test_cli
```

## Estrutura de pastas

```text
src/
	cli/
	encoders/
	decoders/
tests/
```

## Observações

- O projeto está em desenvolvimento acadêmico.
- A interface e os comandos podem mudar conforme os algoritmos forem finalizados.
