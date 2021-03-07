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
        print(arr)
        if replace == False: break
    return arr

print(f'Final: {bubbleSorting([5, 6, -1, 0])}')