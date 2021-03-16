import time,random
def bubblesort(input_list):
    start = time.time()
    for i in range(len(input_list)):
        for j in range(0, (len(input_list)-1)-i):
            if input_list[j] > input_list[j+1]:
                input_list[j], input_list[j+1] = input_list[j+1],input_list[j]
    stop = time.time()
    sorting_time = stop - start
    return input_list, sorting_time
list = [random.randint(0,1000) for i in range(1000)]
list = bubblesort(list[0])