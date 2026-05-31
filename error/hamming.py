"""
Hamming (7,4) — posições 1-indexed:
  Paridade : 1, 2, 4
  Dados    : 3 (d1), 5 (d2), 6 (d3), 7 (d4)
Codeword  : p1 p2 d1 p4 d2 d3 d4

Paridades:
  p1 cobre posições {1,3,5,7}  →  p1 = d1 ⊕ d2 ⊕ d4
  p2 cobre posições {2,3,6,7}  →  p2 = d1 ⊕ d3 ⊕ d4
  p4 cobre posições {4,5,6,7}  →  p4 = d2 ⊕ d3 ⊕ d4
"""


def encode(data_4bits: str) -> str:
    """Codifica 4 bits de dados em 7 bits Hamming (7,4)."""
    if len(data_4bits) != 4 or not all(c in "01" for c in data_4bits):
        raise ValueError("Entrada deve ser exatamente 4 bits (apenas '0' e '1')")

    d1, d2, d3, d4 = (int(b) for b in data_4bits)

    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p4 = d2 ^ d3 ^ d4

    return f"{p1}{p2}{d1}{p4}{d2}{d3}{d4}"


def decode(received_7bits: str) -> dict:
    """
    Decodifica e corrige (até 1 bit) código Hamming (7,4).
    Retorna:
      {"corrected": str, "error_position": int, "has_error": bool, "data": str}
    error_position é 1-indexed (0 = sem erro).
    """
    if len(received_7bits) != 7 or not all(c in "01" for c in received_7bits):
        raise ValueError("Entrada deve ser exatamente 7 bits (apenas '0' e '1')")

    r = [int(b) for b in received_7bits]
    # índices 0-6 → posições 1-7
    # r[0]=p1, r[1]=p2, r[2]=d1, r[3]=p4, r[4]=d2, r[5]=d3, r[6]=d4

    s1 = r[0] ^ r[2] ^ r[4] ^ r[6]   # posições 1,3,5,7
    s2 = r[1] ^ r[2] ^ r[5] ^ r[6]   # posições 2,3,6,7
    s4 = r[3] ^ r[4] ^ r[5] ^ r[6]   # posições 4,5,6,7

    error_position = s1 * 1 + s2 * 2 + s4 * 4  # síndrome em decimal

    corrected = r[:]
    has_error = error_position != 0
    if has_error:
        corrected[error_position - 1] ^= 1

    # Extrai dados das posições 3,5,6,7 (índices 2,4,5,6)
    data = f"{corrected[2]}{corrected[4]}{corrected[5]}{corrected[6]}"

    return {
        "corrected": "".join(str(b) for b in corrected),
        "error_position": error_position,
        "has_error": has_error,
        "data": data,
    }
