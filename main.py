def bubble_sort(array):
    array_size = len(array)
    for i in range(array_size):
        is_sorted = True
        for j in range(array_size - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                is_sorted = False

        if is_sorted:
            break


def insertion_sort(array):
    for i in range(1, len(array)):
        tmp = array[i]
        j = i - 1

        while j >= 0 and array[j] > tmp:
            array[j + 1] = array[j]
            j -= 1

        array[j + 1] = tmp