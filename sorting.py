def bubble_sort(list_to_sort:list):
    for i in range(len(list_to_sort)):
        any_change = False
        for j in range(len(list_to_sort)-i-1):
            if list_to_sort[j] > list_to_sort[j+1]:
                list_to_sort[j], list_to_sort[j+1] = list_to_sort[j+1], list_to_sort[j]
                any_change = True
        if not any_change:
            break
    return list_to_sort


def selection_sort(list_to_sort: list):
    for i in range(len(list_to_sort)):
        min_index = i
        for j in range(i+1, len(list_to_sort)):
            if list_to_sort[min_index] > list_to_sort[j]:
                min_index = j
        list_to_sort[i], list_to_sort[min_index] = list_to_sort[min_index], list_to_sort[i]
    return list_to_sort
