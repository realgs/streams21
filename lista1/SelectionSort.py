def selectSort(arr):
    for i in range(len(arr) - 1):
        for j in range(i, len(arr)):
            if(arr[i] > arr[j]):
                arr[i],arr[j] = arr[j],arr[i]

numbers = [50, 32, 16, 24, 78, 13, 29, 89, 67, 22, 34, 86, 95, 19, 37]
selectSort(numbers)
print(f"Result: {numbers}")