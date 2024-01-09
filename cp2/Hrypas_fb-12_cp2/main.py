import collections
from numpy import inf


def GetProbability(Filename, Alphabet):
    File = open(Filename, "r")
    RawText = File.read().replace("\n","").lower()
    RawText = RawText.replace('ё','е')

    TextList = [i for i in RawText if i in Alphabet]

    LetterCount = collections.Counter(TextList)
    TotalAmount = 0
    for i in LetterCount.values():
        TotalAmount += i
    print(f"Total letters: {TotalAmount}")

    LetterProbablilty =  {}
    for i in LetterCount.keys():
        LetterProbablilty[i] = LetterCount[i]/TotalAmount
    return LetterProbablilty




def vigenere_encrypt(filename, out_filename, cypher, alphabet, print_out=True, write_file = False):
    with open(filename, "r") as file:
        cleartext = file.read().lower()
    cleartext = [i for i in cleartext if i in alphabet]
    file_len = len(cleartext)
    cypher_len = len(cypher)
    adj_cypher = cypher*((file_len // cypher_len) + 1)


    cyphertext = ""
    for i in range(file_len):
        cyphertext += alphabet[(alphabet.index(cleartext[i])  + alphabet.index(adj_cypher[i])) % len(alphabet)]

    if print_out == True:
        print(cyphertext)

    if write_file == True:
        with open(out_filename, "w") as file:
            file.write(cyphertext)
    return cyphertext

def compliance_index(text, alphabet):
    text_len = len(text)
    letter_count = {}
    for i in alphabet:
        letter_count[i] = text.count(i)

    compliance_index_value = 0
    for i in letter_count.keys():
        compliance_index_value += letter_count[i]*(letter_count[i] - 1)
    compliance_index_value = compliance_index_value / (text_len * (text_len - 1))
    return compliance_index_value


def split_text(text, step):
    return_array = []
    for i in range(step):
        return_array.append(text[i::step])
    return return_array

def kron_delta(a, b):
    return int(a==b)

def find_D(text, alphabet, step):
    D = 0
    for i in range(len(text) - step):
        D += kron_delta(alphabet.index(text[i]), alphabet.index(text[i + step]))
    return D

def get_vigenere_prob(cyphertext, alphabet, step, letter_count):
    letter_array = []
    popular_letters = []
    result = []
    for i in range(step):
        for j in range(i, len(cyphertext), step):
                letter_array.append(cyphertext[j])
        popular_letters.append(letter_array)
        letter_array = []
    for i in popular_letters:
        result.append(dict(collections.Counter(i)))
    # print(result)

    return result


def get_vigenere_key(cleartext_letter_prob, cyphertext_letter_prob, alphabet):


    key = ""
    print(len(cyphertext_letter_prob))
    for i in cyphertext_letter_prob:

        i = sorted(i.items(), key=lambda x:x[1], reverse=True)
    
        key += alphabet[(alphabet.index(i[0][0] ) - 14) % len(alphabet)]


    print("looks like your key is: ")

    for i in key:
        print(i.ljust(3, " "), end="")
    print("")
    for i in range(len(key)):
        print(str(i).ljust(3, " "), end="")
    print("")
    key = [ i for i in key]
    backup_key = key
    print("to return to backup key enter 'b'")

    while 1:
        choise = input("to change letter enter its index, to exit enter '-': ")
        if choise == "-":
            break
        if choise == 'b':
            key = backup_key
            continue

        choise_index = input("enter new index: ")
        key[int(choise)] = alphabet[( alphabet.index( list(cyphertext_letter_prob[int(choise)].keys())[int(choise_index)]) - alphabet.index('о') ) % len(alphabet)]

        for i in key:
            print(i.ljust(3, " "), end="")
        print("")
        for i in range(len(key)):
            print(str(i).ljust(3, " "), end="")
        print("")


    return key


def decrypt_vigenere(cyphertext, alphabet, key):
    cleartext = ""

    key_adj = key * (len(cyphertext) // len(key) + 1)

    for i in range(len(cyphertext)):
        cleartext += alphabet[ alphabet.index(cyphertext[i]) - alphabet.index(key_adj[i]) %  (len(alphabet))]
    print(cleartext)
    return cleartext


def main():
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    alphabet = [i for i in alphabet]
    filename = "cleartext.txt"
    key2 = "из"
    key3 = "воз"
    key4 = "раст"
    key5 = "еряша"
    key_big = "чашкаиложкаичай"
    key_big_big = "оченьнеимовернобольшойключ"
    cyphertext = vigenere_encrypt(filename, "test", key_big_big, alphabet, print_out=False)

    with open(filename, "r") as file:
        text = file.read()


    text = [i for i in text if i in alphabet]
    text=  "".join(text)
    print("real compl: ",compliance_index(text, alphabet))


    letter_probability = GetProbability(filename, alphabet)



    with open("cypher.txt", "r") as file:
        work_text = file.read()
        work_text = work_text.replace("\n","").lower()
        work_text= work_text.replace('ё','е')

    for i in range(1,31):
        key2_splitted = split_text(work_text, i)
        print(f"{i}: ",compliance_index(key2_splitted[0], alphabet))

    work_text = [i for i in work_text if i in alphabet]
    # print(work_text)
    choise =  ""
    while choise != "-":
        prob = get_vigenere_prob(work_text, alphabet, 14, letter_probability)
        key = get_vigenere_key(letter_probability, prob, alphabet)
        choise = input("to print small part of text enter p, to continue enter c, to exit enter -: ")
        if choise == "p":
            decrypt_vigenere(work_text, alphabet, key)
        if choise == "c":
            continue

    step = 14
    prob_step = 28

    return
 




if __name__ == "__main__":
    main()
