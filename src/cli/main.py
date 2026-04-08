"""Ponto de entrada da CLI."""

import sys

from . import CLI


def main() -> int:
    """Executa a CLI e retorna código de saída do processo."""
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
