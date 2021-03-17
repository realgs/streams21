from random import randrange
#Bubble Sort
def bubblesort(lst):
    n = len(lst)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst


def insertionSort(lst):

    for i in range(1, len(lst)):
        helper = lst[i]
        j = i-1
        while j >= 0 and helper < lst[j]:
            lst[j+1] = lst[j]
            j -= 1
        lst[j+1] = helper
    return lst


ex = []
for i in range(50):
    ex.append(randrange(0,50))
ex2 = ex

print(bubblesort(ex))
print(insertionSort(ex2))

