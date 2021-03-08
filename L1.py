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




