from collections import Counter

def ReadText(filename, encoding):
    with open(filename, 'r', encoding=encoding) as file:
        file_contents = file.read()
        file_contents = file_contents.lower()

    file_contents = file_contents.replace(",", "")
    file_contents = file_contents.replace("!", "")
    file_contents = file_contents.replace("?", "")
    file_contents = file_contents.replace("=", "")
    file_contents = file_contents.replace("-", "")
    file_contents = file_contents.replace("", "")
    file_contents = file_contents.replace(".", "")
    file_contents = file_contents.replace(":", "")
    file_contents = file_contents.replace(";", "")
    file_contents = file_contents.replace("1", "")
    file_contents = file_contents.replace("2", "")
    file_contents = file_contents.replace("3", "")
    file_contents = file_contents.replace("4", "")
    file_contents = file_contents.replace("5", "")
    file_contents = file_contents.replace("6", "")
    file_contents = file_contents.replace("7", "")
    file_contents = file_contents.replace("8", "")
    file_contents = file_contents.replace("9", "")
    file_contents = file_contents.replace("0", "")
    file_contents = file_contents.replace(" ", "")
    file_contents = file_contents.replace("'", "")
    file_contents = file_contents.replace("\n", "")
    file_contents = file_contents.replace("ъ", "ь")
    file_contents = file_contents.replace("ё", "е")
    file_contents = file_contents.replace("«", "")
    file_contents = file_contents.replace("»", "")
    file_contents = file_contents.replace("…","")
    file_contents = file_contents.replace("„", "")
    file_contents = file_contents.replace("“", "")
    file_contents = file_contents.replace("—", "")
    file_contents = file_contents.replace("*", "")
    return file_contents
def CountFreq(letter, text):
    len_text = len(text)
    freq = text.count(letter)/len_text
    return freq

def RussianCheck(text):  #works good only with large texts or increase difference for smaller ones
    alphabet = "абвгдежзийклмнопрстуфхцчшщыьэюя"
    alphabet_letter_frequencies = [
        0.0801, 0.0159, 0.0454, 0.0165, 0.0298, 0.0849, 0.0072, 0.016, 0.0735,
        0.0106, 0.0321, 0.0497, 0.0333, 0.067, 0.1097, 0.0281, 0.0473, 0.0547, 0.0626,
        0.0262, 0.0026, 0.0097, 0.0048, 0.0144, 0.0073, 0.0061, 0.019, 0.0178,
        0.0032, 0.0064, 0.0201
    ]

    freq = []
    i = 0
    while i < len(alphabet):
        freq.append(CountFreq(alphabet[i],text))
        i = i + 1

    difference = 0
    i = 0
    while i < len(alphabet_letter_frequencies):
        difference = difference + abs(alphabet_letter_frequencies[i] - freq[i])
        i = i + 1
    # any(bigram in text for bigram in ['аы', 'аь', 'бй', 'вй', 'гй', 'гф', 'гх', 'дй', 'еы', 'еь', 'жй', 'жф', 'жх', 'жш', 'жщ', 'зй', 'зп', 'зщ', 'иь', 'йа', 'йж', 'йй', 'йь', 'кщ', 'кй', 'лй', 'мй', 'нй', 'оь', 'пв', 'пг', 'пж', 'пз', 'пй', 'сй', 'тй', 'уь', 'фб', 'фж', 'фз', 'фй', 'фп', 'фх', 'фц', 'фщ', 'хж', 'хй', 'хщ', 'хь', 'хю', 'хя', 'цб', 'цж', 'цй', 'цф', 'цх', 'цч', 'цщ', 'ць', 'цю', 'ця', 'чб', 'чг', 'чз', 'чй', 'чп', 'чф', 'чщ', 'чю', 'чя', 'шд', 'шж', 'шз', 'шй', 'шш', 'шщ', 'щб', 'щг', 'щд', 'щж', 'щз', 'щй', 'щл', 'щп', 'щт', 'щф', 'щх', 'щц', 'щч', 'щш', 'щщ', 'щю', 'щя', 'ьа', 'яй', 'ьл', 'ьу', 'ьь', 'юу', 'юь', 'яа', 'яо', 'яь'])
    if difference > 0.25:  #if difference > 0.15 or increase difference for smaller texts
        return False
    else:
        return True

def find_most_frequent_bigrams(input_string):
    pairs = [input_string[i:i + 2] for i in range(0, len(input_string) - 1, 2)]
    pair_counts = Counter(pairs)
    most_frequent_pairs = pair_counts.most_common(10)
    return most_frequent_pairs

def _euclid(a, b):
    if not a:
        return b, 0, 1

    gcd, temp_u, temp_v = _euclid(b % a, a)
    u = temp_v - (b // a) * temp_u #inverse a modulo b
    v = temp_u #inverse b modulo a

    return gcd, u, v

letters = 'абвгдежзийклмнопрстуфхцчшщьыэюя'

def Extended_Euclid(a, b, n):
    a = a % n
    b = b % n
    gcd, u, v = _euclid(a, n)

    if b % gcd != 0:
        return []

    x0 = (u * (b // gcd)) % n

    if x0 < 0:
        x0 = x0 + n

    return [(x0 + i * (n // gcd)) % n for i in range(gcd)]

def From_Bigram_To_Number(bigram):
    # X = x1*m + x2
    m = 31
    x1 = letters.find(bigram[0])
    x2 = letters.find(bigram[1])
    return x1*m + x2

def From_Number_To_Bigram(num):
    m = 31
    # num = x1*m +x2
    x1 = 0
    while (num-m*x1) >= m:
        x1 += 1

    x2 = num - x1*m
    string = letters[x1] + letters[x2]
    return string

def _generate_keys(bigram1, bigram2):
    x1, y1 = From_Bigram_To_Number(bigram1[0]), From_Bigram_To_Number(bigram1[1])
    x2, y2 = From_Bigram_To_Number(bigram2[0]), From_Bigram_To_Number(bigram2[1])
    possible_coef = Extended_Euclid(x1 - x2, y1 - y2, 31**2)
    if len(possible_coef) == 0:
        return
    keys = []
    for coef in possible_coef:
        a = coef
        b = (y1 - a * x1) % (31**2)
        keys.append([a,b])
    return keys

def Generate_keys(default_bigrams, cyph_bigrams):
    bigram_comb = []
    possible_keys = []
    all_bigram_combs = []
    for default_bigram in default_bigrams:
        for cyph_bigram in cyph_bigrams:
            bigram_comb.append([default_bigram, cyph_bigram])

    for i in bigram_comb:
        for j in bigram_comb:
            all_bigram_combs.append([i, j])

    for _ in all_bigram_combs:
        coef = _generate_keys(_[0], _[1])
        if coef is not None:
            for _ in coef:
                possible_keys.append(_)
    return possible_keys


def Decode_bigram(bigram, coef_array):  #coef_array [a,b]
    m = 31**2
    inverse_a = _euclid(coef_array[0], 31**2)[1]
    decoded_number = (inverse_a * (From_Bigram_To_Number(bigram)-coef_array[1]))%m
    return From_Number_To_Bigram(decoded_number)



def Decode(text, coef_array): #coef_array [a,b]
    decoded_text = ""
    i = 0
    while i < len(text)-2:
        decoded_text = decoded_text + Decode_bigram(text[i:i+2], coef_array)
        i = i + 2
    return decoded_text

encoded_text = ReadText("04.txt", "utf-8")
solutions = Generate_keys(["ст", "но", "то", "ен", "ов", "на", "не", "ра", "ли", "ни"], ['еш', 'еы', 'шя', 'ск', 'до', 'зо', 'бж', 'нш', 'жу', 'йк'])
for coefs in solutions:
    temp = Decode(encoded_text, coefs)
    if RussianCheck(temp):
        print(f"Key found: {coefs}")
        print(f"{Decode(encoded_text, coefs)}")
        break
