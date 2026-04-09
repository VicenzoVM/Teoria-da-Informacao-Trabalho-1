#!/usr/bin/env python3
"""Ponto de entrada do programa CLI de Teoria da Informação."""

import sys

from cli import CLI


def main() -> int:
    """Função principal.

    Returns:
        int: Código de saída.
    """
    cli = CLI()
    try:
        cli.run()
        return 0
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")
        return 1
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
