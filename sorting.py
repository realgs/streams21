
def bubble_sort(list):
    l = len(list)
    for i in range(l-1):
        for j in range(0, l -i-1 ):
            if list[j]>list[j+1]:
                list[j], list[j+1] = list[j+1], list[j]
    return list


def devide_and_conquer_alg(list, min, max):
    i = (min - 1)
    pivot = list[max]  # pivot
    for j in range(min, max):
        if list[j] <= pivot:
            i = i + 1
            list[i], list[j] = list[j], list[i]

    list[i + 1], list[max] = list[max], list[i + 1]
    return (i + 1)

def quick_sort(list, min, max):
    if len(list) == 1:
        return list
    if min < max:
        part = devide_and_conquer_alg(list, min, max)
        quick_sort(list, min, part - 1)
        quick_sort(list, part + 1, max)

def quick_sort_resault(list):
    n = len(list)
    quick_sort(list, 0, n - 1)
    result= []
    for i in range(n):
        result.append(list[i])
    return result

example = [20, 17, 4, 2, 11, 14, 21, 18, 7, 1, 10, 13]
print(bubble_sort(example))
print(quick_sort_resault(example))