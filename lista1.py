import random

n = int(input("Wprowadz ile liczb nalezy posortowac: "))


def main(n):
    lista_wartosci = []
    for i in range(n):
        lista_wartosci.append(random.randint(1, 10000))
    #print(lista_wartosci)
    bubble(lista_wartosci)
    insert(lista_wartosci)
    return lista_wartosci


def bubble(lista_wartosci):
    for i in range(len(lista_wartosci)):
        for j in range(len(lista_wartosci)):
            if lista_wartosci[i] < lista_wartosci[j]:
                lista_wartosci[i], lista_wartosci[j] = lista_wartosci[j], lista_wartosci[i]
    print(lista_wartosci)
    return lista_wartosci


def insert(lista_wartosci):
    for i in range(1, len(lista_wartosci)):
        a = lista_wartosci[i]
        j = i - 1
        while j >= 0 and lista_wartosci[j] > a:
            lista_wartosci[j + 1] = lista_wartosci[j]
            j -= 1
        lista_wartosci[j + 1] = a
    print(lista_wartosci)
    return lista_wartosci


main(n)
