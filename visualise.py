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
import matplotlib.pylab as pylab
import statistics
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


def download_data(currency, category):
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
    result = {}
    for val in data:
        name = val[0]
        ask = val[1]
        bid = val[2]
        volume = val[3]
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
    candidate_object.classificate_candidates(names)
    for plot in plots:
        for t in plot.texts:
            t.set_visible(False)
        plot.plot(x_data, y_ask_data[names[i]],
                  linewidth=1, label='Buy price of ' + names[i], color='Red')
        plot.plot(x_data, y_bid_data[names[i]],
                  linewidth=1, label='Sell price of ' + names[i], color='Blue')
        plot.set_xticks(x_data)
        plot_averages(
            x_data, plot, y_ask_data[names[i]], y_bid_data[names[i]], names, i)
        plot.set_yticks(np.linspace(
            min(y_bid_data[names[i]]), max(y_ask_data[names[i]]), 5))
        i += 1
    candidate_object.print_candidate(names)
    plot_volume_rsi(x_data, names)


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


def plot_volume_rsi(x_data, names):
    if PLOT_RSI == 1:
        plot_rsi(x_data, names)
    if PLOT_VOLUME == 1:
        plot_volume(x_data, names)


def plot_rsi(x_data, names):

    i = 0
    for plot in plots_twinx:
        plot.set_ylabel('RSI value')
        name = names[i]
        RSI = calculate_rsi(name, interval)
        while RSI == 0:
            RSI = calculate_rsi(name, interval)
        RSI = RSI['value']
        recognize_rsi(plot, RSI)
        y_rsi_data.setdefault(name, []).append(RSI)
        plot.plot(x_data, y_rsi_data[name],
                  color='Purple', linewidth=1, label='RSI')
        plot.set_yticks(np.linspace(
            min(y_rsi_data[name]), max(y_rsi_data[name]), 5))
        i += 1


def recognize_rsi(plot, rsi):
    if rsi > 70:
        plot.set_xlabel(
            '                                                     |         Time         |                      [RSI in overbought territory]')
    elif rsi < 30:
        plot.set_xlabel(
            '                                                     |         Time         |                      [RSI in oversold territory]')
    elif rsi == 50:
        plot.set_xlabel(
            '                                                     |         Time         |                      [RSI in sign of no trend]')
    else:
        plot.set_xlabel(
            '                                                     |         Time         |                      [RSI in neutral territory]')


def plot_volume(x_data, names):

    i = 0
    for plot in plots_twinx:
        plot.set_ylabel('Volume value')
        name = names[i]
        plot.bar(x_data, y_volume_data[name],
                 color='Purple', linewidth=1, label='Volume')
        plot.set_yticks(np.linspace(0, max(y_volume_data[name]), 5))
        i += 1


def calculate_rsi(name, interval):
    data = y_bid_data[name]
    increase_tab = []
    decrease_tab = []
    if len(data) > interval:
        value = data[len(data) - 1] - \
            data[len(data) - interval]
        if value > 0:
            increase_tab.append(value)
        elif value < 0:
            decrease_tab.append(value)
        a = (sum(increase_tab) + 1) / (len(increase_tab) + 1)
        b = (sum(decrease_tab) + 1) / (len(decrease_tab) + 1)
    else:
        a = 1
        b = 1
    RSI = 100 - (100 / (1 + (a / b)))
    RSI = get_rsi(name[0:3],intervall)
    return RSI


def draw_legend_once():
    global CHECK_LEGEND
    if CHECK_LEGEND == 0:
        for plot in plots:
            if PLOT_AVERAGES == 0:
                plot.legend(loc=2, bbox_to_anchor=(0, 1.8))
            else:
                plot.legend(loc=2, bbox_to_anchor=(0, 2.15))
        for plot in plots_twinx:
            plot.legend(loc=1, bbox_to_anchor=(1, 1.5))
        CHECK_LEGEND = 1


def plot_setup():
    fig.suptitle("Cryptocurrencies in real time")
    i = 0
    for plot in plots:
        plot.set_xlabel('Time')
        plot.set_ylabel('Value in PLN')
        plot.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plt.setp(plot.xaxis.get_majorticklabels(), rotation=45)
        plot.set_title(currencies[i])
        i += 1
    for plot in plots_twinx:
        plot.set_xlabel('Time')
        plt.setp(plot.xaxis.get_majorticklabels(), rotation=45)
    fig.tight_layout(pad=1.0)


def animate_plots():
    plot_setup()
    anim = FuncAnimation(plt.gcf(), animation_frame, interval=5000)
    plt.show()


def set_plots():
    plt.style.use('fivethirtyeight')
    params = {'legend.fontsize': 'x-small',
              'axes.labelsize': 'x-small',
              'xtick.labelsize': 'x-small',
              'ytick.labelsize': 'x-small'}
    pylab.rcParams.update(params)
    plt.rcParams['legend.numpoints'] = 1
    fig, ((ax1, ax1t), (ax2, ax2t), (ax3, ax3t)
          ) = plt.subplots(nrows=3, ncols=2)
    plots = []
    fig.tight_layout(pad=1.0)
    plots.append(ax1)
    plots.append(ax2)
    plots.append(ax3)

    plots_twinx = []
    plots_twinx.append(ax1t)
    plots_twinx.append(ax2t)
    plots_twinx.append(ax3t)

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
    print('Choice RSI sample size: ', end='')
    interval = int(input())
    return interval, '1d'


def get_change(current, previous):
    if current == previous:
        return 100.0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0


class Choose_candidate(object):
    def __init__(self):
        self.plot1 = 'horizontal'
        self.plot2 = 'horizontal'
        self.plot3 = 'horizontal'
        self.plots_status = []
        self.plots_status.append(self.plot1)
        self.plots_status.append(self.plot2)
        self.plots_status.append(self.plot3)
        self.current_growth = 0
        self.potential_candidates = []
        self.x, self.s = self.ask_for_liquid_and_volitale_parameters()

    def ask_for_liquid_and_volitale_parameters(self):
        print('Volitale parameter: ', end='')
        x = float(input())
        print('Spread parameter: ', end='')
        s = float(input())
        print('Sample size for volitale and spread: ', end='')
        self.y = int(input())
        return x, s

    def classificate_candidates(self, names):
        i = 0
        for name in names:
            # self.potential_candidates.append(name)
            data = y_ask_data[name]
            if len(data) < 3:
                return None
            data = data[-3:]
            if data[0] < data[1] < data[2]:
                self.plots_status[i] = 'growth'
                self.current_growth += 1
                self.potential_candidates.append(name)
            elif data[0] > data[1] > data[2]:
                self.plots_status[i] = 'declining'
            else:
                self.plots_status[i] = 'horizontal'
            i += 1

    def get_candidates_status(self):
        print(self.plots_status)

    def print_candidate(self, names):
        self.classificate_candidates(names)
        candidates_data = []
        i = 0
        for name in names:
            data = y_volume_data[name]
            data = data[-1]
            if name in self.potential_candidates:
                candidates_data.append(data)
        if candidates_data != []:
            winner = max(candidates_data)
        else:
            winner = 0
        for name, p in zip(names, plots):
            if name in self.potential_candidates and y_volume_data[name][-1] == winner:
                p.set_xlabel(
                    '                                                     |         Time         |                      [This is candidate]')
                self.is_volatile(name, self.y, p)
            else:
                p.set_xlabel(
                    f'                                                     |         Time         |                     [This currency is {self.plots_status[i]}]                    ')
                p.set_title(name)
            i += 1
        self.potential_candidates = []

    def is_volatile(self, name, y, plot):
        x = self.x
        data = y_ask_data[name]
        data = data[-y:]
        dat1 = data[0]
        dat2 = data[-1]
        change = get_change(dat1, dat2)
        if change == 100 or change == 0:
            return -1

        name_str = name
        if change > x:
            name_str = name+'[V]'
            plot.set_title(name_str)

        self.is_liquid(name, plot, name_str)

    def is_liquid(self, name, plot, name_str):
        s = self.s
        ask_data = y_ask_data[name][-1]
        bid_data = y_bid_data[name][-1]
        change = get_change(bid_data, ask_data)
        if change < s:
            plot.set_title(name_str+'[L]')


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


if __name__ == "__main__":
    gui_plot_decide()
    if PLOT_RSI == 1:
        interval, intervall = ask_for_interval()
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

    candidate_object = Choose_candidate()
    animate_plots()
