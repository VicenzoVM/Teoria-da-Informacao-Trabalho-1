"""Classe principal da CLI para Teoria da Informação."""

import argparse
from typing import Optional

from encoders.encoders import (
    Golomb_encoder,
    Elias_Gamma_encoder,
    Fibonnaci_Zeckendorf_encoder,
    Huffman_encoder,
    bit_flip,
)
from decoders.decoders import (
    Golomb_decoder,
    Elias_Gamma_decoder,
    Fibonnaci_Zeckendorf_decoder,
    Huffman_decoder,
)


class CLI:
    """Interface de linha de comando para Teoria da Informação."""

    def __init__(self) -> None:
        """Inicializa a CLI."""
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Cria o parser de argumentos."""

        parser = argparse.ArgumentParser(
            description="Programa de Teoria da Informação",
            prog="cripto-da-galera",
        )

        parser.add_argument(
            "--version",
            action="version",
            version="%(prog)s 0.1.0",
        )

        subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

        # hello
        subparsers.add_parser("hello", help="Exibe uma mensagem de boas-vindas")

        # Comando legend ────────────────────────────────────────────
        subparsers.add_parser("legend", help="Exibe exemplos práticos de como usar os comandos")

        # ── ENCODE ──────────────────────────────────────────────────────────
        encode_parser = subparsers.add_parser(
            "encode",
            help="Codifica uma mensagem usando um código específico",
        )
        encode_subparsers = encode_parser.add_subparsers(
            dest="encode_command",
            help="Algoritmo de codificação",
        )

        enc_golomb = encode_subparsers.add_parser(
            "golomb",
            help="Codifica usando Golomb  →  encode golomb <m> <n>",
        )
        enc_golomb.add_argument("m", type=int, help="Parâmetro m (inteiro positivo)")
        enc_golomb.add_argument("message", type=str, help="Inteiro não-negativo a codificar")

        enc_elias = encode_subparsers.add_parser(
            "elias-gamma",
            help="Codifica usando Elias-Gamma  →  encode elias-gamma <n>",
        )
        enc_elias.add_argument("message", type=str, help="Inteiro positivo a codificar")

        enc_fib = encode_subparsers.add_parser(
            "fibonacci",
            help="Codifica usando Fibonacci/Zeckendorf  →  encode fibonacci <n>",
        )
        enc_fib.add_argument("message", type=int, help="Inteiro positivo a codificar")

        enc_huff = encode_subparsers.add_parser(
            "huffman",
            help="Codifica usando Huffman  →  encode huffman <texto>",
        )
        enc_huff.add_argument("message", type=str, help="Texto a codificar")

        enc_bf = encode_subparsers.add_parser(
            "bit-flip",
            help="Aplica bit-flip aleatório  →  encode bit-flip <bits> <prob> [--seed N]",
        )
        enc_bf.add_argument("message", type=str, help="String de bits (ex: 10110)")
        enc_bf.add_argument("probability", type=float, help="Probabilidade de inversão (0.0–1.0)")
        enc_bf.add_argument("--seed", type=int, default=None, help="Semente aleatória (opcional)")

        # ── DECODE ──────────────────────────────────────────────────────────
        decode_parser = subparsers.add_parser(
            "decode",
            help="Decodifica uma mensagem usando um código específico",
        )
        decode_subparsers = decode_parser.add_subparsers(
            dest="decode_command",
            help="Algoritmo de decodificação",
        )

        dec_golomb = decode_subparsers.add_parser(
            "golomb",
            help="Decodifica usando Golomb  →  decode golomb <m> <bits>",
        )
        dec_golomb.add_argument("m", type=int, help="Parâmetro m para o código de Golomb")
        dec_golomb.add_argument("message", type=str, help="Bits codificados a decodificar")

        dec_elias = decode_subparsers.add_parser(
            "elias-gamma",
            help="Decodifica usando Elias-Gamma  →  decode elias-gamma <bits>",
        )
        dec_elias.add_argument("message", type=str, help="Bits codificados a decodificar")

        dec_fib = decode_subparsers.add_parser(
            "fibonacci",
            help="Decodifica usando Fibonacci/Zeckendorf  →  decode fibonacci <bits>",
        )
        dec_fib.add_argument("message", type=str, help="Bits codificados a decodificar")

        dec_huff = decode_subparsers.add_parser(
            "huffman",
            help="Decodifica usando Huffman  →  decode huffman '<json>'",
        )
        dec_huff.add_argument("message", type=str, help="JSON gerado pelo encoder Huffman")

        return parser

    def run(self, args: Optional[list[str]] = None) -> None:
        """Executa a CLI."""

        parsed_args = self.parser.parse_args(args)

        if not parsed_args.command:
            self.parser.print_help()
            return

        if parsed_args.command == "hello":
            self._handle_hello()
        # Redirecionamento para a legenda ───────────────────────────
        elif parsed_args.command == "legend":
            self._handle_legend()
        elif parsed_args.command == "encode":
            self._handle_encode(parsed_args)
        elif parsed_args.command == "decode":
            self._handle_decode(parsed_args)

    def _handle_hello(self) -> None:
        print("Olá! Bem-vindo ao programa de Teoria da Informação.")

    # Método que imprime a legenda ──────────────────────────────
    def _handle_legend(self) -> None:
        """Exibe um menu de ajuda rápida com exemplos de todos os comandos."""
        legenda = """
=====================================================================
          📜 LEGENDA DE COMANDOS - CRIPTO DA GALERA 📜
=====================================================================

🔢 FIBONACCI (Zeckendorf)
   Encode: cripto-da-galera encode fibonacci 13
   Decode: cripto-da-galera decode fibonacci 1000001

🔢 ELIAS-GAMMA
   Encode: cripto-da-galera encode elias-gamma 10
   Decode: cripto-da-galera decode elias-gamma 0001010

🔢 GOLOMB (Requer o parâmetro divisor 'M' antes do valor)
   Encode: cripto-da-galera encode golomb 4 13
   Decode: cripto-da-galera decode golomb 4 111001

🔤 HUFFMAN (Para textos)
   Encode: cripto-da-galera encode huffman "hello"
   
   Decode (Terminal Padrão):
   cripto-da-galera decode huffman '{"codes": {"h": "00", "e": "01", "o": "10", "l": "11"}, "data": "0001111110"}'
   
   Decode (Exclusivo PowerShell):
   cripto-da-galera decode huffman '{\\"codes\\": {\\"h\\": \\"00\\", \\"e\\": \\"01\\", \\"o\\": \\"10\\", \\"l\\": \\"11\\"}, \\"data\\": \\"0001111110\\"}'

⚠️ INSERÇÃO DE ERRO (BIT-FLIP)
   Comando: cripto-da-galera encode bit-flip 00000000 0.5
   * Onde 0.5 é a probabilidade (50%) de inversão de cada bit.

=====================================================================
        """
        print(legenda)

    def _handle_encode(self, parsed_args: argparse.Namespace) -> None:
        cmd = parsed_args.encode_command

        if cmd is None:
            self.parser.parse_args(["encode", "--help"])
            return

        if cmd == "golomb":
            print(Golomb_encoder(parsed_args.m, parsed_args.message))
        elif cmd == "elias-gamma":
            print(Elias_Gamma_encoder(parsed_args.message))
        elif cmd == "fibonacci":
            print(Fibonnaci_Zeckendorf_encoder(parsed_args.message))
        elif cmd == "huffman":
            print(Huffman_encoder(parsed_args.message))
        elif cmd == "bit-flip":
            print(bit_flip(parsed_args.message, parsed_args.probability, parsed_args.seed))

    def _handle_decode(self, parsed_args: argparse.Namespace) -> None:
        cmd = parsed_args.decode_command

        if cmd is None:
            self.parser.parse_args(["decode", "--help"])
            return

        if cmd == "golomb":
            print(Golomb_decoder(parsed_args.m, parsed_args.message))
        elif cmd == "elias-gamma":
            print(Elias_Gamma_decoder(parsed_args.message))
        elif cmd == "fibonacci":
            print(Fibonnaci_Zeckendorf_decoder(parsed_args.message))
        elif cmd == "huffman":
            print(Huffman_decoder(parsed_args.message))
