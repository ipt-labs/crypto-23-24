# coding=utf-8

alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
def gcdd(a, b):
    if a==0:
        return b, 0, 1
    else:
        g, x, y = gcdd(b % a, a)
        return g, y-x*(b//a), x

def mod_minus1(a, m):
    g, x, y = gcdd(a, m)
    if g != 1:
        return None
    else:
        return (x % m + m)%m

def count_bigram_frequency(text):
    text = ''.join([char.lower() for char in text if char.isalpha() or char.isspace()])
    bigram_frequency = {}
    for i in range(0, len(text) - 1, 2):
        bigram = text[i:i + 2]
        if bigram in bigram_frequency:
            bigram_frequency[bigram] += 1
        else:
            bigram_frequency[bigram] = 1
    return bigram_frequency

def find_possible_keys(encrypted_text):
    bigram_frequency = count_bigram_frequency(encrypted_text)
    top5_bigrams = [item[0] for item in sorted(bigram_frequency.items(), key=lambda item: item[1], reverse=True)[:5]]
    bigrams = ["то", "на", "ст", "но", "по"]
    possible_keys = []
    for i in range(len(bigrams)):
        for j in range(len(top5_bigrams)):
            for k in range(len(bigrams)):
                for n in range(len(top5_bigrams)):
                    x1 = (alphabet.index(bigrams[i][0])*31 + alphabet.index(bigrams[i][1]))%961
                    y1 = (alphabet.index(top5_bigrams[j][0])*31 + alphabet.index(top5_bigrams[j][1]))%961

                    x2 = (alphabet.index(bigrams[k][0])*31 + alphabet.index(bigrams[k][1]))%961
                    y2 = (alphabet.index(top5_bigrams[n][0])*31 + alphabet.index(top5_bigrams[n][1]))%961

                    mod_i = mod_minus1(x1 - x2, 961)
                    if mod_i is not None:
                        a_i = (y1 - y2)*mod_i % 961
                        b_i = (y1 - x1*a_i)%961
                        possible_keys.append((a_i, b_i))
    return possible_keys

def text_maye_sens(input_text):
    bigrams_not_exist = ["аь", "йь", "щз", "жф", "ьь"]
    text = [input_text[i:i + 2] for i in range(0, len(input_text) - 1, 2)]
    for bigram in bigrams_not_exist:
        if bigram in text:
            return False
    return True

def decrypt_afinne(input_text, key, i):
    with open(input_text, 'r', encoding='utf-8') as file:
        encrypted_text = file.read()
    text = [encrypted_text[i:i + 2] for i in range(0, len(encrypted_text) - 1, 2)]
    a, b = key
    mod_minus1_a = mod_minus1(a, 961)
    if mod_minus1_a is not None:
        decrypted_text = ""
        for bigram in text:
            y = (alphabet.index(bigram[0])*31 + alphabet.index(bigram[1]))%961
            x = (mod_minus1_a *(y - b))%961
            d_index1 = x//31
            d_index2 = x%31
            d_char1 = alphabet[d_index1]
            d_char2 = alphabet[d_index2]
            decrypted_text += d_char1
            decrypted_text += d_char2
        if text_maye_sens(decrypted_text):
            output_file = f"decrypted{key}.txt"
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(decrypted_text)

with open(r'081.txt', 'r', encoding='utf-8') as file:
    text = file.read()
print("Найчастіші біграми в тексті:")
bigram_frequency = count_bigram_frequency(text)
top5_bigrams_encrypted = [bigram for bigram, i in sorted(bigram_frequency.items(), key=lambda item: item[1], reverse=True)[:5]]
print(top5_bigrams_encrypted)
keys = find_possible_keys(text)
print("Можливі ключі:")
print(keys)
i = 0
for key in keys:
    decrypt_afinne(r'081.txt', key, i)
    i += 1
print("Можливі варіанти розшифрованого тексту збережені у файли decrypted[ключ].txt")

