import random

def ext_gcd(a,b):
    if a==0: 
        return b,0,1
    gcd,x,y = ext_gcd(b%a, a) 
    x,y = y-(b//a)*x,x
    return gcd,x,y

def mod_exp(base, exponent, mod):
    result = 1
    base = base % mod
    while exponent > 0:
        if (exponent & 1):
            result = (result * base) % mod
        exponent = exponent >> 1
        base = (base * base) % mod
    return result

def mod_inv(a, m):
    gcd, x, _ = ext_gcd(a, m)
    if gcd != 1:
        raise ValueError("The modular inverse does not exist")
    else:
        return x % m

def miller_rabin(n, k=40):
    if n <= 1 or n%2 == 0 or n%3 == 0 or n%5 == 0 or n%7 == 0:
        return False
    r, s = 0, n-1
    while s%2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n-1)
        x = mod_exp(a, s, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(r-1):
            x = mod_exp(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True

def generate_prime(length):
    while True:
        num = random.getrandbits(length)
        if miller_rabin(num):
            return num

def generate_prime_pairs(length=256):
    p = generate_prime(length)
    q = generate_prime(length)
    p1 = generate_prime(length)
    q1 = generate_prime(length)
    while p*q > p1*q1 or p == q or p1 == q1:
        if p1 != q1:
            p = generate_prime(length)
            q = generate_prime(length)
        else:
            p1 = generate_prime(length)
            q1 = generate_prime(length)
    return p,q,p1,q1

def generate_key_pair(p,q):
    n = p * q
    phi = (p-1) * (q-1)
    e = 65537
    while ext_gcd(e, phi)[0] != 1:
        e = random.randrange(2, phi)
    d = mod_inv(e, phi)
    public_key = (n, e)
    private_key = (p, q, d)
    return public_key, private_key

def encrypt(message, public_key):
    n, e = public_key
    cipher_text = mod_exp(message, e, n)
    return cipher_text

def decrypt(cipher_text, private_key):
    p, q, d = private_key
    plain_text = mod_exp(cipher_text, d, p*q)
    return plain_text

def sign(message, private_key):
    signature = decrypt(message, private_key)
    return signature

def verify(signature, message, public_key):
    decrypted_signature = encrypt(signature, public_key)
    return decrypted_signature == message

def send_key(private_key_A, public_key_B, message):
    k1 = encrypt(message, public_key_B)
    S = sign(message, private_key_A)
    S1 = encrypt(S, public_key_B)
    return k1,S1

def receive_key(public_key_A, private_key_B, k1, S1):
    k = decrypt(k1, private_key_B)
    S = decrypt(S1, private_key_B)
    if not verify(S, k, public_key_A):
        raise ValueError("Key received is not valid")
    return k,S

def encoding(text):
    return int.from_bytes(text.encode('utf-8'), 'big')

def decoding(integ):
    return integ.to_bytes((integ.bit_length()+7) // 8, 'big').decode('utf-8')
