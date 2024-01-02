import math
import random


def generate_prime_number(bits):
    def get_random_number(bits):
        return random.randint(2 ** bits, 2 ** (bits + 1) - 1)

    def test_miller_rabin(p):
        if p % 2 == 0 or p % 3 == 0 or p % 5 == 0 or p % 7 == 0 or p % 11 == 0:
            print(p, 'not prime')
            return False

        s, d = 0, p - 1

        while d % 2 == 0:
            d //= 2
            s += 1
        assert (p - 1 == d * (2 ** s))

        x = random.randint(2, p - 2)

        if math.gcd(x, p) > 1:
            print(p, 'not prime')
            return False

        if pow(x, d, p) == 1 or pow(x, d, p) == -1:
            return True

        for _ in range(1, s - 1):
            x = (x * x) % p
            if x == -1:
                return True
            if x == 1:
                print(p, 'not prime')
                return False
        print(p, 'not prime')
        return False

    num = get_random_number(bits)
    while not test_miller_rabin(num):
        num = get_random_number(bits)
    print("Find prime")
    print(num)
    return num


def get_pair(bits):
    pair = (generate_prime_number(bits), generate_prime_number(bits))
    return pair


def generate_keys(pair):
    n = pair[0] * pair[1]
    f = (pair[0] - 1) * (pair[1] - 1)
    e = 2**16 + 1
    d = pow(e, -1, f)
    open_key = (n, e)
    secret_key = (d, pair[0], pair[1])
    return open_key, secret_key


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
        print('Message Confirmed')
    else:
        print('Message Declined')

def eye_painkiller():
    print('* ￣へ￣ *')


s = get_pair(256)
r = get_pair(256)

while s[0] * s[1] > r[0] * r[1]:
    s = get_pair(256)
    r = get_pair(256)

s_key = generate_keys(s)
r_key = generate_keys(r)

s_key_0, s_key_1 = s_key[0]
r_key_0, r_key_1 = r_key[0]

print(f'Sender public and private keys: {s_key_0} ({hex(s_key_0)})\n{s_key_1} ({hex(s_key_1)})')
print(f'Receiver public and private keys: {r_key_0} ({hex(r_key_0)})\n{r_key_1} ({hex(r_key_1)})')

message = random.randint(0, r[0] * r[1])
#message = 51
encrypted = encrypt(message, r_key)
signed_msg, signature = sign(message, s_key)
s1 = encrypt(signature, r_key)
final_message = (encrypted, s1)

decrypted = decrypt(final_message[0], r_key)
decrypted_sign = decrypt(final_message[1], r_key)

print(f'Original message: {message} ({hex(message)})')
eye_painkiller()
print(f'Signed message: {signed_msg} ({hex(signed_msg)})')
eye_painkiller()
print(f'Final encrypted message: {final_message} ({hex(final_message[0])}, {hex(final_message[1])})')
eye_painkiller()
print(f'Decrypted message: {decrypted} ({hex(decrypted)})')
eye_painkiller()
print(f'Decrypted sign: {decrypted_sign} ({hex(decrypted_sign)})')
print(verify)



"""
hexi hoch?

s_key_0, s_key_1 = s_key[0]
r_key_0, r_key_1 = r_key[0]

print(f'Sender public and private keys: {s_key_0} ({hex(s_key_0)})\n{s_key_1} ({hex(s_key_1)})')
print(f'Receiver public and private keys: {r_key_0} ({hex(r_key_0)})\n{r_key_1} ({hex(r_key_1)})')

message = random.randint(0, r[0] * r[1])
encrypted = encrypt(message, r_key)
signed_msg, signature = sign(message, s_key)
s1 = encrypt(signature, r_key)
final_message = (encrypted, s1)

decrypted = decrypt(final_message[0], r_key)
decrypted_sign = decrypt(final_message[1], r_key)

print(f'Original message: {message} ({hex(message)})')
eye_painkiller()
print(f'Signed message: {signed_msg} ({hex(signed_msg)})')
eye_painkiller()
print(f'Final encrypted message: {final_message} ({hex(final_message[0])}, {hex(final_message[1])})')
eye_painkiller()
print(f'Decrypted message: {decrypted} ({hex(decrypted)})')
eye_painkiller()
print(f'Decrypted sign: {decrypted_sign} ({hex(decrypted_sign)})')
print(verify)

"""

"""
hexi ne hoch

print(f'Sender public and private keys: {s_key[0]}\n{s_key[1]}')
print(f'Receiver public and private keys: {r_key[0]}\n{r_key[1]}')

message = random.randint(0, r[0] * r[1])
encrypted = encrypt(message, r_key)
signed = sign(message, s_key)
s1 = encrypt(signed[1], r_key)
final_message = (encrypted, s1)

decrypted = decrypt(final_message[0], r_key)
decrypted_sign = decrypt(final_message[1], r_key)

print(f'Original message: {message}')
eye_painkiller()
print(f'Encrypted message: {encrypted}')
eye_painkiller()
print(f'Signed message: {signed}')
eye_painkiller()
print(f'Encrypted message: {final_message}')
eye_painkiller()
print(f'Decrypted message: {decrypted}')
eye_painkiller()
print(f'Decrypted sign: {decrypted_sign}')
print(verify)


"""