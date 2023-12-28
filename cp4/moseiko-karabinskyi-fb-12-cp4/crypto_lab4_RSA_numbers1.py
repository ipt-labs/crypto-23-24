import random
import secrets
def decimalToBinary(decimal):
    binary = []
    while decimal > 0:
        binary.insert(0, decimal % 2)
        decimal //= 2
    return binary if binary else [0]

def d_2s(p):
    s = 0
    while p % 2 == 0:
        s += 1
        p //= 2
    return s, p

def extended_gcd_2(a, b):
    old_r, r = a, b
    x, s = 1, 0
    y, t = 0, 1
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        x, s = s, x - quotient * s
        y, t = t, y - quotient * t
    gcd = old_r
    return (gcd, x, y)

def LongModPowerBarrett(A, B, N):
    if N == 1:
        return 0

    result = 1
    A = A % N
    while B > 0:
        if B % 2 == 1:
            result = (result * A) % N

        B = B // 2
        A = (A * A) % N

    return result

def miller_rabin(p, k=20):
    s, d = d_2s(p - 1)
    for _ in range(k):
        x = random.randint(2, p - 2)
        gcd, _, _ = extended_gcd_2(x, p)
        if gcd > 1:
            return False
        else:
            l = LongModPowerBarrett(x, d, p)
            if l != 1 and l != p - 1:
                for r in range(1, s):
                    xr = LongModPowerBarrett(x, d * 2**r, p)
                    if xr == p - 1:
                        break
                else:
                    return False
    return True

def find_p():
    while True:
        p = secrets.randbits(256)
        if miller_rabin(p, k=20):
            return p

def find_q():
    while True:
        q = secrets.randbits(256)
        if miller_rabin(q, k=20):
            return q

def inverse(a, m):
    gcd, x, y = extended_gcd_2(a, m)
    if gcd != 1:
        return None
    else:
        return x % m

def congurence(a, b, m):
    gcd, x, y = extended_gcd_2(a,m)
    if b % gcd !=0:
        return 0

    find_x = inverse(a//gcd, m//gcd) * (b//gcd) % (m//gcd)
    return find_x

def gen_pp_qq1():
    p = find_p()
    q = find_q()
    p1 = find_p()
    q1 = find_q()
    while p*q >= p1*q1:
        return(gen_pp_qq1())
    return p,q,p1,q1



def GenerateKey(p, q):
     n = p * q
     fn = (p-1)*(q-1)
     e = 2**16 + 1
     d = congurence(e, 1, fn)
     return p, q, n, e, d

def modular_pow(base, e, mod):
    result = 1
    base = base % mod

    while e > 0:
        if e % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        e //= 2

    return result


def encrypt_rsa(message, public_key):
    n, e = public_key
    if type(message) == str:
        message = encode(message)
    return modular_pow(message, e,n)


def decrypt_rsa(message, secret_key,text_or_dec):
    d = secret_key[2]
    p = secret_key[0]
    q = secret_key[1]
    n = p * q
    message = modular_pow(message, d, n)
    if text_or_dec == 'text':
        return decode(message)
    else:
        return message



def signature(message, secret_key):
    d = secret_key[2]
    p = secret_key[0]
    q = secret_key[1]
    n = p * q
    if type(message) == str:
        message_enc = encode(message)
        msg = modular_pow(message_enc, d, n)
    else:
        msg = modular_pow(message, d, n)
    return msg



def verify_sign(sign_mes, message, public_key):
    original_msg_bytes = message
    n, e = public_key
    tst = modular_pow(sign_mes, e, n)
    if type(message) == str:
        original_msg_bytes = encode(message)
    return tst == original_msg_bytes

def send_key(prvt_key_A, public_key_b, msg):
    k1 = encrypt_rsa(msg, public_key_b)
    S = signature(msg, prvt_key_A)
    S1 = encrypt_rsa(S, public_key_b)
    return k1,S1

def recieve_key(prvt_key_B, public_A, k1, S1):
    k = decrypt_rsa(k1, prvt_key_B, 'integer')
    S = decrypt_rsa(S1, prvt_key_B, 'integer')
    if  verify_sign(S, k, public_A) == False:
        raise TypeError("cant verify signature")
    else:
        return k,S

def encode(plain_text):
    return int.from_bytes(plain_text.encode('utf-8'), 'big')

def decode(encoded):
    return encoded.to_bytes((encoded.bit_length()+7) // 8, 'big').decode('utf-8')
print()

qqq = gen_pp_qq1()
print(f"Згенеровані числа p і q для користувача A: \np={qqq[0]} \nq={qqq[1]}")
print("\n")
print(f"Згенеровані числа p1 і q1 для користувача B: \np1={qqq[2]} \nq1={qqq[3]}")
print("\n")
p, q, n, e, d = GenerateKey(qqq[0], qqq[1])
p1, q1, n1, e1, d1 = GenerateKey(qqq[2], qqq[3])
open_key_A = (n, e)
open_key_B = (n1, e1)
secret_key_A = (p,q,d)
secret_key_B = (p1,q1,d1)
print("Відкритий ключ А", open_key_A)
print("Відкритий ключ B", open_key_B)
print("Таємний ключ А", secret_key_A)
print("Таємний ключ B", secret_key_B)
print("\n")

#Завдання 4 користувач A
Message = 'hello lab4'
msg_type = 'text'
encrypted_message_A = encrypt_rsa(Message,  open_key_A)
e_sign_A = signature(Message, secret_key_A)
print("Оригінальне повідовлемення користувача A:", Message)
print("Закодоване повідомлення користувачем A: ", encrypted_message_A)
print("Повідомлення підписане цифровим підписом користувача A",e_sign_A)
print("розкодоване повідомлення користувача A", decrypt_rsa(encrypted_message_A, secret_key_A, msg_type))
print("Перевірка цифрового підпису користувача A, цифровий підпис вірний??? ==", verify_sign(e_sign_A, Message, open_key_A))
print("хекс значення відкритого ключа A", hex(n))
print("хекс значення закодованого повідомлення", hex(encrypted_message_A))

print("\n")

#Завдання 4 користувач B
Message_2 = 'your'
encrypted_message_B = encrypt_rsa(Message_2,  open_key_B)
e_sign_B = signature(Message_2, secret_key_B)
print("Оригінальне повідовлемення користувача B:", Message_2)
print("Закодоване повідомлення користувачем B: ", encrypted_message_B)
print("Повідомлення підписане цифровим підписом користувача B",e_sign_B)
print("розкодоване повідомлення користувача B", decrypt_rsa(encrypted_message_B, secret_key_B, msg_type))
print("Перевірка цифрового підпису користувача B, цифровий підпис вірний??? ==", verify_sign(e_sign_B, Message_2, open_key_B))
#Звдання 5

#print(decrypt_rsa(int("069B8C35792CF3BE2B20688AFE1ACB1646D033862B0B036CA97049A25A9BE35492314E07D0D9C63299281EBAFBAA54AF52B9F8151CBE67AA5D4AC9E4076C8A57", 16), (25885032199362110136563390237314758407507842553587929606344203556051567283313, 60309617786895935430487693515284005771121303011227794353379094104664510721817, 630144394797125928184734966161232222262163418584321928850949735421050962746390854316963071489256753337406921485316432698138881779811797117753093898708737), 'text'))
gen_message = random.randint(1,  open_key_A[0])

k1, S1 = send_key(secret_key_A, open_key_B, gen_message)
print("закодований ключ:", k1)
print("закодований підпис:", S1)
print("\n")
k, S = recieve_key(secret_key_B, open_key_A, k1, S1)
print("декодований ключ:", k)
print("декодований підпис:", S)
print("\n")
#Перевірка на сайті
#Завдання 1 decrypt
encrypted_hex = "759D45E794DF6B83C6B9E350E328BF54EB62B70E9CA301A6D5012967D6AF906E99311B2543BE558BA8BD613A3E21D2289A9867D54FD5F7707B288C4C3AF83F"
prv_key = (77000727766915613692786033325637612867113956129398433538854106165276803537433, 1524306868158978166934791472082457035704546613697452758871792947151835510421, 50647741519546448467726053613022965046388372319712948195480205914166565453678195847813747163542620188574742925957946826671064498867729123714425043747073)
print("decrypted message:", decrypt_rsa(int(encrypted_hex, 16), prv_key, 'text'))
print("\n")

#Завдання 2
msg33 = 'hello lab4'
print("оригінальне повідомлення:", msg33)
serv_pub_key = (int("88CFE8F633B942B446AD21BBB53717A9010A36EBC9C447B8B8BAC8EE1238247B", 16), int("10001", 16))
encr_serv = encrypt_rsa(msg33, serv_pub_key)
print("Зашифроване повідомлення:", encr_serv)
print("Закодоване повідомлення у хексі: ", hex(encr_serv))
print("\n")

#Завдання 3
server_sign = (int("053382B2DCE32C2BE22B0A0B6D6B29882055688DDC118266A1E7F4A74EA6775A", 16))
print("повідомлення підписане сервером: ", server_sign)
message = "hvost bobra"
serv_pub_key = (int("88CFE8F633B942B446AD21BBB53717A9010A36EBC9C447B8B8BAC8EE1238247B", 16), int("10001", 16))
print("перевірка підпису: ", verify_sign(server_sign, message, serv_pub_key))

#Завдання 4
message_to_sign = "server verify"
print("оригінальне повідомлення", message_to_sign)
print(hex(signature(message_to_sign, secret_key_A)))
print(hex(secret_key_A[0]*secret_key_A[1]))
#print(hex(secret_key_A[2]))
