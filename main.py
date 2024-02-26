import numpy as np
from scipy import stats
from prettytable import PrettyTable
import random


def union_frequency(arr):
    k = 0
    for i in range(len(arr)-1, -1, -1):
        if arr[i][1] and i == 0 <= 5:
            k = 0
            arr[1][1] = arr[i][1] + arr[i + 1][1]
            arr[1][2] = arr[i][2] + arr[i + 1][2]
            arr[1][3] = arr[i][3] + arr[i + 1][3]
            arr[1][4] = arr[i][3] ** 2
            arr[1][5] = arr[i][4] / arr[i][2]
            return arr[1:]
        elif arr[i][1] <= 5:
            k = i
            arr[i-1][1] = arr[i][1] + arr[i-1][1]
            arr[i-1][2] = arr[i][2] + arr[i-1][2]
            arr[i-1][3] = arr[i][3] + arr[i-1][3]
            arr[i-1][4] = arr[i][3] ** 2
            arr[i-1][5] = arr[i][4] / arr[i][2]
            return arr[:k] + arr[k + 1:]


poisson_lambda = 10  # Лямбда для закона Пуассона (среднее количество успехов за определенный интервал)
significance_level = 0.05  # Уровень значимости
events_number = 20  # Число событий
numb_of_experiments = 300  # Число экспериментов


# Вероятности Пуассона
print("Вероятности Пуассона:")
poisson_probability = [np.exp(-poisson_lambda) * (poisson_lambda ** i) / np.math.factorial(i) for i in
                       range(events_number)]
print(poisson_probability)

# Генерируем собственное распределение
array = [0 for _ in range(events_number)]

for _ in range(numb_of_experiments):
    U = random.random()
    i = 0
    p = np.exp(-poisson_lambda)
    F = p

    while U > F:
        p *= poisson_lambda / (i + 1)
        F += p
        i += 1
    array[i] += 1  # Эксперимент закончен

print("Сгенерированные случайные числа:\n", array)

# Вычисляем теоретические частоты
theor_frequency = [numb_of_experiments * np.exp(-poisson_lambda) * (poisson_lambda ** i)
                   / np.math.factorial(i) for i in range(events_number)]
print("Теоретические частоты:\n", theor_frequency)

# Разбиение на интервалы
field_names = ["i", "ni(Частоты)", "ni'(Теор. частоты)", "ni -n'i", "(ni -n'i)^2", "X^2 наблюдаемое"]
print_table = PrettyTable(field_names)


matrix = a = [[0] * 6 for i in range(events_number)]  # Создаем двумерный список для удобного объединения событий


print("\n\n\nИсходная таблица до объединения малочисленных частот:")
for i in range(events_number):
    matrix[i][0] = i
    matrix[i][1] = array[i]
    matrix[i][2] = theor_frequency[i]
    matrix[i][3] = matrix[i][1] - matrix[i][2]
    matrix[i][4] = matrix[i][3] ** 2
    matrix[i][5] = matrix[i][4] / matrix[i][2]
print_table.add_rows(matrix)
print(print_table)

while min([row[1] for row in matrix]) <= 5:
    matrix = union_frequency(matrix)

for i in range(len(matrix)):                        #Для нормальной нумерации
    matrix[i][0] = i

print("\n\n\n\nТаблица после объединения малочисленных событий:")
print_table = PrettyTable(field_names)
print_table.add_rows(matrix)
print(print_table)


X_nab = sum([row[5] for row in matrix])
X_kr = stats.chi2.ppf(1-significance_level, len(matrix) - 2)
print("Хи критическое : ", X_kr)
print("Хи наблюдаемое : ", X_nab)


if X_nab < X_kr:
    print("Т.к. Хи критическое > Хи наблюдаемого, принимаем гипотезу")
else:
    print("Т.к. Хи критическое < Хи наблюдаемого, отвергаем гипотезу")
