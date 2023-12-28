import collections
def bigram_freq_nintersec(text):
    bigram_freq = collections.defaultdict(int)
    text_length = len(text)

    for i in range(0, text_length, 2):
        bigram = text[i:i + 2]
        if len(bigram) == 2:
            bigram_freq[bigram] += 1

    tot_bigrams = sum(bigram_freq.values())
    bigram_prob = {bigram: freq / tot_bigrams for bigram, freq in bigram_freq.items()}
    sorted_bigram_prob = dict(sorted(bigram_prob.items(), key=lambda item: item[1], reverse=True))
    return sorted_bigram_prob
def gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = gcd(b % a, a)
        return (g, y - (b // a) * x, x)
def modinv(a, m):
    g, x, y = gcd(a, m)
    if g != 1:
        return None
    else:
        return (x % m + m) % m
def num_big(bigram):
    try:
        return (alphabet.index(bigram[0]) * m + alphabet.index(bigram[1]))
    except ValueError:
        return None
def find_top_5_big(ciphertext):
    sorted_bigram_prob = bigram_freq_nintersec(ciphertext)
    top_5_bigrams = list(sorted_bigram_prob.keys())[:5]
    num_val = [num_big(bigram) for bigram in top_5_bigrams]
    return num_val
def find_keys(m, num_top_bigrams, num2_top_bigrams):
    candidates = set()

    for x1_index, x1 in enumerate(num_top_bigrams):
        for x2_index, x2 in enumerate(num_top_bigrams):
            for y1_index, y1 in enumerate(num2_top_bigrams):
                for y2_index, y2 in enumerate(num2_top_bigrams):
                    if x1_index != x2_index and y1_index != y2_index:
                        try:
                            a_equation = (x1 - x2)
                            y_diff_inv = modinv((y1 - y2), m ** 2)

                            if y_diff_inv is not None and y_diff_inv != 0:
                                a = (a_equation * y_diff_inv) % m ** 2
                                b_equation = (x1 - a * y1) % m ** 2
                                b = b_equation
                                candidates.add((a, b))
                        except TypeError:
                            pass

    return candidates
def decrypt_text(ciphertext, key, alphabet):
    dec_txt = ""
    a, b = key

    for i in range(0, len(ciphertext), 2):
        bigram = ciphertext[i:i + 2]
        num_val = num_big(bigram)
        if num_val is not None:
            a_inv = modinv(a, m ** 2)  # Перевірка на наявність оберненого залишку за модулем
            if a_inv is not None:
                dec_num = (a_inv * (num_val - b)) % m ** 2
                dec_big = alphabet[dec_num // m] + alphabet[dec_num % m]
                dec_txt += dec_big

    return dec_txt
def find_text(ciphertext, forbidden_bigrams):
    freq_count = sum(ciphertext.count(letter) for letter in frequent_letters)
    rare_count = sum(ciphertext.count(letter) for letter in rare_letters)

    for bigram in forbidden_bigrams:
        if bigram in ciphertext:
            return False

    total_bigram_freq = sum(ciphertext.count(ngram) for ngram in forbidden_bigrams)

    # Порогові значення для частоти рідко вживаних літер та сумарної частоти заборонених l-грам
    freq = len(ciphertext) * 0.2  # 20% тексту
    bigram_freq = len(ciphertext) * 0.1  # 10% тексту

    if freq_count > freq or rare_count > freq:
        return True
    elif total_bigram_freq > bigram_freq:
        return False
    else:
        return True

with open('D:\Криптологія\Var20.txt', 'r', encoding='utf-8') as file:
    ciphertext = file.read()

alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
m = 31
language_bigrams = ["ст", "но", "то", "на", "ен"]
frequent_letters = {'о', 'а', 'е'}
rare_letters = {'ф', 'щ', 'ь'}
forbidden_bigrams = ["ьь", "йь", "ьй", "ыь", "ьы"]

num_top_bigrams = find_top_5_big(ciphertext)
top_bigrams = bigram_freq_nintersec(ciphertext)
print("Топ 5 біграм шифртексту:")
print(list(top_bigrams.keys())[:5])
print(num_top_bigrams)
num2_top_bigrams = [num_big(bigram) for bigram in language_bigrams]
print("Топ 5 біграм мови:")
print(language_bigrams)
print(num2_top_bigrams)

candidates = find_keys(m, num_top_bigrams, num2_top_bigrams)
print("Знайдені кандидати в ключі:")
print(f"Усього {len(candidates)}:", candidates)

with open("D:\Криптологія\Var20_dec.txt", "w", encoding="utf-8") as file:
    for candidate in candidates:
        dec_txt = decrypt_text(ciphertext, candidate, alphabet)
        result = find_text(dec_txt, forbidden_bigrams)
        if result and dec_txt:
            print(f"Розшифрований текст для ключа {candidate}:")
            print(dec_txt)

            file.write(dec_txt)
