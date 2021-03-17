import random as ran


def createList(x):
    L = [ran.randint(0, 100) for i in range(0, x)]
    return L


def bubbleSort(L):
    for i in range(len(L)):
        for j in range(0, (len(L) - 1) - i):
            if L[j] > L[j + 1]:
                temp = L[j]
                L[j] = L[j + 1]
                L[j + 1] = temp
    return L


def insertionSort(L):
    for i in range(len(L)):
        for j in range(0, i):
            if L[i] < L[j]:
                temp = L[i]
                L[i] = L[j]
                L[j] = temp
    return L


def merge(left, right):
    if len(left) == 0:
        return right
    if len(right) == 0:
        return left
    result = []
    index_left = index_right = 0
    while len(result) < len(left) + len(right):
        if left[index_left] <= right[index_right]:
            result.append(left[index_left])
            index_left += 1
        else:
            result.append(right[index_right])
            index_right += 1

        if index_right == len(right):
            result += left[index_left:]
            break

        if index_left == len(left):
            result += right[index_right:]
            break
    return result


def mergeSort(L):
    if len(L) < 2:
        return L

    midpoint = len(L) // 2

    return merge(
        left=mergeSort(L[:midpoint]),
        right=mergeSort(L[midpoint:]))


print(f'Bubble sort: {bubbleSort(createList(15))}')
print(f'Insertion sort: {insertionSort(createList(10))}')
print(f'Merge sort: {mergeSort(createList(20))}')
