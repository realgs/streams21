import random as ran

lista = [ran.randint(0, 3000) for i in range(0, 10)]

def bubble_sort(lista):
    L = lista
    for i in range(len(L)):
        for j in range(0, (len(L) - 1) - i):
            if (L[j] > L[j + 1]):
                temp = L[j]
                L[j] = L[j + 1]
                L[j + 1] = temp
    return L

print(bubble_sort(lista))