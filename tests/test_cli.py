"""Testes da CLI."""

from src.cli import CLI


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
