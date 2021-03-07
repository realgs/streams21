def bubbleSorting(arr):
    arrLen = len(arr)
    while arrLen > 1:
        replace = False
        for i in range(0, arrLen - 1):
            if arr[i] > arr[i + 1]:
                # arr[i] = arr[i + 1]
                # arr[i + 1] = arr[i]
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                replace = True
        arrLen -= 1
        if replace == False: break
    return arr


print(f'Final: {bubbleSorting([3, 6, -2, 8, 4, 9, 11, 2])}')

def insertSorting(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


print(f'Final: {insertSorting([3, 6, -2, 8, 4, 9, 11, 2])}')


# Błażej Raducki 254277
