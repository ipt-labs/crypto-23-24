import rsa
from rsa import random_prime
from user import User

a = [random_prime(256),random_prime(256),random_prime(256),random_prime(256)]
a.sort()
p1,q1,p2,q2 = a


print(f'[*]Init users:\n   p1:{p1}\n   q1:{q1}\n   p2:{p2}\n   q2:{q2}')
USER_A = User(p1, q1)
USER_B = User(p2, q2)

print('[*]A public key:\n   ', list(map(lambda x:hex(x),USER_A.public_key)), '\n[*]B public key:\n ', list(map(lambda x:hex(x),USER_B.public_key)))
print('[*]A private key:\n   ', list(map(lambda x:hex(x),USER_A.private_key)), '\n[*]B private key:\n ', list(map(lambda x:hex(x),USER_B.private_key)))




print('[*]A and B exchange public keys: ')
a_pbk = USER_A.send_key()
b_pbk = USER_B.send_key()
USER_B.receive_key(a_pbk)
USER_A.receive_key(b_pbk)



msg = USER_A.random_msg(32)
print('[*]A wanna send msg:\n   ', msg)
enc,sig = USER_A.send_msg(int(msg,16))
print('[*]Encrypted msg:\n  ', hex(enc),'\n[*]Signature:\n   ',hex(sig))
print('[*]B receive msg')
dec = USER_B.receive_msg(enc, sig)
print('[*]Decrypted msg:\n  ',hex(dec))




p,q = random_prime(256),random_prime(256)

# n , e
pbk = (int('0x2f5a82fffe78870614dee6c71a1f3ab37e056a44d3492d9dc8570432de7dc7d29116ce84375e38284ce2ea8034cff2bc9707029df750ee2ea330d8c4c4b8229f',16), int('0x8ad753e9f6579306d44aa691121953651eeba5fa499b829caab2ccc870f1ab6dcf4cd145fa8d2cf7d1b08df362b7277f28953dfe9b120d75b8f6353bad1ba3',16))
# p, q, d
prk = (22883167928459915116713168682106988584368477942666170072859261286288952938011, 108381289601232534540234616626770065778125187457499696152134578633249150350797, 2228946322055142389386887728101888883588735504827796339600932927951004737475411780524150881713192049455484285222876863168972788021962309083628232176761099)
print('[*]public key:\n   ', list(map(lambda x:hex(x),pbk)), '\n[*]private key:\n ', list(map(lambda x:hex(x),prk)))

# Change
server_pbk =(int("95E6FA72517A71E0A5C7D8283CA3FD72C8039DA5233BE87FA90477D8A0C4F9E9",16),int("10001",16))

msg=int("111",16)

encrypted = rsa.encrypt(msg, server_pbk)
signature = rsa.sign(msg, prk)
print('[*]Encrypted:\n  ',hex(encrypted),'\n[*]Signature:\n  ',hex(signature))

# Change
enc_msg = int("134EA395BB3BB759B95C8BA87D7CDE9671A141C3D0345529EC38F8DA10323B2118F97A2486D1E9ABEA10A41C65E0705D6FA2843AA20B8AEAF9CB473E3A2FA23F",16)
dec = rsa.decrypt(enc_msg,prk)
print('[*]Decrypted:\n  ',hex(dec))

# Change
server_sig = int("461EE1A380771F48D90465996A9C4FD5A1C98DED4ECFA421070AC03BF1D29559",16)
sig_msg = int("333",16)
verify = rsa.verify(sig_msg,server_pbk,server_sig)
print('[*] Is verified: ',verify)


k1,s1,k = rsa.send_key(server_pbk, prk)
print('[*] k1:\n    ',hex(k1),'\n[*] s1:\n    ',hex(s1),'\n[*] k:\n    ',hex(k))

k1,s1 = (int("0D810EB1AD0DD6AA2567D6CB4B9C995900B1839175E8F94A24EFD6F71684BDE04371807002486D8DBBBEF36FE37010C78A75BB92E1CAD2C5BE0E6685D4B9173D",16),int("074E72FFBDC889E67799887D32EBAA07D59057A2472783E8A6BE938FBBC002EAA789D88F910488B4AAF7F88C003D90F036EDE8451C135481CE554D1FBC5FAA11",16))
k,s,verified = rsa.receive_key(k1,s1,server_pbk,prk)
print('[*] k:\n    ',hex(k),'\n[*] s:\n    ',hex(s),'\n[*] verified:\n    ',verified)




