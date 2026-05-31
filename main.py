#!/usr/bin/env python3
"""Ponto de entrada: abre a interface gráfica de Teoria da Informação."""

import sys
import os

# Garante que o diretório do projeto está no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import App


def main() -> None:
    app = App()
    app.run()


if __name__ == "__main__":
    main()
