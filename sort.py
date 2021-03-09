def selection_sort(lista):
    for i in range(0, len(lista) - 1):
        min_w = i
        for j in range(i + 1, len(lista)):
            if lista[j] < lista[min_w]:
                min_w = j
        lista[min_w], lista[i] = lista[i], lista[min_w]
    return lista

def insertion_sort(lista):
    for i in range(0, len(lista)):
        for j in range(0, i):
            if lista[i] < lista[j]:
                lista[i], lista[j] = lista[j], lista[i]
    return lista

lista = [5, 80, 10, 40, 22, 6, 103]

print(selection_sort(lista))
print(insertion_sort(lista))