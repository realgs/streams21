from random import randint
#prosze mnie nie bić, jutro skończe bo dziś miałem problemy z ukrytymi plikami
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






