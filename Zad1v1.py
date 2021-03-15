import random


def bubbleSort(array):
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]




array_to_sort = []
for k in range(50):
    array_to_sort.append(random.randint(1, 50))

bubbleSort(array_to_sort)

print(array_to_sort)
