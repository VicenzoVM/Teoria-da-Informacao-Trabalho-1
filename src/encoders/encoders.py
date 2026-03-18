def Golomb_encoder(m: int, message: str) -> str:
    
    pass

def Elias_Gamma_encoder(message: str) -> str:
    pass         

def Fibonnaci_Zeckendorf_encoder(message: int) -> str:
    
    fibonacci = [1, 2]
    while fibonacci[-1] + fibonacci [-2] <= message:
        fibonacci.append(fibonacci[-1] + fibonacci[-2])

    encoder_return: list = []
    for v in fibonacci[::-1]:
        if v <= message:
            encoder_return.append ("1")
            message = message - v 
        else: 
            encoder_return.append("0")
    # stopbit 
    encoder_return.append("1")
    return "".join(encoder_return)  

def Huffman_encoder(message: str) -> str:
    pass

