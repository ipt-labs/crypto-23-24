import matplotlib.pyplot as plt
import numpy as np

# Зчитуємо шифртекст з файлу
file_path = r"C:\Users\Polya\Desktop\KPI\crypto\crypto-23-24\cp2\gogoleva_fb-12_cp2\decode.txt"
with open(file_path, "r", encoding="cp1251") as file:
    ciphertext = file.read()

offsets = []
data = []

# Це для позначення піків
threshold = 0

# Проводимо аналіз на знаходження довжини ключа
for offset in range(1, int(len(ciphertext) / 10)):
    matches = 0
    for j in range(len(ciphertext) - offset):
        if ciphertext[j] == ciphertext[j + offset]:
            matches += 1
    threshold += matches
    data.append(matches)
    offsets.append(offset)

# Встановлюємо поріг, вище якого точки позначаються
if offsets:
    threshold = int(1.2 * threshold / max(offsets))

# Підготовка даних для побудови графіка
x = np.array(offsets)
y = np.array(data)

plt.plot(x, y)

# Позначаємо високі точки та їх значення по осі x
max_indices = np.argpartition(data, -5)[-5:]  # Знаходимо індекси 5 найбільших значень
for i in max_indices:
    plt.scatter(offsets[i], data[i], color='red')  # Позначаємо їх червоним кольором
    plt.text(offsets[i], data[i], str(offsets[i]), fontsize=12, ha='center', va='bottom')

# Як часто мають бути лінії на осі x?
if offsets:
    stepsize = int(max(offsets) / 10)
    plt.xticks(np.arange(0, max(offsets), step=stepsize))
# Підписи для вісей та заголовок
plt.xlabel('Зсуви')
plt.ylabel('Збіги')
plt.title('Пошук піків, які є кратними деякій довжині ключа')

# Встановлюємо сітку
plt.grid(True)

# Відображення графіка
plt.show()
