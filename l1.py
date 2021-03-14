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

def QuickSort(arr, l, r):
    if (len(arr) == 1):
        return arr
    if l < r:
        pi = Partition(arr, l, r)
        QuickSort(arr, l, pi-1)
        QuickSort(arr, pi+1, r)

def MergeSort(arr):
    if (len(arr) == 1):
        return arr 
    elif (len(arr) > 1):
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]
        MergeSort(L)
        MergeSort(R)

        i = 0
        j = 0
        k = 0

        while (i < len(L) and j < len(R)):
            if (L[i] < R[j]):
                arr[k] = L[i]
                i+=1
            else:
                arr[k]= R[j]
                j+=1
            k+=1
        
        while (i < len(L)):
            arr[k] = L[i]
            i+=1
            k+=1

        while (j < len(R)):
            arr[k] = R[j]
            j+=1
            k+=1
        return arr




