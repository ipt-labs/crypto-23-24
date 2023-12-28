def breakingTheCode(path):
    letter_pool = ['а', 'б', 'в', 'г', 'д',
                   'е', 'ж', 'з', 'и',
                   'й', 'к', 'л', 'м', 'н',
                   'о', 'п', 'р', 'с', 'т',
                   'у', 'ф', 'х', 'ц', 'ч',
                   'ш', 'щ', 'ъ', 'ы', 'ь',
                   'э', 'ю', 'я']
    
    with open(path, 'r', encoding='utf-8') as file:
        contents = ''
        for char in file.read(): 
            if char.isalpha():
                contents += char.lower()
    
    def splitting(step):
        table_table = []
        
        for i in range(step):
            table_table.append([])
            
        x = 0
        for char in contents:
            if x == step:
                x = 0
                
            table_table[x].append(char)
            x +=1

        y = 0
        for block in table_table:
            char_table = {}
            for char in block:
                if char in char_table:
                    char_table[char] += 1
                else:
                    char_table[char] = 1
            x = 0
            for count in char_table.values():
                x += count*(count - 1)

            result = x/(len(block)*(len(block)-1))
            y += result

        index = y/step
        
        print(f"{step}:{index}")
        return index 

    result_table = {}
    for i in range(2,30):
        result_table[i] = splitting(i)

    key_length = max(result_table, key=result_table.get)

    table_table = []
    for i in range(key_length):
            table_table.append([])
            
    x = 0
    for char in contents:
        if x == key_length:
            x = 0
                
        table_table[x].append(char)
        x +=1

    keyword1 = ''
    keyword2 = ''
    keyword3 = ''
    for block in table_table:
        char_table = {}
        for char in block:
            if char in char_table:
                char_table[char] += 1
            else:
                char_table[char] = 1
                    
        pop_letter = max(char_table, key=char_table.get)

        key_letter1 = letter_pool.index(pop_letter) - letter_pool.index('о')
        if key_letter1 < 0:
            key_letter1 += 32
            
        key_letter2 = letter_pool.index(pop_letter) - letter_pool.index('е')
        if key_letter2 < 0:
            key_letter2 += 32
            
        key_letter3 = letter_pool.index(pop_letter) - letter_pool.index('а')
        if key_letter3 < 0:
            key_letter3 += 32

        keyword1 += letter_pool[key_letter1]
        keyword2 += letter_pool[key_letter2]
        keyword3 += letter_pool[key_letter3]
        
    print(keyword1)
    print(keyword2)
    print(keyword3)

breakingTheCode(r'C:\Users\yarik\Desktop\Крипта\Lab 2\Encrypted.txt')
