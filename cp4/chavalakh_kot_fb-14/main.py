import random
#random.seed(43)
def euclidean(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_euclidean(a, m):
    if m == 0:
        return a, 1, 0
    gcd_num, x, y = extended_euclidean(m, a % m)
    x, y = y, x - (a // m) * y
    return gcd_num, x, y


def modular_inverse(a, m):
    gcd, _, _ = extended_euclidean(a, m)
    if gcd != 1:
        return None
    _, x, _ = extended_euclidean(a, m)
    return x % m

def decimal_to_hex(decimal_number):
    hex_number = hex(decimal_number).lstrip("0x")
    return hex_number.upper()

def hex_to_decimal(hex_number):
    decimal_number = int(hex_number, 16)
    return decimal_number


def miller_rabin(p, k=40):
    S = 0
    d = p - 1
    while d % 2 == 0:
        S += 1
        d = d // 2
    for _ in range(k):
        a = random.randint(1, p)
        x = fast_exponentiation(a, d, p)
        if x == 1 or x == p - 1:
            continue

        for _ in range(S - 1):
            x = fast_exponentiation(x, 2, p)
            if x == p - 1:
                break
        else:
            return False
    return True



def random_num(start = 0, end = 0, bits = 0):
    for_divide = [2, 3, 5, 7]
    if start and end:
        while True:
            num = random.randint(start, end)
            prime = True
            for i in for_divide:
                if num % i == 0:
                    prime = False
            if prime:
                if miller_rabin(num):
                    return num
    elif bits:
        while True:
            num = random.getrandbits(bits)
            prime = True
            for i in for_divide:
                if num % i == 0:
                    prime = False
            if prime:
                if miller_rabin(num, 40):
                    return num
         
def fast_exponentiation(base, exponent, mod):
    result = 1

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        exponent = exponent // 2
        base = (base * base) % mod
    return result


def GenerateKeyPair(p, q):
    n = p*q
    oyler = (p-1)*(q-1)
    while True:
        e = 2**16 + 1#e = random_num(2, oyler - 1)
        if euclidean(e, oyler) == 1:
            d = modular_inverse(e, oyler)
            return (n, e), (d, p, q)
            

    
def Encrypt(msg, public_key):
    return fast_exponentiation(msg, public_key[1], public_key[0])

def Decrypt(msg, private_key):
    d, p, q = private_key
    n = p * q
    return fast_exponentiation(msg, d, n)

def Sign(msg, private_key):
    d, p, q = private_key
    n = p * q
    return(msg, fast_exponentiation(msg, d, n))

def Verify(msg, public_key):
    return fast_exponentiation(msg[1], public_key[1], public_key[0]) == msg[0]

def Encrypt_text(msg, public_key):
    msg = int.from_bytes(msg.encode('utf-8'), byteorder='big')
    return fast_exponentiation(msg, public_key[1], public_key[0])

def Decrypt_text(msg, private_key):
    d, p, q = private_key
    n = p * q
    msg = fast_exponentiation(msg, d, n)
    return msg.to_bytes((msg.bit_length()), byteorder='big').decode('utf-8')

def Sign_text(msg, private_key):
    d, p, q = private_key
    n = p * q
    msg_b = int.from_bytes(msg.encode('utf-8'), byteorder = 'big')
    return(msg, fast_exponentiation(msg_b, d, n))

def Verify_text(msg, pubkey):
    msg_b = int.from_bytes(msg[0].encode('utf-8'), byteorder='big')
    return msg_b == fast_exponentiation(msg[1], pubkey[1], pubkey[0])

def SendKey(k, public_key_A, private_key_A, public_key_B):
    k1 = fast_exponentiation(k, public_key_B[1], public_key_B[0])
    S = fast_exponentiation(k, private_key_A[0], public_key_A[0])
    S1 = fast_exponentiation(S, public_key_B[1], public_key_B[0])
    return(k1, S1)
    
def ReceiveKey(message, private_key_B, public_key_A, public_key_B):
    k = fast_exponentiation(message[0], private_key_B[0], public_key_B[0])
    S = fast_exponentiation(message[1], private_key_B[0], public_key_B[0])
    if k == fast_exponentiation(S, public_key_A[1], public_key_A[0]):
        return 'Verified', k
    else:
        return 'Not Verified', k

if __name__ == '__main__':
    p, q, p1, q1 = 1, 1, 0, 0
    not_fit = []
    while p*q >= p1*q1:
        p = random_num(bits = 256)
        q = random_num(bits = 256)
        p1 = random_num(bits = 256)
        q1 = random_num(bits = 256)
        not_fit.append((p, q, p1, q1))
    print(f"Not fit: {not_fit[:-1]}\n")
    print(f"p: {p}, \nq: {q}\n")
    print(f"p1: {p1}, \nq1: {q1}\n")
    Public_key_A, Private_key_A = GenerateKeyPair(p, q)
    print(f"A Public key: \n{Public_key_A},\nA Private key: \n{Private_key_A}\n")


    Public_key_B, Private_key_B = GenerateKeyPair(p1, q1)
    print(f"B Public key: \n{Public_key_B},\nB Private key: \n{Private_key_B}\n")


    message = 544
    print(f"Message from A to B: {message}")
    m = Encrypt(message, Public_key_B)
    print(f"Encrypted message: {m}")
    signed = Sign(message, Private_key_A)
    print(f"Sign: {signed[1]}")
    if Verify(signed, Public_key_A):
        print(f"Message Verified")
        m = Decrypt(m, Private_key_B)
        print(f"Decrypted message: {m}")


    message = 322
    print(f"\n\nMessage from B to A: {message}")
    m = Encrypt(message, Public_key_A)
    print(f"Encrypted message: {m}")
    signed = Sign(message, Private_key_B)
    print(f"Sign: {signed[1]}")
    if Verify(signed, Public_key_B):
        print(f"Message Verified")
        m = Decrypt(m, Private_key_A)
        print(f"Decrypted message: {m}\n\n")

    message = "Kot1337"
    print(f"Message: {message}")
    m = Encrypt_text(message, Public_key_A)
    print(f"Encrypted message: {m}")
    signed = Sign_text(message, Private_key_B)
    print(f"Sign: {signed[1]}")
    if Verify_text(signed, Public_key_B):
        print(f"Message Verified")
        m = Decrypt_text(m, Private_key_A)
        print(f"Decrypted message: {m}\n\n")
    
    k = random.randint(1, p * q - 1)
    print(f"Ключ {k}:")
    sent = SendKey(k, Public_key_A, Private_key_A, Public_key_B)
    recieved = ReceiveKey(sent, Private_key_B, Public_key_A, Public_key_B)
    print(recieved)
