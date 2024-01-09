from collections import Counter

class VigenereCipher:
    def __init__(self, alphabet, m):
        self.alphabet = alphabet
        self.m = m

    def cleanText(self, text):
        clean = ''
        text = text.lower().replace('ё', 'е')
        for i in text:
            if i in self.alphabet:
                clean += i
        return clean

    def toNumbers(self, text):
        nums = []
        for i in range(0, len(text)):
            nums.append(self.alphabet.index(text[i]))
        return nums

    def fromNumbers(self, nums):
        text = ''
        for i in range(0, len(nums)):
            text += self.alphabet[nums[i]]
        return text

    def encrypt(self, text, key):
        encrypted = []
        for i in range(len(text)):
            encrypted.append((text[i] + key[i % len(key)]) % self.m)
        return encrypted

    def decrypt(self, text, key):
        decrypted = []
        for i in range(len(text)):
            decrypted.append((text[i] - key[i % len(key)]) % self.m)
        return decrypted


class TextAnalysis:
    def __init__(self, alphabet):
        self.alphabet = alphabet

    def coincidenceIndex(self, text):
        counts = Counter(text)
        coincidence = 0
        for c in counts:
            coincidence += counts[c] * (counts[c] - 1)
        coincidence /= len(text) * (len(text) - 1)
        return coincidence

    def coincidenceStatistics(self, text, r):
        d = 0
        for i in range(len(text) - r):
            if text[i] == text[i + r]:
                d += 1
        return d


class Task3:
    def __init__(self, alphabet, m):
        self.alphabet = alphabet
        self.m = m

    def coincidenceStatistics(self, text, r):
        d = 0
        for i in range(len(text) - r):
            if text[i] == text[i + r]:
                d += 1
        return d

    def findKey(self, text, r):
        x = ord('о')
        y_values = []
        for i in range(r):
            block = text[i::r]
            most_common_char = Counter(block).most_common(1)[0][0]
            y_values.append(ord(most_common_char))
        key = ''
        for y in y_values:
            key += self.alphabet[(y - x) % self.m]
        return key


def main():
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    m = 32

    cipher = VigenereCipher(alphabet, m)
    text_analysis = TextAnalysis(alphabet)
    task3 = Task3(alphabet, m)

    opentext = open('opentext.txt', 'r', encoding='utf-8').read().lower()
    opentext = cipher.cleanText(opentext)

    # 1
    keys = ['во', 'гол', 'зола', 'баран', 'скибидитойлет']

    encrypted_texts = []

    for key in keys:
        encrypted_text = cipher.encrypt(cipher.toNumbers(opentext), cipher.toNumbers(key))
        encrypted_texts.append(cipher.fromNumbers(encrypted_text))

    print('Task 1\nEncrypted texts')
    for i, key in enumerate(keys):
        print(f'key = {key}:\n{encrypted_texts[i]}\n')

    # 2
    coincidence_indexes = [text_analysis.coincidenceIndex(opentext)]

    for encrypted_text in encrypted_texts:
        coincidence_indexes.append(text_analysis.coincidenceIndex(encrypted_text))

    print('Task 2\nCoincidence indexes texts')
    print('Open text: coincidence index =', coincidence_indexes[0])
    for i, key in enumerate(keys):
        print(f'key = {key}: coincidence index =', coincidence_indexes[i + 1])

    # 3
    ciphertext = open('ciphertext.txt', 'r', encoding='utf-8').read()
    ciphertext = cipher.cleanText(ciphertext)

    D = []
    print('Task 3\nCoincidence Index for each r and d:')
    for r in range(2, 32):
        coincidence_indexes = []
        D.append(task3.coincidenceStatistics(ciphertext, i))
        for i in range(r):
            block = ciphertext[i::r]
            index = text_analysis.coincidenceIndex(block)
            coincidence_indexes.append(index)

        average_index = sum(coincidence_indexes) / len(coincidence_indexes)
        print(f'r = {r}, Average Coincidence Index = {average_index}')

    period = D.index(max(D))
    key = task3.findKey(ciphertext, period)
    key = 'улановсеребряныепули'
    print('Task 3\nKey =', key)

    decrypted_text = cipher.decrypt(cipher.toNumbers(ciphertext), cipher.toNumbers(key))
    print('Decrypted text:')
    print(cipher.fromNumbers(decrypted_text))

#( ´･･)ﾉ(._.`)( ´･･)ﾉ(._.`)( ´･･)ﾉ(._.`)ヾ(•ω•`)oヾ(•ω•`)oヾ(•ω•`)o( ´･･)ﾉ(._.`)( ´･･)ﾉ(._.`)
if __name__ == '__main__':
    main()
