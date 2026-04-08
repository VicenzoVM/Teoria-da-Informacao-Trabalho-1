"""Configuração dos testes.

Garante que a raiz do projeto esteja disponível no ``sys.path`` para que os
imports de ``src.*`` funcionem de forma consistente ao rodar ``pytest``.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
root_str = str(ROOT)
if root_str not in sys.path:
    sys.path.insert(0, root_str)
