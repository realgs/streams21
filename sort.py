import random

def bubble(list_of_num):
    for i in range ( len ( list_of_num ) - 1, 0, -1 ):
        for j in range ( i ):
            if list_of_num[j] > list_of_num[j + 1]:
                temp = list_of_num[j]
                list_of_num[j] = list_of_num[j + 1]
                list_of_num[j + 1] = temp

    return list_of_num


def insertion(list_of_num):
    for i in range ( 1, len ( list_of_num ) ):
        j = i - 1
        nxt = list_of_num[i]

        while (list_of_num[j] > nxt) and (j >= 0):
            list_of_num[j + 1] = list_of_num[j]
            j = j - 1
        list_of_num[j + 1] = nxt

    return list_of_num


list_of_num = [3, 15, 8, 26, 29, 54]

sorted_list1 = bubble ( list_of_num )
sorted_list2 = insertion ( list_of_num )

print(sorted_list1)
print(sorted_list2)
