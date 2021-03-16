import random
import unittest


def random_list(k=1000, a=1, b=100):
    m = [random.randint(a, b) for _ in range(k)]
    return m


def bubble(m):
    for i in range(len(m)):
        for j in range(len(m)-1):
            if m[j] > m[j+1]:
                temp = m[j]
                m[j] = m[j+1]
                m[j+1] = temp
    return m


def insertion(m):
    for i in range(len(m)):
        for j in range(i):
            if m[i] < m[j]:
                temp = m[i]
                m[i] = m[j]
                m[j] = temp
    return m


class SortingMethodsTestCase(unittest.TestCase):

    def test_bubble(self):
        m = random_list()
        self.assertEqual(bubble(m), sorted(m))

    def test_insertion(self):
        m = random_list()
        self.assertEqual(insertion(m), sorted(m))


unittest.main()

