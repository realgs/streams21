from random import random

arr = [random() for i in range(100)] 

def Partition(arr, l, r):
    i = (l-1)
    pivot = arr[r]
    for j in range(l, r):
        if (arr[j] <= pivot):
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[r] = arr[r], arr[i+1]
    return i+1

def QuickSort(l, r, d):
    if (len(arr) == 1):
        return arr
    if l < r:
        pi = Partition(arr, l, r)
        QuickSort(arr, l, pi-1)
        QuickSort(arr, pi+1, r)



