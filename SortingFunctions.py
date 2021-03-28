from random import randint


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


list_bubble = []
list_insert = []
for i in range(20):
    list_bubble.append(randint(0, 50))
    list_insert.append(randint(0, 50))

print('Sortowanie bąbelkowe: ', bubble_sort(list_bubble))
print('Sortowanie przez wstawienie: ',insertion_sort(list_insert))

