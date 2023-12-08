def decryptSecrets (path, key):
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

        numbers = []
        decrypted = ''
        
        for char in key:
            numbers.append(letter_pool.index(char))

        x = 0
        for char in contents:
            if x >= len(key):
                x = 0

            y = letter_pool.index(char) - numbers[x]
            if y < 0:
                y += 32

            
            decrypted += letter_pool[y]
            x += 1

        return decrypted

print(decryptSecrets(r'C:\Users\yarik\Desktop\Крипта\Lab 2\Encrypted.txt', 'башяцщросмичерннемчбъ'))
print(decryptSecrets(r'C:\Users\yarik\Desktop\Крипта\Lab 2\Encrypted.txt', 'башяцяросхичернцемчбъ'))
print(decryptSecrets(r'C:\Users\yarik\Desktop\Крипта\Lab 2\Encrypted.txt', 'башяцяросъичерныемчбъ'))
print(decryptSecrets(r'C:\Users\yarik\Desktop\Крипта\Lab 2\Encrypted.txt', 'башияяросъичерныемчбъ'))
print(decryptSecrets(r'C:\Users\yarik\Desktop\Крипта\Lab 2\Encrypted.txt', 'башняяросъичерныемчбъ'))
print(decryptSecrets(r'C:\Users\yarik\Desktop\Крипта\Lab 2\Encrypted.txt', 'башняяростичерныемаки'))
