import random

n = int(input("Ile liczb posortować?: "))


def main(n):
    vlist = []
    for i in range(n):
        vlist.append(random.randint(1, 10000))

    bubble(vlist)
    insert(vlist)
    return vlist


def bubble(vlist):
    for i in range(len(vlist)):
        for j in range(len(vlist)):
            if vlist[i] < vlist[j]:
                vlist[i], vlist[j] = vlist[j], vlist[i]
    print(vlist)
    return vlist


def insert(vlist):
    for i in range(1, len(vlist)):
        a = vlist[i]
        j = i - 1
        while j >= 0 and vlist[j] > a:
            vlist[j + 1] = vlist[j]
            j -= 1
        vlist[j + 1] = a
    print(vlist)
    return vlist


main(n)
