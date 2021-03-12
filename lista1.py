from random import randint


def genData(num_of_numbers, num_range):
    numbers = []
    for i in range(num_of_numbers):
        numbers.append(randint(1, num_range))
    return numbers


dane = genData(100, 200)
print(dane)
