import random
import hashlib


def __gcd(a, b):
        u = 0
        u_ = 1
        v = 1
        v_ = 0
        r = b
        r_ = a

        while r != 0:
            q = r_ // r
            r_, r = r, r_ - q * r
            u_, u = u, u_ - q * u
            v_, v = v, v_ - q * v
        return r_, u_, v_


def __random_num(bits_n):
        return int(random.getrandbits(bits_n))


def __bits(n):
        return [int(digit) for digit in bin(int(n))[2:]]


def __horner_pow(a, b, m):
        b_bits = __bits(b)
        y = 1
        for bit in b_bits:
            y = (y ** 2) % m
            y = y * (a ** bit) % m

        return y


def __prime_test(num, k):
        if num == 2 or num == 3: return True
        if num < 5 or num % 2 == 0: return False
        # step 0
        d = num - 1
        s = 0

        while d % 2 == 0:
            d = d // 2
            s += 1

        for _ in range(k):
            # step 1
            a = random.randint(2, num - 1)
            b0 = __horner_pow(a, d, num)
            c = d
            while c != num - 1:
                if b0 == 1 or b0 == num - 1: break;
                b = (b0 ** 2) % num
                if b == 1: return False
                b0 = b
                c = c * 2
            if c == num - 1: return False
        # step 3
        return True


def random_prime(bits_n):
        n = __random_num(bits_n)
        while not __prime_test(n, 150):
            n = __random_num(bits_n)

        return n


def gen_rsa_keys(p, q):
        n = p * q
        o = (p - 1) * (q - 1)

        e = random.randint(2, o - 1)
        a, d, _ = __gcd(e, o)
        while a != 1:
            e = random.randint(2, o - 1)
            a, d, _ = __gcd(e, o)

        d = (d + o) % o
        return [(n, e), (p, q, d)]


def sign(msg, prk):
        p, q, d = prk

        return __horner_pow(msg, d, p * q)


def verify(msg, pbk, signature):
        n, e = pbk
        sgn = __horner_pow(signature, e, n)

        return msg == sgn


def encrypt(msg_encoded, pbk):
        n, e = pbk
        return __horner_pow(msg_encoded, e, n)


def decrypt(msg, prk):
        p, q, d = prk
        n = p * q
        return __horner_pow(msg, d, n)


def send_key(pbk,prk):
    k = random.randint(0,2**128)
    k1 = encrypt(k,pbk)
    s = sign(k,prk)
    s1 = encrypt(s,pbk)

    return (k1,s1,k)


def receive_key(k1, s1, pbk, prk):
    k = decrypt(k1, prk)
    s = decrypt(s1, prk)

    verified = verify(k, pbk, s)

    return k, s, verified

