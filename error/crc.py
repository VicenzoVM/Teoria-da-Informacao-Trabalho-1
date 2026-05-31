# Polinômio gerador G(x) = x^4 + x + 1  →  binário: 10011
GENERATOR = "10011"
DEGREE = 4


def _xor_divide(dividend: str, divisor: str) -> str:
    """Divisão módulo 2 (XOR). Retorna o resto com (len(divisor)-1) bits."""
    r = list(dividend)
    dlen = len(divisor)

    for i in range(len(r) - dlen + 1):
        if r[i] == "1":
            for j in range(dlen):
                r[i + j] = "0" if r[i + j] == divisor[j] else "1"

    return "".join(r[-(dlen - 1):])


def get_crc(data_bits: str) -> str:
    """Calcula os 4 bits de CRC para os dados fornecidos."""
    data_bits = data_bits.strip()
    if not all(c in "01" for c in data_bits):
        raise ValueError("Entrada deve conter apenas bits '0' e '1'")
    return _xor_divide(data_bits + "0" * DEGREE, GENERATOR)


def encode(data_bits: str) -> str:
    """Retorna dados + 4 bits de CRC concatenados."""
    data_bits = data_bits.strip()
    if not all(c in "01" for c in data_bits):
        raise ValueError("Entrada deve conter apenas bits '0' e '1'")
    return data_bits + get_crc(data_bits)


def verify(received_bits: str) -> dict:
    """
    Verifica os bits recebidos (dados + CRC).
    Retorna {"has_error": bool, "remainder": str, "message": str}.
    """
    received_bits = received_bits.strip()
    if not all(c in "01" for c in received_bits):
        raise ValueError("Entrada deve conter apenas bits '0' e '1'")

    remainder = _xor_divide(received_bits, GENERATOR)
    has_error = remainder != "0" * DEGREE

    return {
        "has_error": has_error,
        "remainder": remainder,
        "message": "Erro detectado! (resto ≠ 0)" if has_error else "Sem erros detectados. (resto = 0)",
    }
