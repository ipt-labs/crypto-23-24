ALPHABET = 'абвгдежзийклмнопрстуфхцчшщьыэюя'  # mind that data from lab1 counts ё
assert len(ALPHABET) == 31


TRANSLATOR = str.maketrans({'ё': 'е', 'ъ': 'ь'})
MOST_FREQUENT_BG = ["ст", "но", "то", "на", "ен"]
