#sortowanie bąbelkowe
list = [6, 3, 7, 8, 20, 5, 64, 2, 10, 24, 2, 4, 6, 1, 1, 18, 20, 1, 14, 15, 16, 11]

def sort1(list):
    x = len(list)
    while x > 1:
        for l in range(0, x - 1):
            if list[l] > list[l + 1]:
                list[l], list[l + 1] = list[l + 1], list[l]
        x = x - 1

sort1(list)
print(list)
