def bubblesort(list, listLen):
    while listLen > 1:
        replace = False
        for i in range(0, listLen - 1):
            if list[i] > list[i + 1]:
                list[i], list[i + 1] = list[i + 1], list[i]
                replace = True
        listLen -= 1
        if replace == False:
            break
    return list