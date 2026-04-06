import pytest
import json
from encoders.encoders import Golomb_encoder, Elias_Gamma_encoder, Huffman_encoder, bit_flip
from decoders.decoders import Golomb_decoder, Elias_Gamma_decoder, Huffman_decoder

# ==========================================
# TESTES GOLOMB
# ==========================================
def test_golomb_encode_decode():
    """Testa se o valor decodificado é igual ao valor original."""
    assert Golomb_decoder(4, Golomb_encoder(4, "13")) == "13"
    assert Golomb_decoder(10, Golomb_encoder(10, "42")) == "42"
    
def test_golomb_aceita_zero():
    """Valida que o Golomb aceita o zero."""
    assert Golomb_decoder(5, Golomb_encoder(5, "0")) == "0"

def test_golomb_m_invalido():
    """Testa a validação de que M deve ser positivo."""
    with pytest.raises(ValueError, match="m deve ser um inteiro positivo"):
        Golomb_encoder(0, "10")

# ==========================================
# TESTES ELIAS-GAMMA
# ==========================================
def test_elias_gamma_encode_decode():
    """Testa se o valor decodificado é igual ao original."""
    assert Elias_Gamma_decoder(Elias_Gamma_encoder("10")) == "10"
    assert Elias_Gamma_decoder(Elias_Gamma_encoder("1")) == "1"

def test_elias_gamma_rejeita_zero():
    """Valida a REGRA DO PDF: entrada deve ser inteiro positivo não-nulo."""
    with pytest.raises(ValueError):
        Elias_Gamma_encoder("0")

def test_elias_gamma_decode_invalido():
    """Testa a validação de entrada corrompida no decoder."""
    with pytest.raises(ValueError):
        Elias_Gamma_decoder("00010") # Incompleto

# ==========================================
# TESTES HUFFMAN
# ==========================================
def test_huffman_encode_decode():
    """Testa a codificação e decodificação de uma string padrão."""
    mensagem = "hello world"
    resultado_json = Huffman_encoder(mensagem)
    
    # Verifica se gerou um JSON válido
    dados = json.loads(resultado_json)
    assert "codes" in dados
    assert "data" in dados
    
    # Verifica se a decodificação retorna o texto original
    assert Huffman_decoder(resultado_json) == mensagem

def test_huffman_caractere_unico():
    """Testa o caso de borda de uma string com apenas um tipo de caractere."""
    mensagem = "aaaaa"
    assert Huffman_decoder(Huffman_encoder(mensagem)) == mensagem

# ==========================================
# TESTES BIT-FLIP (INSERÇÃO DE ERRO)
# ==========================================
def test_bit_flip_probabilidade_zero():
    """Com probabilidade 0.0, a string deve sair exatamente igual."""
    assert bit_flip("101010", 0.0) == "101010"

def test_bit_flip_probabilidade_um():
    """Com probabilidade 1.0, todos os bits devem ser invertidos."""
    assert bit_flip("101010", 1.0) == "010101"