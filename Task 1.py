def sortowanie_babelkowe(lista):
    n = len(lista)

    while n > 1:
        zamien = False
        for l in range(0, n-1):
            if lista[l] > lista[l+1]:
                lista[l], lista[l+1] = lista[l+1], lista[l]
                zamien = True

        n -= 1
        print(lista)
        if zamien == False: break

    return lista

def Insert_sort(A):
    for i in range(1,len(A)):
        klucz = A[i]
        j = i - 1
        while j>=0 and A[j]>klucz:
            A[j + 1] = A[j]
            j = j - 1
        A[j + 1] = klucz