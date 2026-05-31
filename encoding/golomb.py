import math


def encode(m: int, n: int) -> str:
    if m <= 0:
        raise ValueError("m deve ser um inteiro positivo")
    if n < 0:
        raise ValueError("n deve ser um inteiro não-negativo")

    q = n // m
    r = n % m

    unary = "1" * q + "0"

    b = math.ceil(math.log2(m)) if m > 1 else 1
    cutoff = (1 << b) - m

    if r < cutoff:
        remainder_bits = format(r, f"0{b - 1}b")
    else:
        remainder_bits = format(r + cutoff, f"0{b}b")

    return unary + remainder_bits


def decode(m: int, bits: str) -> int:
    if m <= 0:
        raise ValueError("m deve ser um inteiro positivo")

    bits = bits.strip()
    if not bits or any(c not in "01" for c in bits):
        raise ValueError("bits deve conter apenas '0' e '1'")

    q = 0
    i = 0
    while i < len(bits) and bits[i] == "1":
        q += 1
        i += 1

    if i >= len(bits) or bits[i] != "0":
        raise ValueError("código de Golomb inválido: separador '0' ausente")
    i += 1

    b = math.ceil(math.log2(m)) if m > 1 else 1
    cutoff = (1 << b) - m

    if m == 1:
        r = 0
    else:
        if i + (b - 1) > len(bits):
            raise ValueError("código de Golomb incompleto")
        r_temp = int(bits[i: i + b - 1], 2)
        if r_temp < cutoff:
            r = r_temp
        else:
            if i + b > len(bits):
                raise ValueError("código de Golomb incompleto")
            r = int(bits[i: i + b], 2) - cutoff

    return q * m + r
