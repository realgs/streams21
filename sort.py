import random


def bubble(num):
    for i in range ( len ( num ) - 1, 0, -1 ):
        for j in range ( i ):
            if num[j] > num[j + 1]:
                temp = num[j]
                num[j] = num[j + 1]
                num[j + 1] = temp

    return num


def insertion(num):
    for i in range ( 1, len ( num ) ):
        j = i - 1
        nxt = num[i]

        while (num[j] > nxt) and (j >= 0):
            num[j + 1] = num[j]
            j = j - 1
        num[j + 1] = nxt

    return num


list_of_num = [3, 15, 8, 26, 29, 54]

random_list = []

for m in range (10):
    random_list.append (random.randint (1, 50))

sorted_list1 = bubble (list_of_num)
sorted_list2 = insertion (list_of_num)
sorted_list3 = bubble (random_list)
sorted_list4 = insertion (random_list)


def test(sorted):
    for k in range ( 0, len ( sorted ) - 1 ):

        if sorted[k] > sorted[k + 1]:
            print ("Sortowanie nie wykonało się prawidłowo")

    print ("Sortowanie wykonało się prawidłowo")


test (sorted_list1)
test (sorted_list2)
test (sorted_list3)
test (sorted_list4)

print(sorted_list1)
print(sorted_list2)
print(sorted_list3)
print(sorted_list4)