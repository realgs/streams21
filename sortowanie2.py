# Insert Sort
example = [5,4,10,122,1,0,3,2,1]

def InsertSort(array):

    arrayOut = []
    tf = True

    arrayOut.append(array[0])
    for elements in range(1,len(array)):
        var = array[elements]
        for inElem in range(len(arrayOut)):
            if var < arrayOut[inElem]:
                arrayOut.insert(inElem, var)
                tf = False
                break;
        if tf == True:
            arrayOut.append(var)
        tf = True
    print(arrayOut)

InsertSort(example)
