import frequency_lists_creator as flc


# Алфавіт з поміняними ы та ь місцями
alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'

# Отримуємо шифртекст
with open('01.txt', 'r', encoding='utf-8') as file:
    text = file.read().replace('\n', '')

# Записуємо відредагований
with open('01.txt', 'w', encoding="UTF-8") as writer:
    writer.write(text)


#############################
# 1 пункт

# Функція для розширеного алгоритму Евкліда
def extended_euclid(a, b):
    # Повертає d=НСД(x,y) і x, y такі, що ax + by = d
    if (b == 0):
        return a, 1, 0
    d, x, y = extended_euclid(b, a % b)
    return d, y, x - (a // b) * y


# Функція для знаходження оберненого a за модулем m
def mod_inverse(a, m):
    gcd, x, y = extended_euclid(a, m)
    if gcd != 1:
        return None
    else:
        return x % m if x < 0 else x


# Функція для розв'язування порівнянь (лінійних конгруенцій)
def solve_linear_congruence(a, b, m):
    gcd, x, y = extended_euclid(a, m)
    if b % gcd != 0:
        return None
    inverse = mod_inverse(a // gcd, m // gcd)
    x0 = (inverse * (b // gcd)) % (m // gcd)

    ans = []
    for i in range(gcd):
        solution = (x0 + i * (m // gcd)) % m
        ans.append(solution)

    return ans


#############################
# 2 пункт

# Використовуючи функції з минулої лабораторної отримуємо 5 найчастіших біграм
flc.bigrams_frequency('01.txt', 'bigrams_frequency.csv', 2)
fr_bigrams = list(flc.get_frequency('bigrams_frequency.csv').keys())


#############################
# 3 пункт

# Найчастіші біграми для рос мови
most_fr_bigrams = ['ст', 'но', 'ен', 'то', 'на']

# Зробимо список пар пар та приберемо повторювані
pairs_of_bigrams = [(f, s) for f in most_fr_bigrams for s in fr_bigrams]
pairs_of_pairs = list(set([tuple(sorted((f, s))) for f in pairs_of_bigrams for s in pairs_of_bigrams if f[0]!=s[0] and f[1]!=s[1]]))

# Знайдемо можливі кандидати на ключі
poss_keys = []

for p in pairs_of_pairs:
    x1 = alphabet.index(p[0][0][0]) * 31 + alphabet.index(p[0][0][1])
    y1 = alphabet.index(p[0][1][0]) * 31 + alphabet.index(p[0][1][1])

    x2 = alphabet.index(p[1][0][0]) * 31 + alphabet.index(p[1][0][1])
    y2 = alphabet.index(p[1][1][0]) * 31 + alphabet.index(p[1][1][1])

    cong = solve_linear_congruence(x1 - x2, y1 - y2, 31 ** 2)
    if cong:
        poss_keys += [(a, (y1 - a * x1) % (31 ** 2)) for a in cong]

# Прибираємо повторювані кандидати на ключ
poss_keys = set(poss_keys)

#############################
# 4 пункт


# Функція для дешифрування тексту за ключем
def decrypt(ciphertext, key):
    a, b = key
    decrypted_bigrams = ""
    for i in range(0, len(ciphertext) - 1, 2):
        inverted = mod_inverse(a, 31 ** 2)
        if inverted is None:
            return None

        y = alphabet.index(ciphertext[i]) * 31 + alphabet.index(ciphertext[i + 1])
        x = (inverted * (y - b)) % (31 ** 2)
        decrypted_bigrams += (alphabet[x // 31] + alphabet[x % 31])
    return decrypted_bigrams


# Неможливі біграми
bad_bigrams = ['иь', 'юь', 'йь', 'оь', 'йы', 'яь', 'ыю', 'ыь', 'ьь', 'аы', 'юы', 'еь', 'еы', 'хь', 'аь', 'ць', 'ыы', 'яы', 'оы', 'эы', 'кь', 'уь', 'йй', 'уы', 'иы', 'эь']

# Перевіряємо всі розшифровані тексти на наявність недопустимих біграм і повертаємо той, що без них
for k in poss_keys:
    dec_text = decrypt(text, k)
    if dec_text is None:
        continue
    else:
        for b in bad_bigrams:
            if b in dec_text:
                break
        else:
            print(f"Ключ: {k}")
            print(dec_text)
