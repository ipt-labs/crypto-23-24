import re
from math import log2

space = input('Чи є пробіл в алфавіті? (+/-): ')

def replace_words(file, filtered_file, alphabet): #Функція для попередньої фільтрації тексту
    global space
    with open(file, encoding = 'utf-8') as f:
        data = f.read()
        data = data.lower().replace('ъ', 'ь').replace('ё', 'е')
        
        for letter in range(len(data)):
            if data[letter] not in alphabet:
                data = data.replace(data[letter], ' ')

        if space == '+':    
            data = re.sub(r'\s+', ' ', data)
            
        elif space == '-':
            data = re.sub(r'\s+', '', data)

        else:
            print('Введіть "+" або "-"')
            exit('Помилка вводу!')

    with open(filtered_file, 'w', encoding = 'utf-8') as ff:
        ff.write(data)

def frequency_letters(filtered_file, alphabet): #Функція для підрахунку частот букв
    global space
    
    if space == '-':
        alphabet = alphabet[0:-1]
        
    freq = {i: 0 for i in alphabet} #Створення словника, де ключ це буква, а значення це її частота
    with open(filtered_file, encoding = 'utf-8') as ff:
        data = ff.read()
        
    entropy_let = 0
    for i in freq: #Цикл перевіряє к-сть кожної букви, що зустрічається в тексті а в кінці обраховує частоту
        for j in data:
            if j == i:
                freq[i] += 1
        freq[i] = freq[i] / len(data)
        
        #Обчислення значень ентропії по формулі:
        entropy_let += - (freq[i] * log2(freq[i]))

    #Обчислення надлишковості по формулі:
    excess_let = 1 - (entropy_let / log2(len(freq)))
    
    #Сортування частоти за спаданням і подальше її виведення у .txt файл    
    freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse = True))

    if space == '+':
        freq_file = ('frequency_letter_with_spaces.txt')
        lf_entropy_let = ('Значення ентропії для букв з пробілами: ')
        lf_excess_let = ('Надлишковість для букв з пробілами: ')
        
    elif space == '-':
        freq_file = ('frequency_letter_without_spaces.txt')
        lf_entropy_let = ('Значення ентропії для букв без пробілів: ')
        lf_excess_let = ('Надлишковість для букв без пробілів: ')
        
    with open(freq_file, 'w', encoding = 'utf-8') as ws:
        for i in freq:
            ws.write(i + ' : ' + str(freq[i]) + '\n')

    with open(last_file, 'w', encoding = 'utf-8') as lf:
        lf.write(lf_entropy_let + str(entropy_let) + '\n')
        lf.write(lf_excess_let + str(excess_let) + '\n')
            

def frequency_bigrams(filtered_file, freq_cross_bigrams, freq_bigrams): #Функція для підрахунку частот біграм
    freq = {}
    freq_cross = {}

    with open(filtered_file, encoding = 'utf-8') as ff:
        data = ff.read()

    entropy_big = 0
    
    #Підрахунок частот біграм без перетину
    n = 0 #К-сть усього біграм в тексті
    
    for let in range(0, len(data)-1, 2): #Пробіжка по тексту з кроком 2
        big = data[let:let+2] #Утворення біграми

        if big in freq:
            freq[big] += 1
            n+=1

        else:
            freq[big] = 1
            n+=1

    for i in freq:
        freq[i] = freq[i] / n
        entropy_big += - (freq[i] * log2(freq[i])) #Обчислення значень ентропії для біграм
    excess_big = 1 - (entropy_big / log2(len(freq))) #Обчислення надлишковості біграм

    entropy_big_cross = 0
    
    n = 0
    #Підрахунок частот біграм з перетином                
    for let in range(len(data)-1): #Пробіжка по тексту з кроком 1
        big = data[let:let+2]
        if big in freq_cross:
            freq_cross[big] += 1
            n+=1

        else:
            freq_cross[big] = 1
            n+=1
            
    for i in freq_cross:
        freq_cross[i] = freq_cross[i] / n
        entropy_big_cross += - (freq_cross[i] * log2(freq_cross[i]))
    excess_big_cross = 1 - (entropy_big_cross / log2(len(freq_cross)))

    freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse = True))
    freq_cross = dict(sorted(freq_cross.items(), key=lambda item: item[1], reverse = True))
    
    if space == '+':
        freq_bigrams = ('frequency_bigrams_with_spaces.txt')
        freq_cross_bigrams = ('frequency_cross_bigrams_with_spaces.txt')
        lf_entropy_big = ('Значення ентропії для біграм без перетину з пробілами: ')
        lf_entropy_big_cross = ('Значення ентропії для біграм з перетином з пробілами: ')
        lf_excess_big = ('Значення надлишковості для біграм без перетину з пробілами: ')
        lf_excess_big_cross = ('Значення надлишковості для біграм з перетином з пробілами: ')
        
    else:
        freq_bigrams = ('frequency_bigrams_without_spaces.txt')
        freq_cross_bigrams = ('frequency_cross_bigrams_without_spaces.txt')
        lf_entropy_big = ('Значення ентропії для біграм без перетину без пробілів: ')
        lf_entropy_big_cross = ('Значення ентропії для біграм з перетином без пробілів: ')
        lf_excess_big = ('Значення надлишковості для біграм без перетину без пробілів: ')
        lf_excess_big_cross = ('Значення надлишковості для біграм з перетином без пробілів: ')
        
    with open(freq_bigrams, 'w', encoding = 'utf-8') as fb:
        for i in freq:
            fb.write(i + ' : ' + str(freq[i]) + '\n')
            
    with open(freq_cross_bigrams, 'w', encoding = 'utf-8') as fb:
        for i in freq_cross:
            fb.write(i + ' : ' + str(freq_cross[i]) + '\n')

    with open(last_file, 'a', encoding = 'utf-8') as lf:
        lf.write(lf_entropy_big + str(entropy_big/2) + '\n')
        lf.write(lf_entropy_big_cross + str(entropy_big_cross/2) + '\n')
        lf.write(lf_excess_big + str(excess_big) + '\n')
        lf.write(lf_excess_big_cross + str(excess_big_cross) + '\n')

file = ('text.txt')
filtered_file = ('filtered_text.txt')
alphabet = ('абвгдежзийклмнопрстуфхцчшщыьэюя ')
freq_cross_bigrams = ('frequency_cross_bigrams.txt')
freq_bigrams = ('frequency_bigrams')
last_file = ('excesses_and_entropies.txt')


replace_words(file, filtered_file, alphabet)
frequency_letters(filtered_file, alphabet)
frequency_bigrams(filtered_file, freq_cross_bigrams, freq_bigrams)
