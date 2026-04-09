"""Testes da CLI."""

import pytest

from cli import CLI


def test_cli_instantiation() -> None:
    """Testa se a CLI pode ser instanciada."""
    cli = CLI()
    assert cli is not None
    assert cli.parser is not None


def test_cli_hello_command(capsys) -> None:
    """Testa o comando hello."""
    cli = CLI()
    cli.run(["hello"])
    captured = capsys.readouterr()
    assert "Teoria da Informação" in captured.out


def test_cli_fibonacci_encode_command(capsys) -> None:
    """Testa o encode de Fibonacci pela CLI."""
    cli = CLI()
    cli.run(["encode", "fibonacci", "13"])
    captured = capsys.readouterr()
    assert captured.out.strip() == "1000001"


def test_cli_fibonacci_decode_invalido() -> None:
    """Testa erro de validação no decode de Fibonacci pela CLI."""
    cli = CLI()
    with pytest.raises(ValueError):
        cli.run(["decode", "fibonacci", "1010"])
