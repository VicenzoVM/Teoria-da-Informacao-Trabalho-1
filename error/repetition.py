def encode(bits: str, r: int) -> str:
    """Codifica cada bit repetindo-o r vezes."""
    if r < 1:
        raise ValueError("R deve ser pelo menos 1")
    if r % 2 == 0:
        raise ValueError("R deve ser ímpar para que a votação majoritária funcione")
    if not all(c in "01" for c in bits):
        raise ValueError("Entrada deve conter apenas bits '0' e '1'")
    return "".join(b * r for b in bits)


def decode(bits: str, r: int) -> dict:
    """
    Decodifica por votação majoritária.
    Retorna {"decoded": str, "error_positions": list[int], "has_errors": bool}.
    error_positions lista os índices (0-based) dos grupos com votos discordantes.
    """
    if r < 1:
        raise ValueError("R deve ser pelo menos 1")
    if r % 2 == 0:
        raise ValueError("R deve ser ímpar para votação majoritária")
    if not all(c in "01" for c in bits):
        raise ValueError("Entrada deve conter apenas bits '0' e '1'")
    if len(bits) % r != 0:
        raise ValueError(f"Comprimento da entrada ({len(bits)}) não é múltiplo de R ({r})")

    decoded: list = []
    error_positions: list = []

    for idx, i in enumerate(range(0, len(bits), r)):
        group = bits[i: i + r]
        ones = group.count("1")
        zeros = group.count("0")
        decoded.append("1" if ones > zeros else "0")
        if ones != r and zeros != r:  # votos discordantes → provável erro
            error_positions.append(idx)

    return {
        "decoded": "".join(decoded),
        "error_positions": error_positions,
        "has_errors": bool(error_positions),
    }
