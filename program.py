import bubblesort
import selectionsort

list_of_nums = [9, 21, 28, 21, 5, 2, 20, 18, 1, 8, 4, 12, 15, 1, 0, 0, 100, 125, 789, 18]
bubblesort.bubble_sort(list_of_nums)
print(list_of_nums)

list_of_sorted_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
bubblesort.bubble_sort(list_of_sorted_nums)
print(list_of_sorted_nums)

list_of_nums = [9, 21, 28, 21, 5, 2, 20, 18, 1, 8, 4, 12, 15, 1, 0, 0, 100, 125, 789, 18]
selectionsort.selection_sort(list_of_nums)
print(list_of_nums)

list_of_sorted_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
selectionsort.selection_sort(list_of_sorted_nums)
print(list_of_sorted_nums)