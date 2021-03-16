import time,random
def insertionsort(input_list):
    start = time.time()
    for i in range(len(input_list)):
        for j in range(0, i):
            if input_list[i] < input_list[j]:
                input_list[i], input_list[j] = input_list[j], input_list[i]
    stop = time.time()
    sorting_time = stop - start
    return input_list, sorting_time
list = [random.randint(0,1000) for i in range(1000)]
list = insertionsort(list[0])