import random

invalid_prime_numbers = []

def gcdExtended(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = gcdExtended(b % a, a)
        x, y = y - (b // a) * x, x
        return gcd, x, y

def modInverse(a, m):
    gcd, x, y = gcdExtended(a, m)
    if gcd == 1:
        return (x % m + m) % m
    else:
        return 0  # Повертаємо 0, коли оберненого значення не існує

def miller_rabin_test(p, k):
    if p <= 1 or p % 2 == 0:
        return False  # Відразу відкидаємо парні та негативні числа

    s, d = 0, p - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(k):
        x = random.randint(2, p - 2)
        if gcd(x, p) > 1:
            return False  # p складене

        xr = pow(x, d, p)
        if xr == 1 or xr == p - 1:
            continue

        for _ in range(s - 1):
            xr = pow(xr, 2, p)
            if xr == p - 1:
                break
        else:
            return False  # p складене

    return True  # p сильно псевдопросте за всіма основами

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def random_prime(start, end):
    while True:
        candidate = random.randint(start, end)
        if miller_rabin_test(candidate, 100): # 100 - кількість "раундів"
            return candidate
        else:
            invalid_prime_numbers.append(candidate)

def generate_prime_pairs():
    min_bits = 256  # Мінімальна довжина чисел у бітах
    p = random_prime(2**(min_bits-1)+1, 2**min_bits-1)
    q = random_prime(2**(min_bits-1)+1, 2**min_bits-1)
    p1 = random_prime(2**(min_bits-1)+1, 2**min_bits-1)
    q1 = random_prime(2**(min_bits-1)+1, 2**min_bits-1)

    while p * q > p1 * q1:
        p, q, p1, q1 = p1, q1, p, q

    return p, q, p1, q1

def generate_rsa_keys(p, q):
    # Обчислюємо модуль n
    n = p * q

    # Обчислюємо функцію Ейлера phi(n)
    phi_n = (p - 1) * (q - 1)

    # Вибираємо відкритий ключ e (зазвичай це просте число)
    e = random.randint(2, phi_n - 1)
    while gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)

    # Обчислюємо секретний ключ d за допомогою розширеного алгоритму Евкліда
    d = modInverse(e, phi_n)

    return (n, e), (d, p, q)

def encrypt_message(message, e, n):
    encrypted_message = pow(message, e, n)
    return encrypted_message

def decrypt_message(encrypted_message, d, n):
    decrypted_message_numeric = pow(encrypted_message, d, n)
    return decrypted_message_numeric

def sign_message(message, d, n):
    # Створюємо цифровий підпис повідомлення за секретним ключем
    signature = pow(message, d, n)
    print(f"Цифровий підпис: {signature}")
    return signature

def verify_signature(message, signature, e, n):
    # Перевіряємо цифровий підпис за відкритим ключем
    if message == pow(signature, e, n):
        print("Перевірка цифрового підпису вірна.")
        return True
    else:
        print("Помилка перевірки цифрового підпису.")
        return False

def send_key(k, d_A, n_A, e_B, n_B):
    k_1 = encrypt_message(k, e_B, n_B)
    s = sign_message(k, d_A, n_A)
    s_1 = encrypt_message(s, e_B, n_B)
    print(f"Send_key function: ")
    print(f"k_1: {k_1}")
    print(f"s: {s}")
    print(f"s_1: {s_1}")
    return k_1, s_1

def recive_key(k_1, s_1, d_B, n_B, e_A, n_A):
    k_decrypted = decrypt_message(k_1, d_B, n_B)
    s_decrypted = decrypt_message(s_1, d_B, n_B)
    print(f"Recive_key function: ")
    print(f"k_decrypted: {k_decrypted}")
    print(f"s_decrypted: {s_decrypted}")
    verify_signature(k_decrypted, s_decrypted, e_A, n_A)

p, q, p1, q1 = generate_prime_pairs()

# Генеруємо ключі для абонента A та абонента B
public_key_A, private_key_A = generate_rsa_keys(p, q)
public_key_B, private_key_B = generate_rsa_keys(p1, q1)

# Зберігаємо ключі в змінних для подальшого використання
n_A, e_A = public_key_A
d_A, p_A, q_A = private_key_A

n_B, e_B = public_key_B
d_B, p_B, q_B = private_key_B

print(f"n_A: {n_A}")
print(f"e_A: {e_A}")
print(f"d_A: {d_A}")
print(f"p_A: {p_A}")
print(f"q_A: {q_A}")
print("=======")
print(f"n_B: {n_B}")
print(f"e_B: {e_B}")
print(f"d_B: {d_B}")
print(f"p_B: {p_B}")
print(f"q_B: {q_B}")

print(f"                                             Check for encrypt/decrypt: ")
M = random.randint(0, n_A - 1)
C = encrypt_message(M, e_A, n_A)
M_decrypted = decrypt_message(C, d_A, n_A)
print(f"M: {M}")
print(f"C: {C}")
print(f"M_decrypted: {M_decrypted}")

print(f"                                             Check for sign/virify_sign: ")
S = sign_message(M, d_A, n_A)
print(f"S: {S}")
verify_signature(M, S, e_A, n_A)

print(f"                                             Check for Send/Recive Key: ")
k = random.randint(0, n_A)
print(f"k: {k}")
k_1, s_1 = send_key(k, d_A, n_A, e_B, n_B)
recive_key(k_1, s_1, d_B, n_B, e_A, n_A)

print("\nTest #1:")
# Тест 1: Decryption
server_key_n = 'A299D50551C08C396DB6FD18EFC6D1F29F061B7A09E532572ADDD59748990BC5'
server_key_n = int(server_key_n, 16)  # Перетворюємо рядок в ціле число з базою 16
server_key_e = '10001'
server_key_e = int(server_key_e, 16)  # Перетворюємо рядок в ціле число з базою 16
test1_3_message = 3024878116462861011705203732683992790895339644609381717512023354376027472616 #test_message = random.randint(0, server_key_n - 1)

# Шифруємо повідомлення для сервера
encrypted = hex(encrypt_message(test1_3_message, server_key_e, server_key_n))[2:]
print("server_key_n : ", server_key_n)
print("server_key_e : ", server_key_e)
print("test1_3_message : ", test1_3_message)
print("server_key_n_hex : ", hex(server_key_n)[2:])
print("server_key_e_hex : ", hex(server_key_e)[2:])
print("test1_3_message_hex : ", hex(test1_3_message)[2:].upper())
print("test1_3_message_hex (encrypted) : ", encrypted)
decrypted_by_server = "6B00535258A15CC647C03D9A0EFB399CB5F847044E93384367899313A3182E8"
if(hex(test1_3_message)[2:].upper() == decrypted_by_server):
    print("                                             TEST #1 COMPLETED!")
else:
    print("                                             TEST #1 FAILED!")

print("\nTest #2:")
# Тест 2: Encryption
#Генеруэмо n_test2_4_5, e_test2_4_5 та d_test2_4_5 такі, щоб n_test2_4_5 > server_key_n
n_test2_4_5 = 10236544688920630908733659127201053523952666795702849569064738572394506857359238537273473274621675584210073177730092082623878982352980305106439936466201519
e_test2_4_5 = 8548708261584567102091536396918272265649306769833764159348143686627060716741896190909071080925202509241814596015681645067384665979655190870000929213966279
d_test2_4_5 = 318693226333418535651189478929294389333850536881554094920090930524706901059653540961380457755928320151895849962742541550842429532851011351833978899469479
print("n_test2_4_5 : ", n_test2_4_5)
print("e_test2_4_5 : ", e_test2_4_5)
print("d_test2_4_5 : ", d_test2_4_5)
print("n_test2_4_5_hex : ", hex(n_test2_4_5)[2:])
print("e_test2_4_5_hex : ", hex(e_test2_4_5)[2:])
test2_4_message = 3904883498710813137572740169872784211699685537669784500874517353088765008785075699732306647666267512308709597110656714572561368517837596841463469502402309 #test2_message = random.randint(0, n_test2_4 - 1)
print("test2_4_message : ", test2_4_message)
print("test2_4_message_hex : ",hex(test2_4_message)[2:])
server_ciphertext_hex = "6049D202C5EE86776141527EB255076A432A8C796D87F00C279EF97E4CB061F86EF228977A77D5FC0F723C0733A96C413F332C69EBB61ABF670EBCF2001C2D43"
server_ciphertext = int(server_ciphertext_hex, 16)  # Перетворюємо рядок в ціле число з базою 16
print("server_ciphertext : ", server_ciphertext)
print("server_ciphertext_hex : ",server_ciphertext_hex)
test2_decrypted = decrypt_message(server_ciphertext, d_test2_4_5, n_test2_4_5)
print("Decrypted message from server: ", test2_decrypted)
if(test2_4_message == test2_decrypted):
    print("                                             TEST #2 COMPLETED!")
else:
    print("                                             TEST #2 FAILED!")

print("\nTest #3:")
# Тест 3: Sign
server_test3_signature = "3A4396CA9198896E607F0E843EEADE2D213B4DFE453C62061AE5549876AC980A"
server_test3_signature = int(server_test3_signature, 16)  # Перетворюємо рядок в ціле число з базою 16
print("server_test3_signature: ", server_test3_signature)
print("server_test3_signature_hex: ", hex(server_test3_signature)[2:])
# Перевіряємо підпис (за допомогою публічного ключа сервера)
if verify_signature(test1_3_message, server_test3_signature, server_key_e, server_key_n):
    print("                                             TEST #3 COMPLETED!")
else:
    print("                                             TEST #3 FAILED!")

print("\nTest #4:")
# Тест 4: Verify
signed_test2_4_message = sign_message(test2_4_message, d_test2_4_5, n_test2_4_5)
print("signed_test2_4_message: ", signed_test2_4_message)
print("signed_test2_4_message_hex: ", hex(signed_test2_4_message)[2:])
print("                                             TEST #4 COMPLETED!")

print("\nTest #5:")
# Тест 4: Send key
test5_k1 = "49B58C551918F4479BCF648D66B31425673AB32988F8D9D594C22F525891E8988012E1F9634D92DC213BCD2CFF414279F44B834B624A500221AC6C1B5E2FAD6E"
test5_k1= int(test5_k1, 16)  # Перетворюємо рядок в ціле число з базою 16
test5_s1 = "834BD35D70EBA9E6AC64C3B1F3011FE06A767C0119EEDE390E9C093B296AFD3D1C74CF2F0BFD74487F9F6D8E344449450C24505BC3F20EDBE0E5FA3514E82570"
test5_s1= int(test5_s1, 16)  # Перетворюємо рядок в ціле число з базою 16
print("test5_k1: ", test5_k1)
print("test5_s1: ", test5_s1)
print("test5_k1_hex: ", hex(test5_k1)[2:])
print("test5_s1_hex: ", hex(test5_s1)[2:])
recive_key(test5_k1, test5_s1,  d_test2_4_5, n_test2_4_5, server_key_e, server_key_n)
print("                                             TEST #5 COMPLETED!")

print("\nTest #6:")
# Тест 6: Receive key
#Генеруэмо n_test6, e_test6 та d_test6 такі, щоб n_test6 < server_key_n
n_test6 = 37789472534717841175671899531567148998404644961434738557158556010066982875779
e_test6 = 7448316475413135314314101930182047750256351473044609170788801387148232967249
d_test6 = 3870781795797834802343229346210114294609541564756553406129702208214699568849
print("server_key_n : ", server_key_n)
print("n_test6 : ", n_test6)
print("e_test6 : ", e_test6)
print("d_test6 : ", d_test6)
print("n_test6_hex : ", hex(n_test6)[2:])
print("e_test6_hex : ", hex(e_test6)[2:])
test6_k = 11338394042669456235327899003712550181345410369780192633174635275903401768691 #test6_k = random.randint(0, n_test6)
test6_k1, test6_s1 = send_key(test6_k, d_test6, n_test6, server_key_e, server_key_n)
print("test6_k1_hex : ", hex(test6_k1)[2:])
print("test6_s1_hex : ", hex(test6_s1)[2:])
print("                                             TEST #6 COMPLETED!")

with open("invalid_prime_numbers.txt", 'w') as file:
        file.write(F"Числа, що не пройшли перевірку на простоту: {invalid_prime_numbers}")