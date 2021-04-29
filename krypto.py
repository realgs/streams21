import requests
import time
import sys
import itertools

from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import ConciseDateFormatter, AutoDateLocator


def get_bitbay_data(category, resource):
    URL = f'https://bitbay.net/API/Public/{resource}/{category}.json'
    try:
        response = requests.get(URL)
        return response.json()
    except Exception as e:
        print(e)


def print_offers(orders, resource):
    try:
        buy = orders['bids']
        sell = orders['asks']

        print(f'{resource}:')
        print('    buy:')
        for b in buy:
            print(f'\t{b}')
        print('    sell:')
        for s in sell:
            print(f'\t{s}')
    except Exception as e:
        print(e)


def dynamic_plotting(interval):
    global MAIN_CURRENCY, CRYPTO_CURRENCIES

    counter = itertools.count()
    N = len(CRYPTO_CURRENCIES)

    date = []
    bids = [[] for _ in range(N)]
    asks = [[] for _ in range(N)]
    avg_bids = [[] for _ in range(N)]
    avg_asks = [[] for _ in range(N)]
    volumes = [[0] for _ in range(N)]

    fig = plt.figure(figsize=(9, 8), num='Please hire me')
    fig.suptitle('Cryptocurriencies live tracking')

    axes = []
    for i in range(N):
        axes.append(fig.add_subplot(N, 1, i+1))

    lines = []
    for i, ax in enumerate(axes):
        bids_line, = ax.plot_date(date, bids[i], '-', label='bids')
        asks_line, = ax.plot_date(date, asks[i], '-', label='asks')
        avg_bid_line, = ax.plot_date(date, avg_bids[i], '--',
                                     label="bids' avg")
        avg_ask_line, = ax.plot_date(date, avg_asks[i], '--',
                                     label="asks' avg")
        lines.append((bids_line, asks_line, avg_bid_line, avg_ask_line))

    volume_textes = []
    for i in range(N):
        volume_txt = axes[i].text(1.01, 0, '', transform=axes[i].transAxes)
        volume_textes.append(volume_txt)

    def _update(frame):
        orders = []
        for i in range(N):
            orders.append(get_bitbay_data('orderbook',
                                          CRYPTO_CURRENCIES[i]+MAIN_CURRENCY))

        for i in range(N):
            volumes[i][0] += orders[i]['bids'][0][1]
            new_text = f'Trading volume: {round(volumes[i][0], 4)}'
            volume_textes[i].set_text(new_text)

        # date.append(datetime.now())
        date.append(datetime.now() + timedelta(days=next(counter)))

        for i in range(N):
            bids[i].append(orders[i]['bids'][0][0])
            asks[i].append(orders[i]['asks'][0][0])
            avg_bids[i].append(sum(bids[i])/len(bids[i]))
            avg_asks[i].append(sum(asks[i])/len(asks[i]))

        for i, line in enumerate(lines):
            line[0].set_data(date, bids[i])
            line[1].set_data(date, asks[i])
            line[2].set_data(date, avg_bids[i])
            line[3].set_data(date, avg_asks[i])

        for ax, crypto_currency in zip(axes, CRYPTO_CURRENCIES):
            xlocator = AutoDateLocator()
            ylocator = plt.LinearLocator(numticks=3)
            formatter = ConciseDateFormatter(xlocator)

            ax.set(ylabel=f'Rate [{MAIN_CURRENCY}]',
                   title=crypto_currency)
            ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
            ax.yaxis.set_major_locator(ylocator)
            ax.xaxis.set_major_locator(xlocator)
            ax.xaxis.set_major_formatter(formatter)
            ax.relim()
            ax.autoscale_view()

        plt.tight_layout()

        return lines,

    _ = FuncAnimation(fig, _update, interval=interval)
    plt.show()


def monitor_offers(resource, interval, mode):
    if mode == 'CLI':
        while 1:
            orders = get_bitbay_data(category='orderbook', resource=resource)
            bid_rate = orders['bids'][0][0]
            ask_rate = orders['asks'][0][0]
            diff = (ask_rate-bid_rate) / bid_rate
            if diff < 0:
                print('-', abs(diff))
            else:
                print('+', abs(diff))

            time.sleep(interval)
    elif mode == 'plot':
        dynamic_plotting(interval*1000)


if __name__ == '__main__':
    MAIN_CURRENCY = 'PLN'
    CRYPTO_CURRENCIES = ['BTC', 'LTC', 'DASH']
    INTERVAL_SEC = 1

    arg = sys.argv[1]
    if arg == '1':
        for currency in CRYPTO_CURRENCIES:
            resource = currency + MAIN_CURRENCY
            orders = get_bitbay_data('orderbook', resource)
            print_offers(orders, resource)
    elif arg == '2':
        monitor_offers(resource=CRYPTO_CURRENCIES[0]+MAIN_CURRENCY,
                       interval=INTERVAL_SEC, mode='CLI')
    elif arg == '3':
        monitor_offers(resource=CRYPTO_CURRENCIES[0]+MAIN_CURRENCY,
                       interval=INTERVAL_SEC, mode='plot')
