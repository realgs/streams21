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
            print(type(item))
            print('xd')
            return False
    return True


def bubble_sort(array):
    if is_array_of_numbers(array) is not True:
        return print("The argument isn't an array or doesn't contain numbers")
    for i in range(len(array)):
        for j in range(0, len(array)-i-1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]


def insertion_sort(array):
    if is_array_of_numbers(array) is not True:
        return print("The argument isn't an array or doesn't contain numbers")
    for i in range(1, len(array)):
        temp = array[i]
        j = i-1

        while j >= 0 and array[j] > temp:
            array[j+1] = array[j]
            j -= 1

        array[j+1] = temp


test = [9, 8, 7, 6, 5, 4, 3, 2, 1]

print(test)
insertion_sort(test)
print(test)
