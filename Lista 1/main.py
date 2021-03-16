def insertion_sort(list_to_sort):
    print("Insertion Sort")


def counting_sort(list_to_sort):
    print("Counting Sort")
    list_of_results = [0] * 100

    for element in list_to_sort:
        list_of_results[element] += 1

    for iterator in range(len(list_of_results)):
        i = 0
        while i < list_of_results[iterator]:
            print(iterator)
            i += 1


if __name__ == "__main__":
    list_to_sort = [34, 12, 56, 9, 2, 2, 2, 7, 11, 89, 54, 34, 38, 85, 83, 29, 29, 29, 93, 76, 28, 70]

    insertion_sort(list_to_sort)
    counting_sort(list_to_sort)