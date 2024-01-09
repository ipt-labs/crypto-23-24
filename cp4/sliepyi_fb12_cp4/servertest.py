from main import * 

def dec_to_hex(decimal_number):
    hex_representation = hex(decimal_number)[2:] 
    return hex_representation.upper()  

def hex_to_dec(hexadecimal_number):
    decimal_representation = int(hexadecimal_number, 16)
    return decimal_representation

def main():
    p = generate_random_prime(256)
    q = generate_random_prime(256)
    """ Даю на сервер свій модуль і публічну експ, вводжу повідомлення отримую шифротекст і розшифровую його у себе приватним ключем """
    A_keypair = GenerateKeyPair(p,q)
    A_public = A_keypair[0]
    A_private = A_keypair[1]
    print(A_public)
    print(hex(A_public[0])[2:])
    print(hex(A_public[1])[2:])
    text=int(hex_to_dec(input()))
    pt=Bytes2Text(Decode(text,A_private))
    print(pt)
   
main()


