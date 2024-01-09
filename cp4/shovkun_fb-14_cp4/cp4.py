
import random

def gcd(a, m):
    while m != 0:
        a, m = m, a % m
    return a

def mod_inverse(a, m):
    def gcd_extended(a, m):
        if m == 0:
            return a, 1, 0
        else:
            gcd, x, y = gcd_extended(m, a % m)
            return gcd, y, x - (a // m) * y

    gcd, x, y = gcd_extended(a, m)
    if gcd != 1:
        return None
    else:
        return (x % m + m) % m

def keys(pair):
    n = pair[0] * pair[1]
    fi = (pair[0] - 1) * (pair[1] - 1)
    e = 2**16 + 1
    d = mod_inverse(e, fi)
    open_key = (n, e)
    secret_key = (d, pair[0], pair[1])
    return open_key, secret_key

def get_pair(bits):
    pair = (prime_number(bits), prime_number(bits))
    while pair[0] == pair[1]:
        pair = (prime_number(bits), prime_number(bits))

    return pair

def prime_number(bits):
    def random_number(bits):
        return random.randint(2 ** bits, 2 ** (bits + 1) - 1)

    def miller_rabin(p):
        if p % 2 == 0 or p % 3 == 0 or p % 5 == 0 or p % 7 == 0 or p % 11 == 0:
            return False

        s = 0
        d = p - 1

        while d % 2 == 0:
            d //= 2
            s += 1
        assert (p - 1 == d * (2 ** s))

        x = random.randint(2, p - 2)

        if gcd(x, p) > 1:
            return False

        if pow(x, d, p) == 1 or pow(x, d, p) == -1:
            return True

        for i in range(1, s - 1):
            x = (x * x) % p
            if x == -1:
                return True
            if x == 1:
                return False
        return False

    num = random_number(bits)
    while not miller_rabin(num):
        num = random_number(bits)

    return num

def encrypt(message, key):
    encrypted_message = pow(message, key[0][1], key[0][0])
    return encrypted_message

def sign(message, key):
    signed_message = (message, pow(message, key[1][0], key[0][0]))
    return signed_message

def decrypt(encrypted, key):
    decrypted_message = pow(encrypted, key[1][0], key[0][0])
    return decrypted_message

def verify(signed, message, key):
    if message == pow(signed, key[0][1], key[0][0]):
        return 'Verified'
    else:
        return 'Fake sign'

def send_key(msg, B_keys, A_keys):
    encrypted = encrypt(msg, B_keys)
    signed = sign(msg, A_keys)
    s1 = encrypt(signed[1], B_keys)
    final_message = (encrypted, s1)
    return final_message

def receive_key(final_message, B_keys, A_keys):
    decrypted = decrypt(final_message[0], B_keys)
    decrypted_sign = decrypt(final_message[1], B_keys)
    verification = verify(decrypted_sign, decrypted, A_keys)
    return decrypted, verification

A_pair = get_pair(256)
B_pair = get_pair(256)

while A_pair[0] * A_pair[1] > B_pair[0] * B_pair[1]:
    A_pair = get_pair(256)
    B_pair = get_pair(256)

A_keys = keys(A_pair)
B_keys = keys(B_pair)

print(f'Generated public key for A: {A_keys[0]}\nGenerated private key for A: {A_keys[1]}\n')
print(f'Generated public key for B: {B_keys[0]}\nGenerated private key for B: {B_keys[1]}\n')

print('======test======')
M = random.randint(0, min(A_pair[0] * A_pair[1], B_pair[0] * B_pair[1]))
print(f'M: {M}')
# Знаходження криптограми для абонентів A і B
print('======crypto======')
encrypted_A = encrypt(M, A_keys)
encrypted_B = encrypt(M, B_keys)
print(f'encrypted A: {encrypted_A}\nencrypted A: {encrypted_B}')
print('======decrypt======')
# Перевірка правильності розшифрування
decrypted_A = decrypt(encrypted_A, A_keys)
decrypted_B = decrypt(encrypted_B, B_keys)
print(f'Check decrypt for A: {M == decrypted_A}')
print(f'Check decrypt for B: {M == decrypted_B}')

# Складання повідомлення з цифровим підписом для A і B
print('======sign======')
signed_message_A = sign(M, A_keys)
signed_message_B = sign(M, B_keys)

# Перевірка підпису
verification_A = verify(signed_message_A[1], M, A_keys)
verification_B = verify(signed_message_B[1], M, B_keys)
print(f'Check sing for A: {verification_A}')
print(f'Check sing for B: {verification_B}')

print('======protocol======')

msg = random.randint(0, B_pair[0] * B_pair[1])
final_message = send_key(msg, B_keys, A_keys)
decrypted, verification = receive_key(final_message, B_keys, A_keys)
print(f'Original message: {msg}')
print(f'Encrypted message: {final_message[0]}')
print(f'Signed message: {final_message}')
print(f'Decrypted message: {decrypted}')
print(f'Verification result: {verification}')


