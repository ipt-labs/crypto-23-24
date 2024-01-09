from stuff import *

def GenerateKeyPair(lower_bound, upper_bound):
    p = genrand(lower_bound, upper_bound)
    q = genrand(lower_bound, upper_bound)
    phi_n = (p - 1) * (q - 1)

    e = rd.randint(2, phi_n - 1)
    while egcd(e, phi_n)[0] != 1:
        e = rd.randint(2, phi_n - 1)
    
    d = egcd(e, phi_n)[1] % phi_n

    public_key = (p * q, e)
    secret_key = (d, p, q)

    return public_key, secret_key

def Encrypt(message, n, e):
    return pow(message, e, n)

def Decrypt(message, n, d):
    return pow(message, d, n)

def Sign(message, n, d):
    return pow(message, d, n)

def Verify(message, sign, n, e):
    signed_message = pow(sign, e, n)
    return message == signed_message

def SendKey(k, n, d, n1, e1):
    k1 = pow(k, e1, n1)
    s = pow(k , d, n)
    s1 = pow(s, e1, n1)
    return k1, s1

def ReceiveKey(k1, s1, n1, d1, n, e):
    k = pow(k1, d1, n1)
    s = pow(s1, d1, n1)
    if k == pow(s, e, n):
        return k
    return 0

if __name__ == "__main__":
    print("#" * 120)
    print("Keypair generation")
    b_pubkey = (int("0x" + input("B Modulus: "), 16), int("0x" + input("B Public exponent: "), 16))
    a_pubkey, a_seckey = GenerateKeyPair(2 ** 127, 2 ** 128)
    while a_pubkey[0] > b_pubkey[0]:
        a_pubkey, a_seckey = GenerateKeyPair(2 ** 127, 2 ** 128)
    a_seckey = a_seckey[0]
    print("A Modulus: ", hex(a_pubkey[0])[2:])
    print("A Public exponent: ", hex(a_pubkey[1])[2:])
    print("A secret exponent: ", hex(a_seckey)[2:])
    input()
    
    print("#" * 120)
    print("Encryption")
    message = rd.randint(2, a_pubkey[0])
    print("A Modulus: ", hex(a_pubkey[0])[2:])
    print("A Public exponent: ", hex(a_pubkey[1])[2:])
    print("Message: ", hex(message)[2:])
    b_ciphertext = int("0x" + input("B Encrypted message: "), 16)
    test_ciphertext = Encrypt(message, *a_pubkey)
    test_plaintext = Decrypt(b_ciphertext, a_pubkey[0], a_seckey)
    print("B Encrypted message and A Encrypted message match: ", b_ciphertext == test_ciphertext)
    print("Original Message and A Decrypted message match: ", message == test_plaintext)
    input()

    print("#" * 120)
    print("Decryption")
    message = rd.randint(2, b_pubkey[0])
    a_ciphertext = Encrypt(message, *b_pubkey)
    print("Message: ", hex(message)[2:])
    print("A Encrypted message: ", hex(a_ciphertext)[2:])
    b_message = int("0x" + input("B Decrypted message: "), 16)
    print("Message and B Decrypted message match: ", message == b_message)
    input()

    print("#" * 120)
    print("Sign verification")
    message = rd.randint(2, b_pubkey[0])
    print("Message: ", hex(message)[2:])
    b_sign = int("0x" + input("B Sign: "), 16)
    print("B signed message correctly: ", Verify(message, b_sign, *b_pubkey))
    input()

    print("#" * 120)
    print("Signing")
    message = rd.randint(2, a_pubkey[0])
    a_sign = Sign(message, a_pubkey[0], a_seckey)
    print("Message: ", hex(message)[2:])
    print("A Sign: ", hex(a_sign)[2:])
    print("A Modulus: ", hex(a_pubkey[0])[2:])
    print("A Public exponent: ", hex(a_pubkey[1])[2:])
    input()

    print("#" * 120)
    print("Key receiving and verification")
    print("A Modulus: ", hex(a_pubkey[0])[2:])
    print("A Public exponent: ", hex(a_pubkey[1])[2:])
    b_key = int("0x" + input("B Key: "), 16)
    b_sign = int("0x" + input("B Sign: "), 16)
    print("B Sent key: ", hex(ReceiveKey(b_key, b_sign, a_pubkey[0], a_seckey, *b_pubkey))[2:])
    input()

    print("#" * 120)
    print("Key sending")
    k = rd.randint(2, a_pubkey[0])
    print("Key: ", hex(k)[2:])
    k1, s1 = SendKey(k, a_pubkey[0], a_seckey, *b_pubkey)
    print("A Encrypted key: ", hex(k1)[2:])
    print("A Key sign: ", hex(s1)[2:])
    print("A Modulus: ", hex(a_pubkey[0])[2:])
    print("A Public exponent: ", hex(a_pubkey[1])[2:])
    b_key = int("0x" + input("B Key: "), 16)
    print("B Got correct key: ", k == b_key)
    print("")
    print("#" * 120)
    input()