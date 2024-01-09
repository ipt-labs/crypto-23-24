from collections import defaultdict

alpha = "абвгдежзийклмнопрстуфхцчшщьыэюя"
m = 31
  
    
def egcd(a, b):
    u0, u1 = 1, 0
    v0, v1 = 0, 1

    while a != 0:
        q = b // a
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
        a, b = b % a, a

    return b, v0, u0


def inverse_elem(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m
    

def congruence(a, b, n):

    d, x, y = egcd(a, n)
    all_x = []

    if d == 1:
        x = (inverse_elem(a, n) * b) % n
        all_x.append(x)
    else:
        if b % d != 0:
            return None
        else:
            a1 = a // d
            b1 = b // d
            n1 = n // d

            x0 = (inverse_elem(a1, n1) * b1) % n1

            for i in range(d):
                x = x0 + i * n1
                all_x.append(x)

    return all_x
        
    
# This function calculates frequncies of bigrams and sorts them
def count_bigram(text):
    bigram_count = 0
    bigram_pair = defaultdict(float)

    for i in range(0, len(text) - 1, 2):
        non_overlapping_bigram = text[i:i + 2]
        bigram_pair[non_overlapping_bigram] += 1
        bigram_count += 1

    for key, value in bigram_pair.items():
        bigram_pair[key] /= bigram_count

    sorted_bigrams = sorted(bigram_pair.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_bigrams)


# This function calculates bigrams corresponding number 
def bigram_number(a, b):
    number = (alpha.index(a))*m + alpha.index(b)
    return number


# This function transforms number back to bigram
def number_to_bigram(X):
    b = X % m
    a = X // m
    return alpha[a] + alpha[b]


# This function checks if text is meaningful
def check_text(text):

    bigrams = ["гь", "йь", "уы", "ьы", "йь"]      #"зп", "зщ", "йь", "оы", "уы", "уь", "шщ", "ьы"
    for bigram in bigrams:
        if bigram in text:
            return False
    return True

file_input = input("Input file: ")
file_output = input("Output file: ")
with open(file_input, "r") as file_input:

    text = file_input.read()
print(text)
bigrams = count_bigram(text)
list_bigrams = [key for key, value in bigrams.items()][0:5]
print("Most frequent bigrams in ciphertext are: ", list_bigrams)

bigrams_text = []

for bigram in list_bigrams:
    number = bigram_number(bigram[0], bigram[1])
    bigrams_text.append(number)

bigrams_lang = [bigram_number('с', 'т'), bigram_number('н', 'о'), bigram_number('т', 'о'), bigram_number('н', 'а'), bigram_number('е', 'н')]    # Most frequent bigrams in language

# Finding keys 
keys = []
for i in range(0, 5):
    for j in range(0, 5):
        for k in range(0, 5):
            for l in range(0, 5):
                if i != k and j != l:
                    X1_X2 = (bigrams_lang[i] - bigrams_lang[k]) % m**2
                    Y1_Y2 = (bigrams_text[j] - bigrams_text[l]) % m**2
                    inverse = congruence(X1_X2, Y1_Y2, m**2)
                    if inverse is not None:
                        for a in inverse:
                            b = (bigrams_text[j] - a*bigrams_lang[i]) % m**2
                            pair = [a, b]
                            keys.append(pair)

unique_keys = list(set(map(tuple, keys)))
print("Number of candidates:", len(unique_keys))
print("Result in dec_result.txt file")

with open(file_output, "w") as file_output:

    for pair in unique_keys:
        decrypted_text = ""
        a = pair[0]
        b = pair[1]
        for i in range(0, len(text) - 1, 2):
            bigram = text[i:i + 2]
            if inverse_elem(a, m**2) is not None:
                X = congruence(a, (bigram_number(bigram[0], bigram[1]) - b) % m**2, m**2)
                if X[0] is None:
                    continue
                decrypted_text += number_to_bigram(X[0])
               

        if check_text(decrypted_text) == True:
            file_output.write(f"Key ({a}, {b}): {decrypted_text}\n")


# 5 most frequent bigrams in ciphertext
# цл:0.014362151506617854
# ял:0.01379892987890735
# ае:0.012109264995775838
# ле:0.011827654181920586
# чо:0.01098282174035483