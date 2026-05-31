def encode(n: int) -> str:
    if n <= 0:
        raise ValueError("Elias-Gamma é definido apenas para inteiros positivos (n ≥ 1)")

    binary = bin(n)[2:]
    return "0" * (len(binary) - 1) + binary


def decode(bits: str) -> int:
    bits = bits.strip()
    if not bits or any(c not in "01" for c in bits):
        raise ValueError("bits deve conter apenas '0' e '1'")

    zeros = 0
    i = 0
    while i < len(bits) and bits[i] == "0":
        zeros += 1
        i += 1

    if i >= len(bits):
        raise ValueError("código Elias-Gamma inválido: bit '1' ausente")

    length = zeros + 1
    i += 1  # consume the leading '1'

    if i + (length - 1) > len(bits):
        raise ValueError("código Elias-Gamma incompleto")

    return int("1" + bits[i: i + length - 1], 2)
