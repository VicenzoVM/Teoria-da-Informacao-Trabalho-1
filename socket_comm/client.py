import socket
import json

HOST = "localhost"
PORT = 65432


def send(method: str, data: str) -> dict:
    """
    Conecta ao servidor, envia {method, data}, retorna o dict de resposta.
    Lança ConnectionRefusedError se o servidor não estiver rodando.
    """
    request = json.dumps({"method": method, "data": data}, ensure_ascii=False).encode()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        s.connect((HOST, PORT))
        s.sendall(request)
        s.shutdown(socket.SHUT_WR)

        chunks = []
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)

        return json.loads(b"".join(chunks).decode())
