import random
import hashlib

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def trial_division(n):
    if n < 2:
        return False
    for i in range(2, 100):
        if n % i == 0:
            return False
    return True

def miller_rabin_test(p, k=10):
    if p < 2:
        return False
    if p != 2 and p % 2 == 0:
        return False

    factorization_base = p - 1
    while factorization_base % 2 == 0:
        factorization_base //= 2

    for _ in range(k):
        witness = random.randint(1, p - 1)
        if gcd(witness, p) > 1:
            continue

        exponent = factorization_base
        residue = pow(witness, exponent, p)

        while exponent != p - 1 and residue != 1 and residue != p - 1:
            residue = (residue * residue) % p
            exponent *= 2

        if residue != p - 1 and exponent % 2 == 0:
            return False

    return True

def generate_random_prime(start, end, k=10):
    while True:
        p = random.randint(start, end)
        if trial_division(p) and miller_rabin_test(p, k):
            return p

def generate_key_pairs():
    bit_length = 256

    primes = [generate_random_prime(2**(bit_length-1), 2**bit_length - 1) for _ in range(4)]

    primes.sort()

    p, q = primes[:2]
    p1, q1 = primes[2:]

    return p, q, p1, q1

def generate_rsa_keys(p, q, p1, q1):
    n = p * q
    phi_n = (p - 1) * (q - 1)

    while True:
        public_exponent = random.randint(2, phi_n - 1)
        gcd_result, _, private_exponent = extended_gcd(phi_n, public_exponent)
        if gcd_result == 1:
            break

    n1 = p1 * q1
    phi_n1 = (p1 - 1) * (q1 - 1)

    while True:
        public_exponent_1 = random.randint(2, phi_n1 - 1)
        gcd_result_1, _, private_exponent_1 = extended_gcd(phi_n1, public_exponent_1)
        if gcd_result_1 == 1:
            break

    public_key = (n, public_exponent)
    private_key = (private_exponent, p, q)

    public_key_1 = (n1, public_exponent_1)
    private_key_1 = (private_exponent_1, p1, q1)

    return public_key, private_key, public_key_1, private_key_1

def encrypt(message, public_key):
    n, e = public_key
    cipher_text = pow(message, e, n)
    return cipher_text

def decrypt(cipher_text, private_key):
    d, p, q = private_key
    n = p * q
    plain_text = pow(cipher_text, d, n)
    return plain_text

def create_digital_signature(message, private_key):
    d, p, q = private_key
    n = p * q
    hashed_message = int.from_bytes(hashlib.sha256(message.encode()).digest(), byteorder='big')
    signature = pow(hashed_message, d, n)
    return (message, signature)

def verify_digital_signature(signed_message, public_key):
    n, e = public_key
    message, signature = signed_message
    hashed_message = int.from_bytes(hashlib.sha256(message.encode()).digest(), byteorder='big')
    decrypted_signature = pow(signature, e, n)
    return decrypted_signature == hashed_message

def send_key(public_key_B, private_key_A, public_key_A):
    k = random.randint(0, public_key_A[0] - 1)
    print("k value:", k)
    s = pow(k, private_key_A[0], public_key_A[0])
    k_1 = pow(k, public_key_B[1], public_key_B[0])
    S_1 = pow(s, public_key_B[1], public_key_B[0])
    return k_1, S_1

def recv_key(k_1, S_1, public_key_B, private_key_B, public_key_A):
    k = pow(k_1, private_key_B[0], public_key_B[0])
    S = pow(S_1, private_key_B[0], public_key_B[0])
    return k == pow(S, public_key_A[1], public_key_A[0])


p, q, p1, q1 = generate_key_pairs()
alice_public_key, alice_private_key, bob_public_key, bob_private_key = generate_rsa_keys(p, q, p1, q1)

message_to_alice = 42
cipher_text_for_alice = encrypt(message_to_alice, alice_public_key)
decrypted_message_for_alice = decrypt(cipher_text_for_alice, alice_private_key)

message_to_bob = "Hello, Bob!"
signed_message_for_bob = create_digital_signature(message_to_bob, bob_private_key)
signature_verified = verify_digital_signature(signed_message_for_bob, bob_public_key)

k_1, S_1 = send_key(bob_public_key, alice_private_key, alice_public_key)
key_received = recv_key(k_1, S_1, bob_public_key, bob_private_key, alice_public_key)

print("Message to Alice:", message_to_alice)
print("Encrypted Cipher Text for Alice:", cipher_text_for_alice)
print("Decrypted Message for Alice:", decrypted_message_for_alice)

print("Message to Bob:", message_to_bob)
print("Signed Message for Bob:", signed_message_for_bob)
print("Signature Verification Result for Bob:", signature_verified)

if key_received:
    print("Key exchange successful!")
else:
    print("Key exchange failed!")