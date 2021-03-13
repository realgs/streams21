def bubblesort(list, listLen):
    while listLen > 1:
        replace = False
        for i in range(0, listLen - 1):
            if list[i] > list[i + 1]:
                list[i], list[i + 1] = list[i + 1], list[i]
                replace = True
        listLen -= 1
        if replace == False:
            break
    return list


def partition(arr, start, end):
    i = (start-1)
    pivot = arr[end]

    for j in range(start, end):
        if arr[j] <= pivot:
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i+1], arr[end] = arr[end], arr[i+1]
    return (i+1)


def quickSort(arr, start, end):
    if len(arr) == 1:
        return arr
    if start < end:
        p = partition(arr, start, end)
        quickSort(arr, start, p-1)
        quickSort(arr, p+1, end)


list = [41, 91, 414, 156, 236, 24, 101, 9415, 24, 1, 81, 2, 9]
list2 = list
quickSort(list, 0, len(list)-1)
print("Result of quicksort: ", list)
print('Result of bubblesort: ', bubblesort(list2, len(list2)))
