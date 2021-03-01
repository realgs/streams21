def bubble_sort(array):
    if type(array) is not list:
        return print("Arg isn't an array")
    for i in range(len(array)):
        for j in range(0, len(array)-i-1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
