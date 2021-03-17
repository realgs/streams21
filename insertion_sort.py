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

    return L


if __name__ == "__main__":
    liczby = [5, 8, 3, 2, 3, 2, 9, 14, 4, 8, 4, 7, 4, 6, 21, 1, 1]

    print(insertion_sort(liczby))