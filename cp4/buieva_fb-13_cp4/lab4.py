import random

MIN = pow(2, 256 - 1)
MAX = pow(2, 256) - 1
# Task 1 ---------------------------------------------------------------------------------------------------------------
def gorner(X, e, n):
    e, Y = bin(e)[2:], 1
    for i in e:
        Y = (pow(Y, 2)) % n
        if int(i) == 1:
            Y = (X * Y) % n
    return Y

def extended_gcd(a, b):
    if b == 0:
        return a
    else:
        gcd = extended_gcd(b, a % b)
    return gcd

def miller_rabin(n, t=100):
    for _ in range(t):
        a = random.randrange(2, n - 1)
        d = n - 1
        s = 0
        while not d & 1:
            d >>= 1
            s += 1

        if gorner(a, d, n) == 1:
            return True

        for _ in range(s - 1):
            if gorner(a, d, n) == n - 1:
                return True

            d <<= 1
        return False
    return True

def get_random_prime_num(min=MIN, max=MAX):
    p = random.randrange(min, max)
    while not miller_rabin(p):
        # print(f"Кандидат, що не пройшов : {p}")
        p = random.randrange(min, max)
    return p

# Task 2----------------------------------------------------------------------------------------------------------------
def get_pair_pq():
    p, q, p1, q1 = get_random_prime_num(), get_random_prime_num(), get_random_prime_num(), \
                       get_random_prime_num()
    while p * q > p1 * q1:
        p, q = get_random_prime_num(), get_random_prime_num()
    return (p, q, p1, q1)

# Task 3 ---------------------------------------------------------------------------------------------------------------
def generate_rsa_keypair(p, q):
    eiler = (p - 1) * (q - 1)
    e = random.randrange(2, eiler)
    while extended_gcd(e, eiler) != 1:
        e = random.randrange(2, eiler)

    private_key = (pow(e, -1, eiler), p, q)
    open_key = (p*q, e)
    return open_key, private_key

#Task 4 ----------------------------------------------------------------------------------------------------------------
def encrypt (text, open_key):
    n, e = open_key
    encrypted_msg = pow(text, e, n)
    return encrypted_msg

def decrypt (encrypted_text, private_key):
    n = private_key[1]*private_key[2]
    d = private_key[0]
    decrypted_msg = pow(encrypted_text, d, n)
    return decrypted_msg

def sign(text, private_key):
    d, p, q = private_key
    sign = pow(text, d, p*q)
    return sign

def verify (d_text, open_key, sign):
    n, e =open_key
    m = pow(sign, e, n)
    if m == d_text :
        result = True
    else :
        result = False
    return result

#Task 5-----------------------------------------------------------------------------------------------------------------
def send_key(msg, open_key, private_key):
    k1 = encrypt(msg, open_key)
    s = sign(msg, private_key)
    S1 = encrypt(s, open_key)
    return (k1, S1)

def receive_key(message, private_key, open_key):
    k1 = message[0]
    S1 = message[1]
    k = decrypt(k1, private_key)
    S = decrypt(S1, private_key)
    print(f"k : {k}")
    print(f"S : {S}")
    verification = verify(k, open_key, S)
    if verification :
        print("Verification passed")
    else :
        print("Verification failed")
    return k


# result task 2---------------------------------------------------------------------------------------------------
p, q, p1, q1 = get_pair_pq()
print(f"p : {p}, q : {q} \n"
      f"p1 : {p1}, q1 : {q1}")

#result task 3----------------------------------------------------------------------------------------------------
key = generate_rsa_keypair(p, q)
key1 = generate_rsa_keypair(p1, q1)
print("Keys for abonent A :")
print(f"Open key : {key[0]}, Private key : {key[1]}")
print("Keys for abonent B :")
print(f"Open key : {key1[0]}, Private key : {key1[1]}")
#result task 4----------------------------------------------------------------------------------------------------
print("Шифроване та розшифроване повідомлення абонента А :")
msg_A = int("294758203561385694620264389163")
enc_msg_abonent_A = encrypt(msg_A, key[0])
print(f"Encrypted message : {enc_msg_abonent_A}")
dec_msg_abonent_A = decrypt(enc_msg_abonent_A, key[1])
print(f"Decrypted message : {dec_msg_abonent_A}")
print("Абонент А підписав повідомлення :")
signed_msg_A = sign(msg_A, key[1])
print(f"Sign : {signed_msg_A}")
print(f"Перевірка підпису : {verify(dec_msg_abonent_A, key[0], signed_msg_A)}")

print("Шифроване та розшифроване повідомлення абонента B :")
msg_B = int("123456789009478561234882261037")
enc_msg_abonent_B = encrypt(msg_B, key1[0])
print(f"Encrypted message : {enc_msg_abonent_B}")
dec_msg_abonent_B = decrypt(enc_msg_abonent_B, key1[1])
print(f"Decrypted message : {dec_msg_abonent_B}")
print("Абонент B підписав повідомлення :")
signed_msg_B = sign(msg_B, key1[1])
print(f"Sign : {signed_msg_B}")
print(f"Перевірка підпису : {verify(dec_msg_abonent_B, key1[0], signed_msg_B)}")


#result task 5---------------------------------------------------------------------------------------------------------
print("Протокол конфіденційного розсилання ключів :")
msg = send_key(msg_A, key[0], key[1])
receive_key(msg, key[1], key[0])

#check on the website---------------------------------------------------------------------------------------------------
def encode_to_hex(string):
    string = (string.encode('UTF-8'))
    return string.hex().upper()

def decode_from_hex(hex_value):
    return bytes.fromhex(hex_value).decode('UTF-8')

def to_hex(number):
    hex_number = hex(number)[2:].upper()
    return hex_number

def hex_to_dec(hexademical):
    int_number = int(hexademical, 16)
    return int_number
msg =  "1234567890987654321"
n = '928E61C43B9A616D847929C5A498B3539876EA46C44B79EC33FF0BB5735CFEC5'
e = '10001'
server_open_key = [hex_to_dec(n), hex_to_dec(e)]
my_open_key = (4178685425524312053720104210785097143635902791520708522186003596957546466392875611663024405853992857129264996756475519469644331978063724511893986018188747, 471887327704095733587143550644734197521842452922882174147451320859706905840932442230043315611930517517452027898849360083450965270415183985166781167392623)
my_private_key = (3616869444164329807408472851411343271502636250971991184217426122063740468002733777571267052397686024250441499410201673209051208045434131191248059586090255, 67337831522651165910261649599383299944654806434471370377422193230691678058249, 62055538930128478309597233526565092488061985532166655828712042833494075486003)
print(f"m : {to_hex(my_open_key[0])}")
print(f"e : {to_hex(my_open_key[1])}")
enc = encrypt(hex_to_dec(encode_to_hex(msg)),my_open_key)
print('enc= ',to_hex(enc))
# decryption
encrypted = encrypt(hex_to_dec(encode_to_hex(msg)),server_open_key)
print('Encrypted for server = ',to_hex(encrypted))
# sign
site_sign = '6E4455FF669CEDF6BEDC382E94410CC3847764FF8B13DBC194CE44CDBF45AAD6'
print(verify(hex_to_dec(encode_to_hex(msg)), server_open_key, hex_to_dec(site_sign)))
my_sign = sign(hex_to_dec(encode_to_hex(msg)),my_private_key)
print("My sign = ",to_hex(my_sign))



