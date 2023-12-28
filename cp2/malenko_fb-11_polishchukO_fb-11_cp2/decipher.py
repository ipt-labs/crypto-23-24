from main import Lab2CipherText

if __name__ == '__main__':
    with open('task.txt', 'r', encoding='utf8') as f:
        inputText = Lab2CipherText(f.read())

    while True:
        key = input('Enter the key to decipher the text \x1B[3m(\'q\' to exit)\x1B[0m: ')
        if key == 'q':
            exit(1)

        decipheredText = inputText.decipher(key=key)
        print(f'The deciphered text is: {decipheredText[:100]}...')