def insertion_sort(local_list_to_sort):
    for iterator in range(1, len(local_list_to_sort)):
        value = local_list_to_sort[iterator]

        local_iterator = iterator - 1
        while local_iterator >= 0 and value < local_list_to_sort[local_iterator]:
            local_list_to_sort[local_iterator + 1] = local_list_to_sort[local_iterator]
            local_iterator -= 1

        local_list_to_sort[local_iterator + 1] = value

    return local_list_to_sort


def counting_sort(local_list_to_sort):
    list_of_occurrences = [0] * 100
    result_list = []

    for element in local_list_to_sort:
        list_of_occurrences[element] += 1

    for iterator in range(len(list_of_occurrences)):
        local_iterator = 0
        while local_iterator < list_of_occurrences[iterator]:
            local_iterator += 1
            result_list.append(iterator)

    return result_list


if __name__ == "__main__":
    list_to_sort = [34, 12, 56, 9, 2, 2, 2, 7, 11, 89, 54, 34, 38, 85, 83, 29, 29, 29, 93, 76, 28, 70]

    print("Insertion Sort")
    print(insertion_sort(list_to_sort))
    print("Counting Sort")
    print(counting_sort(list_to_sort))
