import random

x = int(input("Ile wylosować liczb, aby później je posortować: "))


def main(x):
    wylosowane_liczby = []
    for i in range(x):
        wylosowane_liczby.append(random.randint(1, 100))
    bubble(wylosowane_liczby)
    return wylosowane_liczby


def bubble(wylosowane_liczby):
    for i in range(len(wylosowane_liczby)):
        for j in range(len(wylosowane_liczby)):
            if wylosowane_liczby[i] < wylosowane_liczby[j]:
                wylosowane_liczby[i], wylosowane_liczby[j] = wylosowane_liczby[j], wylosowane_liczby[i]
    print(wylosowane_liczby)
    return wylosowane_liczby


main(x)