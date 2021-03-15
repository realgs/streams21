
def bubbleSort(list):
    n = len(list)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if list[j] > list[j + 1]:
                list[j], list[j + 1] = list[j + 1], list[j]
    return list

example1 = [5, -6, 11, 9, 4, 3, -2, 15, 8, 0]
example2 = [2.6, 5, -1.25, 96.4, 7, -2, 96]
example3 = ['aaa', 'abc', 'jan', 'zenek', 'baba', 'lody', 'rabarbar']

print (bubbleSort(example1), bubbleSort(example2), bubbleSort(example3), sep='\n')