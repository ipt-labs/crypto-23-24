from random import randint, getrandbits


def extended_euclidean(a: int, b: int) -> tuple:
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_euclidean(b % a, a)
        return gcd, y - (b // a) * x, x


def gorner(x: int, a: int, m: int) -> int:
    a_binary: str = str(bin(a))[2:]
    y: int = 1

    for binary in a_binary:
        y = (y ** 2) % m
        y = (y * x ** int(binary)) % m

    return y


def miller_rabin(p: int, k: int) -> bool:
    counter: int = 0

    d = p - 1
    s = 0

    while d % 2 == 0:
        s += 1
        d //= 2

    while k > counter:
        is_strong_prime: bool = False
        counter += 1

        x = randint(2, p - 1)
        gcd, null, null = extended_euclidean(x, p)
        if gcd > 1:
            return False

        if gorner(x, d, p) == 1 or gorner(x, d, p) == p - 1:
            continue

        for r in range(1, s - 1):
            x_r = gorner(x, d * 2 ** r, p)

            if x_r == p - 1:
                is_strong_prime = True
                break

            if x_r == 1:
                return False

        if not is_strong_prime:
            return False

    return True


def is_prime_by_division(number: int) -> bool:
    bases: tuple = (2, 3, 5, 7)
    for base in bases:
        if number % base == 0:
            return False
    return True


def generate_prime(bits: int, show_fails: bool) -> int:
    while True:
        number = getrandbits(bits)
        if is_prime_by_division(number):
            if miller_rabin(number, 16):
                print(f"\033[1;32;40mCandidate: {number} succeeded\033[0;37;40m")
                return number
        if show_fails:
            print(f"Candidate: {number} failed")


def generate_prime_pair(show_fails: bool) -> tuple:
    while True:
        p = generate_prime(256, show_fails)
        q = generate_prime(256, show_fails)

        p1 = generate_prime(256, show_fails)
        q1 = generate_prime(256, show_fails)

        if p * q > p1 * q1:
            if show_fails:
                print(f'Candidate p {p} failed')
                print(f'Candidate q {q} failed')
                print(f'Candidate p1 {p1} failed')
                print(f'Candidate q1 {q1} failed')
        else:
            print(f'\033[1;32;40mCandidate p {p} succeed\033[0;37;40m')
            print(f'\033[1;32;40mCandidate q {q} succeed\033[0;37;40m')
            print(f'\033[1;32;40mCandidate p1 {p1} succeed\033[0;37;40m')
            print(f'\033[1;32;40mCandidate q1 {q1} succeed\033[0;37;40m')
            return (p, q), (p1, q1)


def key_generate(key_pair: tuple) -> tuple:
    p, q = key_pair
    n: int = p * q
    oiler: int = (p - 1) * (q - 1)
    e: int = 65537
    d: int = extended_euclidean(e, oiler)[1] % oiler
    public_key: tuple = (n, e)
    private_key: tuple = (d, p, q)
    return public_key, private_key


def Encrypt(message: int, public_key: tuple) -> int:
    n, e = public_key
    return gorner(message, e, n)


def Decrypt(cryptogram: int, public_key: tuple, private_key: tuple) -> int:
    n, e = public_key
    d, p, q = private_key
    return gorner(cryptogram, d, n)


def Sign(message: int, public_key: tuple, private_key: tuple) -> int:
    n, e = public_key
    d, p, q = private_key
    return gorner(message, d, n)


def Verify(message: int, signed: int, public_key: tuple) -> bool:
    n, e = public_key
    if message == gorner(signed, e, n):
        return True
    else:
        return False


def SendKey(k: int, sender_private_key: tuple, sender_public_key: tuple, recipient_public_key: tuple) -> tuple:
    n, e = sender_public_key
    d, p, q = sender_private_key
    n1, e1 = recipient_public_key
    s = gorner(k, d, n)
    s1 = gorner(s, e1, n1)
    k1 = gorner(k, e1, n1)
    return k1, s1


def RecieveKey(keycryptogram: tuple, recipient_public_key: tuple, recipient_private_key: tuple,
               sender_public_key: tuple) -> int or None:
    n1, e1 = recipient_public_key
    d1, p1, q1 = recipient_private_key
    n, e = sender_public_key
    k1, s1 = keycryptogram
    k = gorner(k1, d1, n1)
    s = gorner(s1, d1, n1)
    if k == gorner(s, e, n):
        return True, k
    else:
        return False, k


key_pair_A, key_pair_B = generate_prime_pair(show_fails=True)
public_key_A, private_key_A = key_generate(key_pair_A)
print(f"Public A key: {public_key_A}\nPrivate A key: {private_key_A}")
public_key_B, private_key_B = key_generate(key_pair_B)
print(f"Public B key: {public_key_B}\nPrivate B key: {private_key_B}")

message = getrandbits(500)
print("\nMessage generation")
print("\tGenerated message:", message)

print("\nMessage encryption/decryption")

cryptogram_A = Encrypt(message, public_key_A)
print("\tEncrypted message for A:", cryptogram_A)
decrypted_A = Decrypt(cryptogram_A, public_key_A, private_key_A)
print("\tDecrypted message for A:", decrypted_A)
if message == decrypted_A:
    print('\tEncryption/Decryption succeed for A')
else:
    print('\tEncryption/Decryption failed for A')

cryptogram_B = Encrypt(message, public_key_B)
print("\n\tEncrypted message for B:", cryptogram_B)
decrypted_B = Decrypt(cryptogram_B, public_key_B, private_key_B)
print("\tDecrypted message for B:", decrypted_B)
if message == decrypted_B:
    print('\tEncryption/Decryption succeed for B')
else:
    print('\tEncryption/Decryption failed for B')

print("\nMessage signing/verification")

signed_A = Sign(message, public_key_A, private_key_A)
print("\tSigned message for A:", signed_A)
if Verify(message, signed_A, public_key_A):
    print('\tMessage verification succeed for A')
else:
    print('\tMessage verification failed for A')

signed_B = Sign(message, public_key_B, private_key_B)
print("\n\tSigned message for B:", signed_B)
if Verify(message, signed_B, public_key_B):
    print('\tMessage verification succeed for B')
else:
    print('\tMessage verification failed for B')

print('\nConfidential key distribution protocol (From A to B)')
k_A = randint(0, public_key_A[0])
print('\tRandom k value:', k_A)
keycryptogram_A = SendKey(k_A, private_key_A, public_key_A, public_key_B)
print('\tGenerated message to send/recieve', keycryptogram_A)
recieved_key_A = RecieveKey(keycryptogram_A, public_key_B, private_key_B, public_key_A)
if recieved_key_A[0]:
    print('\tKey received, Authorization succeed. Key:', recieved_key_A[1])
else:
    print('\tKey received, Authorization failed. Key:', recieved_key_A[1])

print("\nFor RSA testing environtment")
server_n = int(input("Enter server public key modulus: "), 16)
server_e = int(input("Enter server public exponent: "), 16)
# server_n = int("9800477FFE53E46DBC371AD75481F0D7FF6FAA300ECD5952244C1AC5E2002897",16)
# server_e = int("10001",16)
server_public_key = (server_n, server_e)
message = randint(0, server_n)
local_public_key = public_key_A
local_private_key = private_key_A
print('\nEncryption:')
print('\tModulus:', hex(local_public_key[0])[2:])
print('\tPublic exponent:', hex(local_public_key[1])[2:])
print('\tMessage:', hex(message)[2:])
print('\tExpected answer:', hex(Encrypt(message, local_public_key))[2:])

print('\nDecryption:')
print('\tEncrypted message with server public key:', hex(Encrypt(message, server_public_key))[2:])
print('\tExpected answer:', hex(message)[2:])

print('\nSignature:')
print('\tMessage to sign:', hex(message)[2:])
server_message_signature = int(input("\tEnter server signature: "), 16)
if Verify(message, server_message_signature, server_public_key):
    print('\tMessage verification succeed ')
else:
    print('\tMessage verification failed ')

print('\nVerification:')
print('\tMessage:', hex(message)[2:])
print('\tSignature:', hex(Sign(message, local_public_key, local_private_key))[2:])
print('\tModulus:', hex(local_public_key[0])[2:])
print('\tPublic exponent:', hex(local_public_key[1])[2:])

print('\nSend key:')
while local_public_key[0] < server_public_key[0]:
    print('Local key < server key. Decrease server key length!!!')
    server_n = int(input("Enter server public key modulus: "), 16)
    server_e = int(input("Enter server public exponent: "), 16)
    server_public_key = server_n, server_e

print('\tModulus:', hex(local_public_key[0])[2:])
print('\tPublic exponent:', hex(local_public_key[1])[2:])
# input 1 1 always work ???
recieved_key = int(input('\tEnter recieved key: '), 16)
recieved_signature = int(input('\tEnter recieved signature: '), 16)
server_keycryptogram = (recieved_key, recieved_signature)
key = RecieveKey(server_keycryptogram, local_public_key, local_private_key, server_public_key)
if key[0]:
    print('\tAuthorization succeed. Key:', hex(key[1])[2:])
else:
    print('\tAuthorization failed')

print("Recieve key: ")
while local_public_key[0] > server_public_key[0]:
    print('\tLocal key > server key. Increase server key length!!!')
    server_n = int(input("\tEnter server public key modulus: "), 16)
    server_e = int(input("\tEnter server public exponent: "), 16)
    server_public_key = server_n, server_e

key = randint(0, local_public_key[0])
keycryptogram = SendKey(key, local_private_key, local_public_key, server_public_key)
print('\tKey:', hex(keycryptogram[0])[2:])
print('\tSignature:', hex(keycryptogram[1])[2:])
print('\tModulus:', hex(local_public_key[0])[2:])
print('\tPublic exponent:', hex(local_public_key[1])[2:])
print("\tExpected key value:", hex(key)[2:])


