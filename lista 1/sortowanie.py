def bubbleSort(list):
    n = len(list)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if list[j] > list[j + 1]:
                list[j], list[j + 1] = list[j + 1], list[j]
    return list

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

def mergeSort(list):
    if len(list) < 2:
        return list

    midpoint = len(list) // 2

    return merge(
        left=mergeSort(list[:midpoint]),
        right=mergeSort(list[midpoint:]))

example1 = [5, -6, 11, 9, 4, 3, -2, 15, 8, 0]
example2 = [2.6, 5, -1.25, 96.4, 7, -2, 96]
example3 = ['aaa', 'abc', 'jan', 'zenek', 'baba', 'lody', 'rabarbar']


print('Bubble Sort:', bubbleSort(example1.copy()), bubbleSort(example2.copy()), bubbleSort(example3.copy()), sep='\n')
print('Merge Sort:', mergeSort(example1.copy()), mergeSort(example2.copy()), mergeSort(example3.copy()), sep='\n')
