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

PLOT_VOLUME = 1

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
        print(f'Bitbay error: : {HTTPError}')

    else:
        return response.json()


def fetchFromAPI(currencies, category):
    result = []
    for currency in currencies:
        data = download_data(currency, category)
        while data == None:
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
        plot.set_ylabel('RSI value')
        name = names[i]
        RSI = get_rsi(name[0:3], interval)
        while RSI == 0:
            RSI = get_rsi(name[0:3], interval)
        RSI = RSI['value']
        y_rsi_data.setdefault(name, []).append(RSI)
        plot.plot(x_data, y_rsi_data[name],
                  color='Purple', linewidth=1, label='RSI')
        i += 1


def plot_volume(x_data, names):

    i = 0
    for plot in plots_twinx:
        plot.set_ylabel('Volume value')
        name = names[i]
        plot.plot(x_data, y_volume_data[name],
                  color='Purple', linewidth=1, label='Volume')
        i += 1


def get_rsi(crypto, interval):
    sleep(SLEEP_VALUE)
    secret_api_key = apikey()
    URL = f'https://api.taapi.io/rsi?secret={secret_api_key}&exchange=binance&symbol={crypto}/USDT&interval={interval}'

    try:
        response = r.get(URL)
        response.raise_for_status()

    except HTTPError:
        print('RSI ERROR', response.json())
        return 0
    else:
        return response.json()


def draw_legend_once():
    global CHECK_LEGEND
    if CHECK_LEGEND == 0:
        for plot in plots:
            if PLOT_AVERAGES == 0:
                plot.legend(loc=2, bbox_to_anchor=(0, 1.6))
            else:
                plot.legend(loc=2, bbox_to_anchor=(0, 1.95))
        for plot in plots_twinx:
            plot.legend(loc=1, bbox_to_anchor=(1, 1.4))
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
    fig.suptitle('Cryptocurrencies in real time')
    i = 0
    for plot in plots:
        plot.set_xlabel('Time')
        plot.set_ylabel('Value in PLN')
        plot.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plt.setp(plot.xaxis.get_majorticklabels(), rotation=45)
        plot.set_title(currencies[i])
        i += 1
    for plot in plots_twinx:
        plot.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
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


def gui_plot_decide():
    root = tk.Tk()
    root.title(
        'Cryptocurrency in real time startup, choose what you want then close this window')
    canvas1 = setup_canvas(root)
    button1, button2, button3 = setup_buttons()
    canvas1 = create_windows(canvas1, button1, button2, button3)
    root.mainloop()


def setup_canvas(root):
    canvas1 = tk.Canvas(root, width=600, height=320,
                        bg='gray90', relief='raised')
    canvas1.pack()
    return canvas1


def setup_buttons():
    button1 = tk.Button(text='      Plot Volume      ', command=decide_to_plot_volume,
                        bg='green', fg='white', font=('helvetica', 12, 'bold'))
    button2 = tk.Button(text='      Plot RSI      ', command=decide_to_plot_rsi,
                        bg='green', fg='white', font=('helvetica', 12, 'bold'))
    button3 = tk.Button(text='      Plot Averages      ', command=decide_to_plot_averages,
                        bg='green', fg='white', font=('helvetica', 12, 'bold'))
    return button1, button2, button3


def create_windows(canvas1, button1, button2, button3):
    canvas1.create_window(2*150, 100, window=button1)
    canvas1.create_window(2*150, 200, window=button2)
    canvas1.create_window(2*150, 290, window=button3)
    return canvas1


def decide_to_plot_volume():
    global PLOT_VOLUME
    global PLOT_RSI
    PLOT_VOLUME = 1
    PLOT_RSI = 0
    print('Choosed volume')


def decide_to_plot_rsi():
    global PLOT_VOLUME
    global PLOT_RSI
    PLOT_RSI = 1
    PLOT_VOLUME = 0
    print('Choosed RSI')


def decide_to_plot_averages():
    global PLOT_AVERAGES
    PLOT_AVERAGES = 1
    print('Choosed to plot averages')


def ask_for_interval():
    print('Choice RSI interval (1m,1h,1d): ', end='')
    interval = str(input())
    return interval


if __name__ == "__main__":
    gui_plot_decide()
    if PLOT_RSI == 1:
        interval = ask_for_interval()
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
