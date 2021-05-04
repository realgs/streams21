import requests as r
from time import sleep
from matplotlib import pyplot as plt
from requests.exceptions import HTTPError
from datetime import datetime
from matplotlib.animation import FuncAnimation
from apikey import apikey
import numpy as np
from tabulate import tabulate

SLEEP_VALUE = 0.1

CHECK = 0


def add_currency_to_currencies(currencies, currency):
    result = []
    for c in currencies:
        result.append(c+currency)
    return result


def download_data(currency, caregory):
    URL = f'https://bitbay.net/API/Public/{currency}/{category}.json'
    try:
        response = r.get(URL)
        response.raise_for_status()

    except HTTPError:
        print(f'Error: : {HTTPError}')

    else:
        return response.json()


def fetchFromAPI(currencies, category):
    result = []
    for currency in currencies:
        data = download_data(currency, category)
        sleep(SLEEP_VALUE)
        buy_price = data['ask']
        sell_price = data['bid']
        result.append([currency, buy_price, sell_price])
    return result


def split_data_into_packages(data):
    names = []
    result = {}
    for val in data:
        name = val[0]
        ask = val[1]
        bid = val[2]
        time = datetime.now().strftime("%H:%M:%S")
        result.setdefault('name', []).append(name)
        result.setdefault('ask', []).append(ask)
        result.setdefault('bid', []).append(bid)
    return result


def append_crypto_data_to_lists(names, asks, bids):
    for i in range(len(names)):
        y_ask_data.setdefault(names[i], []).append(asks[i])
        y_bid_data.setdefault(names[i], []).append(bids[i])


def draw_plots(x_data, y_ask_data, y_bid_data, names):
    for i in range(len(names)):
        plt.plot(x_data, y_ask_data[names[i]],
                 linewidth=1, label='Buy price of ' + names[i])
        plt.plot(x_data, y_bid_data[names[i]],
                 linewidth=1, label='Sell price of ' + names[i])

    plt.subplots_adjust(bottom=0.2, left=0.2, right=0.9)
    plt.xticks(x_data)


def draw_legend_once():
    global CHECK
    if CHECK == 0:
        plt.legend()
        CHECK = 1


def animation_frame(i):
    data = fetchFromAPI(currencies, category)
    splitted_data = split_data_into_packages(data)
    names = splitted_data['name']
    asks = splitted_data['ask']
    bids = splitted_data['bid']
    x_data.append(datetime.now().strftime("%H:%M:%S"))

    append_crypto_data_to_lists(names, asks, bids)

    draw_plots(x_data, y_ask_data, y_bid_data, names)

    plt.xlabel('Time')
    plt.ylabel('Value in USD')

    draw_legend_once()


if __name__ == "__main__":
    currencies = ['LSK', 'LTC', 'DASH']
    category = 'ticker'
    currency = 'USD'
    currencies = add_currency_to_currencies(currencies, currency)

    x_data = []
    y_ask_data = {}
    y_bid_data = {}

    anim = FuncAnimation(plt.gcf(), animation_frame, interval=5000)
    plt.show()