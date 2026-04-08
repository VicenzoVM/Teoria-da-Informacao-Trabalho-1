import math
import random
import json
from typing import Dict, Optional


def _validate_integer_string(message: str) -> int:
    """Converte uma string para inteiro, validando se é não-negativo.

    Args:
        message: Representação decimal de um inteiro não-negativo.

    Returns:
        int: Valor inteiro convertido.
    """

    message = message.strip()
    if not message.isdigit():
        raise ValueError("message deve ser um inteiro decimal não-negativo")
    return int(message)


def Golomb_encoder(m: int, message: str) -> str:
    """Codifica um único inteiro usando código de Golomb.

    A mensagem de entrada é interpretada como um inteiro decimal não-negativo.
    O retorno é uma string de bits com o código de Golomb correspondente.
    """

    if m <= 0:
        raise ValueError("m deve ser um inteiro positivo")

    n = _validate_integer_string(message)

    q = n // m
    r = n % m

    # Parte unária (quociente): q vezes '1' seguido de '0'
    unary = "1" * q + "0"

    # Parte binária (resto) com código binário truncado
    b = math.ceil(math.log2(m)) if m > 1 else 1
    cutoff = (1 << b) - m

    if r < cutoff:
        # Usa (b-1) bits
        remainder_bits = format(r, f"0{b-1}b")
    else:
        # Usa b bits para o valor ajustado
        r_adjusted = r + cutoff
        remainder_bits = format(r_adjusted, f"0{b}b")

    return unary + remainder_bits


def Elias_Gamma_encoder(message: str) -> str:
    """Codifica um inteiro positivo usando código Elias-Gamma.

    A mensagem de entrada é interpretada como um inteiro decimal > 0.
    O retorno é uma string de bits com o código Elias-Gamma correspondente.
    """

    n = _validate_integer_string(message)
    if n <= 0:
        raise ValueError("Elias-Gamma é definido apenas para inteiros positivos")

    binary = bin(n)[2:]
    length = len(binary)

    prefix = "0" * (length - 1)
    return prefix + binary

def Fibonnaci_Zeckendorf_encoder(message: int) -> str:
    if not isinstance(message, int):
        raise ValueError("Fibonacci/Zeckendorf exige um inteiro positivo")
    if message <= 0:
        raise ValueError("Fibonacci/Zeckendorf é definido apenas para inteiros positivos")

    fibonacci = [1, 2]
    while fibonacci[-1] + fibonacci[-2] <= message:
        fibonacci.append(fibonacci[-1] + fibonacci[-2])

    encoder_return: list = []
    for v in fibonacci[::-1]:
        if v <= message:
            encoder_return.append("1")
            message = message - v
        else:
            encoder_return.append("0")
    # Stop-bit para delimitar o fim da palavra-código.
    encoder_return.append("1")
    return "".join(encoder_return)


def _build_huffman_codes(message: str) -> Dict[str, str]:
    """Gera o dicionário de códigos de Huffman para a mensagem."""

    from collections import Counter
    import heapq
    from itertools import count

    if not message:
        return {}

    freq = Counter(message)

    # Heap de nós: (frequência, ordem, nó)
    # Nó é ou um caractere (folha) ou um tuplo (esquerda, direita).
    heap = []
    counter = count()
    for symbol, f in freq.items():
        heapq.heappush(heap, (f, next(counter), symbol))

    while len(heap) > 1:
        f1, _, n1 = heapq.heappop(heap)
        f2, _, n2 = heapq.heappop(heap)
        merged = (n1, n2)
        heapq.heappush(heap, (f1 + f2, next(counter), merged))

    _, _, root = heap[0]

    codes: Dict[str, str] = {}

    def build_codes(node, prefix: str) -> None:
        if isinstance(node, str):
            # Caso de apenas um símbolo: garante ao menos um bit
            codes[node] = prefix or "0"
            return
        left, right = node
        build_codes(left, prefix + "0")
        build_codes(right, prefix + "1")

    build_codes(root, "")
    return codes


def Huffman_encoder(message: str) -> str:
    """Codifica uma mensagem usando código de Huffman.

    Retorna uma string JSON contendo o mapa de códigos e os bits
    codificados, por exemplo:

        {"codes": {"a": "0", "b": "10", ...}, "data": "010..."}
    """

    if not message:
        return ""

    codes = _build_huffman_codes(message)
    encoded = "".join(codes[ch] for ch in message)

    payload = {"codes": codes, "data": encoded}
    return json.dumps(payload, ensure_ascii=False)


def bit_flip(message: str, probability: float, seed: Optional[int] = None) -> str:
    """Aplica inserção de erro (bit flip) em uma mensagem binária.

    Cada bit "0" ou "1" da mensagem tem probabilidade ``probability`` de ser
    invertido. Se ``seed`` for fornecido, o gerador aleatório é inicializado
    para permitir reprodutibilidade dos testes.
    """

    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability deve estar entre 0.0 e 1.0")

    if seed is not None:
        random.seed(seed)

    flipped: list[str] = []
    for bit in message:
        if bit not in {"0", "1"}:
            raise ValueError("message deve conter apenas caracteres '0' e '1'")
        if random.random() < probability:
            flipped.append("1" if bit == "0" else "0")
        else:
            flipped.append(bit)

    return "".join(flipped)
