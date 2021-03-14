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