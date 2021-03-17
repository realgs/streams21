def bubble_sort(tab):
    n = len(tab)
    flag = True

    while flag:
        for i in range(0, n - 1):
            if tab[i] > tab[i + 1]:
                tab[i], tab[i + 1] = tab[i + 1], tab[i]
        n = n - 1
        if n == 1:
            flag = False
    return tab

def sort_by_insert(tab):
    n = len(tab)
    for i in range(1,n):
        actvar = tab[i]
        j = i - 1
        while j >= 0 and tab[j] > actvar:
            tab[j + 1] = tab[j]
            j = j - 1
        tab[j + 1] = actvar
    return tab

tab1 = [7, 5, -4, 0, 6, 12, -5]
tab2 = [7, 3, -4, 0, 6, 10, -5]
print(bubble_sort(tab1))
print(sort_by_insert(tab2))