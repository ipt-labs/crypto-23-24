import os

def countIndex (path):
    for file in os.listdir(path):
        if file.endswith(".txt"):
            file_name = os.path.splitext(file)[0]
            file_path = os.path.join(path, file)
            with open(file_path, "r", encoding='latin-1') as file:
                contents = ''
                for char in file.read(): 
                    if char.isalpha():
                        contents += char.lower()

            char_table = {}
            for char in contents:
                if char in char_table:
                    char_table[char] += 1
                else:
                    char_table[char] = 1

            x = 0
            for count in char_table.values():
                x += count*(count - 1)

            result = x/(len(contents)*(len(contents)-1))
            print(f"{file_name}: {result}")

                
countIndex(r'C:\Users\yarik\Desktop\Крипта\Lab 2')
                
            
    
