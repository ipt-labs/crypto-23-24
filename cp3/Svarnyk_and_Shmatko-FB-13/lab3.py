from math import floor
alphabet = 'абвгдежзийклмнопрстуфхцчшщыьэюя'
enum_alphabet = dict(enumerate(alphabet))
letter_indexes_alphabet = {alphabet[i]: i for i in range(len(alphabet))}
with open("lab3_variant17.txt", "r", encoding="utf-8") as f:
    txt = f.read()

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError('modular inverse does not exist')
    else:
        return x % m


def text_preparing(text):
    filtered = "".join([x for x in text if x in 'абвгдежзийклмнопрстуфхцчшщьыэюя'])
    return filtered


def bigram_frequency(text):
    all_bigrams = []
    for idx in range(0, len(text) - 1, 2):
        bigram = text[idx: idx + 2]
        all_bigrams.append(bigram)
    unique_bigrams = set(all_bigrams)
    bigrams_frequency_dict = {bigram: all_bigrams.count(bigram) for bigram in unique_bigrams}
    return bigrams_frequency_dict, all_bigrams


def handle_bigram(lst):  # з біграми в число
    nums = []
    for i in range(len(lst)):
        nums.append(letter_indexes_alphabet[lst[i][0]] * 31 + letter_indexes_alphabet[lst[i][1]])
    return nums


def handle_nums(lst):  # з числа в біграму
    bigrams = []
    for i in range(len(lst)):
        bigram = enum_alphabet[floor(lst[i] / 31)] + enum_alphabet[lst[i] % 31]
        bigrams.append(bigram)
    text = "".join(bigrams)
    return text


def find_all_combinations_of_bigram():
    combs = []
    for i in most_freq_bigram_nums:
        for j in most_freq_bigram_cipher_nums:
            for k in most_freq_bigram_nums:
                for n in most_freq_bigram_cipher_nums:
                    if j != n and i != k:
                        combs.append((i, j, k, n))
    return combs


def find_possible_key(lst):
    keys = []
    modulo = 31**2
    for i in range(len(lst)):  # по всіх комбінаціях рахуємо свій ключ
        x1, y1, x2, y2 = lst[i]
        try:
            # a = (y1-y2)*(x1-x2)^-1 mod m^2
            a = (y1-y2) * modinv((x1-x2), modulo) % modulo  #обернене по модулю через АЕ
            b = (y1 - a*x1) % modulo  # b = (y1-a*x1) mod m^2
            keys.append((a, b))
        except ValueError:
            pass 
    return keys


def check_text(text_to_check):  # біграми брав звідси,але фінальний список підігнав під результат
    forbidden_bigrams = ['щч', 'чй', 'шй', 'жщ', 'жш', 'жц', 'ыь', 'жй',
                        'жы', 'пй', 'жя', 'зй', 'нй', 'цй', 'щх', 'щц',
                        'кй', 'цщ', 'мй', 'щй', 'щэ', 'щы', 'щю', 'щя',
                        'йй', 'гй', 'хй', 'тй', 'чщ', 'юь', 'юы', 'эь',
                        'эы', 'бй', 'хщ', 'дй', 'фй']
    for fibgram in forbidden_bigrams:
        if fibgram in text_to_check:
            return False
    return True


def decode(keys, bgrams):
    modulo = 961
    # k = [(470, 312)] ключ для нашого варіанту
    for key in keys:
        decoded_bigrams = []
        try:
            inverse_a = modinv(key[0], modulo)
            b = key[1]
        except ValueError:  # ValueError може бути коли pow не може порахувати обернений,бо його не існує
            pass
        for bigram in bgrams:
            decoded_bigram = (bigram-b)*inverse_a % modulo  # Xi = (Yi-b)*a^-1 mod m^2 формула
            decoded_bigrams.append(decoded_bigram)
        decoded_text = handle_nums(lst=decoded_bigrams)
        if check_text(text_to_check=decoded_text) is True:  # check_text перевіряє чи є невалідні біграми в тексті
            with open("result_lab3_var17.txt", "w", encoding="utf-8") as file:
                file.write(decoded_text)
            print(f"ключ : {key}")
            print(f"текст : {decoded_text}")


data = text_preparing(text=txt)
count_dict, cipher_bigrams = bigram_frequency(text=data)
most_freq_bigram = ["ст", "но", "то", "на", "ен"]
most_freq_bigram_cipher = ['вк', 'нв', 'ья', 'юв', 'пк']
most_freq_bigram_nums = handle_bigram(lst=most_freq_bigram)
most_freq_bigram_cipher_nums = handle_bigram(lst=most_freq_bigram_cipher)
all_possible_combinations = find_all_combinations_of_bigram()
all_keys = set(find_possible_key(lst=all_possible_combinations))  # set бо ключі повторяються
cipher_bigrams_nums = handle_bigram(lst=cipher_bigrams)
decode(keys=all_keys, bgrams=cipher_bigrams_nums)

# for i in range(5):
#     most_frequent = max(count_dict,key=count_dict.get)
#     most_freq_bigram_cipher.append(most_frequent)
#     count_dict[most_frequent] = 0
# print(most_freq_bigram_cipher)
