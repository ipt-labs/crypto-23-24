import secrets
import random

e = 65537

class Abonent():
	def __init__(self, name):
		self.name = name
	#GENERATE SIGNATURE
	def sign_message(self, cleartext):
		signed = pow(cleartext, self.d, self.n)
		return str(hex(signed))
	
	#VERIFY DIGITAL SIGNATURE
	def verify_message(self, cleartext, signature):
		if pow(signature, self.received_e, self.received_n) == cleartext:
			return True
		else:
			return False

	def encrypt(self, cleartext):
		print("[+]"+"-"*100+"[+]\n")
		#JUST SOME STUFF TO CONVERT CLEARTEXT TO INT
		print("\nCleartext message to encode:", cleartext)
		cleartext_bytes = cleartext.encode('utf-8')
		print("Cleartext message to encode in bytes:", cleartext_bytes.hex())
		cleartext_int = int.from_bytes(cleartext_bytes, byteorder='big')
		#ENCRYPTING USING RECEIVED PUBLIC KEY OF ANOTHER ABONENT
		print("Encrypting with received public key...")
		encrypted = pow(cleartext_int, self.received_e, self.received_n)
		#[2:] to remove 0x
		result = hex(encrypted)+"."+self.sign_message(cleartext_int)[2:]
		print("Encrypted using recieved public key:", result[2:])
		return result
		
	def decrypt(self, encrypted):
		#CUSTOM REALIZATION
		if "." in encrypted:
			print("[+]"+"-"*100+"[+]\n")
			print("\nEncrypted message to decode (hex):", encrypted[2:])
			#DECRYPTING USING OWN PRIVATE KEY VALUES
			cleartext = pow(int(encrypted.split('.')[0], 16), self.d, self.n)
			#VERYFYING DIGITAL SIGNATURE
			verified = self.verify_message(cleartext, int(encrypted.split('.')[1], 16))
			if verified:
				print("\nSignature verified")
				print("Decoded hex values:", hex(cleartext))
				byte_string = bytes.fromhex(hex(cleartext)[2:]).decode('utf-8')
				print("Cleartext plaintext: {}".format(byte_string))
				return hex(cleartext)
			else:
				print("Corrupted signature")
				return None
		#INTERACTION WITH THE SERVER
		else:
			print("[+]"+"-"*100+"[+]\n")
			print("\nEncrypted message to decode (hex):", encrypted)
			#DECRYPTING USING OWN PRIVATE KEY VALUES
			cleartext = pow(int(encrypted, 16), self.d, self.n)
			print("Decoded hex values:", hex(cleartext))
			byte_string = bytes.fromhex(hex(cleartext)[2:]).decode('utf-8')
			print("Cleartext plaintext: {}".format(byte_string))
			return hex(cleartext)


	
	def receive_key(self, public_key):
		#print("Received public key:", public_key)
		self.received_e = public_key[0]
		self.received_n = public_key[1] 
		self.public_key_received = (public_key)

	def send_key(self):
		return self.e, self.n

def miller_rabin_test(n, k=5):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Знаходження чисел s і d, таких, що n - 1 = 2^s * d
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    # Проведення k ітерацій тесту Міллера-Рабіна
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Число не є простим

    return True  # Число, можливо, просте
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x
def mod_inverse(e, phi_n):
    gcd, x, y = extended_gcd(e, phi_n)
    
    if gcd != 1:
        raise ValueError("The modular inverse does not exist.")
    else:
        return x % phi_n 
def pick_random():	
	random = secrets.randbits(256)
	if (miller_rabin_test(random) == False):
		return pick_random()
	else:
		return random	
def generate_pq(a, b):
	pq = []
	for i in range (0, 4): pq.append((pick_random()))
	pq = sorted(pq, reverse=True)
	greatest = pq[:2]
	least = pq[2:]
	print("\nGenerating p, q for abonent A:\np: {}\nq: {}".format(least[0], least[1]))
	print("\n\nGenerating p1, q1 for abonent B:\np: {}\nq: {}\n".format(greatest[0], greatest[1]))
	a.p = least[0]
	a.q = least[1]
	b.p = greatest[0]
	b.q = greatest[1]
	return True
def generate_key_pair(abonent):
	global e
	abonent.e = e
	abonent.phi_n= ((abonent.q) - 1) * ((abonent.p)-1)
	abonent.n = abonent.q * abonent.p
	abonent.d = mod_inverse(e, abonent.phi_n)
	
if __name__ == "__main__":
	#Creating object for anomemts
	Abonent_A = Abonent("Abonent A")
	Abonent_B = Abonent("Abonent B")
	while True:
		print("1. GenerateKeyPair():")
		print("2. Send encrypted | Decrypt received (Encrypt(), Decrypt())")
		print("3. Interaction with the server to check work")
		choise = int(input("\nEnter the number: "))
		if choise == 1:
			print("[+]"+"-"*100+"[+]\n")			
			#Generating p and q for both abonents
			generate_pq(Abonent_A, Abonent_B)
			print("[+]"+"-"*100+"[+]\n")		
			#Generating key pairs for both abonents (returns self.e, self.phi_n, self.d, self.n)
			generate_key_pair(Abonent_A)
			generate_key_pair(Abonent_B)
			#Generating public and private keys for every abonent (returns self.public_key, self.private_key)
			#Keys are contained in list like this: (e, self.n) for public or (self.d) for private
			print("Public key of Abonent A: (e: {}, n: {})\n".format(e, hex(Abonent_A.n)))
			Abonent_A.public_key = (Abonent_A.e, Abonent_A.n)
			Abonent_A.private_key = (Abonent_A.d, Abonent_A.p, Abonent_A.q)
			print("Public key of Abonent B: (e: {}, n: {})\n".format(e, hex(Abonent_B.n)))
			Abonent_B.public_key = (Abonent_B.e, Abonent_B.n)
			Abonent_B.private_key = (Abonent_B.d, Abonent_B.p, Abonent_B.q)
			#Exchanging keys
			#After the lines below, we receive self.public_key_received = another_abonent_public_key
			#public key: list (e, self.n)
			Abonent_A.receive_key(Abonent_B.send_key())
			Abonent_B.receive_key(Abonent_A.send_key())
			#NOW WE HAVE ALL NEEDED FOR THE RSA SYSTEM
			print("[+]"+"-"*100+"[+]\n")
		elif choise == 2:
			message = str(input("Enter the message to encrypt: "))
			print("1. A -> B")
			print("2. B -> A")
			if int(input()) == 1:
				print("\nEncrypting message from Abonent A with public key of Abonent B")
				encrypted = Abonent_A.encrypt(message)
				print("\nDecrypting on the Abonent B with private ley B:")
				Abonent_B.decrypt(encrypted)
			else: 
				print("\nEncrypting message from Abonent B with public key of Abonent A")
				encrypted = Abonent_B.encrypt(message)
				print("\nDecrypting on the Abonent A with private key A:")
				Abonent_A.decrypt(encrypted)
		#INTERACTION WITH THE SERVER BELOW
		#FOR SERVER -> CREATING ABONENT_C AND SENDIND ITS PUBLIC KEY TO ABONENT_A
		elif choise == 3:
			print("[+]"+"-"*100+"[+]\n")
			print("Interaction with the sever to check the work")
			print("Abonent from Server (Abonent_C):")
			Abonent_C = Abonent("Abonent C")
			var1 = str(input("Enter the e value from the server: "))
			var2 = str(input("Enter the n (modulus) value from the server: "))
			Abonent_C.e = int(var1, 16)
			Abonent_C.n = int(var2, 16)
			Abonent_A.receive_key(Abonent_C.send_key())
			print(Abonent_A.public_key_received)
			print("Values to enter on the website:", hex(Abonent_A.public_key[0]), hex(Abonent_A.public_key[1]))
			while True:
				print("[+]"+"-"*100+"[+]\n")
				print("1. Encrypt the message and send it to the server")
				print("2. Decrypt the message from the server")
				print("3. Verify the signature from the server")
				print("4. Sign a message and verify it on the server")
				choise = int(input("\nEnter the number: "))
				if choise == 1:
					msg = str(input("Enter the message to encode: "))
					Abonent_A.encrypt(msg)
				elif choise == 2:
					msg = str(input("Enter the message to decode: "))
					Abonent_A.decrypt(msg)
				elif choise == 3:
					clrtxt = input("Enter the cleartext from the server: ").encode('utf-8').hex()
					sig = input("Enter the signature from the server: ")
					print("Verified") if Abonent_A.verify_message(int(clrtxt, 16), int(sig, 16)) else print("Corrupted")
				elif choise == 4:
					msg = str(input("Enter the message to generate a signature: ")).encode('utf-8').hex()
					print(Abonent_A.sign_message(int(msg, 16)))
				else:
					break
