import rsa
import random
import string


class User:
    def __init__(self,p=rsa.random_prime(256), q=rsa.random_prime(256)):
        self.public_key, self.private_key = rsa.gen_rsa_keys(p, q)
        self.b_public_key = None

    def random_msg(self,length):
        return hex(random.randint(0,2**256))

    def receive_key(self, pub_k):
        self.b_public_key = pub_k

    def send_key(self):
        return self.public_key

    def send_msg(self, msg):
        encrypted = rsa.encrypt(msg, self.b_public_key)
        signature = rsa.sign(msg, self.private_key)

        return encrypted, signature

    def receive_msg(self, msg, signature):
        decrypted = rsa.decrypt(msg, self.private_key)
        verified = rsa.verify(decrypted, self.b_public_key, signature)
        if verified:
            return decrypted
        else:
            return '**MSG IS NOT VERIFIED**'


