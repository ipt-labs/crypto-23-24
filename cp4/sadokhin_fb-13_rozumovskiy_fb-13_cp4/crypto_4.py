import random
import hashlib
import string

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"


def ext_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = ext_gcd(b % a, a)
        return (g, y - (b // a) * x, x)


def mod_inverse(a, m):
    g, x, y = ext_gcd(a, m)
    if g != 1:
        return None  # Оберненого елемента не існує
    else:
        return (x % m + m) % m


def trial_division(n):
    if n < 2:
        return False
    for i in range(2, 100):
        if n % i == 0:
            return False
    return True


def is_prime_miller_rabin(n, k=10):
    def find_s_d(n):
        s = 0
        while n % 2 == 0:
            s += 1
            n //= 2
        return s, n

    s, d = find_s_d(n - 1)

    for i in range(k):
        a = random.randint(1, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        else:
            for j in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
                if x == 1:
                    return False
            if x == n - 1:
                continue
            return False

    return True


def generate_random_prime_number(min_value, max_value):
    while True:
        n = random.randint(min_value, max_value)
        if trial_division(n):
            if is_prime_miller_rabin(n):
                return n
        # else:
        #     print(f"Кандидат що не пройшов: {n}")


def decimal_to_binary(decimal_number):
    binary_representation = bin(decimal_number)[2:]
    return binary_representation


def decimal_to_hexadecimal(decimal_num):
    decimal_num = int(decimal_num)
    hexadecimal_num = hex(decimal_num)
    return hexadecimal_num[2:]


def hex_to_decimal(hex_string):
    decimal_result = int(hex_string, 16)
    return decimal_result


def GenerateKeyPair(p, q):
    n = p*q
    totient = (p-1)*(q-1)
    e = random.randint(2, totient - 1)
    (g, x, y) = ext_gcd(e, totient)
    while g > 1:
        e = random.randint(2, totient-1)
        (g, x, y) = ext_gcd(e, totient)
    d = mod_inverse(e, totient)
    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key


def Encrypt(input_text, key, server = False):
    e, n = key
    if server:
        number_decrypted = pow(input_text, e, n)
        number_decrypted = decimal_to_hexadecimal(number_decrypted)
        return number_decrypted
    input_text = int(input_text)
    text_encrypted = pow(input_text, e, n)
    text_encrypted = str(text_encrypted)
    return text_encrypted


def Decrypt(encrypted_text, key, server = False):
    d, n = key
    if server:
        encrypted_text = str(encrypted_text)
        encrypted_text = encrypted_text.lower()
        number_encrypted = hex_to_decimal(encrypted_text)
        number_decrypted = pow(number_encrypted, d, n)
        return number_decrypted
    encrypted_text = int(encrypted_text)
    text_decrypted = pow(encrypted_text, d, n)
    text_decrypted = str(text_decrypted)
    return text_decrypted


def Sign(input_text, my_private_key):
    input_text = str(input_text)
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_text.encode('utf-8'))
    sha256_hash_value = sha256_hash.hexdigest()
    sha256_hash_value = hex_to_decimal(sha256_hash_value)
    hash_encrypted_with_prv = Encrypt(sha256_hash_value, my_private_key)
    print(f"Signature: {hash_encrypted_with_prv}")
    return hash_encrypted_with_prv


def Verify(input_text, sign, public_key):
    hash_decrypted_with_pbl = Decrypt(sign, public_key)
    hash_decrypted_with_pbl = decimal_to_hexadecimal(hash_decrypted_with_pbl)
    print(f"Hash decrypted with public key(signature is verified): {hash_decrypted_with_pbl}")
    sha256_hash_cal = hashlib.sha256()
    sha256_hash_cal.update(input_text.encode('utf-8'))
    sha256_hash_value = sha256_hash_cal.hexdigest()
    print("Hash calculated from received message: ", sha256_hash_value)

    if hash_decrypted_with_pbl == sha256_hash_value:
        return True
    else:
        return False


def create_message_for_abonent(public_key, length, my_private_key):
    characters = string.digits
    random_message = ''.join(random.choice(characters) for i in range(length))
    print("Generated message: ", random_message)
    encrypted_message = Encrypt(random_message, public_key)
    signed_message = Sign(random_message, my_private_key)
    message = (encrypted_message, signed_message)
    return message


def receive_message_from_abonent(message, my_private_key, public_key):
    enc_mes, signed_mes = message
    decrypted_message = Decrypt(enc_mes, my_private_key)
    print("Decrypted message: ", decrypted_message)
    ver_mes = Verify(decrypted_message, signed_mes, public_key)
    if ver_mes:
        print("Whereas decrypted and calculated hashes match, then message isn`t tampered\n")
    else:
        print("Message is tampered by someone\n")


def Send_key(public_key, my_private_key):
    d, n = my_private_key
    k = random.randint(0, n)
    print("Generated secret k: ", k)
    encrypted_message = Encrypt(k, public_key)
    signed_message = Sign(k, my_private_key)
    signed_message_enc = Encrypt(signed_message, public_key)
    message = (encrypted_message, signed_message_enc)
    return message


def Receive_key(message, my_private_key, public_key):
    enc_mes, signed_mes_enc = message
    decrypted_message = Decrypt(enc_mes, my_private_key)
    print(f"\nDecrypted secret key: {decrypted_message}", )
    signed_mes_dec = Decrypt(signed_mes_enc, my_private_key)
    ver_mes = Verify(decrypted_message, signed_mes_dec, public_key)
    if ver_mes:
        print("Whereas decrypted and calculated hashes match, then message isn`t tampered\n")
        return decrypted_message
    else:
        print("Message is tampered by someone\n")



print("TESTING ENCRYPTION AND DECRYPTION WITH REMOTE SERVER ")
print("-------------------------------------------------------------------------------------------------------------------------------------------")

# p = generate_random_prime_number(100000000000000000000000000000000000000000000000000000000000000000000000000000, 555555555555555555555555555555555555555555555555555555555555555555555555555555)
# q = generate_random_prime_number(100000000000000000000000000000000000000000000000000000000000000000000000000000, 555555555555555555555555555555555555555555555555555555555555555555555555555555)
#
# key = GenerateKeyPair(p, q)


# e, d = key
# print(f"Публічний ключ: {e}\nПриватний ключ: {d}\n")
d = (11058555316205224920568872191096426492969296790347658608885681122685334734663331430357821630536321330953081658391505411768097467261175514434084937818933121, 132393294799818189097283724580025322476457628221172300060096806533776543743259878703847004843444809937171904193824003421582514129868174195636919541092830787)
print(d)
# e1, n1 = e
# e1 = decimal_to_hexadecimal(e1)
# n1 = decimal_to_hexadecimal(n1)
# print(e1, n1)

num_enc_hex = "09C53B3C47E187B5963FD1B7D616A4DC73CC5B838DFA8F7899D20ACCD6DD0384124A213A5950AAD92CBD94D018F45A6977BC124DD9DC67CEFD9B977F87FDF1D6DD"
print("Num encrypted in hex: ", num_enc_hex)
num_dec_hex = Decrypt(num_enc_hex, d, True)

print("Num decrypted: ", decimal_to_hexadecimal(num_dec_hex))
print("-------------------------------------------------------------------------------------------------------------------------------------------")







print("Task1-2")
print("-----------------------------------------------------------------------")
p1 = generate_random_prime_number(100000000000000000000000000000000000000000000000000000000000000000000000000000, 555555555555555555555555555555555555555555555555555555555555555555555555555555)
q1 = generate_random_prime_number(100000000000000000000000000000000000000000000000000000000000000000000000000000, 555555555555555555555555555555555555555555555555555555555555555555555555555555)

p2 = generate_random_prime_number(555555555555555555555555555555555555555555555555555555555555555555555555555555, 999999999999999999999999999999999999999999999999999999999999999999999999999999)
q2 = generate_random_prime_number(555555555555555555555555555555555555555555555555555555555555555555555555555555, 999999999999999999999999999999999999999999999999999999999999999999999999999999)

print(f"\nПерша пара простих чисел: p = {p1}\nq = {q1}")
print(f"Довжина p = {len(decimal_to_binary(p1))} bit, q = {len(decimal_to_binary(q1))} bit\n")
print(f"Дурга пара простих чисел: p1= {p2}\nq1 = {q2}")
print(f"Довжина p1 = {len(decimal_to_binary(p2))} bit, q1 = {len(decimal_to_binary(q2))} bit")
print("-----------------------------------------------------------------------\n")


print("Task3")
print("-----------------------------------------------------------------------")
key1 = GenerateKeyPair(p1, q1)
key2 = GenerateKeyPair(p2, q2)

e1, d1 = key1
e2, d2 = key2

print(f"Публічний ключ: {e1}\nПриватний ключ: {d1}\n")
print(f"Публічний ключ1: {e2}\nПриватний ключ1: {d2}")
print("-----------------------------------------------------------------------\n")


print("Task4-5")
print("-----------------------------------------------------------------------")
print("From A to B")
message_from_A = create_message_for_abonent(e2, 30, d1)
print(f"Encrypted message and encrypted signature from A to B: {message_from_A}\n")
receive_message_from_abonent(message_from_A, d2, e1)

print("From B to A")
message_from_B = create_message_for_abonent(e1, 30, d2)
print(f"Encrypted message and encrypted signature from B to A: {message_from_B}\n")
receive_message_from_abonent(message_from_B, d1, e2)

print("Confidential key distribution protocol")
mes = Send_key(e2, d1)
print("Encrypted key and encrypted signature:", mes)
Receive_key(mes, d2, e1)
print("-----------------------------------------------------------------------\n")