from random import randint

def euclid(a, b):
    if not a:
        return b, 0, 1

    gcd, u1, v1 = euclid(b % a, a)
    u = v1 - (b // a) * u1
    v = u1

    return gcd, u, v

def check_prime(p, k=69):
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
        x = randint(2, p-1)
        gcd = euclid(x, p)[0]
        if gcd > 1:
            return False
        if pow(x, d, p) in (p-1, 1):
            continue

        x_r = pow(x, d, p)
        for r in range(1, s):
            x_r = pow(x_r, 2, p)
            if x_r == p-1:
                break
        else:
            return False
    return True

def generate_prime(length=128):
    lower = 1 << (length - 1)
    higher = (1 << length) - 1
    while True:
        p = randint(lower, higher)
        if check_prime(p):
            return p

def generate_key_pair(length=128):
    p = generate_prime(length=length)
    q = generate_prime(length=length)
    n = p * q
    euler = (p - 1) * (q - 1)
    if 2 ** 16 + 1 < euler:
        e = 2 ** 16 + 1
    else:
        while True:
            e = randint(2, euler)
            if euclid(e, euler)[0] == 1:
                break
    d = pow(e, -1, euler)
    pub = (n, e)
    priv = (d, p, q)
    return pub, priv

def encrypt(message, e, n):
    cypher = pow(message, e, n)
    return cypher

def decrypt(message, d, n):
    plain = pow(message, d, n)
    return plain

def sign_message(message, d, n):
    signature = pow(message, d, n)
    return signature

def verify(message, s, e, n):
    return message == pow(s, e, n)

def send_key(message, sender_public, sender_private, receiver_public):
    s = sign_message(message, sender_private, sender_public[0])
    s1 = encrypt(s, receiver_public[1], receiver_public[0])
    k1 = encrypt(message, receiver_public[1], receiver_public[0])
    return k1, s1

def receive_key(k1, s1, sender_public, receiver_private, receiver_public):
    message = decrypt(k1, receiver_private, receiver_public[0])
    s = decrypt(s1, receiver_private, receiver_public[0])
    return verify(message, s, sender_public[1], sender_public[0])

if __name__ == '__main__':
    public_A, private_A = generate_key_pair(128)
    public_B, private_B = generate_key_pair(128)
    if public_A[0] > public_B[0]:
        public_A, public_B = public_B, public_A
        private_A, private_B = private_B, private_A

    print(f'===== User А =====\n'
          f'Generating p, q....\n'
          f'Calculating n....\n'
          f'Calculating Oyler...\n'
          f'Calculating secret key for deciphering...\n'
          f'  Public Key:\n'
          f'    n = {public_A[0]}\n'
          f'    e = {public_A[1]}\n'
          f'  Private Key:\n'
          f'    p = {private_A[1]}\n'
          f'    q = {private_A[2]}\n'
          f'    d = {private_A[0]}')

    print(f'===== User A Send =====\n'
           f'Sending Public Key..\n'
           f'Sending (n, e)\n')

    print(f'Recieving public key from User A...\n'
          f'Got (n, e)\n')

    print(f'\n===== User B =====\n'
          f'Generating p, q....\n'
          f'Calculating n....\n'
          f'Calculating Oyler...\n'
          f'Calculating secret key for deciphering...\n'
          f'  Public Key:\n'
          f'    n = {public_B[0]}\n'
          f'    e = {public_B[1]}\n'
          f'  Private Key:\n'
          f'    p = {private_B[1]}\n'
          f'    q = {private_B[2]}\n'
          f'    d = {private_B[0]}')
    print(f'Generating message...\n')

    message = randint(1, public_A[0] - 1)
    encrypted_message = encrypt(message, public_A[1], public_A[0])
    decrypted_message = decrypt(encrypted_message, private_A[0], public_A[0])
    signed_message = sign_message(message, private_A[0], public_A[0])

    print(f'Hex n(USER A) {hex(public_A[0])[2:].upper()}\n')
    print(f'\n===== Шифрування повідомлення =====\n'
          f'  Початкове повідомлення: {message}\n'
          f'  Message in hex: {hex(message)[2:].upper()}\n'
          f'  Зашифроване повідомлення: {encrypted_message}\n'
          f'  Cyphered in hex {hex(encrypted_message)[2:].upper()}\n'
          f'  Розшифроване повідомлення: {decrypted_message}\n'
          f'  decrypted in hex: {hex(decrypted_message)[2:].upper()}\n'
          f'  Підпис повідомлення: {signed_message}\n'
          f'  Signature in hex: {hex(signed_message)[2:].upper()}\n')

    verification = verify(message, signed_message, public_A[1], public_A[0])
    if verification:
        print(f'  Підпис підтверджено')
    else:
        print(f'  Підпис не підтверджено')

    k1, s1 = send_key(message, public_A, private_A[0], public_B)
    print(f'\n===== Відправка ключа =====\n'
          f'  Початкове повідомлення: {message}\n'
          f'  Message in hex: {hex(message)[2:].upper()}\n'
          f'  Зашифроване повідомлення: {k1}\n'
          f'  Encrypted in hex: {hex(k1)[2:].upper()}\n'
          f'  Підпис повідомлення: {s1}'
          f'  Verification in hex: {hex(s1)[2:].upper()}\n')
    
    verification = receive_key(k1, s1, public_A, private_B[0], public_B)
    if verification:
        print(f'  Підпис підтверджено')
    else:
        print(f'  Підпис не підтверджено')

