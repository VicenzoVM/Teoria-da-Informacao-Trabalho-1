"""Codificadores do trabalho de Teoria da Informação."""

from .encoders import (
    Elias_Gamma_encoder,
    Fibonnaci_Zeckendorf_encoder,
    Golomb_encoder,
    Huffman_encoder,
    bit_flip,
)

__all__ = [
    "Golomb_encoder",
    "Elias_Gamma_encoder",
    "Fibonnaci_Zeckendorf_encoder",
    "Huffman_encoder",
    "bit_flip",
]
