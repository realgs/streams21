from random import randint
#Bartosz Stec
def insert(list):
    for i in range(1, len(list)):
        temp = list[i]
        j = i - 1
        while j >= 0 and list[j] > temp:
            list[j + 1] = list[j]
            j -= 1
        list[j + 1] = temp
    return list

def bubble(list):
    listLen = len(list)
    while listLen > 1:
        replace = False
        for i in range(0, listLen - 1):
            if list[i] > list[i + 1]:
                list[i], list[i + 1] = list[i + 1], list[i]
                replace = True
        listLen -= 1
        if replace == False: break
    return list

A=[]
for i in range(50):
    A.append(randint(1,100))
B=[]
for i in range(50):
    B.append(randint(-100,-1))

print(f'Przez wstawienie: {insert(A)}')
print(f'Bąbelkowe: {bubble(B)}')





