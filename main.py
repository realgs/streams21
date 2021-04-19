import numpy as np

from math import inf
import requests
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from itertools import count
import copy


def get_data(crypt, req_type):
    url = "https://bitbay.net/API/Public/{Currency[0]}{Currency[1]}/{Category}.json".format(Currency=[crypt, 'USD'],
                                                                                            Category=req_type)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Can't get data from API \n status code: ", response.status_code)


def last_trades(data):
    sell, buy = None, None
    sell_01 = 0
    buy_01 = 0
    for trade in data:
        if (sell_01, buy_01) == (1, 1):
            break
        if sell_01 == 0:
            if trade['type'] == 'sell':
                sell = trade['price']
                sell_01 = 1
        if buy_01 == 0:
            if trade['type'] == 'buy':
                buy = trade['price']
                buy_01 = 1
    return sell, buy


def data_stream(crypt, x, y_1, y_2, i, range=5):
    x.append(i)
    data = get_data(crypt, 'trades')
    min, max = last_trades(data)
    y_1.append(min)
    y_2.append(max)
    if len(x) > range:
        x.pop(0)
        y_1.pop(0)
        y_2.pop(0)
    return [x, y_1, y_2]


def animate(i):
    global x, x_2, y_1, y_2, y_3, y_4, y_5, y_6

    print('LTC: ', x, y_1, y_2)
    print('BTC: ', x_2, y_3, y_4)
    print('DASH: ', x_3, y_5, y_6, '\n')

    temp_LTC = data_stream('LTC', x, y_1, y_2, i)
    temp_BTC = data_stream('BTC', x_2, y_3, y_4, i)
    temp_DASH = data_stream('DASH', x_3, y_5, y_6, i)

    x, y_1, y_2 = temp_LTC[0], temp_LTC[1], temp_LTC[2]
    y_3, y_4 = temp_BTC[1], temp_BTC[2]
    y_5, y_6 = temp_DASH[1], temp_DASH[2]

    ax.plot(x, y_1, label='LTC_sell', color='red')
    ax.plot(x, y_2, label='LTC_buy', color='blue')

    ax.plot(x_2, y_3, label='BTC_sell', color='green')
    ax.plot(x_2, y_4, label='BTC_buy', color='yellow')

    ax.plot(x_3, y_5, label='DASH_sell', color='pink')
    ax.plot(x_3, y_6, label='DASH_buy', color='brown')

    legend = ax.legend(['', 'LTC_sell', 'LTC_buy', 'BTC_sell', 'BTC_buy', 'DASH_sell', 'DASH_buy'])


def plot_data(x_label, y_label, title):
    ani = FuncAnimation(fig, func=animate, interval=1000)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 5))
    line, = ax.plot([], [], lw=3)
    x, x_2, x_3 = [], [], []
    y_1, y_2, y_3, y_4, y_5, y_6 = [], [], [], [], [], []

    plot_data('', 'USD', 'Trades')
