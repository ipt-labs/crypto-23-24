import random


def extended_gcd(a, b):
    if not a:
        return b, 0, 1

    gcd, u1, v1 = extended_gcd(b % a, a)
    u = v1 - (b // a) * u1
    v = u1

    return gcd, u, v


def is_prime(p, k=20):
    if p <= 0 or p % 2 == 0:
        return False
    if p <= 3:
        return True

    s = 0
    d = p - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        x = random.randint(2, p - 1)
        gcd = extended_gcd(x, p)[0]
        if gcd > 1:
            return False
        if pow(x, d, p) in (p - 1, 1):
            continue

        x_r = pow(x, d, p)
        for r in range(1, s):
            x_r = pow(x_r, 2, p)
            if x_r == p - 1:
                break
        else:
            return False
    return True


def generate_prime(length=256):
    lower = 1 << (length - 1)
    higher = (1 << length) - 1
    while True:
        prime_candidate = random.randint(lower, higher)
        if is_prime(prime_candidate):
            return prime_candidate


def generate_rsa_key_pair(length=256):
    p = generate_prime(length=length)
    q = generate_prime(length=length)
    n = p * q
    euler = (p - 1) * (q - 1)
    public_exponent = 2 ** 16 + 1 if 2 ** 16 + 1 < euler else random.randint(2, euler)

    while extended_gcd(public_exponent, euler)[0] != 1:
        public_exponent = random.randint(2, euler)

    private_exponent = pow(public_exponent, -1, euler)

    public_key = (n, public_exponent)
    private_key = (private_exponent, p, q)

    return public_key, private_key


def encrypt(message, public_exponent, modulus):
    ciphertext = pow(message, public_exponent, modulus)
    return ciphertext


def decrypt(ciphertext, private_exponent, modulus):
    plaintext = pow(ciphertext, private_exponent, modulus)
    return plaintext


def sign_message(message, private_exponent, modulus):
    signature = pow(message, private_exponent, modulus)
    return signature


def verify(message, signature, public_exponent, modulus):
    return message == pow(signature, public_exponent, modulus)


def send_key(message, sender_public, sender_private, receiver_public):
    signature = sign_message(message, sender_private, sender_public[0])
    encrypted_signature = encrypt(signature, receiver_public[1], receiver_public[0])
    encrypted_message = encrypt(message, receiver_public[1], receiver_public[0])
    return encrypted_message, encrypted_signature


def receive_key(encrypted_message, encrypted_signature, sender_public, receiver_private, receiver_public):
    message = decrypt(encrypted_message, receiver_private, receiver_public[0])
    signature = decrypt(encrypted_signature, receiver_private, receiver_public[0])
    return verify(message, signature, sender_public[1], sender_public[0])


if __name__ == '__main__':
    public_A, private_A = generate_rsa_key_pair()
    public_B, private_B = generate_rsa_key_pair()
    if public_A[0] > public_B[0]:
        public_A, public_B = public_B, public_A
        private_A, private_B = private_B, private_A

    print(f'User A:\n'
          f'  Public Key:\n'
          f'    n = {public_A[0]}\n'
          f'    e = {public_A[1]}\n'
          f'  Private Key:\n'
          f'    p = {private_A[1]}\n'
          f'    q = {private_A[2]}\n'
          f'    d = {private_A[0]}')

    print(f'\nUser B:\n'
          f'  Public Key:\n'
          f'    n = {public_B[0]}\n'
          f'    e = {public_B[1]}\n'
          f'  Private Key:\n'
          f'    p = {private_B[1]}\n'
          f'    q = {private_B[2]}\n'
          f'    d = {private_B[0]}')

    message = random.randint(1, public_A[0] - 1)
    encrypted_message = encrypt(message, public_A[1], public_A[0])
    decrypted_message = decrypt(encrypted_message, private_A[0], public_A[0])
    signed_message = sign_message(message, private_A[0], public_A[0])

    print(f'\n===== Encryption/Decryption =====\n'
          f'  Original Message: {message}\n'
          f'  Encrypted Message: {encrypted_message}\n'
          f'  Decrypted Message: {decrypted_message}\n'
          f'  Message Signature: {signed_message}')

    verification = verify(message, signed_message, public_A[1], public_A[0])
    if verification:
        print(f'  Signature Verified')
    else:
        print(f'  Signature Not Verified')

    encrypted_key, encrypted_signature = send_key(message, public_A, private_A[0], public_B)
    print(f'\n===== Key Exchange =====\n'
          f'  Original Message: {message}\n'
          f'  Encrypted Message: {encrypted_key}\n'
          f'  Message Signature: {encrypted_signature}')

    verification = receive_key(encrypted_key, encrypted_signature, public_A, private_B[0], public_B)
    if verification:
        print(f'  Signature Verified')
    else:
        print(f'  Signature Not Verified')
