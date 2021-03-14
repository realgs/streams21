def bubble_sort(numbers):
  l = numbers.copy()
  for i in range(len(l)):
    for j in range((len(l)-1)-i):
      if l[j] > l[j + 1]:
        temp = l[j]
        l[j] = l[j + 1]
        l[j + 1] = temp
  return l

def insertion_sort(numbers):
  l = numbers.copy()
  for i in range(len(l)):
    for j in range(i):
      if l[i] < l[j]:
        temp = l[i]
        l[i] = l[j]
        l[j] = temp
  return l
  