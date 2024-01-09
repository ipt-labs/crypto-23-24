import requests
import json
from RSA import *
from lab4_math import os2ip, i2osp, i2byte


WHITE = "\u001b[37m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
BOLD = "\u001b[1m"
RESET = "\u001b[0m"

S = f"{GREEN}[*]{WHITE}"


def serverGetKey(session: requests.Session, keySize=256) -> tuple[int, int]:
    resp = session.get(f"http://asymcryptwebservice.appspot.com/rsa/serverKey?keySize={keySize}")
    serverKey = json.loads(resp.content.decode("utf-8"))

    servKey = int(serverKey['modulus'], 16)
    publicExponent = int(serverKey['publicExponent'], 16)

    print(f"{S} Server PublicKey: {servKey, publicExponent}")

    return servKey, publicExponent


def serverDecrypt(session: requests.Session, Alice: RSA, message: str) -> None:
    servKey, publicExponent = serverGetKey(session)
    print(f"{S} Message (bytes): {message.encode('utf-8')}")

    encrypted = Alice.encrypt(os2ip(message), (servKey, publicExponent))
    print(f"{S} Encrypted message (long): {encrypted}")

    enc_hex = bytes.hex(i2byte(encrypted))
    resp = session.get(f"http://asymcryptwebservice.appspot.com/rsa/decrypt?cipherText={enc_hex}&expectedType=TEXT")

    decrypted = json.loads(resp.content.decode('utf-8'))
    print(f"{S} Server response: {decrypted}")


def serverEncrypt(session: requests.Session, Alice: RSA, AlicePubKey: tuple[int, int], message: str) -> None:
    mod = bytes.hex(i2byte(AlicePubKey[0]))
    publicExp = bytes.hex(i2byte(AlicePubKey[1]))

    print(f"{S} Alice PublicKey: {AlicePubKey}")
    print(f"{S} Message (bytes): {message.encode('utf-8')}")

    print(f"{S} Server received public key and starts encrypting...")

    resp = session.get(f"http://asymcryptwebservice.appspot.com/rsa/encrypt?modulus={mod}&publicExponent={publicExp}&message={message}&type=TEXT")
    encrypted = json.loads(resp.content.decode('utf-8'))    
    
    print(f"{S} Server response: {encrypted}")

    encrypted = int(encrypted['cipherText'], 16)
    decrypted = Alice.decrypt(encrypted)

    print(f"{S} Decrypted message (long): {decrypted}")
    print(f"{S} Decrypted message: {i2osp(decrypted)}")


def serverSign(session: requests.Session, Alice: RSA, message: str) -> None:
    servKey, publicExponent = serverGetKey(session)
    print(f"{S} Message (bytes): {message.encode('utf-8')}")

    resp = session.get(f"http://asymcryptwebservice.appspot.com/rsa/sign?message={message}&type=TEXT")
    
    signature = json.loads(resp.content.decode('utf-8'))
    print(f"{S} Server response: {signature}")

    signature = os2ip(message), int(signature['signature'], 16)

    print(f"{S} Signature verification: {Alice.verify(signature, (servKey, publicExponent))}")


def serverVerify(session: requests.Session, Alice: RSA, AlicePubKey: tuple[int, int], message: str) -> None:
    mod = bytes.hex(i2byte(AlicePubKey[0]))
    publicExp = bytes.hex(i2byte(AlicePubKey[1]))

    print(f"{S} Alice PublicKey: {AlicePubKey}")
    print(f"{S} Message (bytes): {message.encode('utf-8')}")

    signature = Alice.sign(os2ip(message))

    print(f"{S} Alice signed message: {signature}")
    print(f"{S} Server received signature and starts verification...")

    sig_hex = bytes.hex(i2byte(signature[1]))
    resp = session.get(f"http://asymcryptwebservice.appspot.com/rsa/verify?message={message}&signature={sig_hex}&modulus={mod}&publicExponent={publicExp}&type=TEXT")
    
    verified = json.loads(resp.content.decode('utf-8'))
    print(f"{S} Server response: {verified}")


def serverSendKey(session: requests.Session, Alice: RSA, AlicePubKey: tuple[int, int]) -> None:
    mod = bytes.hex(i2byte(AlicePubKey[0]))
    publicExp = bytes.hex(i2byte(AlicePubKey[1]))

    servKey, servPublicExp = serverGetKey(session)

    print(f"{S} Alice PublicKey: {AlicePubKey}")

    resp = session.get(f"http://asymcryptwebservice.appspot.com/rsa/sendKey?modulus={mod}&publicExponent={publicExp}")
    key = json.loads(resp.content.decode('utf-8'))
    print(f"{S} Server sent encrypted key: {key}")

    key, sig = int(key['key'], 16), int(key['signature'], 16)
    key = Alice.decrypt(key)
    sig = Alice.decrypt(sig)

    print(f"{S} Signature verification: {Alice.verify((key, sig), (servKey, servPublicExp))}")
    print(f"{S} Decrypted key: {key}")


def serverReceiveKey(session: requests.Session, Alice: RSA, AlicePubKey: tuple[int, int], key: int):
    mod = bytes.hex(i2byte(AlicePubKey[0]))
    publicExp = bytes.hex(i2byte(AlicePubKey[1]))

    servKey, servPublicExp = serverGetKey(session)

    print(f"{S} Alice PublicKey: {AlicePubKey}")

    signature = Alice.sign(key)
    print(f"{S} Alice signed key: {signature}")

    k, s = Alice.encrypt(signature[0], (servKey, servPublicExp)), Alice.encrypt(signature[1], (servKey, servPublicExp))
    k, s = bytes.hex(i2byte(k)), bytes.hex(i2byte(s))

    print(f"{S} Alice encrypted key with server public key: {k, s}")
    print(f"{S} Server received key and starts verification...")

    resp = session.get(f"http://asymcryptwebservice.appspot.com/rsa/receiveKey?key={k}&signature={s}&modulus={mod}&publicExponent={publicExp}")

    k_resp = json.loads(resp.content.decode('utf-8'))
    print(f"{S} Server response: {k_resp}")
    print(f"{S} Key: {int(k_resp['key'], 16)}")
    

def main():
    s = requests.Session()
    e = 2**16 + 1

    rsa = RSA(e, 256, "Alice")
    rsa.generateKeyPair()

    print(WHITE)
    print(f"\n{BOLD}{RED}GET rsa/serverKey:{RESET}{WHITE}\n")
    serverGetKey(s)

    print(f"\n{BOLD}{RED}GET rsa/encrypt:{RESET}{WHITE}\n")
    serverEncrypt(s, rsa, rsa.getPubKey(), 'Hello, Biden! I love RSA')

    print(f"\n{BOLD}{RED}GET rsa/decrypt:{RESET}{WHITE}\n")
    serverDecrypt(s, rsa, "Biden, do you love RSA?")

    print(f"\n{BOLD}{RED}GET rsa/sign:{RESET}{WHITE}\n")
    serverSign(s, rsa, "Biden")

    print(f"\n{BOLD}{RED}GET rsa/verify:{RESET}{WHITE}\n")
    serverVerify(s, rsa, rsa.getPubKey(), "Hello! Biden!")

    print(f"\n{BOLD}{RED}GET rsa/sendKey:{RESET}{WHITE}\n")
    serverSendKey(s, rsa, rsa.getPubKey())

    print(f"\n{BOLD}{RED}GET rsa/receiveKey:{RESET}{WHITE}\n")
    serverReceiveKey(s, rsa, rsa.getPubKey(), 1337228322)


if __name__ == "__main__":
    main()
