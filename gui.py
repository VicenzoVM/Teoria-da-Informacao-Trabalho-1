"""Interface gráfica Tkinter — TP1 + TP2 de Teoria da Informação."""

import random
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

import encoding.golomb as golomb
import encoding.elias_gamma as elias_gamma
import encoding.fibonacci as fibonacci
import encoding.huffman as huffman
import error.crc as crc
import error.hamming as hamming
import error.repetition as repetition
import socket_comm.client as sock_client
from socket_comm.server import start_server
from utils import flip_bit, text_to_ascii


# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────

def _scrolled_text(parent, height=12, **kwargs) -> scrolledtext.ScrolledText:
    st = scrolledtext.ScrolledText(parent, height=height, wrap=tk.WORD,
                                   font=("Courier New", 10), **kwargs)
    return st


def _append(widget: scrolledtext.ScrolledText, text: str) -> None:
    widget.config(state=tk.NORMAL)
    widget.insert(tk.END, text + "\n")
    widget.see(tk.END)
    widget.config(state=tk.DISABLED)


def _clear(widget: scrolledtext.ScrolledText) -> None:
    widget.config(state=tk.NORMAL)
    widget.delete("1.0", tk.END)
    widget.config(state=tk.DISABLED)


def _section(parent, text: str) -> ttk.LabelFrame:
    return ttk.LabelFrame(parent, text=text, padding=6)


# ──────────────────────────────────────────────────────────────
# Tab 1 — TP1: Codificação / Decodificação
# ──────────────────────────────────────────────────────────────

class Tab1(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self._last_encoded = ""
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=1)

        # ── Entrada ──────────────────────────────────────────
        sec_in = _section(self, "Entrada")
        sec_in.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))
        sec_in.columnconfigure(1, weight=1)

        ttk.Label(sec_in, text="Texto / Número(s):").grid(row=0, column=0, sticky="w")
        self.entry_input = ttk.Entry(sec_in, font=("Courier New", 11))
        self.entry_input.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        ttk.Label(sec_in, text="(Para Huffman numérico use: '65 66 67' ou '65,66,67')").grid(
            row=1, column=1, sticky="w", pady=(2, 0))

        # ── Método ───────────────────────────────────────────
        sec_met = _section(self, "Método de Codificação")
        sec_met.grid(row=1, column=0, sticky="ew", padx=8, pady=4)

        self.method_var = tk.StringVar(value="golomb")
        methods = [
            ("Golomb", "golomb"),
            ("Elias-Gamma", "elias_gamma"),
            ("Fibonacci / Zeckendorf", "fibonacci"),
            ("Huffman", "huffman"),
        ]
        for i, (label, val) in enumerate(methods):
            rb = ttk.Radiobutton(sec_met, text=label, variable=self.method_var,
                                 value=val, command=self._on_method_change)
            rb.grid(row=0, column=i, padx=8, sticky="w")

        golomb_frame = ttk.Frame(sec_met)
        golomb_frame.grid(row=1, column=0, sticky="w", pady=(4, 0))
        ttk.Label(golomb_frame, text="Parâmetro M:").pack(side=tk.LEFT)
        self.entry_m = ttk.Entry(golomb_frame, width=6, font=("Courier New", 11))
        self.entry_m.insert(0, "4")
        self.entry_m.pack(side=tk.LEFT, padx=(4, 0))
        self._golomb_frame = golomb_frame

        # ── Ações principais ─────────────────────────────────
        sec_act = _section(self, "Ações")
        sec_act.grid(row=2, column=0, sticky="ew", padx=8, pady=4)

        ttk.Button(sec_act, text="Codificar", command=self._encode).pack(
            side=tk.LEFT, padx=4)
        ttk.Button(sec_act, text="Decodificar", command=self._decode).pack(
            side=tk.LEFT, padx=4)
        ttk.Button(sec_act, text="Limpar", command=lambda: _clear(self.result_area)).pack(
            side=tk.LEFT, padx=4)

        # ── Inserção de erro ──────────────────────────────────
        sec_err = _section(self, "Inserção de Erro (Bit Flip)")
        sec_err.grid(row=3, column=0, sticky="ew", padx=8, pady=4)

        ttk.Label(sec_err, text="Codeword atual:").grid(row=0, column=0, sticky="w")
        self.entry_codeword = ttk.Entry(sec_err, width=50, font=("Courier New", 11))
        self.entry_codeword.grid(row=0, column=1, padx=4, sticky="ew")
        sec_err.columnconfigure(1, weight=1)

        ttk.Label(sec_err, text="Posição do bit (0-based):").grid(row=1, column=0,
                                                                    sticky="w", pady=(4, 0))
        self.entry_err_pos = ttk.Entry(sec_err, width=8, font=("Courier New", 11))
        self.entry_err_pos.grid(row=1, column=1, sticky="w", padx=4, pady=(4, 0))

        ttk.Button(sec_err, text="Inserir Erro", command=self._insert_error).grid(
            row=1, column=2, padx=4, pady=(4, 0))
        ttk.Button(sec_err, text="Erro Aleatório", command=self._insert_random_error).grid(
            row=1, column=3, padx=4, pady=(4, 0))

        # ── Resultado ─────────────────────────────────────────
        sec_res = _section(self, "Resultado")
        sec_res.grid(row=4, column=0, sticky="nsew", padx=8, pady=(4, 8))
        self.rowconfigure(4, weight=1)
        sec_res.columnconfigure(0, weight=1)
        sec_res.rowconfigure(0, weight=1)

        self.result_area = _scrolled_text(sec_res, height=14, state=tk.DISABLED)
        self.result_area.grid(row=0, column=0, sticky="nsew")

    # ── Callbacks ────────────────────────────────────────────

    def _on_method_change(self):
        if self.method_var.get() == "golomb":
            self._golomb_frame.grid()
        else:
            self._golomb_frame.grid_remove()

    def _get_m(self) -> int:
        try:
            m = int(self.entry_m.get().strip())
            if m < 1:
                raise ValueError
            return m
        except ValueError:
            raise ValueError("Parâmetro M deve ser um inteiro positivo (≥ 1)")

    def _encode(self):
        raw = self.entry_input.get().strip()
        if not raw:
            messagebox.showwarning("Aviso", "Digite um valor no campo de entrada.")
            return
        method = self.method_var.get()
        lines = []
        try:
            if method == "golomb":
                m = self._get_m()
                lines.append(f"Método: Golomb  (M={m})")
                nums = self._parse_nums(raw)
                codes = []
                for n in nums:
                    c = golomb.encode(m, n)
                    lines.append(f"  {n:>6}  →  {c}")
                    codes.append(c)
                codeword = "".join(codes)

            elif method == "elias_gamma":
                lines.append("Método: Elias-Gamma")
                nums = self._parse_nums(raw)
                codes = []
                for n in nums:
                    c = elias_gamma.encode(n)
                    lines.append(f"  {n:>6}  →  {c}")
                    codes.append(c)
                codeword = "".join(codes)

            elif method == "fibonacci":
                lines.append("Método: Fibonacci / Zeckendorf")
                nums = self._parse_nums(raw)
                codes = []
                for n in nums:
                    c = fibonacci.encode(n)
                    lines.append(f"  {n:>6}  →  {c}")
                    codes.append(c)
                codeword = "".join(codes)

            elif method == "huffman":
                lines.append("Método: Huffman")
                result_json = huffman.encode(raw)
                import json as _json
                payload = _json.loads(result_json)
                lines.append(f"Modo: {'numérico' if payload['mode'] == 'numeric' else 'texto'}")
                lines.append("Tabela de códigos:")
                for sym, code in sorted(payload["codes"].items()):
                    lines.append(f"  '{sym}'  →  {code}")
                lines.append(f"Bits codificados: {payload['data']}")
                lines.append(f"JSON (cole no campo Huffman da aba Socket):")
                lines.append(result_json)
                codeword = result_json

            lines.insert(0, f"{'='*55}")
            lines.insert(1, "CODIFICAÇÃO")
            lines.insert(2, f"Entrada: {raw}")
            lines.append(f"{'='*55}")

            self._last_encoded = codeword
            self.entry_codeword.delete(0, tk.END)
            # Para Huffman exibe o JSON abreviado; para outros exibe os bits
            if method == "huffman":
                import json as _json
                self.entry_codeword.insert(0, payload["data"])
                self._last_encoded_bits = payload["data"]
            else:
                self.entry_codeword.insert(0, codeword)
                self._last_encoded_bits = codeword

            for line in lines:
                _append(self.result_area, line)

        except Exception as exc:
            messagebox.showerror("Erro de Codificação", str(exc))

    def _decode(self):
        raw = self.entry_codeword.get().strip() or self.entry_input.get().strip()
        if not raw:
            messagebox.showwarning("Aviso", "Cole o codeword no campo 'Codeword atual' ou na entrada.")
            return
        method = self.method_var.get()
        lines = [f"{'='*55}", "DECODIFICAÇÃO", f"Entrada: {raw[:80]}{'...' if len(raw)>80 else ''}",
                 f"{'='*55}"]
        try:
            if method == "golomb":
                m = self._get_m()
                lines.append(f"Método: Golomb  (M={m})")
                nums = self._stream_golomb_decode(raw.replace(" ", ""), m)
                for n in nums:
                    lines.append(f"  {n}  (ASCII: {chr(n) if 32 <= n < 127 else '—'})")

            elif method == "elias_gamma":
                lines.append("Método: Elias-Gamma")
                nums = self._stream_elias_decode(raw.replace(" ", ""))
                for n in nums:
                    lines.append(f"  {n}  (ASCII: {chr(n) if 32 <= n < 127 else '—'})")

            elif method == "fibonacci":
                lines.append("Método: Fibonacci / Zeckendorf")
                parts = raw.split() if " " in raw else self._split_fib_codewords(raw)
                for part in parts:
                    n = fibonacci.decode(part)
                    lines.append(f"  {part}  →  {n}  (ASCII: {chr(n) if 32 <= n < 127 else '—'})")

            elif method == "huffman":
                lines.append("Método: Huffman")
                last = getattr(self, "_last_encoded", "")
                if last and last.strip().startswith("{"):
                    src = last
                elif raw.strip().startswith("{"):
                    src = raw
                else:
                    raise ValueError(
                        "Para decodificar Huffman, codifique a mensagem primeiro "
                        "ou cole o JSON completo gerado na codificação no campo de entrada."
                    )
                decoded = huffman.decode(src)
                lines.append(f"Mensagem decodificada: {decoded}")

            for line in lines:
                _append(self.result_area, line)

        except Exception as exc:
            messagebox.showerror("Erro de Decodificação", str(exc))

    def _stream_elias_decode(self, bits: str) -> list:
        import math as _math
        nums, i = [], 0
        while i < len(bits):
            k = 0
            while i + k < len(bits) and bits[i + k] == "0":
                k += 1
            end = i + k + (k + 1)
            if end > len(bits):
                break
            nums.append(elias_gamma.decode(bits[i:end]))
            i = end
        return nums

    def _stream_golomb_decode(self, bits: str, m: int) -> list:
        import math as _math
        b = _math.ceil(_math.log2(m)) if m > 1 else 1
        cutoff = (1 << b) - m
        nums, i = [], 0
        while i < len(bits):
            q = 0
            while i < len(bits) and bits[i] == "1":
                q += 1
                i += 1
            if i >= len(bits):
                break
            i += 1  # consume '0'
            if m == 1:
                nums.append(q)
                continue
            if i + b - 1 > len(bits):
                break
            r_temp = int(bits[i:i + b - 1], 2)
            if r_temp < cutoff:
                nums.append(q * m + r_temp)
                i += b - 1
            else:
                if i + b > len(bits):
                    break
                nums.append(q * m + int(bits[i:i + b], 2) - cutoff)
                i += b
        return nums

    def _split_fib_codewords(self, bits: str) -> list:
        """Divide bits contínuos de Fibonacci usando o stop-bit '1' após sequência sem '11'."""
        parts, i = [], 0
        while i < len(bits):
            j, prev1 = i, False
            while j < len(bits):
                cur = bits[j] == "1"
                if cur and prev1:
                    parts.append(bits[i:j + 1])
                    i = j + 1
                    break
                prev1 = cur
                j += 1
            else:
                if j > i:
                    parts.append(bits[i:j])
                break
        return parts

    def _insert_error(self):
        codeword = self.entry_codeword.get().strip()
        if not codeword:
            messagebox.showwarning("Aviso", "Nenhum codeword no campo para inserir erro.")
            return
        pos_str = self.entry_err_pos.get().strip()
        if not pos_str.isdigit():
            messagebox.showerror("Erro", "Posição deve ser um inteiro não-negativo.")
            return
        pos = int(pos_str)
        # Remove espaços para operar nos bits
        bits_only = codeword.replace(" ", "")
        try:
            modified = flip_bit(bits_only, pos)
        except ValueError as exc:
            messagebox.showerror("Erro", str(exc))
            return
        # Reinsere espaços na mesma posição relativa
        self.entry_codeword.delete(0, tk.END)
        self.entry_codeword.insert(0, modified)
        _append(self.result_area, f"{'='*55}")
        _append(self.result_area, f"ERRO INSERIDO na posição {pos}")
        _append(self.result_area, f"  Antes : {bits_only}")
        _append(self.result_area, f"  Depois: {modified}")
        _append(self.result_area, f"{'='*55}")

    def _insert_random_error(self):
        codeword = self.entry_codeword.get().strip()
        if not codeword:
            messagebox.showwarning("Aviso", "Nenhum codeword no campo para inserir erro.")
            return
        bits_only = codeword.replace(" ", "")
        pos = random.randint(0, len(bits_only) - 1)
        self.entry_err_pos.delete(0, tk.END)
        self.entry_err_pos.insert(0, str(pos))
        self._insert_error()

    def _parse_nums(self, raw: str) -> list:
        """
        Converte entrada em lista de inteiros:
        - Se for texto puro (não-numérico) → converte cada char para ASCII.
        - Se for número(s) separados por espaço ou vírgula → usa como inteiros.
        """
        normalized = raw.replace(",", " ")
        parts = normalized.split()
        if all(p.isdigit() for p in parts):
            return [int(p) for p in parts]
        # Texto → ASCII
        nums = text_to_ascii(raw)
        _append(self.result_area, f"Conversão ASCII: {list(zip(raw, nums))}")
        return nums


# ──────────────────────────────────────────────────────────────
# Tab 2 — TP2: Detecção e Correção de Erro
# ──────────────────────────────────────────────────────────────

class Tab2(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=1)

        # ── Método ───────────────────────────────────────────
        sec_met = _section(self, "Método de Detecção / Correção de Erro")
        sec_met.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))

        self.method_var = tk.StringVar(value="crc")
        rb_crc = ttk.Radiobutton(sec_met, text="CRC-4  [G(x)=x⁴+x+1]",
                                 variable=self.method_var, value="crc",
                                 command=self._on_method_change)
        rb_crc.grid(row=0, column=0, padx=8, sticky="w")

        rb_hamming = ttk.Radiobutton(sec_met, text="Hamming (7,4)",
                                     variable=self.method_var, value="hamming",
                                     command=self._on_method_change)
        rb_hamming.grid(row=0, column=1, padx=8, sticky="w")

        rep_frame = ttk.Frame(sec_met)
        rep_frame.grid(row=0, column=2, padx=8, sticky="w")
        rb_rep = ttk.Radiobutton(rep_frame, text="Repetição Ri  R=",
                                 variable=self.method_var, value="repetition",
                                 command=self._on_method_change)
        rb_rep.pack(side=tk.LEFT)
        self.entry_r = ttk.Entry(rep_frame, width=4, font=("Courier New", 11))
        self.entry_r.insert(0, "3")
        self.entry_r.pack(side=tk.LEFT)
        ttk.Label(rep_frame, text="(ímpar)").pack(side=tk.LEFT, padx=(2, 0))

        # ── Entrada ──────────────────────────────────────────
        sec_in = _section(self, "Entrada (bits binários)")
        sec_in.grid(row=1, column=0, sticky="ew", padx=8, pady=4)
        sec_in.columnconfigure(1, weight=1)

        self._hint_labels = {
            "crc":        "Qualquer sequência de bits  (ex: 1101)",
            "hamming":    "Exatamente 4 bits para codificar  |  7 bits para decodificar",
            "repetition": "Qualquer sequência de bits  (ex: 1011)",
        }
        self.lbl_hint = ttk.Label(sec_in, text=self._hint_labels["crc"],
                                  foreground="#555")
        self.lbl_hint.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 4))

        ttk.Label(sec_in, text="Bits:").grid(row=1, column=0, sticky="w")
        self.entry_bits = ttk.Entry(sec_in, font=("Courier New", 12))
        self.entry_bits.grid(row=1, column=1, sticky="ew", padx=(6, 0))

        # ── Ações ─────────────────────────────────────────────
        sec_act = _section(self, "Ações")
        sec_act.grid(row=2, column=0, sticky="ew", padx=8, pady=4)

        ttk.Button(sec_act, text="Codificar", command=self._encode).pack(
            side=tk.LEFT, padx=4)
        ttk.Button(sec_act, text="Verificar / Decodificar", command=self._verify_decode).pack(
            side=tk.LEFT, padx=4)
        ttk.Button(sec_act, text="Limpar", command=lambda: _clear(self.result_area)).pack(
            side=tk.LEFT, padx=4)

        # ── Inserção de erro manual ───────────────────────────
        sec_err = _section(self, "Inserção de Erro Manual")
        sec_err.grid(row=3, column=0, sticky="ew", padx=8, pady=4)
        sec_err.columnconfigure(1, weight=1)

        ttk.Label(sec_err, text="Codeword:").grid(row=0, column=0, sticky="w")
        self.entry_codeword = ttk.Entry(sec_err, font=("Courier New", 12))
        self.entry_codeword.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        ttk.Label(sec_err, text="Posição (0-based):").grid(row=1, column=0,
                                                            sticky="w", pady=(4, 0))
        self.entry_err_pos = ttk.Entry(sec_err, width=8, font=("Courier New", 11))
        self.entry_err_pos.grid(row=1, column=1, sticky="w", padx=(6, 0), pady=(4, 0))
        ttk.Button(sec_err, text="Inserir Erro", command=self._insert_error).grid(
            row=1, column=2, padx=4, pady=(4, 0))
        ttk.Button(sec_err, text="Erro Aleatório", command=self._insert_random_error).grid(
            row=1, column=3, padx=4, pady=(4, 0))

        # ── Resultado ─────────────────────────────────────────
        sec_res = _section(self, "Resultado")
        sec_res.grid(row=4, column=0, sticky="nsew", padx=8, pady=(4, 8))
        self.rowconfigure(4, weight=1)
        sec_res.columnconfigure(0, weight=1)
        sec_res.rowconfigure(0, weight=1)

        self.result_area = _scrolled_text(sec_res, height=12, state=tk.DISABLED)
        self.result_area.grid(row=0, column=0, sticky="nsew")

    def _on_method_change(self):
        m = self.method_var.get()
        self.lbl_hint.config(text=self._hint_labels.get(m, ""))

    # ── Encode ───────────────────────────────────────────────

    def _encode(self):
        bits = self.entry_bits.get().strip()
        if not bits:
            messagebox.showwarning("Aviso", "Digite bits no campo de entrada.")
            return
        method = self.method_var.get()
        lines = [f"{'='*55}", "CODIFICAÇÃO (TP2)", f"Entrada: {bits}", f"{'='*55}"]
        try:
            if method == "crc":
                if not all(c in "01" for c in bits):
                    raise ValueError("CRC aceita apenas bits '0' e '1'")
                crc_bits = crc.get_crc(bits)
                codeword = crc.encode(bits)
                lines.append(f"Método: CRC-4  (G(x) = 10011)")
                lines.append(f"Dados originais : {bits}")
                lines.append(f"Bits de CRC     : {crc_bits}  (4 bits)")
                lines.append(f"Codeword final  : {codeword}  ({len(codeword)} bits)")

            elif method == "hamming":
                if len(bits) != 4:
                    raise ValueError("Hamming (7,4) exige exatamente 4 bits de dados")
                if not all(c in "01" for c in bits):
                    raise ValueError("Hamming aceita apenas bits '0' e '1'")
                codeword = hamming.encode(bits)
                lines.append(f"Método: Hamming (7,4)")
                lines.append(f"Dados (4 bits)   : {bits}")
                lines.append(f"Codeword (7 bits): {codeword}")
                lines.append(f"  pos:  1  2  3  4  5  6  7")
                lines.append(f"  bit:  {' '.join(codeword)}")
                lines.append(f"  tipo: p1 p2 d1 p4 d2 d3 d4")

            elif method == "repetition":
                r = self._get_r()
                if not all(c in "01" for c in bits):
                    raise ValueError("Repetição aceita apenas bits '0' e '1'")
                codeword = repetition.encode(bits, r)
                lines.append(f"Método: Repetição (R={r})")
                lines.append(f"Bits originais  : {bits}")
                lines.append(f"Bits codificados: {codeword}  ({len(codeword)} bits)")

            self.entry_codeword.delete(0, tk.END)
            self.entry_codeword.insert(0, codeword)
            lines.append(f"{'='*55}")
            for line in lines:
                _append(self.result_area, line)

        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # ── Verify / Decode ──────────────────────────────────────

    def _verify_decode(self):
        bits = self.entry_codeword.get().strip() or self.entry_bits.get().strip()
        if not bits:
            messagebox.showwarning("Aviso",
                "Preencha o campo 'Codeword' (ou codifique primeiro).")
            return
        method = self.method_var.get()
        lines = [f"{'='*55}", "VERIFICAÇÃO / DECODIFICAÇÃO", f"Recebido: {bits}",
                 f"{'='*55}"]
        try:
            if method == "crc":
                if not all(c in "01" for c in bits):
                    raise ValueError("CRC aceita apenas bits '0' e '1'")
                r = crc.verify(bits)
                lines.append(f"Método: CRC-4  (G(x) = 10011)")
                lines.append(f"Resto da divisão: {r['remainder']}")
                lines.append(f"{'⚠ ' if r['has_error'] else '✓ '}{r['message']}")
                if not r["has_error"] and len(bits) > 4:
                    lines.append(f"Dados recuperados: {bits[:-4]}")

            elif method == "hamming":
                if len(bits) != 7:
                    raise ValueError("Hamming (7,4) exige exatamente 7 bits recebidos")
                if not all(c in "01" for c in bits):
                    raise ValueError("Hamming aceita apenas bits '0' e '1'")
                r = hamming.decode(bits)
                lines.append(f"Método: Hamming (7,4)")
                lines.append(f"Recebido  : {bits}")
                if r["has_error"]:
                    lines.append(f"⚠ Erro detectado na posição {r['error_position']} (1-based)")
                    lines.append(f"Corrigido : {r['corrected']}")
                else:
                    lines.append("✓ Sem erros detectados")
                lines.append(f"Dados (4 bits): {r['data']}")

            elif method == "repetition":
                r_val = self._get_r()
                if not all(c in "01" for c in bits):
                    raise ValueError("Repetição aceita apenas bits '0' e '1'")
                r = repetition.decode(bits, r_val)
                lines.append(f"Método: Repetição (R={r_val})")
                lines.append(f"Recebido        : {bits}")
                if r["has_errors"]:
                    lines.append(f"⚠ Erros nos grupos (0-based): {r['error_positions']}")
                else:
                    lines.append("✓ Sem erros detectados")
                lines.append(f"Dados decodificados: {r['decoded']}")

            lines.append(f"{'='*55}")
            for line in lines:
                _append(self.result_area, line)

        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # ── Insert error ─────────────────────────────────────────

    def _insert_error(self):
        bits = self.entry_codeword.get().strip()
        if not bits:
            messagebox.showwarning("Aviso", "Preencha o campo 'Codeword' primeiro.")
            return
        pos_str = self.entry_err_pos.get().strip()
        if not pos_str.isdigit():
            messagebox.showerror("Erro", "Posição deve ser um inteiro não-negativo.")
            return
        pos = int(pos_str)
        try:
            modified = flip_bit(bits, pos)
        except ValueError as exc:
            messagebox.showerror("Erro", str(exc))
            return
        self.entry_codeword.delete(0, tk.END)
        self.entry_codeword.insert(0, modified)
        _append(self.result_area, f"{'='*55}")
        _append(self.result_area, f"ERRO MANUAL INSERIDO na posição {pos}")
        _append(self.result_area, f"  Antes : {bits}")
        _append(self.result_area, f"  Depois: {modified}")
        _append(self.result_area, f"{'='*55}")

    def _insert_random_error(self):
        bits = self.entry_codeword.get().strip()
        if not bits:
            messagebox.showwarning("Aviso", "Preencha o campo 'Codeword' primeiro.")
            return
        pos = random.randint(0, len(bits) - 1)
        self.entry_err_pos.delete(0, tk.END)
        self.entry_err_pos.insert(0, str(pos))
        self._insert_error()

    def _get_r(self) -> int:
        try:
            r = int(self.entry_r.get().strip())
            if r < 1:
                raise ValueError
            if r % 2 == 0:
                raise ValueError("R deve ser ímpar")
            return r
        except ValueError as exc:
            raise ValueError("Parâmetro R deve ser um inteiro ímpar positivo (≥ 1)") from exc


# ──────────────────────────────────────────────────────────────
# Tab 3 — TP2: Comunicação Socket
# ──────────────────────────────────────────────────────────────

class Tab3(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self._server_thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._server_running = False
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=1)

        # ── Controle do servidor ──────────────────────────────
        sec_srv = _section(self, "Servidor TCP  (localhost:65432)")
        sec_srv.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))

        self.btn_server = ttk.Button(sec_srv, text="Iniciar Servidor",
                                     command=self._toggle_server)
        self.btn_server.pack(side=tk.LEFT, padx=4)

        self.lbl_status = ttk.Label(sec_srv, text="● Parado", foreground="red")
        self.lbl_status.pack(side=tk.LEFT, padx=8)

        # ── Cliente ───────────────────────────────────────────
        sec_cli = _section(self, "Cliente — Enviar Mensagem")
        sec_cli.grid(row=1, column=0, sticky="ew", padx=8, pady=4)
        sec_cli.columnconfigure(1, weight=1)

        ttk.Label(sec_cli, text="Mensagem (bits):").grid(row=0, column=0, sticky="w")
        self.entry_msg = ttk.Entry(sec_cli, font=("Courier New", 12))
        self.entry_msg.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        ttk.Label(sec_cli, text="Método de erro:").grid(
            row=1, column=0, sticky="w", pady=(6, 0))

        method_frame = ttk.Frame(sec_cli)
        method_frame.grid(row=1, column=1, sticky="w", pady=(6, 0), padx=(6, 0))
        self.method_var = tk.StringVar(value="hamming")

        rb_h = ttk.Radiobutton(method_frame, text="Hamming (7,4)",
                               variable=self.method_var, value="hamming",
                               command=self._on_method_change)
        rb_h.pack(side=tk.LEFT, padx=(0, 8))

        rb_c = ttk.Radiobutton(method_frame, text="CRC-4",
                               variable=self.method_var, value="crc",
                               command=self._on_method_change)
        rb_c.pack(side=tk.LEFT, padx=(0, 8))

        rep_frame = ttk.Frame(method_frame)
        rep_frame.pack(side=tk.LEFT)
        rb_r = ttk.Radiobutton(rep_frame, text="Repetição R=",
                               variable=self.method_var, value="repetition",
                               command=self._on_method_change)
        rb_r.pack(side=tk.LEFT)
        self.entry_r = ttk.Entry(rep_frame, width=4, font=("Courier New", 11))
        self.entry_r.insert(0, "3")
        self.entry_r.pack(side=tk.LEFT)

        ttk.Label(sec_cli, text="Inserir erro antes de enviar:").grid(
            row=2, column=0, sticky="w", pady=(6, 0))
        err_frame = ttk.Frame(sec_cli)
        err_frame.grid(row=2, column=1, sticky="w", pady=(6, 0), padx=(6, 0))
        self.var_insert_err = tk.BooleanVar(value=False)
        ttk.Checkbutton(err_frame, text="Sim, posição:", variable=self.var_insert_err).pack(
            side=tk.LEFT)
        self.entry_err_pos = ttk.Entry(err_frame, width=6, font=("Courier New", 11))
        self.entry_err_pos.insert(0, "0")
        self.entry_err_pos.pack(side=tk.LEFT, padx=(4, 0))
        self.var_random_err = tk.BooleanVar(value=False)
        ttk.Checkbutton(err_frame, text="Aleatória", variable=self.var_random_err).pack(
            side=tk.LEFT, padx=(8, 0))

        self.btn_send = ttk.Button(sec_cli, text="Enviar (Cliente)",
                                   command=self._send_message)
        self.btn_send.grid(row=3, column=0, columnspan=2, pady=(8, 0), sticky="w", padx=0)

        # ── Codificação original ──────────────────────────────
        sec_enc = _section(self, "Codificação original dos dados (para decodificar após verificação)")
        sec_enc.grid(row=2, column=0, sticky="ew", padx=8, pady=4)

        self.enc_var = tk.StringVar(value="none")
        enc_opts = [
            ("Nenhuma", "none"),
            ("Elias-Gamma", "elias_gamma"),
            ("Fibonacci/Zeckendorf", "fibonacci"),
            ("Golomb", "golomb"),
            ("Huffman", "huffman"),
        ]
        for i, (lbl, val) in enumerate(enc_opts):
            ttk.Radiobutton(sec_enc, text=lbl, variable=self.enc_var,
                            value=val, command=self._on_enc_change).grid(
                row=0, column=i, padx=8, sticky="w")

        self._golomb_enc_frame = ttk.Frame(sec_enc)
        self._golomb_enc_frame.grid(row=1, column=3, sticky="w", pady=(4, 0))
        ttk.Label(self._golomb_enc_frame, text="M:").pack(side=tk.LEFT)
        self.entry_golomb_m = ttk.Entry(self._golomb_enc_frame, width=5, font=("Courier New", 11))
        self.entry_golomb_m.insert(0, "4")
        self.entry_golomb_m.pack(side=tk.LEFT, padx=(4, 0))
        self._golomb_enc_frame.grid_remove()

        self._huffman_enc_frame = ttk.Frame(sec_enc)
        self._huffman_enc_frame.grid(row=1, column=0, columnspan=5, sticky="ew", pady=(4, 0))
        ttk.Label(self._huffman_enc_frame, text="JSON do Huffman (cole da Tab TP1):").pack(side=tk.LEFT)
        self.entry_huffman_json = ttk.Entry(self._huffman_enc_frame, font=("Courier New", 10))
        self.entry_huffman_json.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))
        self._huffman_enc_frame.grid_remove()

        # ── Log ───────────────────────────────────────────────
        sec_log = _section(self, "Log de Comunicação")
        sec_log.grid(row=3, column=0, sticky="nsew", padx=8, pady=(4, 8))
        self.rowconfigure(3, weight=1)
        sec_log.columnconfigure(0, weight=1)
        sec_log.rowconfigure(0, weight=1)

        self.log_area = _scrolled_text(sec_log, height=14, state=tk.DISABLED)
        self.log_area.grid(row=0, column=0, sticky="nsew")

        ttk.Button(sec_log, text="Limpar Log",
                   command=lambda: _clear(self.log_area)).grid(
            row=1, column=0, sticky="w", pady=(4, 0))

    def _on_method_change(self):
        pass

    def _on_enc_change(self):
        enc = self.enc_var.get()
        if enc == "golomb":
            self._golomb_enc_frame.grid()
        else:
            self._golomb_enc_frame.grid_remove()
        if enc == "huffman":
            self._huffman_enc_frame.grid()
        else:
            self._huffman_enc_frame.grid_remove()

    def _decode_original(self, bits: str, algorithm: str) -> str:
        if algorithm == "huffman":
            json_src = self.entry_huffman_json.get().strip()
            if not json_src:
                raise ValueError("Cole o JSON gerado na aba TP1 no campo Huffman.")
            import json as _json
            payload = _json.loads(json_src)
            payload["data"] = bits
            return huffman.decode(_json.dumps(payload))
        if algorithm == "elias_gamma":
            nums = self._stream_elias(bits)
        elif algorithm == "fibonacci":
            nums = self._stream_fib(bits)
        elif algorithm == "golomb":
            m = int(self.entry_golomb_m.get().strip())
            nums = self._stream_golomb(bits, m)
        else:
            return bits
        chars = "".join(chr(n) if 32 <= n <= 126 else f"[{n}]" for n in nums)
        return f"{chars}  {nums}"

    def _stream_elias(self, bits: str) -> list:
        nums, i = [], 0
        while i < len(bits):
            k = 0
            while i + k < len(bits) and bits[i + k] == "0":
                k += 1
            end = i + k + (k + 1)
            if end > len(bits):
                break
            nums.append(elias_gamma.decode(bits[i:end]))
            i = end
        return nums

    def _stream_fib(self, bits: str) -> list:
        nums, i = [], 0
        while i < len(bits):
            end = bits.find("11", i)
            if end == -1:
                break
            end += 2
            nums.append(fibonacci.decode(bits[i:end]))
            i = end
        return nums

    def _stream_golomb(self, bits: str, m: int) -> list:
        import math as _math
        b = _math.ceil(_math.log2(m)) if m > 1 else 1
        cutoff = (1 << b) - m
        nums, i = [], 0
        while i < len(bits):
            q = 0
            while i < len(bits) and bits[i] == "1":
                q += 1
                i += 1
            if i >= len(bits):
                break
            i += 1
            if m == 1:
                nums.append(q)
                continue
            if i + b - 1 > len(bits):
                break
            r_temp = int(bits[i:i + b - 1], 2)
            if r_temp < cutoff:
                nums.append(q * m + r_temp)
                i += b - 1
            else:
                if i + b > len(bits):
                    break
                nums.append(q * m + int(bits[i:i + b], 2) - cutoff)
                i += b
        return nums

    def _log(self, msg: str) -> None:
        self.after(0, lambda: _append(self.log_area, msg))

    # ── Server ───────────────────────────────────────────────

    def _toggle_server(self):
        if self._server_running:
            self._stop_event.set()
            self._server_running = False
            self.btn_server.config(text="Iniciar Servidor")
            self.lbl_status.config(text="● Parado", foreground="red")
            self._log("[Sistema] Servidor encerrado.")
        else:
            self._stop_event.clear()
            self._server_thread = threading.Thread(
                target=start_server,
                kwargs={"log_cb": self._log, "stop_event": self._stop_event},
                daemon=True,
            )
            self._server_thread.start()
            self._server_running = True
            self.btn_server.config(text="Parar Servidor")
            self.lbl_status.config(text="● Rodando", foreground="green")
            self._log("[Sistema] Servidor iniciado em localhost:65432")

    # ── Client ───────────────────────────────────────────────

    def _send_message(self):
        bits = self.entry_msg.get().strip()
        if not bits:
            messagebox.showwarning("Aviso", "Digite os bits a enviar.")
            return
        if not all(c in "01" for c in bits):
            messagebox.showerror("Erro", "A mensagem deve conter apenas bits '0' e '1'.")
            return

        method = self.method_var.get()

        try:
            # Codifica com o método selecionado
            if method == "hamming":
                if len(bits) != 4:
                    raise ValueError("Hamming (7,4) exige exatamente 4 bits de dados")
                codeword = hamming.encode(bits)
                server_method = "hamming"

            elif method == "crc":
                codeword = crc.encode(bits)
                server_method = "crc"

            elif method == "repetition":
                try:
                    r = int(self.entry_r.get().strip())
                    if r < 1 or r % 2 == 0:
                        raise ValueError
                except ValueError:
                    raise ValueError("R deve ser um inteiro ímpar positivo")
                codeword = repetition.encode(bits, r)
                server_method = f"repetition_{r}"

            self._log(f"[Cliente] Dados originais : {bits}")
            self._log(f"[Cliente] Método          : {method}")
            self._log(f"[Cliente] Codeword enviado: {codeword}")

            # Insere erro se solicitado
            if self.var_insert_err.get():
                if self.var_random_err.get():
                    pos = random.randint(0, len(codeword) - 1)
                    self.entry_err_pos.delete(0, tk.END)
                    self.entry_err_pos.insert(0, str(pos))
                else:
                    pos_str = self.entry_err_pos.get().strip()
                    if not pos_str.isdigit():
                        raise ValueError("Posição de erro deve ser um inteiro não-negativo")
                    pos = int(pos_str)
                codeword = flip_bit(codeword, pos)
                self._log(f"[Cliente] ⚠ Erro inserido na posição {pos}: {codeword}")

            threading.Thread(
                target=self._do_send, args=(server_method, codeword), daemon=True
            ).start()

        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    def _do_send(self, method: str, codeword: str) -> None:
        try:
            response = sock_client.send(method, codeword)
            self._log(f"[Servidor] Recebido   : {response.get('received', '?')}")
            self._log(f"[Servidor] Erro?       : {'Sim' if response.get('has_error') else 'Não'}")
            if response.get("corrected") != response.get("received"):
                self._log(f"[Servidor] Corrigido  : {response.get('corrected', '?')}")
            clean_bits = response.get("decoded", "")
            self._log(f"[Servidor] Bits limpos : {clean_bits}")
            self._log(f"[Servidor] Mensagem    : {response.get('message', '')}")

            enc = self.enc_var.get()
            if enc != "none" and clean_bits and all(c in "01" for c in str(clean_bits)):
                try:
                    original = self._decode_original(clean_bits, enc)
                    self._log(f"[Original ] Decodificado ({enc}): {original}")
                except Exception as exc:
                    self._log(f"[Original ] Não foi possível decodificar: {exc}")

            self._log("-" * 55)
        except ConnectionRefusedError:
            self._log("[Erro] Servidor não está rodando! Clique em 'Iniciar Servidor' primeiro.")
        except Exception as exc:
            self._log(f"[Erro] {exc}")


# ──────────────────────────────────────────────────────────────
# Aplicação principal
# ──────────────────────────────────────────────────────────────

class App:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Teoria da Informação — TP1 + TP2")
        self.root.geometry("920x760")
        self.root.resizable(True, True)
        self._build()

    def _build(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=6, pady=6)

        tab1 = Tab1(notebook)
        tab2 = Tab2(notebook)
        tab3 = Tab3(notebook)

        notebook.add(tab1, text="  TP1 — Codificação / Decodificação  ")
        notebook.add(tab2, text="  TP2 — Detecção e Correção de Erro  ")
        notebook.add(tab3, text="  TP2 — Comunicação Socket  ")

    def run(self):
        self.root.mainloop()
