def partition(arr, start, end): 
	i = start - 1 
	pivot = arr[end]	 

	for j in range(start, end): 
		if arr[j] <= pivot: 
			i = i+1
			arr[i],arr[j] = arr[j],arr[i] 

	arr[i+1],arr[end] = arr[end],arr[i+1] 
	return i+1