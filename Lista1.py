from random import randint


def moja_Lista(n):
    Lista = []
    for i in range(n):
        Lista.append(randint(1, 100000))
    return Lista


def Sortowanie_Babelkowe(Lista):
    for i in range(len(Lista)):
        for j in range(0,(len(Lista))-1):
            if (Lista[j] > Lista[j+1]):
                temp = Lista[j]
                Lista[j] = Lista[j+1]
                Lista[j+1] = temp

    return Lista


def Sortowanie_wstawianie(Lista):
    for i in range(len(Lista)):
        for j in range(0, i):
            if (Lista[i] < Lista[j]):
                temp = Lista[i]
                Lista[i] = Lista[j]
                Lista[j] = temp
    return Lista
