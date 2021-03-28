import random


def bubble_sort(list):
    for i in range(len(list)):
        j = len(list) - 1
        while j > i:
            if list[j] < list[j - 1]:
                temp = list[j]
                list[j] = list[j - 1]
                list[j - 1] = temp
            j -= 1
    return list


def insertion_sort(list):
    for i in range(1, len(list)):
        temp = list[i]
        j = i - 1
        while j >= 0 and list[j] > temp:
            list[j + 1] = list[j]
            j -= 1
        list[j + 1] = temp
    return list


list = []
for i in range(15):
    list.append(random.randint(1,99))

print("\nLista do sortowania:", list)
print("\nSortownie bąbelkowe:", bubble_sort(list.copy()))
print("Pierwonta lista:",list)
print("\nSortowanie szybkie:",insertion_sort(list.copy()))
print("Pierwonta lista:",list)