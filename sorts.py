import numpy as np


A = np.random.randint(100, size=20)
B = np.random.randint(10000, size=1000)


def select_sort(arr):
    for i in range(len(arr) - 1):
        min_index = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr


print(A)
print(select_sort(A))
