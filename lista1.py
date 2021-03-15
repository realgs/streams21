import random

n = int(input("Wprowadz ile liczb nalezy posortowac: "))


def main(n):
    lista_wartosci = []
    for i in range(n):
        lista_wartosci.append(random.randint(1, 10000))
    #print(lista_wartosci)
    bubble(lista_wartosci)
    return lista_wartosci


def bubble(lista_wartosci):
    for i in range(len(lista_wartosci)):
        for j in range(len(lista_wartosci)):
            if lista_wartosci[i] < lista_wartosci[j]:
                lista_wartosci[i], lista_wartosci[j] = lista_wartosci[j], lista_wartosci[i]
    print(lista_wartosci)
    return lista_wartosci


main(n)
