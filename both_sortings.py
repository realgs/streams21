import random

def bubblesort(input_list):
    for i in range(len(input_list)):
        for j in range(0, (len(input_list)-1)-i):
            if input_list[j] > input_list[j+1]:
                input_list[j], input_list[j+1] = input_list[j+1],input_list[j]
    return input_list

def insertionsort(input_list):
    for i in range(len(input_list)):
        for j in range(0, i):
            if input_list[i] < input_list[j]:
                input_list[i], input_list[j] = input_list[j], input_list[i]
    return input_list

list = [random.randint(0,1000) for i in range(1000)]

list_1 = insertionsort(list)
list_2 = bubblesort(list)