import random

def generate_key_pair(self):
    n = self.p*self.q
    phi = (self.p-1) * (self.q-1)
    e = pow(2, 16) + 1
    d = pow(e, -1, phi)
    # print(f"n == {n}\nphi == {phi}\ne == {e}\nd == {d}")
    return [d, (n, e)]


def horner_scheme(a, exp, modulo):
    binary_exp = bin(exp)[2:]
    result = 1
    for bit in binary_exp:
        result **= 2
        result %= modulo
        if bit == '1':
            result *= a
            result %= modulo

    return result


def gcd_euclid(x, y):
    while y:
        x, y = y, x % y
    return abs(x)


def miller_rabin_test(p, k=30):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
              107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
              227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293]

    if p % 2 == 0:
        return False

    # попереднє ділення
    for num in primes:
        if p % num == 0:
            return False

    # знаходимо розклад p-1 = d * 2^s
    s = 0
    d = p - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    # print(d,s)
    for i in range(1, k+1):
        x = random.randint(1, p)
        gcd = gcd_euclid(x, p)
        # print(f"k == {i} x == {x},p == {p}, gcd == {gcd}")
        x = horner_scheme(x, d, p)
        # print(x)
        if gcd > 1:
            return False
        if x == 1 or x == p - 1:
            # print(f"p : {p} cильнопсевдопросте за основою x : {x}")
            continue

        for r in range(s-1):
            x = horner_scheme(x, 2, p)
            # print(f"x_r = {x} r = {r}")
            if x == p - 1:
                # print(f"x_r :{x} = -1 mod {p} отже p сильнопсевднопросте за основою x:{x}  ")
                break
            elif x % p == 1:
                # print(f"x не є сильнопсевдопростим")
                return False
        else:
            return False

    return True


def generate_prime_with_len(bits):
    while True:
        num = random.getrandbits(bits)
        if miller_rabin_test(num) is True:
            return num


def rsa_cypher(message, e, n):
    # M^e mod n
    cypher_text = horner_scheme(a=message, exp=e, modulo=n)
    # print(cypher_text)
    return cypher_text


def rsa_decypher(message, d, n):
    decyphered_text = horner_scheme(a=message, exp=d, modulo=n)
    # print(decyphered_text)
    return decyphered_text


def sign(message, d, n):
    digital_sign = horner_scheme(a=message, exp=d, modulo=n)
    return digital_sign


def verify(message, signature, e, n):
    verif = horner_scheme(a=signature, exp=e, modulo=n)
    if verif == message:
        return True
    else:
        return False


class Abonent:
    def __init__(self, uuid):
        self.uuid = uuid
        self.gen_pq()
        self.private_key, self.public_key = self.generate_key_pair()  # [d, (n, e)] return from gen_key
        self.public_key_other = None
        self.message = None

    # генерація ключових пар
    def generate_key_pair(self):
        n = self.p*self.q
        phi = (self.p-1) * (self.q-1)
        e = pow(2, 16) + 1
        d = pow(e, -1, phi)
        # print(f"n == {n}\nphi == {phi}\ne == {e}\nd == {d}")
        return [d, (n, e)]

    def gen_pq(self):
        self.p = generate_prime_with_len(256)
        self.q = generate_prime_with_len(256)

    def generate_message(self):
        self.message = random.getrandbits(128)

    def recieve_public_key(self, key):
        self.public_key_other = key

    def send_public_key(self):
        key = self.public_key
        return key

    def send_message(self):
        # шифруємо відкритим ключем абонента B
        cypher = rsa_cypher(message=self.message, e=self.public_key_other[1], n=self.public_key_other[0])
        signature = sign(message=self.message, d=self.private_key, n=self.public_key[0])
        return cypher, signature

    def recieve_message(self, var):
        message = var[0]
        signature = var[1]
        # розшифровуємо своїм d та n
        decypher_text = rsa_decypher(message=message, d=self.private_key, n=self.public_key[0])
        # верифікація за допомогою відкритого ключа абонента В
        verif = verify(message=decypher_text, signature=signature, e=self.public_key_other[1], n=self.public_key_other[0])

        return verif, decypher_text


def site_vefify():
    p = generate_prime_with_len(256)
    q = generate_prime_with_len(256)
    d_test, pub_test = generate_key_pair(p,q)
    n, e = pub_test

    print(f"d = {hex(d_test)}")
    print(f"n = {hex(n)}")
    print(f"e = {hex(e)}")
    server_cypher = int(input("enter server cypher: "), 16)

    print(type(server_cypher),type(d_test),type(n))
    decrypted_server_cypher = rsa_decypher(server_cypher, d_test, n)
    print(hex(decrypted_server_cypher))

    message = 0x200320036969 # random msg
    ds = sign(message=message, d=d_test, n=n)

    print(hex(ds))
            


def main():
    is_run = True
    abonents = []

    def get_abonent():
      current_abonent = None
      id = int(input('abonent`s uuid: '))

      for i in abonents:
          if id == i.uuid:
              current_abonent = i

      if current_abonent == None:
          raise Exception('no abonent with such id')
              
      return current_abonent


    print('input h or help to see all commands')
    while is_run:
        command = input('\nyour command: ')
        if command == 'h' or command == 'help':
            print('C, Create abonent with p,q')
            print('S, Show info')
            print('SM, Send msg')
            print('GM, Generate msg')
            print('RM, Receive msg')
            print('Q, Quit program')

        elif command == 'C':
            uuid = len(abonents)+1
            abonent = Abonent(uuid=uuid)
            abonents.append(abonent)
            print('abonent created with uuid ', uuid)
        elif command == 'S':
            if (len(abonents) == 0):
                print('no abonents, create one firstly')
                return 
            
            for a in abonents:
                print('uuid: ', a.uuid)
                print('public key: ', a.public_key)
                print()

        elif command == 'GM':
            current_abonent = get_abonent()
            current_abonent.generate_message()

            print('message was generated: ',hex(current_abonent.message))
        elif command == 'SM':
            print('who should send?')
            current_abonent = get_abonent()

            print('who should receive?')
            receiver = get_abonent()

            current_abonent.recieve_public_key(receiver.send_public_key())
            receiver.recieve_public_key(current_abonent.send_public_key())


            res = current_abonent.send_message()
            print('message was sent: ', res)

        elif command == 'RM':
            print('who should receive?')
            receiver = get_abonent()

            cypher = int(input('cypher: '))
            signature = int(input('signature: '))

            verif, decypher_text = receiver.recieve_message(var=[cypher, signature])

            if verif is True:
                print(f"Message : {hex(decypher_text)}")
            else:
                print("Signature does not match")

        elif command == 'Q':
            is_run = False
        else:
            print('unknown command, write h to see all commands')
        
main()