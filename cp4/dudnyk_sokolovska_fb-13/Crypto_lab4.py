import random
from typing import List
import sys

E = 2**16 + 1


def get_inversed(a, m):

    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x

    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m

# lab4

def gcd(a:int, b:int):
    # easy gcd
    if b == 0:
        return a
    else:
        return gcd(b, a % b)
    

def horner_pow(num:int, exp:int, mod:int):
    res = 1
    num %= mod
    bits_num = bin(exp)[2:]
    for i in bits_num:
        res = (res*res) % mod
        if i == '1':
            res *= num % mod
    res %= mod
    return res

def test_easy_deviders(p:int):
    if p % 2 == 0 or p % 3 == 0 or p % 5 == 0 or p % 7== 0 or p % 11 == 0: 
        return False
    return True

def miller_rabin(p:int, k:int = 50):

    if test_easy_deviders(p) and p > 1:
        d, s = p-1, 0

        while d % 2 == 1:
            s += 1
            d //= 2

        for _ in range(k):
            x = random.randint(2, p-1)
            if gcd(x, p) != 1:  return False
            
            x_1 = horner_pow(x, d, p)
            if x_1 == 1 or x_1 == -1 : return True

            for r in range(1, s):
                x_r = horner_pow(x, d*(2**r), p)
                if x_r == -1 :  return True
    
    return False

# print(miller_rabin(324))        # ділиться на 2
# print(miller_rabin(321))        # ділиться на 3 
# print(miller_rabin(657))        # ділиться на 3   
# print(miller_rabin(179))        # посте


def get_random_prime(start:int = None, end:int = None, bits = None, toprint:bool=False):
    if bits is not None:
        while True:
            num = random.getrandbits(bits)
            if miller_rabin(num) : 
                if toprint: print(num)
                return num

    elif start is not None and end is not None:
        while True:
            num = random.randint(start, end)
            if miller_rabin(num): 
                if toprint: print(num)
                return num
    else:
        raise ValueError("Некорректно задано початкове та кінцеве значення інтервалу або кількість бітів!")
    
# get_random_prime(bits=64, toprint=True)
# get_random_prime(bits=128, toprint=True)
# get_random_prime(start=690, end=20578, toprint=True)


def get_keys_pairs(bits:int=256):
    secret_keys = {}
    open_keys = {}

    # for A, n and e - keys
    secret_keys['p'] = get_random_prime(bits=bits)
    secret_keys['q'] = get_random_prime(bits=bits)

    open_keys['n'] = secret_keys['p'] * secret_keys['q']
    euler = (secret_keys['p'] - 1) * (secret_keys['q'] - 1)

    open_keys['e'] = E
    secret_keys['d'] = get_inversed(open_keys['e'], euler)

    return secret_keys, open_keys

# print("get_key_pairs: ", get_keys_pairs()) 

def generate_pairs_AB():
    A_secretKeys, A_openKeys = get_keys_pairs()
    # перевірка q1*p1 <= q2*p2
    # міняємо якщо не задовольняється умова
    B_secretKeys, B_openKeys = get_keys_pairs()
    if B_secretKeys['q'] * B_secretKeys['p'] > A_secretKeys['q'] * A_secretKeys['p']: 
        A_secretKeys, B_secretKeys = B_secretKeys, A_secretKeys

    return A_openKeys, A_secretKeys, B_openKeys, B_secretKeys

# A_openKeys, A_secretKeys, B_openKeys, B_secretKeys = generate_pairs_AB()
# print("A\n", A_openKeys, A_secretKeys, "\n\nB\n", B_openKeys, B_secretKeys)

def cipher_message(M: int, openKeys: dict):
    n, e = openKeys['n'], openKeys['e']
    if M >= n:
        raise ValueError(f"Ваше повідомлення занадто велике для шифрування!\nПовідомлення: {M}\nn: {n}")
    elif M < 0:
        raise ValueError("Ваше повідомлення менше 0")
    res = horner_pow(M, e, n)
    return res

def decipher_message(C: int, privateKeys: dict):
    p, q, d = privateKeys['p'], privateKeys['q'], privateKeys['d']
    n = p * q
        
    if C >= n:
        raise ValueError(f"Криптограма завелика для розшифрування!\nКриптограма: {C}\nn: {n}")
    elif C < 0:
        raise ValueError("Криптограма менше нуля!")
    res = horner_pow(C, d, n)
    return res

def crypto_sign(M:int, private_keys:dict, open_keys:dict):
    S = horner_pow(M, private_keys['d'], open_keys['n'])
    return S

def verification(M:int, S:int, open_keys:dict):
    return M == horner_pow(S, open_keys['e'], open_keys['n'])

def send_message(M:int, A_openKeys, A_privateKeys:dict, B_openKeys:dict):
    encrypted_M = cipher_message(M, B_openKeys)
    S = crypto_sign(M, A_privateKeys, A_openKeys)
    S1 = horner_pow(S, B_openKeys['e'], B_openKeys['n'])
    if encrypted_M and S and S1:
        print("Підписанне повідомлення відправлено успішно!")

    return encrypted_M, S1

def receive_message(encrypted_M:int, S1:int, B_privateKeys:dict, A_openKeys:dict):
    M = decipher_message(encrypted_M, B_privateKeys)
    d = B_privateKeys['d']
    n = B_privateKeys['p'] * B_privateKeys['q']
    S = horner_pow(S1, d, n)
    verified = verification(M, S, A_openKeys)

    if not verified:
        print("Аутентифікацію провалено! Підпис та/або ключі невірні!")
    else:
        print("Аутентифікацію за підписом пройдено успішно!\nОтримане повідомлення:", M)

messageA = random.randint(1, 130)       # задаємо різні проміжки щою упевнитися в правильній роботі
messageB = random.randint(131, 260)
print("messageA:", messageA, f"(length={sys.getsizeof(messageA)})\nmessageB:", messageB, f"(length={sys.getsizeof(messageB)})")
A_openKeys, A_secretKeys, B_openKeys, B_secretKeys = generate_pairs_AB()

print(f"\nsending message {messageA} to B")
encrypted_A, s1a = send_message(messageA, A_openKeys, A_secretKeys, B_openKeys)

print(f"\nsending message {messageB} to A")
encrypted_B, s1b = send_message(messageB, B_openKeys, B_secretKeys, A_openKeys)

print("\nreceiving message from A:")
receive_message(encrypted_A, s1a, B_secretKeys, A_openKeys)

print("\nreceiving message from B:")
receive_message(encrypted_B, s1b, A_secretKeys, B_openKeys)



# статичні дані для перевірки

# A_open_static = {'n': 2473737842202304934787222987836508747179338223921489399061250469701340947202938217684161015132617360930669790884492247351288673941655064409712301120118031, 
#                  'e': 65537}
# A_secret_static = {'p': 22265940615939518654421354186895036624144229614508843228257056207427890116167, 
#                    'q': 111099633510718619897142263161279998876195698223355000056868443411384083193593, 
#                    'd': 2223861520195205759233086909293430975747517740189242579374882797860657408583665005596333280605144797294794843233212631180363022087762053355600318904779025}

# B_open_static = {'n': 318364486092893208619427667853533833650943617879195340493482118970501846613364636276430456903206261414312196320388291127571713722901711520673894880680103, 
#                  'e': 65537}
# B_secret_static = {'p': 7797314612703150363262210733209742905963352618298642126655537251488120650741, 
#                    'q': 40830016730916996314612890465226273697823794106448457431491205995781196864683, 
#                    'd': 94396427876727662692718898358635113836537168052070187168612303520679797418099038494604992780457750626919550638923668787949070836700064860383511420165953}


# static_secret_keys = {'p': 69819953805287766503459646966142998171613528092044328272563921438650723424849, 
#                       'q': 59990584485103357398000765071984267951170634416743890283750519191068638236107, 
#                       'd': 1888891693201938364012848145832313386426576551493966477173661553842167363314715505737594531118518480110207984568594845872784566495703169248672251115517793}
# static_open_keys = {'n': 4188539837502129404916597155588303921713366518533584199442742590226835475877528223650275936240272484975824311826163400436055806808605328247100141332822843, 
#                     'e': 65537}
# print(static_secret_keys, static_open_keys)
# message_static = 126

# print("n = ", hex(static_open_keys['n'])[2:].upper(), "\ne = ", bin(static_open_keys['e'])[2:])

# encrypted = cipher_message(message_static, static_open_keys)
# encrypted_server = int('4253C72DDF34930D77E4672C701A23DB57CBAE97D4CD6ADD00310D9D96846792', 16)
# print("encrypted message: ", encrypted)
# print("decrypted message:", decipher_message(encrypted, privateKeys=static_secret_keys))
# csign = crypto_sign(message_static, static_secret_keys)

# print("crypto sign: ", csign)
# print("verification: ", verification(message_static, csign, static_open_keys))