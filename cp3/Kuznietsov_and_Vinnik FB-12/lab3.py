import re

global array_with_a, array_with_b

def filter():
    with open("02.txt", 'r', encoding='utf-8') as file:
        text = file.read()

    # Робимо всі букви маленькими
    text = text.lower()

    # Прибираєм все, що не входить в російський алфавіт, лишаєм пробіли
    text = re.sub(r'[^\sа-я]', '', text)

    # Прибираємо подвійні пробіли, або всі пробіли
    text = re.sub(r'\s+', '', text)

    with open("02.txt", 'w', encoding='utf-8') as file:
        file.write(text)

#filter()

def chastota_bigram():
    with open("02.txt", 'r', encoding='utf-8') as file:
        text = file.read()

    dictionary = {}
    array = []

    for i in range(0, len(text), 2):
        bigram = text[i:i + 2]
        if len(bigram) == 2:
            array.append(bigram)

    for i in array:
        if i in dictionary:
            dictionary[i] += 1
        else:
            dictionary[i] = 1

    #print(dictionary)

    # Cортування біграм в спадному орядку
    sorted_dictionary = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    sorted_dictionary = dict(sorted_dictionary)

    print(f"Відсортована частота біграм : {sorted_dictionary}")

chastota_bigram()

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def keys():

    global array_with_a, array_with_b

    #Алфавіт
    #0 а / 1 б / 2 в / 3 г /4 д / 5 е / 6 ж / 7 з / 8 и / 9 й / 10 к /11 л / 12 м/ 13 н/ 14 о / 15 п / 16 р / 17 с / 18 т
    # / 19 у / 20 ф / 21 х / 22 ц / 23 ч / 24 ш / 25 щ / 26 ы / 27 ь / 28 э / 29 ю / 30 я

    # ст - 545 / но - 417 / то - 572 / на - 403 / ен - 168
    X = [545, 417, 572, 405, 168]

    # йа - 279 / юа - 899 / чш - 737 / юд - 903 / рщ - 521 Y
    Y = [279, 899, 737, 903, 521]

    all_combinations = []

    for x1 in X:
        for y1 in Y:
            remaining_X = [x for x in X if x != x1]
            remaining_Y = [y for y in Y if y != y1]
            for x2 in remaining_X:
                for y2 in remaining_Y:
                    combination = (x1, y1, x2, y2)
                    all_combinations.append(combination)

    array_with_a = []
    array_with_b = []

    # a = (y1 - y2) * (x1 - x2)^(-1) mod m^2
    for combination in all_combinations:
        x1 = combination[0]
        x2 = combination[2]

        y1 = combination[1]
        y2 = combination[3]

        res_gcd, x, y = extended_gcd(31**2, x1-x2)
        #print(res_gcd, x, y)
        if res_gcd == 1:
            a = ((y1-y2)*y) % (31**2)
            array_with_a.append(a)
            b = (y1 - a*x1) % (31**2)
            array_with_b.append(b)
        if res_gcd > 1:
            if ((y1-y2) % res_gcd) != 0:
                #print("Немає розв'язків")
                pass
            if (abs((y1-y2)) % res_gcd) == 0:
                a1 = abs(x1-x2)/res_gcd
                b1 = abs(y1-y2)/res_gcd
                n1 = (31**2)/res_gcd

                res_gcd1, x, y = extended_gcd(n1, a1)

                x0 = (b1 * y) % n1

                for j in range(int(res_gcd1)):
                    a = x0 + j*n1
                    array_with_a.append(a)
                    b = (y1 - a * x1) % (31 ** 2)
                    array_with_b.append(b)

    print(f"Варінанти можливого 'a': {array_with_a}")
    print(f"Варінанти можливого 'b': {array_with_b}")

keys()

def convert_bigram_to_numbers():
    with open("02.txt", 'r', encoding='utf-8') as file:
        text = file.read()

    array = []
    array_bigram_to_numbers = []
    letter_to_number_dictionary = {
        'а': 0,
        'б': 1,
        'в': 2,
        'г': 3,
        'д': 4,
        'е': 5,
        'ж': 6,
        'з': 7,
        'и': 8,
        'й': 9,
        'к': 10,
        'л': 11,
        'м': 12,
        'н': 13,
        'о': 14,
        'п': 15,
        'р': 16,
        'с': 17,
        'т': 18,
        'у': 19,
        'ф': 20,
        'х': 21,
        'ц': 22,
        'ч': 23,
        'ш': 24,
        'щ': 25,
        'ы': 26,
        'ь': 27,
        'э': 28,
        'ю': 29,
        'я': 30
    }

    for i in range(0, len(text), 2):
        bigram = text[i:i + 2]
        if len(bigram) == 2:
            array.append(bigram)

    #print(array)

    for bigram in array:

        #Обираємо літери
        letter1 = bigram[0]
        #print(letter1)
        letter2 = bigram[1]
        #print(letter2)

        #Конвертуєм літери в цифри
        number1 = letter_to_number_dictionary[letter1]
        #print(number1)
        number2 = letter_to_number_dictionary[letter2]
        #print(number2)

        #Знаходим цифровий еквівалент біграмі
        sum = number1 * 31 + number2
        array_bigram_to_numbers.append(sum)

    #print(f"Біграми в цифровому еквіваленті: {array_bigram_to_numbers}")
    return array_bigram_to_numbers

result_array = convert_bigram_to_numbers()

def decrypt(a, b):

    array_decrypted_numbers = []

    for number in result_array:
        res_gcd, x, y = extended_gcd(31 ** 2, a)

        new_number = (y * (number - b)) % (31**2)
        array_decrypted_numbers.append(new_number)

    #print(f"Розшифровані біграми в цифровому еквіваленті: {array_decrypted_numbers}")
    return array_decrypted_numbers

def convert_numbers_to_bigram():
    array_real_bigrams = []

    number_to_letters_dictionary = {
        0: 'а',
        1: 'б',
        2: 'в',
        3: 'г',
        4: 'д',
        5: 'е',
        6: 'ж',
        7: 'з',
        8: 'и',
        9: 'й',
        10: 'к',
        11: 'л',
        12: 'м',
        13: 'н',
        14: 'о',
        15: 'п',
        16: 'р',
        17: 'с',
        18: 'т',
        19: 'у',
        20: 'ф',
        21: 'х',
        22: 'ц',
        23: 'ч',
        24: 'ш',
        25: 'щ',
        26: 'ы',
        27: 'ь',
        28: 'э',
        29: 'ю',
        30: 'я'
    }

    for number in decrypted_array:
        a = number // 31
        b = number % 31

        letter1 = number_to_letters_dictionary[a]
        letter2 = number_to_letters_dictionary[b]
        bigram = letter1 + letter2

        array_real_bigrams.append(bigram)

    #print(f"Розшифровані біграми в цифровому еквіваленті: {array_real_bigrams}")
    return array_real_bigrams

def check_language_1():

    if 'аь' not in result_bigrams \
            and ('еь' not in result_bigrams) \
            and 'иь' not in result_bigrams \
            and 'оь' not in result_bigrams \
            and 'уь' not in result_bigrams \
            and 'ыь' not in result_bigrams \
            and 'ьь' not in result_bigrams \
            and "эь" not in result_bigrams \
            and "юь" not in result_bigrams \
            and "яь" not in result_bigrams \
            and 'аы' not in result_bigrams \
            and 'еы' not in result_bigrams \
            and 'иы' not in result_bigrams \
            and 'оы' not in result_bigrams \
            and 'уы' not in result_bigrams \
            and 'ыы' not in result_bigrams \
            and 'ьы' not in result_bigrams \
            and "эы" not in result_bigrams \
            and "юы" not in result_bigrams \
            and "яы" not in result_bigrams:

        text = ''.join(result_bigrams)
        print(f"Наш ймовірний розшифрований текст: {text}")
        print(f"Наш ймовірний 'a': {a}")
        print(f"Наш ймовірний 'a': {b}")
result = []

for i in range(len(array_with_a)):
    a = array_with_a[i]
    b = array_with_b[i]

    decrypted_array = decrypt(a,b)

    result_bigrams = convert_numbers_to_bigram()

    check_language_1()
