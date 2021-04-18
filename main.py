import numpy as np

from math import inf
import requests
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from itertools import count
import copy



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

def data_stream(crypt, x, y_1, y_2, i, range=5):
    x.append(i)
    data = get_data(crypt, 'trades')
    min, max = count_minmax(data)
    y_1.append(min)
    y_2.append(max)
    if len(x) > range:
        x.pop(0)
        y_1.pop(0)
        y_2.pop(0)
    return [x, y_1, y_2]



def animate(i):
    global x, y_1, y_2, legend
    print(x, y_1, y_2)

    temp = data_stream('DASH', x, y_1, y_2, i)
    x = temp[0]
    y_1 = temp[1]
    y_2 = temp[2]

    ax.plot(x, y_1, label= 'min1', color= 'red')
    ax.plot(x, y_2, label= 'max1', color = 'blue')
    legend = ax.legend(['min1', 'max1'])


def plot_data(x_label, y_label, title):
    ani = FuncAnimation(fig, func=animate, interval=1000)


    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    #plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 5))
    line, = ax.plot([], [], lw=3)
    legend = ''
    x = []
    y_1 = []
    y_2 = []
    stop_point = 10
    crypt = 'BTC'
    currency = 'USD'
    plot_data('', currency, crypt)

    url = "https://bitbay.net/API/Public/{Currency[0]}{Currency[1]}/{Category}.json?sort=desc".format(Currency=[crypt, currency], Category='trades')
    print(url)