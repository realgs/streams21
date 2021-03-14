from random import randint


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


def gen_random_array(size=10):
    return [randint(-100, 100) for _ in range(size)]


def run_usage_example():
    first_array_to_sort, second_array_to_sort = gen_random_array(), gen_random_array()

    print('Unsorted arrays:')
    print(f'#1: {first_array_to_sort}')
    print(f'#2: {second_array_to_sort}')

    bubble_sort(first_array_to_sort)
    insertion_sort(second_array_to_sort)

    print('Sorted arrays:')
    print(f'#1: {first_array_to_sort}')
    print(f'#2: {second_array_to_sort}')


if __name__ == '__main__':
    run_usage_example()
