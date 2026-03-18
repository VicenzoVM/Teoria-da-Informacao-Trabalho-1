def Golomb_decoder(m: int, message: str) -> str:
    
    pass

def Elias_Gamma_decoder(message: str) -> str:
    pass         

def Fibonnaci_Zeckendorf_decoder(message: str) -> int:
    
    fibonacci = [1, 2]

    while len(fibonacci) < len(message)-1:
        fibonacci.append(fibonacci[-1] + fibonacci[-2])
    
    fibonacci = fibonacci[::-1]
    return_fibonacci = 0 

    for i in range(len(fibonacci)):
        if message[i] == "1":
            return_fibonacci += fibonacci[i]
    return return_fibonacci
            

        




        
        
        

def Huffman_decoder(message: str) -> str:
    pass