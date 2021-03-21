from random import randint
import unittest

List_to_sort = []
for i in range(30):
    List_to_sort.append(randint(1, 1000))


def Bubble_sort(List_to_sort):
    for i in range(len(List_to_sort)):
        for j in range(0,(len(List_to_sort))-1):
            if (List_to_sort[j] > List_to_sort[j+1]):
                temp = List_to_sort[j]
                List_to_sort[j] = List_to_sort[j+1]
                List_to_sort[j+1] = temp

    return List_to_sort


def Insert_sort(List_to_sort):
    for i in range(len(List_to_sort)):
        for j in range(0, i):
            if (List_to_sort[i] < List_to_sort[j]):
                temp = List_to_sort[i]
                List_to_sort[i] = List_to_sort[j]
                List_to_sort[j] = temp
    return List_to_sort

sorted_bubble=Bubble_sort(List_to_sort)
sorted_insert=Insert_sort(List_to_sort)
print(sorted_bubble)
print(sorted_insert)


class SortingMethodsTest(unittest.TestCase):
    def Bubble_sort_test(self):
        self.assertEqual(Bubble_sort(List_to_sort), sorted(List_to_sort))
    def Insert_sort_test(self):
        self.assertEqual(Insert_sort(List_to_sort), sorted(List_to_sort))


unittest.main()