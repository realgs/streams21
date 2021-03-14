from random import randint
import copy


def tworzenie_rand_list(n):
    return [randint(1, 99) for x in range(n)]


def bubble_sort(L):
    for i in range(len(L)):
        for j in range(0, (len(L)-1)-i):
            if L[j] > L[j+1]:
                temp = L[j]
                L[j] = L[j+1]
                L[j+1] = temp

    print("posortowana lista:", L)
    return(L)


def select_sort(L):
    for i in range(len(L)):
        for j in range(i+1, len(L)):
            if L[i] > L[j]:
                temp = L[i]
                L[i] = L[j]
                L[j] = temp

    print("posortowana lista: ", L)
    return(L)


def bucket_sort(L, maxL):
    out = []
    ctr = [0] * maxL
    for i in L:
        ctr[i] += 1

    for i in range(maxL):
        for k in range(ctr[i]):
            out.append(i)

    print("posortowana lista:", out)
    return out


def listy(n):
    L = tworzenie_rand_list(n)
    L1 = copy.deepcopy(L)
    L2 = copy.deepcopy(L)
    print(f"Tablica do sortowania: {L}")
    # bubble_sort(L)
    select_sort(L1)
    bucket_sort(L2, 100)


if __name__ == "__main__":
    listy(200)
