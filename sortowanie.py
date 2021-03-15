def bubble_sort(A):
    for i in range(len(A)):
        for j in range(len(A)-1):
            if A[j] > A[j+1]:
                A[j], A[j+1] = A[j+1], A[j]

    print(A)


def insertion_sort(A):
    for i in range(1, len(A)):
        k = A[i]
    j = 0
    while k > A[j] and j < i:
        j += 1
    A.insert(j, k)
    del A[i + 1]
