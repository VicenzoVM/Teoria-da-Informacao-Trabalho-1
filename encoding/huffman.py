import json
import heapq
from collections import Counter
from itertools import count
from typing import Dict, List, Tuple, Union


def _parse_symbols(message: str) -> Tuple[List[str], str]:
    """
    Detecta modo de entrada:
    - Se a entrada for números separados por espaço ou vírgula → modo numérico, cada número é símbolo
    - Caso contrário → modo texto, cada caractere é símbolo
    Retorna (lista_de_símbolos, modo: 'numeric' | 'text')
    """
    stripped = message.strip()
    normalized = stripped.replace(",", " ")
    parts = normalized.split()

    if len(parts) >= 2 and all(p.lstrip("-").isdigit() for p in parts):
        return parts, "numeric"

    return list(message), "text"


def _build_tree(symbols: List[str]) -> Dict[str, str]:
    freq = Counter(symbols)

    if len(freq) < 2:
        raise ValueError("Huffman requer ao menos 2 símbolos distintos na entrada")

    heap: list = []
    counter = count()
    for symbol, f in freq.items():
        heapq.heappush(heap, (f, next(counter), symbol))

    while len(heap) > 1:
        f1, _, n1 = heapq.heappop(heap)
        f2, _, n2 = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, next(counter), (n1, n2)))

    _, _, root = heap[0]

    codes: Dict[str, str] = {}

    def _walk(node: Union[str, tuple], prefix: str) -> None:
        if isinstance(node, str):
            codes[node] = prefix or "0"
            return
        left, right = node
        _walk(left, prefix + "0")
        _walk(right, prefix + "1")

    _walk(root, "")
    return codes


def encode(message: str) -> str:
    """
    Codifica a mensagem com Huffman.
    Aceita texto (cada caractere é símbolo) ou números separados por espaço/vírgula
    (ex: '3 5 7' ou '65,66,67' — cada número é um símbolo distinto).
    Retorna JSON com {codes, data, mode}.
    """
    if not message:
        return ""

    symbols, mode = _parse_symbols(message)
    codes = _build_tree(symbols)
    data = "".join(codes[s] for s in symbols)

    return json.dumps({"codes": codes, "data": data, "mode": mode}, ensure_ascii=False)


def decode(message: str) -> str:
    """
    Decodifica o JSON gerado por encode().
    Retorna o texto original ou os números separados por espaço.
    """
    if not message:
        return ""

    try:
        payload = json.loads(message)
    except json.JSONDecodeError as exc:
        raise ValueError("Entrada inválida: use o JSON gerado pelo codificador Huffman") from exc

    codes: Dict[str, str] = payload["codes"]
    data: str = payload["data"]
    mode: str = payload.get("mode", "text")

    inv = {code: sym for sym, code in codes.items()}

    decoded: List[str] = []
    buf = ""
    for bit in data:
        if bit not in "01":
            raise ValueError("Dados binários inválidos no campo 'data'")
        buf += bit
        if buf in inv:
            decoded.append(inv[buf])
            buf = ""

    if buf:
        raise ValueError("Dados Huffman incompletos: bits restantes não formam símbolo válido")

    return " ".join(decoded) if mode == "numeric" else "".join(decoded)
