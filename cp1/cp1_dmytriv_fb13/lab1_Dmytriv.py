import math 

original_text = 'text.txt'
filtered = 'text_with_spaces.txt'
without_spaces = 'text_without_spaces.txt'

# спершу відфільтруємо текст
with open(original_text, 'r', encoding='utf-8') as t:
    with open(filtered, 'w', encoding='utf-8') as t1:
        str_text = t.read()  
        # Залишаємо букви та пробіли і всі букви робимо в нижньому регістрі
        changed = ''.join(e.lower() if e.isalpha() and e in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя " or e.isspace() else ' ' for e in str_text)
        changed1 = changed.replace('ё', 'е')
        changed2 = changed1.replace('ъ', 'ь')
        changed3 = " ".join(changed2.split())

        t1.write(changed3)

#текст без пробілів
with open(filtered, 'r', encoding='utf-8' ) as f:
    data = f.read()
res = data.replace(' ', '')
with open(without_spaces, 'w', encoding='utf-8') as ws:
    ws.write(res)

#напишемо функцію для обрахунку частоти букв в тексті і занесення цих даних в файл
def how_often(letters):
    all = "абвгдежзийклмнопрстуфхцчшщыьэюя "
    number_of_letters = len(letters)
    dict_with_res = {element: letters.count(element) / number_of_letters for element in all}

    sorted_dict = dict(sorted(dict_with_res.items(), key=lambda item: item[1], reverse=True))

    return sorted_dict

  
#функція для підрахунку частоти біграм
def how_often_bigram(text, step):
    bigrams = []  
    for num in range(0, len(text) - 1, step):
        bi = text[num: num + 2]
        bigrams.append(bi)

    no_duplicates = set(bigrams)
    res = {bigram: bigrams.count(bigram) / len(bigrams) for bigram in no_duplicates}
    return res

#спочатку планувалось вносити дані в файл одразу у функціях, але потім з'ясувалось, що краще результатом функції буде словник
#тому напишемо функцію занесення даних зі словника у файл
def save_data(dictionary, file):
    with open(file, "w", encoding="utf-8") as fres:

        for element, frequency in dictionary.items():
            fres.write(f"{element} {frequency}\n")

#напишемо функцію для обрахунку ентропії
def entropy_h1(res_of_freq):
    h1 = -sum(p * math.log2(p) for p in res_of_freq.values() if p > 0)
    return h1

def entropy_h2(entropy):
    h2 = entropy / 2
    return h2

#функція для визначення надлишковості
def redundancy(entropy, len_of_alphabet):
    r = 1 - entropy / math.log(len_of_alphabet, 2)
    return r 


letters_how_often_with_spaces = 'how_often_letter_with_spaces.txt'
letters_how_often_without_spaces = 'how_often_letter_without_spaces.txt'
bi_how_often_with_step1 = 'how_often_bigram_with_step1.txt'
bi_how_often_with_step2 = 'how_often_bigram_with_step2.txt'
bi_how_often_without_step1 = 'how_often_bigram_without_step1.txt'
bi_how_often_without_step2 = 'how_often_bigram_without_step2.txt'


with open(filtered, 'r', encoding='utf-8') as withS:
    text_with_spaces = withS.read()

with open(without_spaces, 'r', encoding='utf-8') as without:
    text_without_spaces = without.read()


#обрахуємо та запишемо у файл частоту літер в тексті з пробілами
ltrs_sp = how_often(text_with_spaces)
save_data(ltrs_sp, letters_how_often_with_spaces)
#обрахуємо та запишемо у файл частоту літер в тексті без пробілів
ltrs = how_often(text_without_spaces)
save_data(ltrs, letters_how_often_without_spaces)

#обрахуємо та запишемо у файл частоту біграм(перетинаються) в тексті з пробілами
bi1_sp = how_often_bigram(text_with_spaces, 1)
save_data(bi1_sp, bi_how_often_with_step1)
#обрахуємо та запишемо у файл частоту біграм(перетинаються) в тексті з без пробілів
bi1 = how_often_bigram(text_without_spaces, 1)
save_data(bi1, bi_how_often_without_step1)

#обрахуємо та запишемо у файл частоту біграм(не перетинаються) в тексті з пробілами 
bi2_sp =  how_often_bigram(text_with_spaces, 2)
save_data(bi2_sp, bi_how_often_with_step2)
#обрахуємо та запишемо у файл частоту біграм(не перетинаються) в тексті без пробілів
bi2 = how_often_bigram(text_without_spaces, 2)
save_data(bi1, bi_how_often_without_step2)

#ентропія
#H1 і R з пробілами 
H1 = entropy_h1(ltrs_sp)
R = redundancy(H1, 32)
print("Ентропія літер в тексі з пробілами: ", H1, " Надлишковість: ", R, '\n')
#H1 і R без пробілів 
H1 = entropy_h1(ltrs)
R = redundancy(H1, 31)
print("Ентропія літер в тексі без пробілів: ", H1, " Надлишковість: ", R, '\n')
#H2 і R з пробілами (перетинаються)
H2 = entropy_h2(entropy_h1(bi1_sp))
R = redundancy(H2, 32)
print("Ентропія біграм(перетинаються) в тексі з пробілами: ", H1, " Надлишковість: ", R, '\n')
#H2 і R без пробілами (перетинаються)
H2 = entropy_h2(entropy_h1(bi1))
R = redundancy(H2, 31)
print("Ентропія біграм(перетинаються) в тексті без пробілів : ", H1, " Надлишковість: ", R, '\n')
#H2 і R з пробілами (не перетинаються)
H2 = entropy_h2(entropy_h1(bi2_sp))
R = redundancy(H2, 32)
print("Ентропія біграм(не перетинаються) в тексі з пробілами: ", H1, " Надлишковість: ", R, '\n')
#H2 і R без пробілами (не перетинаються)
H2 = entropy_h2(entropy_h1(bi2))
R = redundancy(H2, 31)
print("Ентропія біграм(не перетинаються) в тексі без пробілів: ", H1, " Надлишковість: ", R, '\n')



