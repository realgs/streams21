def insertion_sort(t):
    for i in range(1, len(t)):
        el = t[i]
        k = i - 1
        while k >= 0 and t[k] > el:
            t[k + 1] = t[k]
            k -= 1
        t[k + 1] = el
    return t