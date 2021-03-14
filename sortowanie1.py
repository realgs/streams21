#Bubble Sort
example = [10,5,4,12,3,2,1]

def BubbleSort(array):
    while True:
        onOff = True
        
        for elements in range(0,len(array)-1):
            if array[elements] > array[elements+1]:
                var = array[elements]
                array[elements] = array[elements+1]
                array[elements+1] = var
                onOff = False
        if onOff == True:
            print(array)
            break;
        if onOff == False:
            onOff = True

BubbleSort(example)