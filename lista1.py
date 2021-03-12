from random import randint


def genData(num_of_numbers, num_range):
    numbers = []
    for i in range(num_of_numbers):
        numbers.append(randint(1, num_range))
    return numbers


def quickSort(dane, from_index, to_index):
    pivot = dane[to_index]
    j = from_index
    for i in range(from_index, to_index + 1):
        if dane[i] < pivot:
            dane[i], dane[j] = dane[j], dane[i]
            j += 1

    dane[j], dane[to_index] = dane[to_index], dane[j]

    if j - from_index > 1:
        quickSort(dane, from_index, j - 1)
    if to_index - j > 1:
        quickSort(dane, j + 1, to_index)


def insertionSort(dane):
    for i in range(1, len(dane)-1):
        slider = dane[i]
        y = i - 1
        while y >= 0 and slider < dane[y]:
            dane[y+1] = dane[y]
            y -= 1
            dane[i] = slider


dane = genData(100, 200)
print(dane)

quickSort(dane, 0, len(dane) - 1)
print(dane)

insertionSort(dane)
print(dane)

print(quickSort(dane, 0, len(dane)-1) == insertionSort(dane))