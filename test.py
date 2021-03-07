import copy
import unittest
import time
import sorting


my_list = [436, 361, 710, 169, 169, 291, 288, 736, 316, 859, 475, 167, 506, 644, 626, 307, 986, 270, 13, 652, 789, 932,
           59, 73, 207, 226, 438, 448, 830, 154, 911, 487, 152, 321, 78, 451, 474, 140, 750, 35, 846, 869, 964, 665,
           488, 200, 320, 744, 164, 352, 478, 224, 44, 468, 639, 327, 628, 248, 995, 856, 872, 693, 59, 465, 142, 949,
           829, 326, 210, 977, 247, 915, 426, 705, 575, 375, 258, 623, 581, 394, 590, 661, 576, 804, 987, 717, 720,
           453, 962, 595, 765, 661, 489, 513, 711, 2, 944, 687, 710, 668]


class TestSortingAlgorithms(unittest.TestCase):
    def test_bubble_sort(self):
        global my_list
        start = time.perf_counter()
        self.assertEqual(sorted(copy.copy(my_list)), sorting.bubble_sort(copy.copy(my_list)),
                         "Bubble Sort not implemented correctly")
        stop = time.perf_counter()
        print(f"\nduration: {stop-start}")

    def test_selection_sort(self):
        global my_list
        start = time.perf_counter()
        self.assertEqual(sorted(copy.copy(my_list)), sorting.selection_sort(copy.copy(my_list)),
                         "Selection Sort not implemented correctly")
        stop = time.perf_counter()
        print(f"\nduration: {stop - start}")
