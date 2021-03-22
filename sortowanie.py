from numpy.random import randint


def insertion_sort(t):
    for i in range(1, len(t)):
        el = t[i]
        k = i - 1
        while k >= 0 and t[k] > el:
            t[k + 1] = t[k]
            k -= 1
        t[k + 1] = el
    return t


def quick_sort(t, x, y):
    if x >= y:
        return
    i = x
    j = y
    v = t[x + (y - x) // 2]
    while i <= j:
        while v > t[i]:
            i += 1
        while v < t[j]:
            j -= 1
        if i <= j:
            t[i], t[j] = t[j], t[i]
            i += 1
            j -= 1
    if x < j:
        quick_sort(t, x, j)
    if i < y:
        quick_sort(t, i, y)


def issorted(t):
    return t == sorted(t)


# przykladowy komentarz
a = [randint(150) for x in range(100)]
t = a.copy()
t2 = a.copy()
print("Czy a jest posortowane? :", issorted(insertion_sort(t)))
print("Czy b jest posortowane? :", issorted(insertion_sort(t2)))
