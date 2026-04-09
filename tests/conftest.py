"""Configuração dos testes.

Garante que o diretório ``src`` esteja disponível no ``sys.path`` para que os
pacotes instaláveis do projeto funcionem de forma consistente ao rodar
``pytest`` sem depender de instalação prévia.
"""

from pathlib import Path
import sys


SRC = Path(__file__).resolve().parents[1] / "src"
src_str = str(SRC)
if src_str not in sys.path:
    sys.path.insert(0, src_str)
