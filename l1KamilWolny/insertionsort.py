import numpy as np


def insertion_sort(numbers):
    for insert_index in range(len(numbers)):
        insert_number = numbers[insert_index]
        index_number_replace = insert_index - 1

        while index_number_replace >= 0 and numbers[index_number_replace] > insert_number:
            numbers[index_number_replace + 1] = numbers[index_number_replace]
            index_number_replace -= 1

        numbers[index_number_replace + 1] = insert_number


def insertion_sort_to_new(numbers):
    array = numbers.copy()
    insertion_sort(array)
    return array


# Example usage
print(insertion_sort_to_new(np.array([30, 5, 7, 4, 6, 10, 17, 3, 21, 4])))
