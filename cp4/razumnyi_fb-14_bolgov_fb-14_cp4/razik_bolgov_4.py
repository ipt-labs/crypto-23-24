import random

trivial_prime = [2, 3, 5, 7, 11, 13, 17, 19, 23,
                 29, 31, 37, 41, 43, 47, 53, 59,
                 61, 67, 71, 73, 79, 83, 89, 97]


def gcd_(a, b):
    """ Euclid algorithm to find gcd """

    if a == 0:
        return b, 0, 1

    gcd, v1, u1 = gcd_(b % a, a)
    u = u1 - (b // a) * v1
    v = v1

    return gcd, u, v


def find_reverse_a(a, m):
    """ Find a**-1 mod m """

    g, x, y = gcd_(a, m)

    if g != 1:
        return None
    else:
        return x % m


def solve_linear_congruence(a, b, m):
    """ Solve ax = b mod(m) """

    gcd, x, y = gcd_(a, m)

    if not b % gcd == 0:
        return []
    else:
        a = a // gcd
        b = b // gcd
        m = m // gcd

        x = b * find_reverse_a(a, m) % m
        solutions = [(x + m * k) for k in range(gcd)]  # x_formula = x + m*k, k є Z

        return solutions


def euler_phi(n):
    """ Calculate φ(n) """

    result = n
    p_ = 2

    while p_ * p_ <= n:
        if n % p_ == 0:
            while n % p_ == 0:
                n //= p_
            result -= result // p_
        p_ += 1
    if n > 1:
        result -= result // n

    return result


def horny_power(x, y, mod):
    """ Horner scheme for finding (x**y) mod m """

    result = 1

    while y > 0:
        if y % 2 == 1:
            result = (result * x) % mod
        x = (x * x) % mod
        y //= 2

    return result


def if_prime_trial_div(n):
    """ Check if the number is prime using trial division """

    global trivial_prime

    if n < 2:
        return False
    for i in trivial_prime:
        if n % i == 0:
            return False
    return True


def if_prime_mil_rab(p_, k):
    """ Check if the number is prime using Miller-Rabin algorithm """

    if p_ == 2 or p_ == 3:
        return True
    if p_ % 2 == 0:
        return False

    s, d_ = 0, p_ - 1
    while d_ % 2 == 0:
        s += 1
        d_ //= 2

    for _ in range(k):
        a = random.randint(2, p_ - 2)
        x = horny_power(a, d_, p_)

        if x == 1 or x == p_ - 1:
            continue

        for _ in range(s - 1):
            x = horny_power(x, 2, p_)
            if x == p_ - 1:
                break
        else:
            return False
    return True


def generate_prime(bits=256, k=20, interval=False):
    """ Generate a random number of specific (256) bit """

    if interval:
        candidate = random.randint(10 ** 77, int("9" * 78))
    else:
        candidate = random.getrandbits(bits)
        candidate |= (1 << bits - 1) | 1

    if if_prime_trial_div(candidate):
        if if_prime_mil_rab(candidate, k):
            return candidate
        else:
            return generate_prime(bits, k, interval=interval)
    else:
        return generate_prime(bits, k, interval=interval)


def generate_p_q(bits=256, interval=False):
    """ Generate (p, q) and (p_1, q_1) which are suitable """

    p_ = generate_prime(bits, 20, interval=interval)
    q_ = generate_prime(bits, 20, interval=interval)
    p_1_ = generate_prime(bits, 20, interval=interval)
    q_1_ = generate_prime(bits, 20, interval=interval)

    while p_ * q_ > p_1_ * q_1_:
        print(f"These candidates are invalid:\np = {p_}\nq = {q_}\np_1 = {p_1_}\nq_1 = {q_1_}")
        return generate_p_q(interval=interval)

    return p_, q_, p_1_, q_1_


def GenerateKeyPair(p_, q_):
    """ Generate key-pair for a user """

    n_ = p_ * q_
    phi = (p_ - 1) * (q_ - 1)
    # e_ = random.randint(2, phi - 1)
    e_ = 2**16+1
    while gcd_(e_, phi)[0] != 1:
        e_ = random.randint(2, phi - 1)

    d_ = find_reverse_a(e_, phi)

    return (d_, p_, q_), (n_, e_)


def Encrypt(M_, pubkey):
    """ Encrypt valid message using C = (M**e) mod n formula """

    if not isinstance(M_, int):  # convert str to int
        M_ = int.from_bytes(M_.encode('utf-8'), byteorder='big')

    if 0 <= M_ <= pubkey[0] - 1:
        C_ = horny_power(M_, pubkey[1], pubkey[0])
        return C_
    else:
        return None


def Decrypt(C_, privkey, text=False):
    """ Decrypt valid message using M = (C**d) mod n """

    n_ = privkey[1] * privkey[2]

    if 0 <= C_ <= n_ - 1:
        M_ = horny_power(C_, privkey[0], n_)

        if text:
            return M_.to_bytes((M_.bit_length() + 7) // 8, byteorder='big').decode('utf-8')
        else:
            return M_
    else:
        return None


def Sign(M_, privkey):
    """ A digital signature for a message """

    if not isinstance(M_, int):  # convert str to int
        M_ = int.from_bytes(M_.encode('utf-8'), byteorder='big')

    S_ = horny_power(M_, privkey[0], privkey[1] * privkey[2])

    return (M_, S_)


def Verify(signature, pubkey):
    """ Verify the signed message """

    M_ = signature[0]
    S_ = signature[1]

    if not isinstance(M_, int):
        M_ = int.from_bytes(M_.encode('utf-8'), byteorder='big')

    M__ = horny_power(S_, pubkey[1], pubkey[0])

    return M_ == M__


def SendKey(k_, pubkey_a, privkey_a, pubkey_b):
    """ Send keys using public pipe """

    # k_1_ = horny_power(k_, pubkey_b[1], pubkey_b[0])
    k_1_ = Encrypt(k_, pubkey_b)

    # S_ = horny_power(k_, privkey_a[0], pubkey_a[0])
    S_ = Sign(k_, privkey_a)

    # S_1_ = horny_power(S_, pubkey_b[1], pubkey_b[0])
    # S_1_ = horny_power(S_[1], pubkey_b[1], pubkey_b[0])
    S_1_ = Encrypt(S_[1], pubkey_b)

    return (k_1_, S_1_)


def ReceiveKey(received, privkey_b, pubkey_a):
    """ Receive keys using public pipe """

    k_1_ = received[0]
    S_1_ = received[1]

    # k_ = horny_power(k_1_, privkey_b[0], pubkey_b[0])
    k_ = Decrypt(k_1_, privkey_b)

    # S_ = horny_power(S_1_, privkey_b[0], pubkey_b[0])
    S_ = Decrypt(S_1_, privkey_b)

    # k_a = horny_power(S_, pubkey_a[1], pubkey_a[0])
    # if k_ == k_a:
    #     return (k_, S_)
    # else:
    #     print("k could not be verified")
    #     return None

    if Verify((k_, S_), pubkey_a):
        print("k is verified")
        return (k_, S_)
    else:
        print("k could not be verified")
        return None


if __name__ == "__main__":

    # Generate p q, p_1 q_1 which are valid
    p, q, p_1, q_1 = generate_p_q(bits=256, interval=False)
    print(f'p * q <= p_1 * q_1 is {p * q <= p_1 * q_1}')
    print(f"p = {p} \nq = {q}")
    print(f"p_1 = {p_1} \nq_1 = {q_1}")
    print(f"len of p_1 = {len(bin(p_1)[2:])} \nlen of q_1 = {len(bin(q_1)[2:])}")

    # static examples
    # for user A
    p = 62292051873732111696239942114403170513866646571234155956926929905487334616531
    q = 107856527211449048964097072747761105850090651956211176122828103303232450011733
    print(f"p = {p} \nq = {q}")
    print(f"len of p = {len(bin(p)[2:])} \nlen of q = {len(bin(q)[2:])}\n")

    # for user B
    p_1 = 102212875132880649877270819301141701576819197983714203788291325382307197654689
    q_1 = 79788335472330262274200476827445331604017075565917214625517614772660663877009
    print(f"p_1 = {p_1} \nq_1 = {q_1}")
    print(f"len of p_1 = {len(bin(p_1)[2:])} \nlen of q_1 = {len(bin(q_1)[2:])}")

    print(f"p * q <= p_1 * q_1 is {p * q <= p_1 * q_1}")  # for this case return True

    ############################ Generate keys

    keys_a = GenerateKeyPair(p, q)
    keys_b = GenerateKeyPair(p_1, q_1)

    public_key_a = keys_a[1]
    private_key_a = keys_a[0]

    public_key_b = keys_b[1]
    private_key_b = keys_b[0]

    print(f"pubkey a: {public_key_a}")  # (n ,e)
    print(f"privkey a: {private_key_a}")  # (d, p, q)
    print(f"pubkey b: {public_key_b}")  # (n ,e)
    print(f"privkey b: {private_key_b}")  # (d, p, q)

    d = private_key_a[0]
    d_1 = private_key_b[0]
    print(f"d = {d}")
    print(f"d_1 = {d_1}")

    ###################################### Test encryption and decryption, sign and verify
    M = random.randint(1, 25000)

    # print(M)
    M = 'Hello Mario'
    print(M)

    cryptogram_a = Encrypt(M, public_key_b)  # A encrypts for B
    cryptogram_b = Encrypt(M, public_key_a)  # B encrypts for A

    print(f"This is cryptogram for A using pubkey B: {cryptogram_a}")
    print(f"This is cryptogram for B using pubkey A: {cryptogram_b}")

    open_a = Decrypt(cryptogram_b, private_key_a, text=True)  # A decrypts from B
    open_b = Decrypt(cryptogram_a, private_key_b, text=True)  # B decrypts from A

    print(f"This is decrypted for A using privkey A: {open_a}")
    print(f"This is decrypted for B using privkey B: {open_b}")

    signed_a = Sign(M, private_key_a)
    signed_b = Sign(M, private_key_b)

    print(f"This is signed A: {signed_a}")
    print(f"This is signed B: {signed_b}")

    print(f"Verification of A is {Verify(signed_a, public_key_a)}")
    print(f"Verification of B is {Verify(signed_b, public_key_b)}")

    ################################################# Test sending and receiving keys

    k = random.randint(0, public_key_a[0])

    print(f"This is k: {k}")
    k_encrypted = Encrypt(k, public_key_a)
    print(f"This is k_encrypted to send: {k_encrypted}")
    k_sign = Sign(k, private_key_a)
    print(f"This is k_sign by user A: {k_sign}")

    a = SendKey(k, public_key_a, private_key_a, public_key_b)
    print(f"This is sent by A: {a}")

    b = ReceiveKey(a, private_key_b, public_key_a)
    print(f"This is received by B: {b}")

    b_verify = Verify(k_sign, public_key_a)
    print(f"The verification of k_sign for user B is: {b_verify}")


    ############################################

    #1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1 Test website features

    """ How to perceive our keys:
    
    pubkey (n, e): n - modulus, e - exponent
    privkey (d, p, q)
    
    """
    p, q, p_1, q_1 = generate_p_q(bits=128, interval=False)

    # static examples
    p = 181207594698208181078258173571185530019
    q = 295474412342678748021019178493214795663

    keys_a = GenerateKeyPair(p, q)

    public_key_a = keys_a[1]
    private_key_a = keys_a[0]

    pubkey_serv = (int("AD32E0612BF9A008D477B3577954200347BBB1BF7A95A05AAC6E647597D528FB", 16), int("10001", 16))
    message = 'Hello Mario'

    ciphertext_serv = (int("21C65A58CAF2261744EED65089444287B5EF86F759C9A1012A15AECDBEDBAD35", 16))
    ciphertext_our = Encrypt(message, pubkey_serv)

    print(f"ciphertext encrypted by server: {ciphertext_serv}\nciphertext encrypted by us: {ciphertext_our}")

    print(hex(15276783273093125926050098888444103147478315780042180554430612431664079154485))  # for server to decrypt

    print(f"pubkey a: {public_key_a}")  # (n ,e)
    print(f"privkey a: {private_key_a}")  # (d, p, q)

    print()

    print(f'pubkey a in hex: {hex(public_key_a[0]), hex(public_key_a[1])}')
    print(f'privkey a in hex: {hex(private_key_a[0]), hex(private_key_a[1]), hex(private_key_a[2])}')

    decrypted_with_ours = Decrypt(int("75985089BE1004238206DDDF5D32AD4828B8CBB0F0E1020C1B6A8174E47CA735", 16),
                                  private_key_a, text=True)

    print(decrypted_with_ours)

    signed = (message, int("93F348EB1AABA82D622607BB7C8726E40DE24658146B59D0F757737C18BA90DA", 16))

    verified = Verify(signed, pubkey_serv)

    print(verified)

    generated_sign = Sign(message, private_key_a)
    print(hex(generated_sign[1]))

    k = int("5A338EC013E364F20E7E7D09DB62B54EBC18DAB3103C592EE0832306FE93DB6A", 16)
    print(k)
    S = int("3FEBECC84ADC81FE2082B3DFBE6C642672D934B57329B7FDF66D2D00A42E5D87", 16)

    received = ReceiveKey((k, S), private_key_a, pubkey_serv)

    print(hex(received[0]), hex(received[1]))

    sent = SendKey(message, public_key_a, private_key_a, pubkey_serv)
    print(hex(sent[0]), hex(sent[1]))
    
    key_ = 0x48656C6C6F204D6172696F

    print(key_.to_bytes((key_.bit_length() + 7) // 8, byteorder='big').decode('utf-8'))