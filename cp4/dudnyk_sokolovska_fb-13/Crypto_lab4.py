import random
from typing import List

E = 2**16 + 1


def get_inversed(a, m):

    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x

    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m

# lab4

def gcd(a:int, b:int):
    # easy gcd
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def horner_pow(num:int, exp:int, mod:int):
    res = 1
    num %= mod
    bits_num = bin(exp)[2:]
    for i in bits_num:
        res = (res*res) % mod
        if i == '1':
            res *= num % mod
    return res

def miller_rabin(p:int, k:int = 50):
    d = p-1
    s = 0
    while d % 2 == 1:
        s += 1
        d //= 2

    for _ in range(k):
    
        x = random.randint(2, p-1)
        if gcd(x, p) != 1: 
            return False
        
        x_1 = horner_pow(x, d, p)
        if x_1 == 1 or x_1 == -1 : 
            return True

        for r in range(1, s+1):
            x_r = horner_pow(x, d*(2**r), p)
            if x_r == -1 : 
                return True
    
    return False

# print(miller_rabin(324))

def get_random_prime(start:int = None, end:int = None, bits = None, toprint:bool=False):
    if bits is not None:
        while True:
            num = random.getrandbits(bits)
            if miller_rabin(num) : 
                if toprint: print(num)
                return num

    elif start is not None and end is not None:
        while True:
            num = random.randint(start, end)
            if miller_rabin(num): 
                if toprint: print(num)
                return num
    else:
        raise ValueError("Некорректно задано початкове та кінцеве значення інтервалу або кількість бітів!")
    
# get_random_prime(bits=64, toprint=true)

def get_keys_pairs(bits:int=256):
    secret_keys = {}
    open_keys = {}

    # for A, n and e - keys
    secret_keys['p'] = get_random_prime(bits=bits)
    secret_keys['q'] = get_random_prime(bits=bits)
    open_keys['n'] = secret_keys['p']*secret_keys['q']
    # euler = (secret_keys['p'] - 1)*(secret_keys['q'] - 1)
    e = E
    open_keys['e'] = e
    # while True:
    #     # while True:
    #     #     e = random.randint(2, euler - 1)
    #     #     if gcd(e, euler) == 1:
    #     #         open_keys['e'] = e
    #     #         break
    #     if gcd(e, euler) != 1:
    #         return None
    #     open_keys['e'] = e
    #     break
    secret_keys['d'] = get_inversed(open_keys['e'], secret_keys['p'])

    return secret_keys, open_keys

# print(get_keys_pairs()) 

def generate_pairs_AB():
    
    A_secretKeys, A_openKeys = get_keys_pairs()
    B_secretKeys, B_openKeys = get_keys_pairs()
    # перевірка q1*p1 <= q2*p2
    while B_secretKeys['q']*B_secretKeys['p'] < A_secretKeys['q']*A_secretKeys['p']:
        B_secretKeys, B_openKeys = get_keys_pairs()
    else: 
        return A_openKeys, A_secretKeys, B_openKeys, B_secretKeys

def cipher_message(M:int, openKeys:dict):
    n, e = openKeys['n'], openKeys['e']
    if M > n-1 :
        raise ValueError(f"Ваше повідомлення занадто велике для шифрування!\nПовідомлення:{M}")
    elif M < 0:
        raise ValueError("Ваше повідомлення менше 0")
    res = horner_pow(M, e, n)
    return res

def decipher_message(C:int, privateKeys:dict):
    p, q, d = privateKeys['p'], privateKeys['q'], privateKeys['d']
    n = p*q
    if C > n:
        raise ValueError(f"Криптограма завелика для розшифрування!\nКриптограма: {C}\nn:{n}")
    elif C < 0:
        raise ValueError("Криптограма менше нуля!")
    res = horner_pow(C, d, n)
    return res


def crypto_sign(M:int, private_keys:dict):
    S = horner_pow(M, private_keys['d'], private_keys['p'] * private_keys['q'])
    return S

def verification(M:int, S:int, open_keys:dict):
    return M == horner_pow(S, open_keys['e'], open_keys['n'])

def send_message(M:int, A_privateKeys:dict, B_openKeys:dict):
    encrypted_M = cipher_message(M, B_openKeys)
    S = crypto_sign(M, A_privateKeys)
    S1 = horner_pow(S, B_openKeys['e'], B_openKeys['n'])

    return encrypted_M, S1

def receive_message(encrypted_M:int, S1:int, B_privateKeys:dict, A_openKeys:dict):
    M = decipher_message(encrypted_M, B_privateKeys)
    S = decipher_message(S1, B_privateKeys)

    verified = verification(M, S, A_openKeys)

    if not verified:
        print("Аутентифікацію провалено! Підпис та/або ключі невірні!")
    else:
        print("Аутентифікацію пройдено успішно!\n", M)

    

A_openKeys, A_secretKeys, B_openKeys, B_secretKeys = generate_pairs_AB()
print("A", A_openKeys, A_secretKeys, "B", B_openKeys, B_secretKeys)

message = 2
# print(A_openKeys, A_secretKeys)
# encrypted_message, sign1 = send_message(message, A_secretKeys, B_openKeys)
# receive_message(encrypted_message, sign1, B_secretKeys, A_openKeys)