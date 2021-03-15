import random


def insertion_sort(array):
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
    return array


array_to_sort = []
for k in range(50):
    array_to_sort.append(random.randint(1, 50))

insertion_sort(array_to_sort)

print(array_to_sort)
