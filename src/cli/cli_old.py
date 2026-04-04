"""Classe principal da CLI para Teoria da Informação."""

import argparse
from typing import Optional

from src.decoders.decoders import Golomb_decoder


class CLI:
    """Interface de linha de comando para Teoria da Informação."""

    def __init__(self) -> None:
        """Inicializa a CLI."""
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Cria o parser de argumentos.

        Returns:
            ArgumentParser: Parser configurado com os comandos.
        """

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

        # Comando de exemplo simples
        subparsers.add_parser("hello", help="Exibe uma mensagem de boas-vindas")

        # Comando de decodificação
        decode_parsers = subparsers.add_parser(
            "decode",
            help="Decodifica uma mensagem usando um código específico",
        )

        decode_subparsers = decode_parsers.add_subparsers(
            dest="decode_command",
            help="Comandos de decodificação",
        )

        golomb_parser = decode_subparsers.add_parser(
            "golomb",
            help="Decodifica uma mensagem usando o código de Golomb",
        )

        golomb_parser.add_argument("m", type=int, help="Parâmetro m para o código de Golomb")
        golomb_parser.add_argument("message", type=str, help="Mensagem codificada a ser decodificada")

        return parser

    def run(self, args: Optional[list[str]] = None) -> None:
        """Executa a CLI.

        Args:
            args: Argumentos da linha de comando.
        """

        parsed_args = self.parser.parse_args(args)

        if not parsed_args.command:
            self.parser.print_help()
            return

        # Roteamento de comandos
        if parsed_args.command == "hello":
            self._handle_hello()
        elif parsed_args.command == "decode":
            self._handle_decode(parsed_args)

    def _handle_hello(self) -> None:
        """Manipulador do comando hello."""
        print("Olá! Bem-vindo ao programa de Teoria da Informação.")

    def _handle_decode(self, parsed_args: argparse.Namespace) -> None:
        """Manipulador do comando decode e seus subcomandos."""

        if parsed_args.decode_command == "golomb":
            result = Golomb_decoder(parsed_args.m, parsed_args.message)
            print(result)
