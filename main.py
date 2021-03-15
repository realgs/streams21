from random import randint


def is_array(array):
    if type(array) is not list:
        print("Arg isn't an array")
        return False
    return True


def is_array_of_numbers(array):
    if is_array(array) is not True:
        return False
    for item in array:
        if type(item) is not int and type(item) is not float:
            return False
    return True


def bubble_sort(array):
    for i in range(len(array)):
        for j in range(0, len(array)-i-1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]


def insertion_sort(array):
    for i in range(1, len(array)):
        temp = array[i]
        j = i-1

        while j >= 0 and array[j] > temp:
            array[j+1] = array[j]
            j -= 1

        array[j+1] = temp


def handler(array, alg='bubble'):
    print('=====================')
    if is_array_of_numbers(array) is not True:
        return print("The argument isn't an array or doesn't contain numbers")

    print(f'Before sort: {array}')

    if alg == 'bubble':
        bubble_sort(array)
    elif alg == 'insertion':
        insertion_sort(array)

    print(f'[{alg}] Sorted: {array}')
    print('=====================')


if __name__ == "__main__":
    test_array_one = [randint(1, 50) for _ in range(10)]
    test_array_two = [randint(1, 50) for _ in range(10)]

    handler(test_array_one, 'bubble')
    handler(test_array_two, 'insertion')
