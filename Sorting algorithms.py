from time import time
import numpy as np

numlist = np.random.randint(1, 100, 200)
print(numlist)


def insert_sort(arr):
    if len(arr) < 2:
        return arr
    l = len(arr)
    for i in range(1, l):
        j = i - 1
        current = arr[i]
        while j >= 0 and arr[j] > current:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr


def quicksort(arr):
    if len(arr) < 2:
        return arr
    piv = arr[0]
    smaller, same, bigger = [], [], []
    for el in arr:
        if el < piv:
            smaller.append(el)
        elif el == piv:
            same.append(el)
        else:
            bigger.append(el)
    return quicksort(smaller) + same + quicksort(bigger)


cur_time = time()
insert_sorted = insert_sort(numlist)
cur_time = time() - cur_time
print('Insert sort\n', insert_sorted, '\n sorting time:', cur_time)
cur_time = time()
quick_sorted = quicksort(numlist)
cur_time = time() - cur_time
print('Quick sort\n', quick_sorted, '\n sorting time:', cur_time)
