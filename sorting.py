from random import randint
numbers = [randint(0,100) for i in range(100)]

def bubble_sort(numbers):
    for i in range(len(numbers)):
        for j in range(0, len(numbers) - 1 - i):
            if numbers[j] > numbers[j+1]:
                temp = numbers[j]
                numbers[j] = numbers[j+1]
                numbers[j+1] = temp
    return numbers

def insertion_sort(numbers):
    for i in range(len(numbers)):
        for j in range(0, i):
            if numbers[i] < numbers[j]:
                temp = numbers[i]
                numbers[i] = numbers[j]
                numbers[j] = temp
    return numbers
print(numbers)
numbers2=numbers.copy()
print(bubble_sort(numbers))
print(insertion_sort(numbers))

def sort_test(sorted_numbers):
    for i in range(len(sorted_numbers)-1):
        if sorted_numbers[i] <= sorted_numbers[i+1]:
            continue
        else:
            print('Sort failed')

sort_test(bubble_sort(numbers))
sort_test(insertion_sort(numbers))
