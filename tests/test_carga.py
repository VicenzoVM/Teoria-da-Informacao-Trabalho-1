import random
import string

from decoders.decoders import (
    Elias_Gamma_decoder,
    Fibonnaci_Zeckendorf_decoder,
    Golomb_decoder,
    Huffman_decoder,
)
from encoders.encoders import (
    Elias_Gamma_encoder,
    Fibonnaci_Zeckendorf_encoder,
    Golomb_encoder,
    Huffman_encoder,
    bit_flip
)

# ==========================================
# TESTES DE LARGA ESCALA (STRESS TESTING)
# ==========================================

def test_huffman_carga_pesada():
    """Testa a compressão de um texto gigantesco com 100.000 caracteres aleatórios."""
    # Gera uma string aleatória de 100 mil letras e espaços
    texto_gigante = ''.join(random.choices(string.ascii_letters + " ", k=100000))
    
    resultado_json = Huffman_encoder(texto_gigante)
    
    # Valida se a descompressão de 100 mil caracteres ocorre sem perda de dados
    assert Huffman_decoder(resultado_json) == texto_gigante

def test_golomb_carga_pesada():
    """Testa o Golomb com um número na casa dos 10 milhões."""
    numero_gigante = 10000000
    m = 1024 # Um divisor alto
    
    bits = Golomb_encoder(m, str(numero_gigante))
    assert Golomb_decoder(m, bits) == str(numero_gigante)

def test_elias_gamma_carga_pesada():
    """Testa o Elias-Gamma com um número na casa dos 10 milhões."""
    numero_gigante = "10000000"
    
    bits = Elias_Gamma_encoder(numero_gigante)
    assert Elias_Gamma_decoder(bits) == numero_gigante

def test_fibonacci_carga_pesada():
    """Testa a decomposição de Zeckendorf para um número na casa de 1 milhão."""
    numero_gigante = 1000000
    
    bits = Fibonnaci_Zeckendorf_encoder(numero_gigante)
    assert Fibonnaci_Zeckendorf_decoder(bits) == numero_gigante

def test_bit_flip_carga_pesada():
    """Testa o gerador de ruído processando uma string de 1 milhão de bits."""
    # Cria uma string com 1 milhão de bits alternados (101010...)
    bits_gigantes = "10" * 500000 
    
    # Aplica 50% de chance de erro
    resultado = bit_flip(bits_gigantes, 0.5)
    
    # Garante que o tamanho da string não foi corrompido
    assert len(resultado) == 1000000
    # Estatisticamente impossível a string voltar idêntica com 50% de mutação
    assert resultado != bits_gigantes
