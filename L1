import random as rd

def bubblesort(lista):
    for i in range(len(lista)):
        for j in range(len(lista)):
            if lista[i] < lista[j]:
                lista[i],lista[j] = lista[j],lista[i]
    return lista

def insertsort(lista):
    for i in range(1, len(lista)):
        pivot = lista[i]
        j = i - 1
        while j >= 0 and lista[j] > pivot:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = pivot
    return lista

n = 10
lista = []

for i in range (n):
    lista.append(rd.randint(1,100))

print(bubblesort(lista))
print(insertsort(lista))
