def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def find_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m

def bigram_to_number(birgam):
    number = alphabet.find(birgam[0]) * 31 + alphabet.find(birgam[1])
    return number
def number_to_birgam(number):
    a = number // 31
    b = number % 31
    return a, b

def find_chiper_birgam(text):
    bigram_no_cross = {}
    for i in range(0, len(text) - 1, 2):
        pair = text[i: i + 2]
        if pair != '':
            if pair not in bigram_no_cross:
                bigram_no_cross[pair] = 1
            else:
                bigram_no_cross[pair] += 1
    return bigram_no_cross


def linear_congruence_solver(a, b, n):
    d = extended_gcd(a, n)
    if d[0] > 1:
        if b % d[0] != 0:
            return None
        else:
            solutions = []
            a1, b1, n1 = a // d[0], b // d[0], n // d[0]
            x0 = linear_congruence_solver(a1, b1, n1)
            if x0 is not None:
                for i in range(d[0]):
                    solutions.append((x0[0] + i * n1) % n)
            return solutions
    else:
        a_inv = find_inverse(a, n)
        if a_inv is not None:
            x = (a_inv * b) % n
            return [x]
        else:
            return None

def find_a_and_b(y1, y2):
    a = []
    b = []
    for bigram_x1 in open_text_bigram:
        for bigram_x2 in open_text_bigram:
            if bigram_x1 != bigram_x2:
                number_x1, number_x2 = bigram_to_number(bigram_x1), bigram_to_number(bigram_x2)
                temp_a = linear_congruence_solver(number_x1-number_x2, y1-y2, 31*31)
                if temp_a is not None:
                    a += temp_a
                    for a_value in temp_a:
                        b_value = (y1 - a_value*number_x1) % (31*31)
                        b.append(b_value)
    return a, b

def valid_text(text):
    forbiden_bigrams = ['аь', 'эь', 'ыь', 'иь', 'юь', 'оь', 'уь', 'еь', 'яь', 'ьь', 'йь']
    for bigram in forbiden_bigrams:
        if bigram in text:
            return False
    return True

if __name__ == '__main__':
    alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
    open_text_bigram = ['ст', 'но', 'то', 'на', 'ен']
    chiper_text_bigram = []
    solutions_a = []
    solutions_b = []
    with open('D:/study/5th_sem/крипта/crypto-23-24/tasks/cp3/variants.utf8/06.txt', 'r', encoding='utf-8') as f:
        text = f.read().replace("\n", '')
    bigram = find_chiper_birgam(text)
    sorted_dict = dict(sorted(bigram.items(), key=lambda item: item[1], reverse=True))
    chiper_text_bigram = list(sorted_dict.keys())[:12]
    for bigram_y1 in chiper_text_bigram:
        for bigram_y2 in chiper_text_bigram:
            if bigram_y1 != bigram_y2:
                number_y1, number_y2 = bigram_to_number(bigram_y1), bigram_to_number(bigram_y2)
                temp_result = find_a_and_b(number_y1, number_y2)
                solutions_a += temp_result[0]
                solutions_b += temp_result[1]
    decrypted_text = []
    for i in range(0, len(text) - 1, 2):
        pair = text[i: i + 2]
        decrypted_text.append(pair)

    for i in range(len(solutions_a)):
        encrypted_text = []
        try:
            a_inv = find_inverse(solutions_a[i], 31 * 31)
            for j in range(len(decrypted_text)):
                number_y_j = bigram_to_number(decrypted_text[j])
                temp = a_inv*(number_y_j - solutions_b[i]) % (31*31)
                temp = number_to_birgam(temp)
                bigram = alphabet[temp[0]] + alphabet[temp[1]]
                encrypted_text.append(bigram)
            string = ''.join(encrypted_text)
            check = valid_text(string)
            if check:
                print(f"Key: a = {solutions_a[i]}, b = {solutions_b[i]}")
                print("Possible text:")
                print(string)
        except:
            continue













