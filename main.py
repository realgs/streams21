import numpy as np

from math import inf
import requests
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from itertools import count


#liczba punktów na X = 20. jest przemiszczny wykres w prawo

#to co jest w korniu wpisać w __main__

def get_data(crypt, req_type):
    url = "https://bitbay.net/API/Public/{Currency[0]}{Currency[1]}/{Category}.json".format(Currency=[crypt, 'USD'],
                                                                                            Category= req_type)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
         print("Can't get data from API \n status code: ", response.status_code)


def count_minmax(data):
    min_sell = inf
    max_buy = -inf
    for trade in data:
        if trade['type'] == 'sell':
            if min_sell > trade['price']:
                min_sell = trade['price']
        elif trade['type'] == 'buy':
            if max_buy < trade['price']:
                max_buy = trade['price']

    return min_sell, max_buy

def data_stream(crypt, x, y_1, y_2, i):
    x.append(i)
    data = get_data(crypt, 'orderbook')
    min, max = count_minmax(data)
    y_1.append(min)
    y_2.append(max)
    return [x, y_1, y_2]



def animate(i):
    global x, y_1, y_2, stop_point
    if i == stop_point:
        exit('FINISHED')
    temp = data_stream('DASH', x, y_1, y_2, i)
    #fig, ax = plt.subplots(1)
    x = temp[0]
    y_1 = temp[1]
    y_2 = temp[2]
    plt.plot(x, y_1, label= 'min1', color= 'red')
    plt.plot(x, y_2, label= 'max1', color = 'green')
    plt.legend()

def plot_data():
    ani = FuncAnimation(plt.gcf(), func=animate, interval=1000)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Jakiś wykres')
    #plt.legend()
    plt.tight_layout()
    plt.show()


x = []
y_1 = []
y_2 = []
stop_point = 10

#plot_data()
crypt = 'BTC'
url = "https://bitbay.net/API/Public/{Currency[0]}{Currency[1]}/{Category}.json".format(Currency=[crypt, 'USD'], Category='market')
print(url)