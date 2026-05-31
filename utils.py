def text_to_ascii(text: str) -> list:
    """Converte texto em lista de valores ASCII."""
    return [ord(c) for c in text]


def ascii_to_text(values: list) -> str:
    """Converte lista de valores ASCII em texto."""
    return "".join(chr(v) for v in values)


def flip_bit(bits: str, position: int) -> str:
    """Inverte o bit na posição dada (0-indexed)."""
    if position < 0 or position >= len(bits):
        raise ValueError(f"Posição {position} inválida para sequência de {len(bits)} bits")
    lst = list(bits)
    lst[position] = "1" if lst[position] == "0" else "0"
    return "".join(lst)


def validate_binary(bits: str) -> bool:
    """Retorna True se a string contém apenas '0' e '1'."""
    return bool(bits) and all(c in "01" for c in bits)
