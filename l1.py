import random as ran


def createList(x):
    L = [ran.randint(0, 100) for i in range(0, x)]
    return L


def bubbleSort(L):
    for i in range(len(L)):
        for j in range(0, (len(L) - 1) - i):
            if L[j] > L[j + 1]:
                temp = L[j]
                L[j] = L[j + 1]
                L[j + 1] = temp
    return L


print(bubbleSort(createList(15)))
print(bubbleSort(createList(10)))
