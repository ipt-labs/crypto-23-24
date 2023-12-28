#!/usr/bin/python3
from rsa import * 

a_,e_,q_ = "[*]","[!]","[?]"

def main() -> None:
    privA, pubA = PrivKey.gen_rsa()
    privB, pubB = PrivKey.gen_rsa()
    if pubA.n > pubB.n:
        privA,privB = privB,privA 
        pubA,pubB = pubB,pubA
    print(f"{a_} Alice {'-'*50} {privA}")
    print(f"{a_} Bob   {'-'*50} {privB}")
    ae,an = pubA.e,pubA.n 
    be,bn = pubB.e,pubB.n
    message = "Crypto is fun!"
    ct,s = privA.signEncrypt(be,bn,message)
    print(f"{a_} Alice signed&encrypted \n{ct = }\n{s = }")
    check,pt = privB.verifyDecrypt(ae,an,ct,s)
    print(check,pt)
    if check:
        print(f"{e_} Bob verified&decrypted message {pt}")
    
    ct = pubA.encrypt(message)
    print(f"{a_} Message: {message}")
    print(f"{e_} Message encrypted: {ct}")
    pt = privA.decrypt(ct)
    print(f"{e_} Message decrypted: {pt}")
    
    s = privA.sign(message)
    print(f"{a_} Alice signed message: {s = }")
    print(f"{e_} Alice public key verified message, result: {pubA.verify(message,s)}")
    print(f"{q_} This is sign/verify oracle, it works with hex format\nPress 1 to sign\nPress 2 to verify\nPress 3 to exit")
    while True:
        try:
            inp = int(input(f"{a_} # "))
            if inp not in [1,2,3]:
                print(f"{e_} Invalid paramter")
                continue
            if inp == 1:
                signRoutine()
            elif inp == 2:
                verifyRoutine()
            elif inp == 3:
                break

        except:
            print(f"{e_} Invalid paramter")




   
if __name__ == "__main__":
    main()
