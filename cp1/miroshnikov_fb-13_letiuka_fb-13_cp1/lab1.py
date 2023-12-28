from edit_text import preprocess_text
import math
import csv

def count_frequency_letter(text, file_name : str):
    with open(f'Labs\Krypt_labs\Lab1\{file_name}.csv', 'w', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
            'Літера',
            'Частота'
            )
        )
    data = []
    d = {}
    for i in text:
        if i in d:
            d[i] += 1
        else:
            d[i] = 1
    sum = 0
    for i in d:
        frequency = d[i]/len(text)
        if frequency == 0:
            continue
        else:
            sum += -frequency*math.log2(frequency)
        with open(f'Labs\Krypt_labs\Lab1\{file_name}.csv', 'a', encoding='cp1251', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    i,
                    frequency
                )
            )
    data.append(
        {
            f'Загальна ентропія' : sum,
            f'Надлишковість': 1 - sum / math.log2(len(d)),
            f'Розмір алфавіту': len(d)
        }
    )
    return data

def count_frequency_bigram(text, step, file_name : str):
    with open(f'Labs\Krypt_labs\Lab1\{file_name}.csv', 'w', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
            'Біграма',
            'Частота'
            )
        )
    data = []
    sum = 0
    sum_b = 0
    dictionary = {}
    for i in range(0, len(text)-1, step):
        if text[i:i+2] in dictionary:
            dictionary[text[i:i+2]] += 1
        else:
            dictionary[text[i:i+2]] = 1

    for i in dictionary:
        sum += dictionary[i]
    
    for i in dictionary:
        frequency_bigram = dictionary[i]/sum
        sum_b += -frequency_bigram*math.log2(frequency_bigram)
        with open(f'Labs\Krypt_labs\Lab1\{file_name}.csv', 'a', encoding='cp1251', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                i,
                frequency_bigram
                )
            )
    data.append(
        {
            f'Загальна ентропія' : sum_b/2,
            f'Надлишковість' : 1 - sum_b / math.log2(len(dictionary)),
            f'Розмір алфавіту': len(dictionary)
        }
    )
    return data 

def main():
    with open('D:\VSCode\Python\Labs\Krypt_labs\Lab1\edited.txt', encoding='utf-8') as file:
        text = file.read()

    print(count_frequency_letter(text=text, file_name='Letter_with_space'))
    print('========================')
    print(count_frequency_letter(text=text.replace(" ", ""), file_name='Letter_without_space'))
    print('========================')
    #Біграми з перетином
    print(count_frequency_bigram(text=text.strip(), step=1, file_name='Bigram1_with_space'))
    print('========================')
    print(count_frequency_bigram(text=text.strip().replace(" ", ''),  step=1, file_name='Bigram1_without_space'))
    print('========================')
    #Біграми без перетину
    print(count_frequency_bigram(text=text.strip(), step=2, file_name='Bigram2_with_space'))
    print('========================')
    print(count_frequency_bigram(text=text.strip().replace(" ", ''),  step=2, file_name='Bigram2_without_space'))
    
if __name__ == '__main__':
    main()

    