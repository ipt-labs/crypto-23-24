#main
import random

""" Generate prime number Block"""
def miller_rabin(n, k=100):
    if n <= 1 or any(n % i == 0 for i in [2, 3, 5, 7]):
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = Exponentiation(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = Exponentiation(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_random_prime(bits):
    while True:
        candidate = random.getrandbits(bits)
        candidate |= (1 << bits - 1) | 1   
        if  miller_rabin(candidate):
            return candidate
        
""""""
def GCD(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = GCD(b % a, a)
        return g, y - (b // a) * x, x

def Inverse(a, m):
    g, x, y = GCD(a, m)
    if g != 1:
        return None 
    else:
        return (x % m + m) % m
    
def Exponentiation(base, exponent, module):
    return pow(base, exponent, module)

""" Generate Private & Public Keys"""
def GenerateKeyPair(p, q):
    n = p*q
    phi = (p-1) *(q-1)
    e = 65537 
    while GCD(e, phi)[0] != 1:
        e = random.randrange(2, phi-1)
    d = Inverse(e, phi)
    public_key =  [n,e]
    private_key =  [p,q,d]
    return public_key, private_key

""" Encode-Decode Block """
def Encode(message, public_key):
    n, e = public_key[0], public_key[1]
    cipher_text = Exponentiation(message, e, n)
    return cipher_text

def Decode(ct, private_key):
    p, q, d = private_key[0], private_key[1], private_key[2]
    plain_text = Exponentiation(ct, d, p * q)
    return plain_text

def SigEncode(message, private_key):
    p, q, d = private_key[0], private_key[1], private_key[2]
    sig_text = Exponentiation(message,d, p*q)
    return sig_text

def SigDecode(sig_text,public_key):
    n, e = public_key[0], public_key[1]
    verified_text = Exponentiation(sig_text, e, n) 
    return verified_text

""" Sign - Verify Block """
def Sign(message, private_key):
    signature = SigEncode(message, private_key)
    print('Digital signature created.')
    return signature

def Verify(sig_text, message, public_key):
    decrypted_sig_text = SigDecode(sig_text, public_key)
    verification_result = decrypted_sig_text == message
    print(f'Signature Verification Result: {verification_result}')
    return verification_result

""" Send-ReceiveKey Block """
def SendKey(private_key_A, public_key_B, message):
    k1 = Encode(message, public_key_B)
    S = Sign(message, private_key_A)
    S1 = Encode(S, public_key_B)
    return k1,S1

def ReceiveKey(public_key_A, private_key_B, k1, S1):
    k = Decode(k1, private_key_B)
    S = Decode(S1, private_key_B)
    if Verify(S, k, public_key_A):
        print("Key is valid")
        return k,S
    else:
        print("Invalid Key!")
    
def Text2Bytes(text):
    byte_array = bytearray()
    for char in text:
        byte_array.extend(char.encode('utf-8'))
    return int.from_bytes(byte_array, 'big')

def Bytes2Text(integ):
    byte_array = integ.to_bytes((integ.bit_length() + 7) // 8, 'big')
    decoded_text = ""
    i = 0
    while i < len(byte_array):
        try:
            char = byte_array[i:].decode('utf-8')
            decoded_text += char
            i += len(char.encode('utf-8'))
        except UnicodeDecodeError:
            decoded_text += f"\\x{byte_array[i]:02x}"
            i += 1
    return decoded_text

def Test():
    sent = True
    while sent:
        p = generate_random_prime(256)
        p1 = generate_random_prime(256)
        q = generate_random_prime(256)
        q1 = generate_random_prime(256)
        if p * q < p1 * q1 or p * q == p1 * q1:
            sent = False
    A_keypair = GenerateKeyPair(p,q)
    B_keypair = GenerateKeyPair(p1,q1)
    A_public = A_keypair[0]
    print(A_public)
    A_private = A_keypair[1]
    print(A_private)
    B_public = B_keypair[0]
    print(B_public)
    B_private = B_keypair[1]
    print(B_private)
    message = random.randint(10,100)
    print(message)
    A_ct = Encode(message, A_public)
    A_pt = Decode(A_ct, A_private)
    print(A_pt)
    A_sg = Sign(message, A_private)
    A_ver = Verify(A_sg, message ,A_public)
    if not A_ver:
        print("Verification failed on A-side ")
    B_ct = Encode(message, B_public)
    B_pt = Decode(B_ct, B_private)
    B_sg = Sign(message, B_private)
    B_ver = Verify(B_sg,message, B_public)
    if not B_ver:
        print("Verification failed on B-side ")
    k1, S1 = SendKey(A_private,B_public,message)
    k, S = ReceiveKey(A_public,B_private, k1, S1)
    print("Key exchange:")
    print(f"message: {message}")
    print(f"k1: {k1}")
    print(f"S1: {S1}")
    print(f"k: {k}")
    print(f"S: {S}")
    print("Key exchange passed the test\n")
    text_message='RSA is cool. Best computer workshop' 
    pt = Text2Bytes(text_message)
    print(pt)
    ct = Encode(pt, A_public)
    print(ct)
    pt_dec= Decode(ct, A_private)
    print(Bytes2Text(pt_dec))

if __name__ == '__main__':
    Test()