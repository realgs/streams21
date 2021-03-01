def insertion_sort(L):
    n = len(L)
    for i in range(n):
        j = i
        while j>0 and L[j] < L[j-1]:
            temp = L[j]
            L[j], L[j-1] = L[j-1], temp
            j -= 1
    return L


def bubble_sort(L):
    n = len(L)
    for i in range(n-1):
        for j in range(n-1):
            if L[j] > L[j+1]:
                temp = L[j]
                L[j], L[j+1] = L[j+1], temp
    return L
