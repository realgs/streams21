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
    test = [3, 6, 2, 1, 1, 5, 9, 11, 4, 22, 7, 2, 5, 2]

    print(insertion_sort(test))
