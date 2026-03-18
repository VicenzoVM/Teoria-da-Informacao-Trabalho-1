"""Classe principal da CLI para Teoria da Informação."""

import argparse
from typing import Optional


class CLI:
    """Interface de linha de comando para Teoria da Informação."""

    def __init__(self):
        """Inicializa a CLI."""
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Cria o parser de argumentos.

        Returns:
            ArgumentParser: Parser configurado com os comandos.
        """
        parser = argparse.ArgumentParser(
            description="Programa de Teoria da Informação",
            prog="teoria-info",
        )

        parser.add_argument(
            "--version",
            action="version",
            version="%(prog)s 0.1.0",
        )

        subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")
        decode_parsers = subparsers.add_parser("decode", help= "Decodifica uma mensagem usando um código específico")
         

        # Exemplo de subcomando
        subparsers.add_parser(
            "Golomb",
            help="",
        )

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

    def _handle_hello(self) -> None:
        """Manipulador do comando hello."""
        print("Olá! Bem-vindo ao programa de Teoria da Informação.")
