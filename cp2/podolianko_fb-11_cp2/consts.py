ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'  # mind that data from lab1 counts ё
assert len(ALPHABET) == 32
TRANSLATOR = str.maketrans({'ё': 'е'})

KEY_2 = 'КП'
KEY_3 = 'ДОМ'
KEY_4 = 'КЛЮЧ'
KEY_5 = 'МЕТАЛ'

KEY_15 = 'СДАЛЛАБУВОВРЕМЯ'

IOC_RANDOM = 1 / len(ALPHABET)

# Key length guessing. also guessed...
THRESHOLD = 0.01