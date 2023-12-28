from generator import * 

e_,a_ = "[!]","[*]"

def s2l(message:str) -> int:
    return int.from_bytes(message.encode('utf-8'), byteorder='big')

def l2s(number:int) -> str:
    message = number.to_bytes((number.bit_length() + 7) // 8, byteorder='big')
    try:
        message = message.decode()
    except Exception as e:
        message = f"Can't decode bytes: {e}"
    return message 


class PubKey:
    def __init__(self, e, n):
        self.e = e 
        self.n = n
    
    def encrypt(self, pt, e=None, n=None) -> int:
        if e == None: e = self.e
        if n == None: n = self.n
        if type(pt) == str: pt = s2l(pt)
        ct = mod_pow(pt,e,n)
        return ct
        
    def verify(self, pt, s):
        if type(pt) == str: pt = s2l(pt)
        pt_ = self.encrypt(s)
        if pt == pt_:
            return True 
        else:
            return False

    def export(self) -> list:
        return [self.e,self.n]

    def __str__(self) -> str:
        return f"\nPublicKey:\ne = {hex(self.e)[2:]}\nn = {hex(self.n)[2:]}\n"

    def __repr__(self) -> str:
        return f"\nPublicKey:\ne = {hex(self.e)[2:]}\nn = {hex(self.n)[2:]}\n"



class PrivKey(PubKey):
    def __init__(self, e, d, n, p=None):
        self.e = e 
        self.d = d 
        self.n = n
        self.p = p
        if self.p != None:
            self.q = n//self.p
            self.dp = self.d % (self.p - 1)
            self.dq = self.d % (self.q - 1)
            self.q_inv = inverse(self.q, self.p)
            self.p_inv = inverse(self.p, self.q)

    def decrypt(self,ct:int):
        if self.p is None:
            pt = pow(ct, self.d, self.n)
        else:
            # print(f"{e_} p,q are seted, CRT-RSA is used")
            pt_p = mod_pow(ct % self.p, self.dp, self.p)
            pt_q = mod_pow(ct % self.q, self.dq, self.q)
            pt = (pt_p * self.q_inv * self.q + pt_q * self.p_inv * self.p) % self.n
        pt_ = l2s(pt)
        if not "Can't decode bytes: " in pt_:
            pt = pt_
        return pt 
    
    def sign(self, pt) -> list:
        if type(pt) == str: pt = s2l(pt)
        s = self.decrypt(pt)
        return s

    def signEncrypt(self, e, n, pt) -> list:
        ct = self.encrypt(pt, e, n)
        if type(pt) == str: pt = s2l(pt)
        s = self.decrypt(pt)
        s = self.encrypt(s, e, n)
        return ct, s
        
    def verifyDecrypt(self, e, n, ct, s):
        pt = self.decrypt(ct)
        s_ = self.decrypt(s)
        pt_ = self.encrypt(s_, e, n)
        if type(pt) == str: pt_ = l2s(pt_)
        if pt != pt_:
            return False, 0
        else:
            return True, pt

    def export(self) -> list:
        return [self.e,self.d,self.n]

    def __str__(self) -> str:
        return f"\nPrivateKey:\ne = {hex(self.e)[2:]}\nd = {hex(self.d)[2:]}\nn = {hex(self.n)[2:]}\n"

    def __repr__(self) -> str:
        return f"\nPrivateKey:\ne = {hex(self.e)[2:]}\nd = {hex(self.d)[2:]}\nn = {hex(self.n)[2:]}\n"

    @staticmethod
    def gen_rsa(bits=1024,e=None) -> list:
        while True:
            if e == None: e = gen_prime(bits//32)
            q,p = [gen_prime(bits) for _ in range(2)]
            assert is_prime(q)
            assert is_prime(p)
            n = q*p 
            φ = (q - 1) * (p - 1)
            d = inverse(e,φ)
            if d != -1:
                return PrivKey(e,d,n,p), PubKey(e,n)


def signRoutine(): 
    try:
        print(f"{e_} Please enter here your Private Key [d,n]:")
        d1 = int(input(f"{a_} d = "), 16)
        n1 = int(input(f"{a_} n = "), 16)
        print(f"{e_} Please enter here reciever Public Key [e,n]: ")
        e2 = int(input(f"{a_} e = "), 16)
        n2 = int(input(f"{a_} n = "), 16)
        print(f"{e_} Please enter here decimal value you want to sign")
        pt = int(input(f"{a_} pt = "), 16)
    except:
        print(f"{e_} Please enter only integer values.")
        return 
    priv = PrivKey(0,d1,n1)
    ct,s = priv.signEncrypt(e2,n2,pt)
    print(f"{e_} Signed message:\nct = {hex(ct)[2:]}\ns = {hex(s)[2:]}")

def verifyRoutine():
    try:
        print(f"{e_} Please enter here your Private Key [d,n]:")
        d1 = int(input(f"{a_} d = "), 16)
        n1 = int(input(f"{a_} n = "), 16)
        print(f"{e_} Please enter here sender Public Key [e,n]: ")
        e2 = int(input(f"{a_} e = "), 16)
        n2 = int(input(f"{a_} n = "), 16)
        print(f"{e_} Please enter here decimal value you want to verify")
        ct = int(input(f"{a_} ct = "), 16)
        print(f"{e_} Please enter here signature value")
        s = int(input(f"{a_} s = "), 16)
    except:
        print(f"{e_} Please enter only integer values.")
        return 
    priv = PrivKey(0,d1,n1)
    check, pt = priv.verifyDecrypt(e2,n2,ct,s)
    if check:
        print(f"{e_} Signature verified! Recieved message: {hex(pt)[2:]}")
    else:
        print(f"{e_} Invalid signature")
    
