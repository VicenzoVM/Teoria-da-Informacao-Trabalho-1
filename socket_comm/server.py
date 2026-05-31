import socket
import threading
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from error.crc import verify as crc_verify
from error.hamming import decode as hamming_decode
from error.repetition import decode as rep_decode

HOST = "localhost"
PORT = 65432


def _handle_client(conn: socket.socket, addr, log_cb=None) -> None:
    try:
        chunks = []
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
            try:
                request = json.loads(b"".join(chunks).decode())
                break
            except json.JSONDecodeError:
                continue

        request = json.loads(b"".join(chunks).decode())
        method: str = request.get("method", "")
        data: str = request.get("data", "")

        result = {
            "received": data,
            "has_error": False,
            "corrected": data,
            "decoded": data,
            "message": "OK",
        }

        if method == "crc":
            r = crc_verify(data)
            result["has_error"] = r["has_error"]
            result["remainder"] = r["remainder"]
            result["message"] = r["message"]
            if not r["has_error"] and len(data) > 4:
                result["decoded"] = data[:-4]  # remove CRC bits
            else:
                result["decoded"] = "Erro CRC — dado não confiável"

        elif method == "hamming":
            r = hamming_decode(data)
            result["has_error"] = r["has_error"]
            result["corrected"] = r["corrected"]
            result["decoded"] = r["data"]
            result["error_position"] = r["error_position"]
            result["message"] = (
                f"Erro corrigido na posição {r['error_position']}"
                if r["has_error"]
                else "Sem erros"
            )

        elif method.startswith("repetition"):
            try:
                r_factor = int(method.split("_")[1])
            except (IndexError, ValueError):
                r_factor = 3
            r = rep_decode(data, r_factor)
            result["has_error"] = r["has_errors"]
            result["decoded"] = r["decoded"]
            result["message"] = (
                f"Erros detectados nos grupos: {r['error_positions']}"
                if r["has_errors"]
                else "Sem erros"
            )

        response = json.dumps(result, ensure_ascii=False)
        conn.sendall(response.encode())

        if log_cb:
            log_cb(f"[Servidor] <- {addr[0]}:{addr[1]}  dados={data!r}")
            log_cb(f"[Servidor] -> resultado: {result['message']}")

    except Exception as exc:
        err = json.dumps({"error": str(exc)}, ensure_ascii=False)
        try:
            conn.sendall(err.encode())
        except Exception:
            pass
        if log_cb:
            log_cb(f"[Servidor] Erro ao processar cliente {addr}: {exc}")
    finally:
        conn.close()


def start_server(log_cb=None, stop_event: threading.Event = None) -> None:
    """Inicia o servidor TCP em loop. Passa stop_event para encerrar graciosamente."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen()
        srv.settimeout(1.0)

        if log_cb:
            log_cb(f"[Servidor] Ouvindo em {HOST}:{PORT} ...")

        while stop_event is None or not stop_event.is_set():
            try:
                conn, addr = srv.accept()
                t = threading.Thread(
                    target=_handle_client, args=(conn, addr, log_cb), daemon=True
                )
                t.start()
            except socket.timeout:
                continue
            except Exception as exc:
                if log_cb:
                    log_cb(f"[Servidor] Encerrado: {exc}")
                break

        if log_cb:
            log_cb("[Servidor] Servidor parado.")
