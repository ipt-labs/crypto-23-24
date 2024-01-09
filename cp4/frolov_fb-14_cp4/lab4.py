import random  # not secure random, but ok for lab


def extended_gcd(a: int, b: int):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x


def modular_inverse(a: int, m: int):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m


def miller_rabin_test(n: int, a: int):
    exp = n - 1
    while not exp & 1:
        exp >>= 1

    if pow(a, exp, n) == 1:
        return True

    while exp < n - 1:
        if pow(a, exp, n) == n - 1:
            return True

        exp <<= 1

    return False


def miller_rabin(n: int, k: int = 40):
    for i in range(k):
        a = random.randrange(2, n - 1)
        if not miller_rabin_test(n, a):
            return False

    return True


def prime_gen(prime_len: int):
    prime = random.getrandbits(prime_len)
    while miller_rabin(prime) is False:
        prime = random.getrandbits(prime_len)
    return prime


def prime_pair_gen(prime_len: int = 256):  # not effective
    p, q = prime_gen(prime_len), prime_gen(prime_len)
    p1, q1 = prime_gen(prime_len), prime_gen(prime_len)
    while p1 * q1 < p * q or p == q or p1 == q1:
        p = prime_gen(prime_len)
        q = prime_gen(prime_len)
        p1 = prime_gen(prime_len)
        q1 = prime_gen(prime_len)
    return p, q, p1, q1


def key_pair_gen(p: int, q: int):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # can be randomed
    d = modular_inverse(e, phi)
    key_pub = [n, e]
    key_priv = [p, q, d]
    return key_pub, key_priv


def encrypt(plaintext: int, key_pub: list):
    n, e = key_pub
    cipher_text = pow(plaintext, e, n)
    return cipher_text


def decrypt(ciphertext: int, key_priv: list):
    p, q, d = key_priv
    plain_text = pow(ciphertext, d, p * q)
    return plain_text


p, q, p1, q1 = prime_pair_gen()
pubA, privA = key_pair_gen(p, q)
pubB, privB = key_pair_gen(p1, q1)
print(f"--A--\nn: {pubA[0]}\ne: {pubA[1]}\np: {privA[0]}\nq: {privA[1]}\nd: {privA[2]}\n")
print(f"--B--\nn: {pubB[0]}\ne: {pubB[1]}\np: {privB[0]}\nq: {privB[1]}\nd: {privB[2]}\n")

plaintextA = random.randint(1, pubA[0] - 1)
ciphertextA = encrypt(plaintextA, pubA)
ciphertextAdecrypted = decrypt(ciphertextA, privA)
print(
    f"Tестування А\nДані: {plaintextA}\nЗашифровані дані: {ciphertextA}\nРозшифровані зашифровані дані: {ciphertextAdecrypted}")
if ciphertextAdecrypted == plaintextA:
    print("Успішна перевірка для A\n\n")

plaintextB = random.randint(1, pubB[0] - 1)
ciphertextB = encrypt(plaintextB, pubB)
ciphertextBdecrypted = decrypt(ciphertextB, privB)
print(
    f"Tестування B\nДані: {plaintextB}\nЗашифровані дані: {ciphertextB}\nРозшифровані зашифровані дані: {ciphertextBdecrypted}")
if ciphertextBdecrypted == plaintextB:
    print("Успішна перевірка для B\n\n")
