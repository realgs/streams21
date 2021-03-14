import random as rd

data_bubble = []
data_ins = []

for i in range(10):
    data_bubble.append(rd.randint(1,10))
    data_ins.append(rd.randint(1, 10))

def bubble_sort(data):
    for i in range(len(data)):
        for j in range(len(data) - 1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]


def insertion_sort(data):
    for i in range(1,len(data)):
        temp = data[i]
        j = i - 1
        while j>=0 and data[j]>temp:
            data[j + 1] = data[j]
            j = j - 1
        data[j + 1] = temp

print(data_bubble)
bubble_sort(data_bubble)
print(data_bubble)

print(data_ins)
insertion_sort(data_ins)
print(data_ins)
