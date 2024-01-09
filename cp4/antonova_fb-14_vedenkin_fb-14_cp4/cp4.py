import random

def gcd(a, b):            # НСД
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):        # розширений алгоритм Евкліда
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise Exception('Modular inverse does not exist :(')
    return x % m

def encrypt(message, public_key):
    n, e = public_key
    encrypted_message = pow(message, e, n)
    return encrypted_message

def decrypt(ciphertext, secret_key, public_key):
    n, _ = public_key
    d, _, _ = secret_key
    decrypted_message = pow(ciphertext, d, n)
    return decrypted_message

def sign(message, secret_key, public_key):
    n, _ = public_key
    d, _, _ = secret_key
    signature = pow(message, d, n)
    return signature

def verify(signature, message, public_key):
    n, e = public_key
    decrypted_signature = pow(signature, e, n)
    return decrypted_signature == message

def send_key(key, public_key):
    return encrypt(key, public_key)

def receive_key(encrypted_key, secret_key, public_key):
    return decrypt(encrypted_key, secret_key, public_key)

def is_prime(n, k=5):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0:
        return False

    def miller_rabin_test(d, n):  # тест Міллера-Рабіна
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        while d != n - 1:
            x = (x * x) % n
            d *= 2
            if x == 1:
                return False
            if x == n - 1:
                return True
        return False

    d = n - 1
    while d % 2 == 0:
        d //= 2

    for _ in range(k):
        if not miller_rabin_test(d, n):
            return False

    return True

def generate_prime(bits=256):
    while True:
        candidate = random.getrandbits(bits)
        if candidate % 2 == 0:
            candidate += 1
        if is_prime(candidate):
            return candidate

def generate_prime_pair(min_bits=256):
    while True:
        p = generate_prime(min_bits)
        q = generate_prime(min_bits)
        if p != q:
            break

    while True:
        p1 = generate_prime(min_bits)
        q1 = generate_prime(min_bits)
        if p1 != q1 and p * q <= p1 * q1:
            break

    return p, q, p1, q1

def generate_rsa_keys(bits=2048):
    p, q, p1, q1 = generate_prime_pair(bits // 2)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # Спільно використовуване значення для e
    d = mod_inverse(e, phi)

    public_key = (n, e)
    secret_key = (d, p, q)

    n1 = p1 * q1
    phi1 = (p1 - 1) * (q1 - 1)
    e1 = 65537  # Спільно використовуване значення для e1
    d1 = mod_inverse(e1, phi1)

    public_key1 = (n1, e1)
    secret_key1 = (d1, p1, q1)

    return secret_key, public_key, secret_key1, public_key1

random_prime = generate_prime()
print("Random number:", random_prime)

# Генерація пар простих чисел
p, q, p1, q1 = generate_prime_pair()

print("Abonent A:")
print("p =", p)
print("q =", q)
print("\nAbonent B:")
print("p1 =", p1)
print("q1 =", q1)

keys_A = generate_rsa_keys()
keys_B = generate_rsa_keys()

secret_key_A, public_key_A, secret_key_B, public_key_B = keys_A

print("Abonent A:")
print("p =", secret_key_A[1])
print("q =", secret_key_A[2])
print("Public Key (e, n):", public_key_A)
print("Private Key (d, p, q):", secret_key_A)

print("\nAbonent B:")
print("p1 =", secret_key_B[1])
print("q1 =", secret_key_B[2])
print("Public Key (e1, n1):", public_key_B)
print("Private Key (d1, p1, q1):", secret_key_B)

# Збереження секретних ключів для подальшого використання
d_A, _, _ = secret_key_A
d_B, _, _ = secret_key_B

d1_A, _, _ = keys_A[2]
d1_B, _, _ = keys_B[2]

# Вибір відкритого повідомлення M
message_M = random.randint(2, public_key_A[0] - 1)

# Шифрування для абонентів A та B
ciphertext_A = encrypt(message_M, public_key_A)
ciphertext_B = encrypt(message_M, public_key_B)

# Розшифрування для абонентів A та B
decrypted_message_A = decrypt(ciphertext_A, secret_key_A, public_key_A)
decrypted_message_B = decrypt(ciphertext_B, secret_key_B, public_key_B)

# Створення та перевірка цифрового підпису для абонентів A та B
signature_A = sign(message_M, secret_key_A, public_key_A)
signature_B = sign(message_M, secret_key_B, public_key_B)

verification_A = verify(signature_A, message_M, public_key_A)
verification_B = verify(signature_B, message_M, public_key_B)

print("\nOriginal Message:", message_M)
print("\nEncrypted Message A:", ciphertext_A)
print("\nDecrypted Message A:", decrypted_message_A)
print("\nEncrypted Message B:", ciphertext_B)
print("\nDecrypted Message B:", decrypted_message_B)
print("\nSignature A:", signature_A)
print("Verification A:", verification_A)
print("\nSignature B:", signature_B)
print("Verification B:", verification_B)