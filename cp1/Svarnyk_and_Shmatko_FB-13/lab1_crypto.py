import math

file_letter_freq_w_whitespaces = 'sorted_letter_freq_w_whitespaces.txt'
file_letter_freq_w_o_whitespaces = 'sorted_letter_freq_w_o_whitespaces.txt'

file_bigram_freq_w_whitespaces_w_inner = 'sorted_bigram_freq_w_whitespaces_w_inner.txt'
file_bigram_freq_w_o_whitespaces_w_inner = 'sorted_bigram_freq_w_o_whitespaces_w_inner.txt'

file_bigram_freq_w_whitespaces_w_o_inner = 'sorted_bigram_freq_w_whitespaces_w_o_inner.txt'
file_bigram_freq_w_o_whitespaces_w_o_inner = 'sorted_bigram_freq_w_o_whitespaces_w_o_inner.txt'


def text_preparing():
    with open("lab_1_txt.txt","r",encoding="utf-8") as f:
        data = f.read()
        formatted = "".join([l if l.isalpha() and l in "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ " else " " for l in data])
        formatted = " ".join(formatted.split())
        formatted = formatted.replace('ё', 'е')
        formatted = formatted.replace('ъ', 'ь')
        formatted = "".join([l.lower() for l in formatted])

    with open("processed_text.txt", "w", encoding="utf-8") as t:
        t.write(formatted)

    return formatted


def deleting_whitespaces(file):
    with open("processed_text_w_o_whitespaces.txt", "w", encoding="utf-8") as w:
        formatted = "".join([x for x in file if x != " "])
        w.write(formatted)
    return formatted


def letter_frequency(text):
    alphabet = "абвгдежзийклмнопрстуфхцчшщыьэюя "
    length = len(text)
    frequency_dict = {letter:text.count(letter)/length for letter in alphabet}
    return frequency_dict


def bigram_frequency(text, step):
    all_bigrams = []
    if step == 1:  # з перетином
        for idx in range(len(text) - 1):
            bigram = text[idx: idx + 2]
            all_bigrams.append(bigram)
    else:  # без перетину
        for idx in range(0, len(text) - 1, 2):
            bigram = text[idx: idx + step]
            all_bigrams.append(bigram)
    unique_bigrams = set(all_bigrams)
    bigrams_frequency_dict = {bigram:all_bigrams.count(bigram)/len(all_bigrams) for bigram in unique_bigrams}
    return bigrams_frequency_dict


def entropy(freq):
    sum = 0
    for prob in freq.values():
        sum -= prob * math.log2(prob)

    return sum / len(list(freq.keys())[0])


def write_to_file(unpacked, name):
    with(open(name, "w", encoding="utf-8")) as file:
        for t in unpacked:
            file.write(f"{t[0]} : {t[1]} \n")
    return unpacked


def format_dict_output(num_to_get,data):
    counter = 0
    for val in data:
        if (counter == num_to_get):
            return
        print(f'{val[0]}: {round(val[1], 10)}')
        counter+=1

        

def handle_data(data=dict, file_name='', whitespace=True):
    if (not whitespace): 
        data.pop(' ')
    
    # посортуємо і запишемо дані у файл
    unpacked = []
    for k in data:
        v = data[k]
        unpacked.append((k, v))
    unpacked.sort(key=lambda a: a[1], reverse=True)
    write_to_file(unpacked, file_name)

    print('Частота')
    # виведемо лише 10 елементів
    format_dict_output(10, unpacked)

    print('Ентропія')
    print(entropy(data))
    print('\n')


#підготуємо текстові дані
text_w_whitespaces = text_preparing()
text_w_o_whitespaces = deleting_whitespaces(text_w_whitespaces)

# виведемо результати
print("Букви в тексті з пробілами")
handle_data(letter_frequency(text_w_whitespaces), file_letter_freq_w_whitespaces)

print("Букви в тексті без пробілів")
handle_data(letter_frequency(text_w_o_whitespaces), file_letter_freq_w_o_whitespaces, False)

print("Біграми в тексті з пробілами з перетином")
handle_data(bigram_frequency(text_w_whitespaces, 1), file_bigram_freq_w_whitespaces_w_inner)

print("Біграми в тексті без пробілів з перетином")
handle_data(bigram_frequency(text_w_o_whitespaces, 1), file_bigram_freq_w_o_whitespaces_w_inner)

print("Біграми в тексті з пробілами без перетину")
handle_data(bigram_frequency(text_w_whitespaces, 2), file_bigram_freq_w_whitespaces_w_o_inner)

print("Біграми в тексті без пробілів без перетину")
handle_data(bigram_frequency(text_w_o_whitespaces, 2), file_bigram_freq_w_o_whitespaces_w_o_inner)

