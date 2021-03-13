import unittest
from lista1 import quickSort, insertionSort

test_cases = [
    ([2, 6, 4, 9, 1, 10, 23, 55, 3, 107, 15], [1, 2, 3, 4, 6, 9, 10, 15, 23, 55, 107]),
    ([7, 4, 7, 20, 60, 3, 100], [3, 4, 7, 7, 20, 60, 100]),
    ([15, 74, 68, 3, 21, 180, 11, 10000], [3, 11, 15, 21, 68, 74, 180, 10000])
]

class TestSortingAlgorithms(unittest.TestCase):

    def test_quick_sort(self):
        for case in test_cases:
            test_list = case[0].copy()
            sorted_test_list = case[1]
            quickSort(test_list, 0, len(test_list) - 1)
            self.assertEqual(sorted_test_list, test_list)

    def test_insertion_sort(self):
        for case in test_cases:
            test_list = case[0].copy()
            sorted_test_list = case[1]
            insertionSort(test_list)
            self.assertEqual(sorted_test_list, test_list)


if __name__ == '__main__':
    unittest.main()