import matplotlib.pyplot as plt

# Довжина r
r = [1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# Індекс відповідності
index_of_similarity = [0.0562, 0.0472, 0.0395, 0.0375, 0.0379, 0.0338, 0.0336, 0.0338, 0.0342, 0.0338, 0.0346, 0.0340, 0.0341, 0.0338, 0.0332, 0.0328]

# Створення графіка
plt.figure(figsize=(10, 6))
plt.plot(r, index_of_similarity, marker='o', linestyle='-', color='b')
plt.title('Індекс відповідності для різної довжини r')
plt.xlabel('Довжина r')
plt.ylabel('Індекс відповідності')
plt.grid(True)

# Відобразити графік
plt.show()
