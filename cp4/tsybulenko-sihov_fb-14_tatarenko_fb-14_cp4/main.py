from random import randint, getrandbits

def generate_prime(lenn = 256, start = None, end = None):

    while True:
        if start and not end:
            raise ValueError("You must provide both 'start' and 'end'")
        elif not start and end:
            raise ValueError("You must provide both 'start' and 'end'")
        elif start and end:
            candidate = randint(start, end)
        else:
            candidate = getrandbits(lenn)

        if try_division(candidate):
            if is_prime_miller_rabin(candidate):
                return candidate

def horner(x, power, mod):

    result = 1
    while power > 0:
        if power % 2 == 1:
            result = (result * x) % mod
        x = (x * x) % mod
        power //= 2

    return result

def try_division(n):

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    for i in primes:
        if n // i == 0:
            return False
    return True

def is_prime_miller_rabin(p, k=10):

    if p == 2 or p == 3:
        return True
    if p % 2 == 0 or p == 1:
        return False

    s, d = 0, p - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    # Кроук 0, 1
    for _ in range(k):
        a = randint(2, p - 2)
        # Кроук 2
        x = horner(a, d, p)
        if x == 1 or x == p - 1:
            for r in range(s - 1):
                x = horner(x, 2, p)
                if x == p - 1:
                    break
        else:
            return False  # n - складене
    return True  # n - просте

def get_prime_pairs():
    while True:
        p1 = generate_prime()
        q1 = generate_prime()
        p2 = generate_prime()
        counter = 0
        while counter < 5:
            q2 = generate_prime()
            if p1 * q1 // p2 < q2:
                return p1, q1, p2, q2
            print(f"Не пройшов q2 - {q2}")
            counter += 1
        print(f"Не пройшли:\n p1 - {p1}\n q1 - {q1}\n p2 - {p2}")

def GenerateKeyPair(p, q):
    n = p * q
    euler = (p - 1) * (q - 1)
    while True:
        e = randint(2, euler - 1)
        if gcd(e, euler) == 1:
            break
    d = invert(e, euler)
    return [d, p, q], [e, n]

def gcd(a, b):
    while(b):
       a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def invert(a, m):
    g, x, _ = extended_gcd(a, m)

    if g == 1:
        return x % m

def Encrypt(M, pubkey):
    if not isinstance(M, int):
        M = int.from_bytes(M.encode('utf-8'), byteorder='big')
    return horner(M, pubkey[0], pubkey[1])

def Decrypt(C, prkey, text=False):
    M = horner(C, prkey[0], prkey[1] * prkey[2])
    if text:
        return M.to_bytes((M.bit_length() + 7) // 8, byteorder='big').decode('utf-8')
    else:
        return M

def Sign(M, prkey):
    if not isinstance(M, int):
        M = int.from_bytes(M.encode('utf-8'), byteorder='big')
    return (M, horner(M, prkey[0], prkey[1] * prkey[2]))

def Verify(kS, pubkey):

    if not isinstance(kS[0], int):
        kS[0] = int.from_bytes(kS[0].encode('utf-8'), byteorder='big')
    sign = horner(kS[1], pubkey[0], pubkey[1])
    # print(sign)
    return sign == kS[0]

def SendKey(k, pr_key_a, pub_key_b):
    k1 =  Encrypt(k, pub_key_b)
    S = Sign(k, pr_key_a)
    S1 = Encrypt(S[1], pub_key_b)
    return [k1, S1]


def RecieveKey(msg, pr_key_b, pub_key_a):
    k1 = msg[0]
    S1 = msg[1]

    k = Decrypt(k1, pr_key_b)
    S = Decrypt(S1, pr_key_b)

    if Verify([k, S], pub_key_a):
        print("k is verified")
        return k
    else:
        print("k is NOT verified")
        return None


if __name__ == "__main__":

    p1, q1, p2, q2 = get_prime_pairs()
    pr_key_a, pub_key_a  = GenerateKeyPair(p1, q1)
    pr_key_b, pub_key_b = GenerateKeyPair(p2, q2)
    print(f"p = {p1}\n"
          f"q = {q1}\n"
          f"Public key A: {pub_key_a}\n"
          f"Private key A: {pr_key_a}\n"
          f"p = {p2}\n"
          f"q = {q2}\n"
          f"Public key B: {pub_key_b}\n"
          f"Private key B: {pr_key_b}")

    # ============================== Static test ==============================
    print("A is sending k to B ...")
    k = randint(0, 1000)
    print(f"k = {k}")
    msg = SendKey(k, pr_key_a, pub_key_b)
    print(f"(k1, S1): {msg}")
    print("B receives k from A ...")
    rec_k = RecieveKey(msg, pr_key_b, pub_key_a)
    print(f"Received k = {rec_k}")

    # ============================== Server =====================================
    print("\n\n============ Server testing ============")

    static_pub_a = [1230690436486742605955483905417004293863344386960894259738264369698059363901632496390551421167324290816844912655712779264726563350685213300292594310015573, 4627594997100633657789449053303746917566045828504651681708806865953057852413669825592408036808912872419362322077666239142654185893871838265485472817142673]
    static_pr_a = [2397013581942836437048449750615206678116228106429442358853285562791574132147781110817166312153830607578774150129424351394831355063236287955106174893990653, 50308006593981080820863088049073605520611173756414089560774450852748306251859, 91985258617945030942308640685119267525719642224500691729972303113880023156747]
    static_pub_b = [3446855684120996316501967256937452334515160993292507206509730219840778528621320836610613907417924366645154226621998915387365521245975938007921220083549919, 6279464609120981212780550085261209136400116364102245437920884959276857079640151429241561173246499655220098149287759791242962531984963582035536214624922361]
    static_pr_b = [5094541903339229875976644817980376164777698738613455355945165516399842666726331355076592488397059441173227615490276414923813961533927273931511492246058159, 58332525169232218901723450180189779848660428123017026800225133084023650700339, 107649456129375933725524942972514471405206550907670365682798737923055385739299]

    serv_pub_key = [int('10001', 16),int('A277F4A3E5EBC9B7B113F4B75FFCEB7238A8CC7DA117D082E258035C634687616CBF255575ED225FE194D904E0D91001CD7784EABCE662B94F7DE461A8B2EE1B',16)]

    # ==== Decryption test (server encrytion) ====
    print("\n==== Decryption test (server Encrytion) ====")
    our_pub_e, our_pub_n = hex(static_pub_a[0]), hex(static_pub_a[1])
    print(f"e = {our_pub_e}\nn = {our_pub_n}")

    serv_msg = int("0D1801344AC617BC141EE2320E8937A116EA08D908F68E4D9C3EAF1E2E63F755FB09439443CB54DCBDDBE49D214A90851E630A958E03788D8152CCF7D0C12B2F", 16)
    msg = Decrypt(serv_msg, static_pr_a)
    print(f"received msg: {msg}, {(hex(msg))}")

    # ==== Encryption test (server Decrytpion) ====
    print("\n==== Encryption test (server Decrytpion) ====")
    k = randint(2, 100)
    print(f'Sending k: {k}, {hex(k)}')
    k_encr = Encrypt(k, serv_pub_key)
    print(f'Ciphertext:({hex(k_encr)}')

    # ==== Verificaton test (Server Sign) ====
    print('\n==== Verificaton test (Server Sign) ====')
    k = int('34', 16)
    ks = [k, int("64BC8ABD92842CE0B5AF807E2C4E7C71D56D9751B20422B81FE2EB765068DCC4F116C633FAA7F8B5F90690B6816DC1933E6B7A7842B671BD38E4C04A6A5A24F9", 16)]
    if Verify(ks, serv_pub_key):
        print("k is verified")
    else:
        print("k is NOT verified")

    # ==== Sign test (Server Verification) ====
    print('\n==== Sign test (Server Verification) ====')
    k = 77
    k, S = Sign(k, static_pr_a)
    print(f'Message:    {k} ({hex(k)})')
    print(f'Siganture:  {hex(S)}')
    print(f'Modulus :   {hex(static_pub_a[1])}')
    print(f'Public exponent:    {hex(static_pub_a[0])}')

    # ==== SendKey test (Server ReceiveKey) ====
    print("\n==== SendKey test (Server ReceiveKey) ====")
    k = 59
    print(f'k : {k}, ({hex(k)})')
    k1S1 = SendKey(k, static_pr_a, serv_pub_key)
    print(f'Key :       {hex(k1S1[0])}')
    print(f'Signature : {hex(k1S1[1])}')
    print(f'Modulus :   {hex(static_pub_a[1])}')
    print(f'Public exponent:    {hex(static_pub_a[0])}')

    # ==== ReceiveKey test (Server SendKey) ====
    print("\n==== ReceiveKey test (Server SendKey) ====")
    print(f'Modulus :   {hex(static_pub_a[1])}')
    print(f'Public exponent:    {hex(static_pub_a[0])}')
    k1 = int("0E2DC499494214202C08E3D0DE38FE7D6309D158DE5D5802B3B7F58F38278A279DA8CBB7100D98F73C730E70F629120551FBE388786B67BAD123AB518597447E", 16)
    S1 = int("399BF5B0E8A5F96555DC7BF688A2408FF8CBF2E42DD21257271B13713C1ABAB17B101873B1B7D8AF2E08CE85540A55624B360DBEC2D19E7E38EEAEA474C75608", 16)
    msg = [k1, S1]
    k = RecieveKey(msg, static_pr_a, serv_pub_key)
    print(f"k : {k}")
