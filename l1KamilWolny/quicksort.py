import numpy as np


def pivot_partition(numbers, min_index, max_index):
    pivot = numbers[(min_index + max_index) // 2]
    replace_index_1 = min_index - 1
    replace_index_2 = max_index + 1

    while True:
        replace_index_1 += 1
        while numbers[replace_index_1] < pivot:
            replace_index_1 += 1

        replace_index_2 -= 1
        while numbers[replace_index_2] > pivot:
            replace_index_2 -= 1

        if replace_index_1 >= replace_index_2:
            return replace_index_2

        numbers[replace_index_1], numbers[replace_index_2] = numbers[replace_index_2], numbers[
            replace_index_1]


def quick_sort(numbers, min_index, max_index):
    if min_index is None:
        min_index = 0
    if max_index is None:
        max_index = len(numbers - 1)
    if min_index < max_index:
        split_index = pivot_partition(numbers, min_index, max_index)
        quick_sort(numbers, min_index, split_index)
        quick_sort(numbers, split_index + 1, max_index)


def quick_sort_to_new(numbers):
    array = numbers.copy()
    quick_sort(array, 0, len(numbers) - 1)
    return array


# Example usage
print(quick_sort_to_new([5, 7, 4, 6, 10, 17, 3, 21, 4]))
