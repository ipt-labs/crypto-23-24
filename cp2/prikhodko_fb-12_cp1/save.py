from hashlib import md5
def findKey(text):
    hash = md5(text.encode()).hexdigest()
    with open('db') as f:
        lines = f.readlines()
    for line in lines:
        text,key = line.split(":")
        if hash == text:
            return key[:-1] 
    return None

def save(text,key):
    hash = md5(text.encode()).hexdigest()
    with open('db', 'a') as f:
        f.write(hash+":"+key+"\n")

