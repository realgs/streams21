test_arr = [5, 7, 9, 6, 1, 5, 4, 2, 3]

def bubble_sort(list):
    n = len(list)
    for i in range(0, n-1):
        for j in range(0, n-1-i):
            if list[j] > list[j+1]:
                list[j], list[j+1] = list[j+1], list[j]
    return list

def selection_sort(list):
    n = len(list)
    for i in range(0, n):
        index_of_min = i
        for j in range(i + 1, n):
            if list[j] < list[index_of_min]:
                index_of_min = j

        list[i], list[index_of_min] = list[index_of_min], list[i]

    return list
