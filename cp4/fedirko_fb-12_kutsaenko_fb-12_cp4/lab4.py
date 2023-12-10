import random
from random import randrange

## ex 1

def GCD(a,b):
    if b == 0:
        return a, 1, 0
    d, x, y = GCD(b, a % b)
    return d, y, x - (a // b) * y

def reverse(num, mod):
    gcd, x, y = GCD(num, mod)
    if gcd == 1:
        return (x % mod + mod) % mod
    else:
        return -1

def horner(num, pow, mod):
    result = 1

    while pow > 0:
        if pow & 1:
            result = (result * num) % mod
        num = (num * num) % mod
        pow >>= 1

    return result

def rand_prime(N = 256):
    iter = 0
    while (True):
        iter = iter + 1
        bin_str = "1"
        for i in range(N - 1):
            bit = random.randint(0, 1)
            bin_str = bin_str + str(bit)
        num = int(bin_str, 2)
        if Miller_Rabin(num) == True:
            return num

def Miller_Rabin(number):
    if number % 2 == 0 or number % 3 == 0 or number % 5 == 0 or number % 7 == 0:
        return False
    s, d = 0, number - 1
    while d % 2 == 0:
        s += 1
        d //= 2
    for k in range(40):
        x = randrange(2, number - 1)
        gcd = GCD(x, number)[0]
        if gcd > 1:
            return False
        y = horner(x, d, number)
        if y == 1 or y == number - 1:
            return True
        while s > 1:
            y = horner(y, y, number)
            if y == 1:
                return False
            if y == -1:
                return True
            s -= 1
        return False

def rand_primes(N=256):
    p = rand_prime()
    q = rand_prime()

    p1 = rand_prime()
    q1 = rand_prime()

    while p * q <= p1 * q1:
        # Якщо pq ≤ p1q1, генеруємо нові пари чисел
        p = rand_prime()
        q = rand_prime()
        p1 = rand_prime()
        q1 = rand_prime()

    return p, q, p1, q1

def key_pair(p, q):
    n = p * q
    f = (p - 1) * (q - 1)

    while True:
        e = randrange(2, f)
        if GCD(e, f)[0] == 1:
            break

    d = reverse(e, f)

    public_key = [e, n]
    private_key = [d, p, q]

    return public_key, private_key

def encrypt(message, public_key):
    e, n = public_key
    if message >= n:
        raise ValueError("Message size exceeds the modulus (n). Choose a shorter message.")
    ciphertext = horner(message, e, n)#[horner(ord(char), e, n) for char in message]
    return ciphertext

def decrypt(ciphertext, private_key):
    d, p, q = private_key
    decrypted = horner(ciphertext, d, p * q)#[chr(horner(char, d, p * q)) for char in ciphertext]
    return decrypted#''.join(decrypted)

def sign(message, private_key):
    d, p, q = private_key
    #signature = [horner(ord(char), d, p * q) for char in message]
    #print(message)
    signature = horner(message, d, p * q)
    return signature

def verify(signature, message, public_key):
    e, n = public_key
    verified = horner(signature, e, n)#[chr(horner(char, e, n)) for char in signature]
    return verified==message#''.join(verified) == message

# ex 5
def send_key(private_key, public_key, message):
    message = encode(message)
    encrypted_message = encrypt(message, public_key)
    signature = sign(encrypted_message, private_key)

    print('Encrypted: ', encrypted_message)
    print('Encrypted hex: ', hex(encrypted_message))
    print('Signature: ', signature)

    return encrypted_message, signature


def receive_key(private_key, public_key, encrypted_message, signature):
    if verify(signature, encrypted_message,  public_key):
        print('Message is verified')
    else:
        print('Message is not verified')
        exit()

    decrypted_message = decrypt(encrypted_message, private_key)
    decrypted_message = decode(decrypted_message)
    print('Decrypted: ', decrypted_message)

    return decrypted_message

def encode(text): # перевод симфолів ASCII у хекс
    text = text.encode('utf-8')
    return int(text.hex(), 16)

def decode(text): # перевод цифр у букв
    return bytes.fromhex(hex(text)[2:]).decode('ASCII')



p, q, p1, q1 = rand_primes()
print("For A:", "\np=", p, "\nq=", q,"\nFor B:", "\np1=", p1, "\nq1=", q1)
print("For A:", "\nhex_p=", hex(p), "\nhex_q=", hex(q),"\nFor B:", "\nhex_p1=", hex(p1), "\nhex_q1=", hex(q1))
public_key_A, private_key_A = key_pair(p, q)
print("\nPublic key A:", "\ne", public_key_A[0],"\nn", public_key_A[1], "\nPrivate key A:", "\nd", private_key_A[0],"\np", private_key_A[1], "\nq", private_key_A[2])
print("\nPublic key A:", "\nhex_e", hex(public_key_A[0]),"\nhex_n", hex(public_key_A[1]), "\nPrivate key A:", "\nhex_d", hex(private_key_A[0]),"\nhex_p", hex(private_key_A[1]), "\nhex_q", hex(private_key_A[2]))
public_key_B, private_key_B = key_pair(p1, q1)
print("\nPublic key B:", "\ne", public_key_B[0],"\nn", public_key_B[1], "\nPrivate key B:", "\nd", private_key_B[0],"\np", private_key_B[1], "\nq", private_key_B[2])
print("\nPublic key B:", "\nhex_e", hex(public_key_B[0]),"\nhex_n", hex(public_key_B[1]), "\nPrivate key B:", "\nhex_d", hex(private_key_B[0]),"\nhex_p", hex(private_key_B[1]), "\nhex_q", hex(private_key_B[2]))
message = "Hello" #1234567890
print(message)
encrypted_message, signature = send_key(private_key_A, public_key_B, message)
receive_key(private_key_B, public_key_A, encrypted_message, signature)
