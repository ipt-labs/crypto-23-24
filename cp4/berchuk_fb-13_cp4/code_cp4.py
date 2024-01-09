import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def MillerRabin(p, k = 100):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    for prime in primes:
        if p % prime == 0:
            return False

    d = p - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for i in range(k):
        x = random.randint(2, p - 1)
        if gcd(x, p) > 1:
            return False

        if pow(x, d, p) != 1 and pow(x, d, p) != p - 1:
            for r in range(1, s - 1):
                xr = pow(x, d * (2 ** r), p)
                if xr == - 1:
                    break
            else:
                return False
    return True

def PrimeGen(bits):
    while True:
        p = random.randint(2 ** (bits - 1), 2 ** bits)
        if MillerRabin(p):
            return p

p, q = PrimeGen(256), PrimeGen(256)
p1, q1 = PrimeGen(256), PrimeGen(256)
while p * q > p1 * q1:
    p1, q1 = PrimeGen(256), PrimeGen(256)

print('TASK 2 ' + '-' * 175)
print(f"p = {p}")
print(f"q = {q}")
print('-' * 40)
print(f"p1 = {p1}")
print(f"q1 = {q1}")
print('\nTASK 3 ' + '-' * 175)

def GenerateKeyPair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537 #2^16 + 1
    d = pow(e, -1, phi)
    return (d, p, q), (n, e)

A_private, A_public = GenerateKeyPair(p, q)
B_private, B_public = GenerateKeyPair(p1, q1)

print("Відкритий ключ абонента A:")
print(A_public)
print("Відкритий ключ абонента A (hex):")
print("(" + ", ".join(map(lambda x: format(x, 'X'), A_public)) + ")")
print('-' * 40)

print("Відкритий ключ абонента B:")
print(B_public)
print("Відкритий ключ абонента B (hex):")
print("(" + ", ".join(map(lambda x: format(x, 'X'), B_public)) + ")")
print('-' * 40)

print("Таємний ключ абонента A:")
print(A_private)
print("Таємний ключ абонента A (hex):")
print("(" + ", ".join(map(lambda x: format(x, 'X'), A_private)) + ")")
print('-' * 40)

print("Таємний ключ абонента B:")
print(B_private)
print("Таємний ключ абонента B (hex):")
print("(" + ", ".join(map(lambda x: format(x, 'X'), B_private)) + ")")
print('\nTASK 4 ' + '-' * 175)

def Encrypt(m, pubkey):
    n, e = pubkey
    c = pow(m, e, n)
    return c

def Decrypt(c, privkey):
    d, p, q = privkey
    m = pow(c, d, p * q)
    return m

def Sign(m, privkey):
    d, p, q = privkey
    s = pow(m, d, p * q)
    return s

def Verify(m, s, pubkey):
    n, e = pubkey
    v = pow(s, e, n)
    return v == m

m = random.randint(10**50,  10**60)
print("Відкрите повідомлення:", m)
print("Відкрите повідомлення (hex):", hex(m).upper()[2:])
print('-' * 40)

c1 = Encrypt(m, A_public)
print("Шифротекст для A:", c1)
print("Шифротекст для A (hex):", hex(c1).upper()[2:])
print('-' * 40)

m1 = Decrypt(c1, A_private)
print("Розшифроване повідомлення для A:", m1)
print("Розшифроване повідомлення для A (hex):", hex(m1).upper()[2:])
print('-' * 40)

c2 = Encrypt(m, B_public)
print("Шифротекст для B:", c2)
print("Шифротекст для B (hex):", hex(c2).upper()[2:])
print('-' * 40)

m2 = Decrypt(c2, B_private)
print("Розшифроване повідомлення для B:", m2)
print("Розшифроване повідомлення для B (hex):", hex(m2).upper()[2:])
print('-' * 40)

s1 = Sign(m, A_private)
print("Цифровий підпис абонента A:", s1)
print("Цифровий підпис абонента A (hex):", hex(s1).upper()[2:])
print("Верифікація підпису для абонента A: ", Verify(m, s1, A_public))
print('-' * 40)

s2 = Sign(m, B_private)
print("Цифровий підпис абонента B:", s2)
print("Цифровий підпис абонента B (hex):", hex(s2).upper()[2:])
print("Верифікація підпису для абонента B: ", Verify(m, s2, B_public))
print('\nTASK 5 ' + '-' * 175)

def SendKey(k, B_public, A_private):
    k1 = Encrypt(k, B_public)
    s = Sign(k, A_private)
    s1 = Encrypt(s, B_public)
    return k1, s1

k = random.randint(1, A_public[0] - 1)
k1, s1 = SendKey(k, B_public, A_private)
print("Відправлений k1:", k1)
print("Відправлений k1 (hex):", hex(k1).upper()[2:])
print('-' * 40)
print("Відправлений підпис s1:", s1)
print("Відправлений підпис s1 (hex):", hex(s1).upper()[2:])
print('-' * 40)

def ReceiveKey(k1, s1, A_public, B_private):
    k = Decrypt(k1, B_private)
    s = Decrypt(s1, B_private)
    check = Verify(k, s, A_public)
    return k, check

k_res, check = ReceiveKey(k1, s1, A_public, B_private)
print("Отриманий k:", k_res)
print("Отриманий k (hex):", hex(k_res).upper()[2:])
print("Перевірка підпису:", check)

