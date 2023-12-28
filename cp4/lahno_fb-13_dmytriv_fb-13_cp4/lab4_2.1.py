import random


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


#a^-1
def inverse_mod(a, mod, v = None):
    if v is None:
        v = [0, 1]
    if a == 0 or gcd(a, mod) != 1:
        return None
    else:
        d = mod % a
        q = mod // a
        v.append((v[len(v) - 2] - q * v[len(v) - 1]))
        if d != 0:
            mod, a = a, d
            return inverse_mod(a, mod, v)
        else:
            return v[len(v) - 2]


def miller_rabin(n):
    k = 100
    if n <= 1:
        return False
    if n <= 3:
        return True
    # Розклад n - 1 = 2^s * d, де d непарне
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(k):
        x = random.randint(1, n)
        if gcd(n, x) != 1:
            return False
        xd = pow(x, d, n)
        if xd == 1 or xd == n - 1:
            return True
        for i in range(0, s-1):
            w = (2**i)*d
            if pow(x, w, n) == n-1:
                return True
    return False


def decimal_to_hex(decimal_num):
    decimal_num = int(decimal_num)
    res = hex(decimal_num)
    return res[2:].upper()


def generate_random_prime(bits):
    while True:
        number = random.randint(2**(bits-1), 2**bits - 1)
        if miller_rabin(number):
            return number


def generate_prime_pair(bits):
    p = generate_random_prime(bits)
    q = generate_random_prime(bits)
    p1 = generate_random_prime(bits)
    q1 = generate_random_prime(bits)

    if p*q > p1*q1:
        p, p1 = p1, p
        q, q1 = q1, q

    return p, q, p1, q1


def GenerateKeyPair(p, q):
    n = p*q
    f = (p-1)*(q-1) #ойлера
    e = (2**16) + 1
    if gcd(e, f) != 1:
        return false
    else:
        m = inverse_mod(e, f)
        if m < 0:
            d = m + f
        else:
            d = m
        public_k = (e, n)
        secret_k = (d, n)
        return public_k, secret_k


def Encrypt(key_p, M): #tuple
    e, n = key_p[0], key_p[1]
    C = pow(M, e, n)
    return C


def Decrypt(key_s, C):
    d, n = key_s[0], key_s[1]
    M = pow(C, d, n)
    return M


def Sign(key_s, k):
    d, n = key_s[0], key_s[1]
    S = pow(k, d, n)
    return S


def Verify(k, S, key_p):
    e, n = key_p[0], key_p[1]
    return k == pow(S, e, n)


def SendKey(key_s, key_p):
    e1, n1 = key_p[0], key_p[1]
    k = random.randint(1, 1000)
    k1 = pow(k, e1, n1)
    S = Sign(key_s, k)
    S1 = pow(S, e1, n1)
    return k1, S1, k


def ReceiveKey(key_s, k1, S1, key_p):
    d1, n1 = key_s[0], key_s[1]
    k = pow(k1, d1, n1)
    S = pow(S1, d1, n1)
    check = Verify(k, S, key_p)
    return check


#генерація ключів для А та В
a = generate_prime_pair(256)
Public_A, Secret_A = GenerateKeyPair(a[0], a[1])[0], GenerateKeyPair(a[0], a[1])[1]
Public_B, Secret_B = GenerateKeyPair(a[2], a[3])[0], GenerateKeyPair(a[2], a[3])[1]

print('Keys of A: ')
print('Public_A (e, n): ', Public_A, '\n', 'Secret_A (d, n): ', Secret_A)
print('')
print('Keys of B: ')
print('Public_B (e, n): ', Public_B, '\n', 'Secret_B (d, n): ', Secret_B)
print('')
print('')
#шифрування
print('Encryption')
M_A = random.randint(0, 1000)
M_B = random.randint(0, 1000)
print('Message for B: ', '\n', M_B)
print('Encrypted text by A for B: ', '\n', Encrypt(Public_B, M_B))
print('')
print('Message for A: ', '\n', M_A)
print('Encrypted text by B for A: ', '\n', Encrypt(Public_A, M_A))
print('')
print('')
#розшифрування
print('Decryption')
print('Decrypted text by A from B: ', '\n', Decrypt(Secret_A,  Encrypt(Public_A, M_A)))
print('Origin B`s message : ', '\n', M_A)
print('')
print('Decrypted text by B from A: ', '\n', Decrypt(Secret_B,  Encrypt(Public_B, M_B)))
print('Origin A`s message : ', '\n', M_B)
print('')
print('')
#Протокол конфіденційного розсилання ключів

s1 = SendKey(Secret_A, Public_B)
k1 = s1[0]
S1 = s1[1]
print('----------------------------------------------------------------------------')
print("Keys trading")
print('A generate k1 and  S1', '\n', 'k1: ', k1, '\n', 'S1: ', S1)
print('A sends message (k1, S1) to B ------> B recieved message')
print('B verifies the signature', '\n', 'Has it been verified? ', ReceiveKey(Secret_B, k1, S1, Public_A))
print('')
print('')

s2 = SendKey(Secret_B, Public_A)
k2 = s2[0]
S2 = s2[1]

print('B generate k2 and  S2', '\n', 'k2: ', k2, '\n', 'S2: ', S2)
print('B sends message (k2, S2) to A ------> A recieved message')
print('A verifies the signature', '\n', 'Has it been verified? ', ReceiveKey(Secret_A, k2, S2, Public_B))
print('')
print('')

#перевірка з сервером
e, n, d = Public_A[0], Public_A[1], Secret_A[0]
print('----------------------------------------------------------------------------')
print('Checking using the server')
print('\n Public_A: ')
print('e: ', decimal_to_hex(e), '\n n: ', decimal_to_hex(n))
print('\n Secret_A: ')
print('d: ', d)
#приймаємо відкритий ключ сервера. оскільки він задається в hex, то одразу переводимо його для наших функцій
e_server = int(str(input('Please enter server exponent: ')), 16)
n_server = int(str(input('Please enter server modulus: ')), 16)
public_server = (e_server, n_server)

#розшифровуємо повідомлення від сервера
mess = int(str(input('Encrypted message from server: ')), 16)
print('Decrypted message by A: ', decimal_to_hex(Decrypt(Secret_A, mess)))
print('')
#шифруємо повідомлення для сервера
MM = random.randint(0, 1000)
print('Message for server: ', '\n', decimal_to_hex(MM))
print('Encrypted text by A for server: ', '\n', decimal_to_hex(Encrypt(public_server, MM)))
print('')
#верифікуємо сигнатуру яку отримаємо від сервера
print('Use of verify function')
serverk = int(str(input('Message from server: ')), 16)
serverS =  int(str(input('Signature from server: ')), 16)
print('Verify?', Verify(serverk ,serverS, public_server))
print('')
#створюємо сигнатуру та перевіряємо на сайті
print('Use of sign function')
k = random.randint(0, 1000)
SA = Sign(Secret_A, k)
print('k: ', decimal_to_hex(k))
print('SA: ', decimal_to_hex(SA))
print('Modulus: ', decimal_to_hex(n))
print('Exponent: ', decimal_to_hex(e))
print('')
#приймаємо від сервер ключ та сигнатуру, намагаємось верифікувати
print('Server send key and we try to verify it')
k1s = int(str(input('k from server: ')), 16)
S1s = int(str(input('S from server: ')), 16)
print('A verifies the server signature', '\n', 'Has it been verified? ', ReceiveKey(Secret_A, k1s, S1s, public_server))
print('')
#надсилаємо свій ключ та сигнатуру серверу
print('Sending key and S for server')

while Public_A[1] > public_server[1]:
    a = generate_prime_pair(256)
    Public_A, Secret_A = GenerateKeyPair(a[0], a[1])[0], GenerateKeyPair(a[0], a[1])[1]

print('New keys of A: ')
print('Public_A (e, n): ', '\n e: ', decimal_to_hex(Public_A[0]), '\n n: ', decimal_to_hex(Public_A[1]) )
print('')


sA = SendKey(Secret_A, public_server)
k1A = sA[0]
S1A = sA[1]
kA = sA[2]
print('A generate k1 and  S1', '\n', 'k1: ', decimal_to_hex(k1A), '\n', 'S1: ', decimal_to_hex(S1A))
print('Modulus: ', decimal_to_hex(Public_A[1]))
print('Exponent: ', decimal_to_hex(Public_A[0]))
print('Key (for checking): ', decimal_to_hex(kA))


