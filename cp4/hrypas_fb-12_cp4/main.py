import random
import math

BIT_SIZE = 512

class public_key:
    def __init__(self, e = 0, n = 0):
        self.e = e
        self.n = n

    
class rsa_box:

    def __init__(self, key_length=BIT_SIZE):
        self.secret_key = 0
        self.public_key = 0
        self.friend_public_key = public_key()
        self.miller_rabin_constant = 10
        self.n = 0
        self.phi_n = 0
        self.e = 1 + 2**16
        self.d = 0
        if key_length & 1 == 1:
            print("must be able to divide by 2")
            return
        self.key_length = key_length


    def miller_rabin(self, p):
        if p & 1  == 0:
            return False
        d = p - 1
        s = 0
        while (d % 2 == 0):
            d //= 2
            s+=1
        for _ in range(self.miller_rabin_constant):
            a = random.randint(2,p-2)
            x = pow(a,d,p)
            if x==1 or x ==p-1:
                continue
            for _ in range (1,s-1):
                x= (x*x) % p
                if x==p-1: continue
                if x==1: 
                    return False
            return False
        return True

            
    def generate_keys(self):
        q = 0
        p = 0
        while len(bin(self.n)) != 514 or q + p == 0:
            while(1):
                p = random.getrandbits(256)
                if p & 1 == 0:
                    p += 1
                while (self.miller_rabin(p) == False):
                    p += 2
                    print("possible p: ", p)
                if len(bin(p)) == BIT_SIZE/2 + 2:
                    break

            while(1):
                q = random.getrandbits(256)
                if q & 1 == 0:
                    q += 1
                while (self.miller_rabin(q) == False):
                    q += 2
                    print("possible q: ",q)
                if len(bin(q)) == BIT_SIZE/2 + 2:
                    break

            print("possible prime P: ", p)
            print("possible prime q ", q)
                
    
            
            self.n = p*q
        self.phi_n = (q-1)*(p-1)
        self.d = pow(self.e,  -1, self.phi_n)
        if math.gcd(self.e, self.phi_n) != 1:
            print("wrong 'e'")
        # print(f"p is {p}\nq is {q}\nn is {self.n}\nd is {self.d}")
        self.public_key = public_key(self.e, self.n)
        self.secret_key = self.d

    def encrypt(self, message):
        if self.friend_public_key.e == 0:
            print("dont have friend's public key")
            return
        if type(message) == str:
            message = int.from_bytes(bytes(message, "utf-8"))
        return pow(message, self.friend_public_key.e, self.friend_public_key.n)

    def decrypt(self, message):
        if type(message) == str:
            message = int.from_bytes(bytes(message, 'utf-8'))
        return pow(message, self.d, self.n)
    
    def sign(self, message):
        if type(message) == str:
            message = int.from_bytes(bytes(message, 'utf-8'))
        S = pow(message, self.d, self.n)
        print("signed message: ", hex(S))
        return S

    def verify(self, message, orig_message):
        if type(message) == str:
            message = int.from_bytes(bytes(message, "utf-8"))
        if type(orig_message) == str:
            orig_message = int.from_bytes(bytes(orig_message, "utf-8"))
        if pow(message, self.friend_public_key.e, self.friend_public_key.n) == orig_message:
            print("verified successfully")
        else:
            print("verification error")
    
    def send_key(self):
        return self.public_key.e, self.public_key.n

    def recive_public_key(self, e1, n1):
        self.friend_public_key.e = e1
        self.friend_public_key.n  = n1
        return

    def SendKey(self):
        k = random.randint(1, self.public_key.n-1)
        print("generated k: ", hex(k))
        k1=  pow(k, self.friend_public_key.e, self.friend_public_key.n)
        S = pow(k, self.d, self.public_key.n)
        print("generated S: ", hex(S))
        S1 = pow(S, self.friend_public_key.e, self.friend_public_key.n)
        print("sending S1: ", hex(S1))
        print("sending k1: ", hex(k1))
        return k1, S1
    
    def RecieveKey(self, k, S1):
        k = pow(k, self.d, self.public_key.n)
        S = pow(S1, self.d, self.public_key.n)
        print("decrypted k: ", hex(k))
        print("decrypted S: ", hex(S))
        return k == pow(S, self.friend_public_key.e, self.friend_public_key.n)






def phi(a):
    b=a-1
    c=0
    while b:
        if not math.gcd(a,b)-1:
            c+=1
        b-=1
    return c

def main():
    a = rsa_box()
    b = rsa_box()
    while b.n <= a.n:
        print("for a: ")
        a.generate_keys()
        print("for b: ")
        b.generate_keys()



    print("\n\n")
    print("a stats: ")
    print(f"d = {hex(a.d)}")
    print(f"modulus = {hex(a.public_key.n)}")
    print(f"exponent = {hex(a.public_key.e)}")
    
    print(f"a private is {hex(a.secret_key)}")
    print("\n\n")


    print("b stats: ")
    print(f"d = {hex(b.d)}")
    print(f"modulus = {hex(b.public_key.n)}")
    print(f"exponent = {hex(b.public_key.e)}")
    
    print(f"b private is {hex(b.secret_key)}")


    message = b"hello from srv"
    message = int.from_bytes(message)
    print(f"cleartext: {hex(message)}")
    mess_to_sign_a = random.randint(1, 12312314124)
    mess_to_sign_b = random.randint(1, 12312314124)

    a.recive_public_key(*b.send_key())
    b.recive_public_key(*a.send_key())

    print(b.RecieveKey(*a.SendKey()))

    print("verifying for b: ")
    b.verify(a.sign(mess_to_sign_a), mess_to_sign_a)
    print("verifying for a: ")
    a.verify(b.sign(mess_to_sign_b), mess_to_sign_b)
    msg = a.encrypt(message)
    print(f"syphertext = {hex(msg)}")
    msg =  b.decrypt(msg)
    print("decryption result: ", hex(msg))
    print(msg.to_bytes(14, "big"))
    
    return




if __name__ == "__main__":
    main()
