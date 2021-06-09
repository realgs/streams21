#sortowanie przez wstawianie
list = [6, 3, 7, 8, 20, 5, 64, 2, 10, 24, 2, 4, 6, 1, 1, 18, 20, 1, 14, 15, 16, 11]

def sort2(list):
    for i in range(1, len(list)):
        key = list[i]
        j = i - 1
        while j >= 0 and list[j] > key:
            list[j + 1] = list[j]
            j = j - 1
        list[j + 1] = key

sort2(list)
print(list)