def encode(n: int) -> str:
    if n <= 0:
        raise ValueError("Fibonacci/Zeckendorf é definido apenas para inteiros positivos")

    fibs = [1, 2]
    while fibs[-1] + fibs[-2] <= n:
        fibs.append(fibs[-1] + fibs[-2])

    bits = []
    remaining = n
    for v in reversed(fibs):
        if v <= remaining:
            bits.append("1")
            remaining -= v
        else:
            bits.append("0")
    bits.append("1")  # stop-bit
    return "".join(bits)


def decode(bits: str) -> int:
    bits = bits.strip()
    if not bits or any(c not in "01" for c in bits):
        raise ValueError("bits deve conter apenas '0' e '1'")
    if len(bits) < 2 or not bits.endswith("1"):
        raise ValueError("código Fibonacci/Zeckendorf inválido: stop-bit ausente")

    payload = bits[:-1]
    if not payload or "1" not in payload:
        raise ValueError("código inválido: representação vazia")
    if "11" in payload:
        raise ValueError("código inválido: '11' antes do stop-bit não é permitido")

    fibs = [1, 2]
    while len(fibs) < len(payload):
        fibs.append(fibs[-1] + fibs[-2])

    fibs = list(reversed(fibs))
    result = 0
    for i, bit in enumerate(payload):
        if bit == "1":
            result += fibs[i]
    return result
