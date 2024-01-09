import re

alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"


def filter_read(filename: str) -> str:
    with open(filename, "r") as f:
        text = f.read().strip().lower()
    text = re.sub('[^а-я]+', '', text)
    return text


def bigram_freq(text: str, mode: int):
    bigram_dict = {}
    if mode == 1:
        bigram_range = range(len(text) - 1)
    elif mode == 2:
        bigram_range = range(0, len(text) - 1, 2)
    for i in bigram_range:
        bigram = text[i:i + 2]
        if bigram in bigram_dict:
            bigram_dict[bigram] += 1
        else:
            bigram_dict[bigram] = 1
    return bigram_dict


def extended_gcd(a: int, b: int):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x


def modular_inverse(a: int, m: int):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m


def bigram_num(bigram: str):
    l1 = alphabet.index(bigram[0])
    l2 = alphabet.index(bigram[1])
    return l1 * len(alphabet) + l2


def find_keys(num_values_ciphertext: list, num_values_language: list):
    keys = []
    for x1 in num_values_ciphertext:
        for x2 in num_values_ciphertext:
            for y1 in num_values_language:
                for y2 in num_values_language:
                    if x1 != x2 and y1 != y2:
                        if modular_inverse(y1 - y2, len(alphabet) ** 2) is not None:
                            a = (x1 - x2) * modular_inverse(y1 - y2, len(alphabet) ** 2) % (len(alphabet) ** 2)
                            b = (x1 - a * y1) % (len(alphabet) ** 2)
                            keys.append((a, b))

    return keys


def decrypt(keys: set[tuple], text: str):
    for key in keys:
        a, b = key[0], key[1]
        plaintext = ''
        if modular_inverse(a, 31 ** 2) is None:
            continue
        for i in range(0, len(text) - 1, 2):
            x = (modular_inverse(a, 31 ** 2) * (bigram_num(text[i:i + 2]) - b)) % (31 ** 2)
            plaintext += alphabet[x // 31] + alphabet[x % 31]

        found_state = True
        for bigram in impossible_bigrams:
            if bigram in plaintext:
                found_state = False
        if found_state:
            print(f'Ключ: {a, b}')
            return plaintext


text = filter_read("11.txt")
print(f"Топ 5 біграм в тексті: {sorted(bigram_freq(text, 2).items(), key=lambda item: item[1])[::-1][:5]}\n")

text_bigrams = ["нк", "юж", "шь", "хб", "бй"]
rus_bigrams = ["ст", "но", "то", "на", "ен"]
bigrams_num_text = [bigram_num(i) for i in text_bigrams]
bigrams_num_rus = [bigram_num(i) for i in rus_bigrams]

key_list = set(find_keys(bigrams_num_text, bigrams_num_rus))
print(f"Можливі ключі:: {key_list}\n")

impossible_bigrams = ["ёё", "ёщ", "ыё", "ёу", "йэ", "гъ", "кщ", "эщ", "щк", "гщ", "щп", "щт", "щш", "щм", "фщ", "щд",
                      "дщ", "чц", "вй", "ёц", "ёэ", "ёа", "шя", "ёе", "йё", "гю", "хя", "йы", "ця", "сй", "хю", "хё",
                      "ёи", "ёо", "яё", "ёя", "ёь", "ёэ", "ъж", "эё", "ъд", "цё", "уь", "щч", "чй", "шй", "жщ", "жш",
                      "ыъ", "ыь", "жй", "ыы", "жъ", "ъш", "ъщ", "зщ", "ъч", "ъц", "ъу", "ъф", "ъх", "ъъ", "ъы", "ыо",
                      "жя", "зй", "ъь", "ъэ", "еь", "цй", "ьй", "пъ", "еъ", "шъ", "ёы", "ёъ" "ът", "щс", "оь", "къ",
                      "оы", "щщ", "щъ", "щц", "кй", "оъ", "цщ", "лъ", "мй", "шщ", "цъ", "щй", "ъг", "иъ", "ъб", "ъв",
                      "ъи", "ъй", "ъп", "ър", "ъс", "ъо", "ън", "ък", "ъл", "ъм", "иы", "иь", "щэ", "йы", "йъ", "щы",
                      "щю", "щя", "ъа", "мъ", "йй", "гй", "эъ", "уъ", "аь", "чъ", "хй", "тй", "чщ", "ръ", "юъ", "фъ",
                      "аъ", "юь", "аы", "юы", "эь", "эы", "яь", "ьы", "ьь", "ьъ", "яъ", "яы", "хщ", "дй"]
with open("11_result.txt", "w") as f:
    f.write(decrypt(key_list, text))
