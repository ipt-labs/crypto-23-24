from pprint import pprint
from math import log

class TextAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.alphabet = 'абвгдежзийклмнопрстуфхцчшщыьэюя '

    def load_text(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            self.text = f.read()
        self.length = len(self.text)

    def count_letters(self):
        self.letters = {}
        for i in self.alphabet:
            self.letters[i] = self.text.count(i)

    def calculate_entropy(self):
        h1 = 0
        for i in self.alphabet:
            if self.letters[i] == 0:
                continue
            h1 -= (self.letters[i] / self.length) * log(self.letters[i] / self.length, 2)
        return h1

    def analyze_text(self):
        self.load_text()
        self.count_letters()
        result = sorted(self.letters.items(), key=lambda item: item[1], reverse=True)
        return result, self.calculate_entropy()

analyzer1 = TextAnalyzer('spaces_text.txt')
result1, h1_1 = analyzer1.analyze_text()
pprint(result1, sort_dicts=False)
print(f"H1 (spaces): {h1_1}")


analyzer2 = TextAnalyzer('NOspaces_text.txt')
result2, h1_2 = analyzer2.analyze_text()
pprint(result2, sort_dicts=False)
print(f"H1 (no spaces): {h1_2}")

