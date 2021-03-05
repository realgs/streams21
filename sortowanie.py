def bubble_sort(A):
    for i in range(len(A)):
        for j in range(len(A)-1):
            if A[j] > A[j+1]:
                A[j], A[j+1] = A[j+1], A[j]

    print(A)

def insertion_Sort(A):
    for i in range(1, len(A)):
        if A[i] < A[i-1]:
            A[i - 1], A[i] = A[i], A[i - 1]

    print(A)

A = [8, 7, 4, 3, 6, 2, 5, 1]

bubble_sort(A)

insertion_Sort(A)