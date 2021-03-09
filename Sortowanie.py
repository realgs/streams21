import random

lista=[]
for i in range(10):
    lista.append(random.randint(0,10000))

def bąbelkowe(lista):
    for i in range (len(lista)):
        for j in range (0,(len(lista)-1)-i):
            if (lista[j]>lista[j+1]):
                większa=lista[j]
                lista[j]=lista[j+1]
                lista[j+1]=większa
    print(lista)

def wstawianie(lista):
    for i in range (len(lista)):
        for j in range (0,i):
            if (lista[i]<lista[j]):
                mniejsza=lista[i]
                lista[i]=lista[j]
                lista[j]=mniejsza
    print(lista)

bąbelkowe(lista)
wstawianie(lista)