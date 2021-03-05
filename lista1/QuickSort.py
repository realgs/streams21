def partition(arr, start, end): 
	i = start - 1 
	pivot = arr[end]	 

	for j in range(start, end): 
		if arr[j] <= pivot: 
			i = i+1
			arr[i],arr[j] = arr[j],arr[i] 

	arr[i+1],arr[end] = arr[end],arr[i+1] 
	return i+1

def quickSort(arr, start, end): 
	if start < end: 
		p = partition(arr, start, end) 
		quickSort(arr, start, p-1) 
		quickSort(arr, p+1, end) 

numbers = [50, 32, 16, 24, 78, 13, 29, 89, 67, 22, 34, 86, 95, 19, 37]
length = len(numbers) 
quickSort(numbers, 0, length-1) 
print (f"Result: {numbers}")