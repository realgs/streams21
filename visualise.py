import requests as r
from time import sleep
from matplotlib import pyplot as plt
from requests.exceptions import HTTPError
from datetime import datetime
from matplotlib.animation import FuncAnimation
from apikey import apikey
import numpy as np
from tabulate import tabulate
import os
import tkinter as tk
from matplotlib.ticker import FormatStrFormatter

SLEEP_VALUE = 0.1

CHECK_LEGEND = 0

PLOT_VOLUME = 0

PLOT_RSI = 0

PLOT_AVERAGES = 0


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
        volume = data['volume']
        result.append([currency, buy_price, sell_price, volume])
        print_fetched_data(result)
    return result


def print_fetched_data(result):
    result = np.array(result)
    print('======================')
    print(tabulate(result, headers=[
          'currency', 'buy_price', 'sell_price', 'volume'], tablefmt='orgtbl'))


def split_data_into_packages(data):
    names = []
    result = {}
    for val in data:
        name = val[0]
        ask = val[1]
        bid = val[2]
        volume = val[3]
        time = datetime.now().strftime("%H:%M:%S")
        result.setdefault('name', []).append(name)
        result.setdefault('ask', []).append(ask)
        result.setdefault('bid', []).append(bid)
        result.setdefault('volume', []).append(volume)
    return result


def append_crypto_data_to_lists(names, asks, bids, volumes):
    for i in range(len(names)):
        y_ask_data.setdefault(names[i], []).append(asks[i])
        y_bid_data.setdefault(names[i], []).append(bids[i])
        y_volume_data.setdefault(names[i], []).append(volumes[i])


def draw_plots(x_data, y_ask_data, y_bid_data, y_volume_data, names):
    i = 0
    for plot in plots:
        plot.plot(x_data, y_ask_data[names[i]],
                  linewidth=1, label='Buy price of ' + names[i], color='Red')
        plot.plot(x_data, y_bid_data[names[i]],
                  linewidth=1, label='Sell price of ' + names[i], color='Blue')
        plot.set_xticks(x_data)
        plot_averages(
            x_data, plot, y_ask_data[names[i]], y_bid_data[names[i]], names, i)
        i += 1
    plot_volume_rsi(x_data, names, i)


def plot_averages(x_data, plot, ask_data, bid_data, names, i):
    if PLOT_AVERAGES == 0:
        return 0
    average_ask = sum(ask_data)/len(ask_data)
    y_ask_average_data.setdefault(names[i], []).append(average_ask)
    plot.plot(x_data, y_ask_average_data[names[i]],
              color='Orange', linewidth=0.5, label='Average buy price')

    average_bid = sum(bid_data)/len(bid_data)
    y_bid_average_data.setdefault(names[i], []).append(average_bid)
    plot.plot(x_data, y_bid_average_data[names[i]],
              color='Black', linewidth=0.5, label='Average sell price')


def plot_volume_rsi(x_data, names, i):
    if PLOT_RSI == 1:
        plot_rsi(x_data, names)
    if PLOT_VOLUME == 1:
        plot_volume(x_data, names)


def plot_rsi(x_data, names):

    i = 0
    for plot in plots_twinx:
        name = names[i]
        RSI = get_rsi(name[0:3])
        while RSI == 0:
            RSI = get_rsi(name[0:3])
        RSI = RSI['value']
        y_rsi_data.setdefault(name, []).append(RSI)
        plot.plot(x_data, y_rsi_data[name],
                  color='Purple', linewidth=1, label='RSI')
        i += 1


def plot_volume(x_data, names):

    i = 0
    for plot in plots_twinx:
        name = names[i]
        plot.plot(x_data, y_volume_data[name],
                  color='Purple', linewidth=1, label='Volume')
        i += 1


def get_rsi(crypto):
    sleep(SLEEP_VALUE)
    secret_api_key = apikey()
    URL = f'https://api.taapi.io/rsi?secret={secret_api_key}&exchange=binance&symbol={crypto}/USDT&interval=1h'

    try:
        response = r.get(URL)
        response.raise_for_status()

    except HTTPError:
        print(f'Error: : {HTTPError}')

    else:
        return response.json()


def draw_legend_once():
    global CHECK_LEGEND
    if CHECK_LEGEND == 0:
        for plot in plots:
            plot.legend()
        for plot in plots_twinx:
            plot.legend()
        CHECK_LEGEND = 1


def animation_frame(i):
    data = fetchFromAPI(currencies, category)
    splitted_data = split_data_into_packages(data)
    names = splitted_data['name']
    asks = splitted_data['ask']
    bids = splitted_data['bid']
    volumes = splitted_data['volume']
    x_data.append(datetime.now().strftime("%H:%M:%S"))

    append_crypto_data_to_lists(names, asks, bids, volumes)

    draw_plots(x_data, y_ask_data, y_bid_data, y_volume_data, names)

    draw_legend_once()


def plot_setup():
    plt.style.use('seaborn')
    fig.suptitle('Cryptocurrencies in real time')
    for plot in plots:
        plot.set_xlabel('Time')
        plot.set_ylabel('Value in PLN')
        plt.setp(plot.xaxis.get_majorticklabels(), rotation=45)
    plt.tight_layout()


def animate_plots():
    plot_setup()
    anim = FuncAnimation(plt.gcf(), animation_frame, interval=5000)
    plt.show()


def set_plots():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1)
    plots = []
    plots.append(ax1)
    plots.append(ax2)
    plots.append(ax3)

    plots_twinx = []
    plots_twinx.append(ax1.twinx())
    plots_twinx.append(ax2.twinx())
    plots_twinx.append(ax3.twinx())

    return fig, plots, plots_twinx


if __name__ == "__main__":
    currencies = ['LSK', 'LTC', 'BTC']
    category = 'ticker'
    currency = 'PLN'
    currencies = add_currency_to_currencies(currencies, currency)

    x_data = []
    y_ask_data = {}
    y_bid_data = {}
    y_ask_average_data = {}
    y_bid_average_data = {}
    y_volume_data = {}
    y_rsi_data = {}
    fig, plots, plots_twinx = set_plots()

    animate_plots()
