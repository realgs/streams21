import numpy as np
from math import inf
import requests
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from itertools import count


def get_data(crypt, since):
    url = "https://bitbay.net/API/Public/{Currency[0]}{Currency[1]}/{Category}.json?since={since}".format(Currency=[crypt, 'USD'],
                                                                                            Category='trades', since=since)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
         print("Can't get data from API \n status code: ", response.status_code)


def count_minmax(data):
    max_sell = -inf
    min_buy = inf
    for trade in data:
        if trade['type'] == 'sell':
            if max_sell < trade['price']:
                max_sell = trade['price']
        elif trade['type'] == 'buy':
            if min_buy > trade['price']:
                min_buy = trade['price']

    return max_sell, min_buy

def data_stream(crypt, x, y_1, y_2, i):
    x.append(i)
    data = get_data(crypt, since= 50*i)
    max, min = count_minmax(data)
    y_1.append(min)
    y_2.append(max)
    return [x, y_1, y_2]



def animate(i):
    if i == stop_point:
        exit('FINISHED')
    global x, y_1, y_2
    temp = data_stream('DASH', x, y_1, y_2, i)
    x = temp[0]
    y_1 = temp[1]
    y_2 = temp[2]
    plt.plot(x, y_1)
    plt.plot(x, y_2)


def plot_data():
    ani = FuncAnimation(plt.gcf(), animate, interval=1000)

    plt.tight_layout()
    plt.show()

x = []
y_1 = []
y_2 = []
stop_point = 10

plot_data()

