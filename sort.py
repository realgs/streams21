import random
import copy


def bubble(num):
    for i in range(len(num)-1, 0, -1):
        for j in range(i):
            if num[j] > num[j+1]:
                temp = num[j]
                num[j] = num[j+1]
                num[j + 1] = temp

    return num


def insertion(num):
    for i in range(1, len(num)):
        j = i - 1
        nxt = num[i]

        while (num[j] > nxt) and (j >= 0):
            num[j + 1] = num[j]
            j = j - 1
        num[j + 1] = nxt

    return num


def rnd_data(a, b):
    rnd_list = []
    for m in range(10):
        rnd_list.append(random.randint(a, b))

    return rnd_list


data = [3, 15, 8, 26, 29, 54]

rnd_data1 = copy.deepcopy(rnd_data(1, 50))
rnd_data2 = copy.deepcopy(rnd_data(1, 50))
data1 = copy.deepcopy(data)
data2 = copy.deepcopy(data)


def test(sort):
    for k in range(0, len(sort) - 1):

        if sort[k] > sort[k + 1]:
            print ("Sortowanie nie wykonało się prawidłowo")

    print ("Sortowanie wykonało się prawidłowo")


bbl1 = bubble(rnd_data1)
ins1 = insertion(rnd_data2)
bbl2 = bubble(data1)
ins2 = insertion(data2)

print(bbl1, bbl2, ins1, ins2)

test(bbl1)
test(bbl2)
test(ins1)
test(ins2)
