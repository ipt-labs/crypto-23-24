import re
from collections import Counter

alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"

def filter_text(text):
    text = re.sub(r'[a-zA-Z]', '', text)
    text = text.lower()
    text = text.replace('ё', 'е')
    text = re.sub(r'[^а-яА-Я]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace(" ", "")
    return text


with open("text_cp3.txt", "r", encoding="utf-8") as input_file:
    text = input_file.read()

filtered_text = filter_text(text)

with open("text_cp3_edited.txt", "w", encoding="utf-8") as output_file:
    output_file.write(filtered_text)


def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return (gcd, y - (b // a) * x, x)


def modular_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None
    else:
        return (x % m + m) % m


def count_bigram_frequency(text):
    ngrams = [text[i:i + 2] for i in range(0, len(text) - 1, 2)]
    ngram_frequency = Counter(ngrams)
    total_ngrams = len(ngrams)
    sorted_ngram_frequency = sorted(ngram_frequency.items(), key=lambda x: x[1], reverse=True)
    for ngram, frequency in sorted_ngram_frequency:
        relative_frequency = frequency / total_ngrams
        print(f'"{ngram}" {relative_frequency:.6f}')
    return ngrams


def bigram_to_numeric(bigrams, alphabet):
    numeric_values = []
    for bigram in bigrams:
        index1 = alphabet.index(bigram[0])
        index2 = alphabet.index(bigram[1])
        numeric_value = index1 * len(alphabet) + index2
        numeric_values.append(numeric_value)
    return numeric_values


def find_possible_key(num_values_ciphertext, num_values_language, alphabet):
    key_candidates = []
    for ct_bigram1 in num_values_ciphertext:
        for ct_bigram2 in num_values_ciphertext:
            for lang_bigram1 in num_values_language:
                for lang_bigram2 in num_values_language:
                    if ct_bigram1 != ct_bigram2 and lang_bigram1 != lang_bigram2:
                        try:
                            a = (ct_bigram1 - ct_bigram2) * modular_inverse(lang_bigram1 - lang_bigram2, len(alphabet) ** 2) % (len(alphabet) ** 2)
                            b = (ct_bigram1 - a * lang_bigram1) % (len(alphabet) ** 2)
                            key_candidates.append((a, b))
                        except TypeError:
                            pass
    return key_candidates


def decrypt_text(keys, text, alhabet):
    ngrams = [text[i:i + 2] for i in range(0, len(text) - 1, 2)]
    text_bigrams_numbers = bigram_to_numeric(ngrams, alphabet)
    for key in keys:
        a,b = key
        decrypted_bigrams = []
        modular_inverse_result = modular_inverse(a, len(alphabet) ** 2)
        if modular_inverse_result is None:
            continue
        for bigram in text_bigrams_numbers:
                decrypted_bigram_num = (modular_inverse_result * (bigram - b)) % (len(alphabet) ** 2)
                decrypted_bigrams.append(decrypted_bigram_num)
        decrypted_text = ""
        for value in decrypted_bigrams:
            index1 = value // len(alphabet)
            index2 = value % len(alphabet)
            bigram = alhabet[index1] + alhabet[index2]
            decrypted_text += bigram
        if is_meaningful_text(decrypted_text, invalid_bigrams) is True:
            print(decrypted_text)
            print(f"Наш ключ: {key}")


def is_meaningful_text(txt, bigrams):
    ngrams = [txt[i:i + 2] for i in range(0, len(txt) - 1, 2)]
    for ngram in ngrams:
        if ngram in bigrams:
            return False

    return True



# Частота биграмм в фильтрованном тексте (вариант 11)
# count_bigram_frequency(filtered_text)

# Превращаем биграммы в цифровые значения
ciphertext_bigrams = ["нк", "юж", "хб", "шь", "мк"]
language_bigrams = ["ст", "но", "то", "на", "ен"]
num_values_ciphertext = bigram_to_numeric(ciphertext_bigrams, alphabet)
print(num_values_ciphertext)
num_values_language = bigram_to_numeric(language_bigrams, alphabet)
print(num_values_language)


# Ищем возможные ключи перебором комбинаций биграмм и решения системы конгруенций
key_candidates = set(find_possible_key(num_values_ciphertext, num_values_language, alphabet))
print(f"Возможные ключи: {key_candidates}")

# Ищем ключ перебором всех вариантов текстов (если в тексте есть invalid_bigrams то скорее всего не наш вариант)
invalid_bigrams = set(["ёё", "ёщ", "ыё", "ёу", "йэ", "гъ", "кщ",  "эщ", "щк", "гщ", "щп", "щт", "щш", "щм", "фщ", "щд", "дщ", "чц", "вй", "ёц", "ёэ", "ёа", "шя", "ёе", "йё", "гю", "хя", "йы", "ця", "сй", "хю", "хё", "ёи", "ёо", "яё", "ёя", "ёь", "ёэ", "ъж", "эё", "ъд", "цё", "уь", "щч", "чй", "шй",  "жщ", "жш", "ыъ", "ыь", "жй", "ыы", "жъ", "ъш", "ъщ", "зщ", "ъч", "ъц", "ъу", "ъф", "ъх", "ъъ", "ъы", "ыо", "жя", "зй", "ъь", "ъэ", "еь", "цй", "ьй", "пъ", "еъ", "шъ", "ёы", "ёъ", "ът", "щс", "оь", "къ", "оы", "щщ", "щъ", "щц", "кй", "оъ", "цщ", "лъ", "мй", "шщ", "цъ", "щй", "ъг", "иъ", "ъб", "ъв", "ъи", "ъй", "ъп", "ър", "ъс", "ъо", "ън", "ък", "ъл", "ъм", "иы", "иь", "щэ", "йы", "йъ", "щы", "щю", "щя", "ъа", "мъ", "йй", "гй", "эъ", "уъ", "аь", "чъ", "хй", "тй", "чщ", "ръ", "юъ", "фъ", "аъ", "юь", "аы", "юы", "эь", "эы", "яь", "ьы", "ьь", "ьъ", "яъ", "яы", "хщ", "дй"])
decrypt_text(key_candidates, filtered_text, alphabet)


