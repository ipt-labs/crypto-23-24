def encryptSecrets (path, key = 0):

    with open(path, 'r', encoding='utf-8') as file:
        contents = file.read()
    letter_pool = ['а', 'б', 'в', 'г', 'д',
                   'е', 'ё', 'ж', 'з', 'и',
                   'й', 'к', 'л', 'м', 'н',
                   'о', 'п', 'р', 'с', 'т',
                   'у', 'ф', 'х', 'ц', 'ч',
                   'ш', 'щ', 'ъ', 'ы', 'ь',
                   'э', 'ю', 'я']
    better_contents = ''

    for char in contents: 
        if char.isalpha():
            better_contents += char.lower()

    def encryptAlgorithm(word):
        numbers = []
        encrypted = ''
        
        for char in word:
            numbers.append(letter_pool.index(char))

        x = 0
        for char in better_contents:
            if x >= len(word):
                x = 0

            encrypted += letter_pool[(letter_pool.index(char) + numbers[x])%len(letter_pool)]
            x += 1

        filename = 'Encrypted_by_' + word + '.txt'
        with open(filename, 'w') as file:
            file.write(encrypted)
            
        return filename

    def convertToKey(value):
        keyword = ''
        for char in value:
            if char.isalpha() and char in letter_pool:
                keyword += char.lower()
        if len(keyword) == 0:
            print('You should write something containing russian letters')
        else:
            return keyword
        
    match key:
        case 0:
            print('Do you really want to hide your secrets?')
        case 2:
            print(encryptAlgorithm('ой'))
        case 3:
            print(encryptAlgorithm('мяу'))
        case 4:
            print(encryptAlgorithm('пиво'))
        case 5:
            print(encryptAlgorithm('котик'))
        case 10:
            print(encryptAlgorithm('люблюжрать'))
        case 20:
            print(encryptAlgorithm('мненадопридуматьключ'))
        case _:
            print(encryptAlgorithm(convertToKey(key)))
            
encryptSecrets(r'C:\Users\yarik\Desktop\Крипта\Lab 2\Sample.txt', 2) 
encryptSecrets(r'C:\Users\yarik\Desktop\Крипта\Lab 2\Sample.txt', 3)
encryptSecrets(r'C:\Users\yarik\Desktop\Крипта\Lab 2\Sample.txt', 4) 
encryptSecrets(r'C:\Users\yarik\Desktop\Крипта\Lab 2\Sample.txt', 5)
encryptSecrets(r'C:\Users\yarik\Desktop\Крипта\Lab 2\Sample.txt', 10)
encryptSecrets(r'C:\Users\yarik\Desktop\Крипта\Lab 2\Sample.txt', 20)
encryptSecrets(r'C:\Users\yarik\Desktop\Крипта\Lab 2\Sample.txt', 'тест свободного ключа, вдруг получится') 


    

    
    
    
    
