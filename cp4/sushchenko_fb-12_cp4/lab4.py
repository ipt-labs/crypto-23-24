import random

log = []


def ext_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = ext_gcd(b % a, a)
        return gcd, y - (b // a) * x, x


def modInverse(num, mod):
    a, b = num, mod
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = divmod(b, a)
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    return x % mod


def miller_rabin(p):
    d = p - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(10):
        x = random.randint(1, p - 1)
        pw = pow(x, d, p)
        if pw == 1 or pw == p - 1:
            continue

        for _ in range(1, s):
            pw = pow(pw, 2, p)
            if pw == p - 1:
                break
        else:
            return False

    return True


def find_primes():
    prime = random.getrandbits(256)
    if prime % 2 == 0:
        prime += 1
    while not miller_rabin(prime):
        log.append(prime)
        prime += 2

    return prime

def gen_pairs():
    p, q, p1, q1 = 0, 0, 0, 0
    while True:
        p = find_primes()
        q = find_primes()
        p1 = find_primes()
        q1 = find_primes()
        if p*q <= p1*q1:
            break
    return p, q, p1, q1


def gen_rsa_keys(p, q):
    n = p*q
    oiler = (p-1)*(q-1)

    while True:
        e = random.randint(2, oiler-1)
        #e = 65537
        if ext_gcd(e, oiler)[0] == 1:
            d = modInverse(e, oiler)
            break

    return (e, n), (d, p, q)


def encrypt(M, e, n):
    return pow(M, e, n)


def decrypt(C, d, n):
    return pow(C, d, n)


def sign(M, Sec_key):
    S = pow(M, Sec_key[0], Sec_key[1]*Sec_key[2])
    return S


def verify(M, S, Pub_key):
    return M == pow(S, Pub_key[0], Pub_key[1])


def send_key(k, Sec_key, Pub_B):
    k1 = encrypt(k, Pub_B[0], Pub_B[1])
    S = sign(k, Sec_key)
    S1 = encrypt(S, Pub_B[0], Pub_B[1])
    print(f"k1: {k1} \nS: {S}\nS1: {S1}")
    return (k1, S1)


def recieve_key(msg, Sec_key, Pub_A):
    k = decrypt(msg[0], Sec_key[0], Sec_key[1]*Sec_key[2])
    S = decrypt(msg[1], Sec_key[0], Sec_key[1]*Sec_key[2])
    check = verify(k, S, Pub_A)
    print(f"k: {k} \nS: {S}\ncheck: {check}")
    return (k, check)


if __name__ == '__main__':
    p, q, p1, q1 = gen_pairs()
    Pub_A, Sec_A = gen_rsa_keys(p, q)
    Pub_B, Sec_B = gen_rsa_keys(p1, q1)

    print("Відкритий ключA (e, n):", Pub_A)
    print("Секретний ключA (d, p, q):", Sec_A)
    print("Відкритий ключB (e, n):", Pub_B)
    print("Секретний ключB (d, p, q):", Sec_B)
    print(f"Кандидати, що не пройшли ({len(log)}):", log[:10])
    M = 4561119
    print("ВТ:", M)
    C = encrypt(M, Pub_A[0], Pub_A[1])
    print("ШТ:", C)
    M = decrypt(C, Sec_A[0], Pub_A[1])
    print("Розшифрований:", M)
    signed = sign(M, Sec_A)
    print("Підпис S:", signed)
    print("Перевірка підпису:", verify(M, signed, Pub_A))
    k = random.randint(0, Pub_A[1])
    print("k:", k)
    msg = send_key(k, Sec_A, Pub_B)
    #print(Pub_B[1] >= Pub_A[1])
    print("Відправлений ключ (k1, S1):", msg)
    print("Отриманий ключ (k, check):", recieve_key(msg, Sec_B, Pub_A))
    print("---------------")
    M = 4561119
    print("ВТ:", hex(M))
    m = 5305960512707629841442515833661084058562762878355119201853129312962340025770214010720538446853744323527655052091932568360456540587057370566022074996520867
    print("m:", hex(m))
    e = 3916586186136903342915117154323316045631285621401634288542736693723028692209679594314837428255383879983135058969049129222249031314517667534786111118003965
    print("e:", hex(e))
    print("ШТ:", hex(encrypt(M, e, m)))
    m = 92786990002988907719652550608980892375635558691369000555109972603867429243781
    e = 65537
    print("---------------")
    print("m:", hex(m))
    print("e:", hex(e))
    print("ШТ:", hex(encrypt(M, e, m)))
    print("---------------")
    M = 1938572304
    print("M:", hex(M))
    S = 2935231723390141546401135832555754721151535406204611218226675084725685207703
    print("S:", hex(S))
    print("Verify:", verify(M, S, (e, m)))
    print("---------------")
    M = 93217509358
    print("M:", hex(M))
    sec_key = (329505922172195841115746731553923783053678201718895159417570805638393840637750743927520556451098736334932075404857751203394250089977717048523234122387429, 40579744356376223807099927945683212405087196913505853242083573676362283328141, 28633471310308254319831997550533605289978359050092793232916603261249542134329)
    pub_key = (968738930756157653593740847055873301390678725793902309393311372256032228229160736505294459230578934731311734961006551135090117119181232722532481230767789, 1161938945807941901442265855219021587743836625195666738881218866797062824626719645259205076783721663340363092805469023189319126755883138946141118607852389)
    S = sign(M, sec_key)
    print("m:", hex(pub_key[1]))
    print("e:", hex(pub_key[0]))
    print("S:", hex(S))
