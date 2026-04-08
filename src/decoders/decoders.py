import math
import json
from typing import Dict


def _decode_golomb_single(m: int, message: str) -> int:
    """Decodifica um único inteiro codificado com Golomb.

    Args:
        m: Parâmetro do código de Golomb (inteiro positivo).
        message: String de bits contendo um único código de Golomb.
    """

    if m <= 0:
        raise ValueError("m deve ser um inteiro positivo")

    bits = message.strip()
    if not bits or any(b not in {"0", "1"} for b in bits):
        raise ValueError("message deve conter apenas bits '0' e '1'")

    # Lê parte unária: conta '1' até encontrar o primeiro '0'
    q = 0
    i = 0
    while i < len(bits) and bits[i] == "1":
        q += 1
        i += 1

    if i >= len(bits) or bits[i] != "0":
        raise ValueError("código de Golomb inválido: faltando separador unário")

    i += 1  # pula o '0'

    b = math.ceil(math.log2(m)) if m > 1 else 1
    cutoff = (1 << b) - m

    # Primeiro tenta ler (b-1) bits
    if m == 1:
        r = 0
    else:
        if i + (b - 1) > len(bits):
            raise ValueError("código de Golomb incompleto")
        r_temp = int(bits[i : i + b - 1], 2)
        if r_temp < cutoff:
            r = r_temp
            i += b - 1
        else:
            # Precisa de mais um bit
            if i + b > len(bits):
                raise ValueError("código de Golomb incompleto")
            r_temp = int(bits[i : i + b], 2)
            r = r_temp - cutoff
            i += b

    n = q * m + r
    return n


def Golomb_decoder(m: int, message: str) -> str:
    """Decodifica um único inteiro codificado com Golomb.

    Retorna o inteiro em forma de string decimal.
    """

    n = _decode_golomb_single(m, message)
    return str(n)


def Elias_Gamma_decoder(message: str) -> str:
    """Decodifica um inteiro positivo codificado com Elias-Gamma.

    Retorna o inteiro em forma de string decimal.
    """

    bits = message.strip()
    if not bits or any(b not in {"0", "1"} for b in bits):
        raise ValueError("message deve conter apenas bits '0' e '1'")

    # Conta zeros iniciais
    zeros = 0
    i = 0
    while i < len(bits) and bits[i] == "0":
        zeros += 1
        i += 1

    if i >= len(bits) or bits[i] != "1":
        raise ValueError("código Elias-Gamma inválido: faltando bit '1' após prefixo de zeros")

    # Comprimento total do binário
    length = zeros + 1
    i += 1  # consome o '1'

    if i + (length - 1) > len(bits):
        raise ValueError("código Elias-Gamma incompleto")

    binary = "1" + bits[i : i + length - 1]
    n = int(binary, 2)
    return str(n)

def Fibonnaci_Zeckendorf_decoder(message: str) -> int:
    bits = message.strip()
    if not bits or any(bit not in {"0", "1"} for bit in bits):
        raise ValueError("message deve conter apenas bits '0' e '1'")
    if len(bits) < 2 or not bits.endswith("1"):
        raise ValueError("código Fibonacci/Zeckendorf inválido: stop-bit ausente")

    payload = bits[:-1]
    if not payload or "1" not in payload:
        raise ValueError("código Fibonacci/Zeckendorf inválido: representação vazia ou malformada")
    if "11" in payload:
        raise ValueError(
            "código Fibonacci/Zeckendorf inválido: representação não pode ter '11' antes do stop-bit"
        )

    fibonacci = [1, 2]
    while len(fibonacci) < len(payload):
        fibonacci.append(fibonacci[-1] + fibonacci[-2])

    fibonacci = fibonacci[::-1]
    return_fibonacci = 0

    for i in range(len(fibonacci)):
        if payload[i] == "1":
            return_fibonacci += fibonacci[i]
    return return_fibonacci

def Huffman_decoder(message: str) -> str:
    """Decodifica uma mensagem gerada por ``Huffman_encoder``.

    Espera uma string JSON no formato:

        {"codes": {"a": "0", "b": "10", ...}, "data": "010..."}
    """

    if not message:
        return ""

    try:
        payload = json.loads(message)
    except json.JSONDecodeError as exc:  # type: ignore[no-untyped-call]
        raise ValueError("message não é um JSON válido gerado por Huffman_encoder") from exc

    if not isinstance(payload, dict) or "codes" not in payload or "data" not in payload:
        raise ValueError("message não possui o formato esperado de Huffman_encoder")

    codes: Dict[str, str] = payload["codes"]
    data: str = payload["data"]

    if not isinstance(codes, dict) or not isinstance(data, str):
        raise ValueError("message não possui o conteúdo esperado de Huffman_encoder")

    # Mapa invertido: código -> símbolo
    inv_codes: Dict[str, str] = {code: ch for ch, code in codes.items()}

    decoded_chars: list[str] = []
    buffer = ""
    for bit in data:
        if bit not in {"0", "1"}:
            raise ValueError("dados codificados devem conter apenas bits '0' e '1'")
        buffer += bit
        if buffer in inv_codes:
            decoded_chars.append(inv_codes[buffer])
            buffer = ""

    if buffer:
        raise ValueError("dados codificados de Huffman incompletos ou inválidos")

    return "".join(decoded_chars)
