import requests
import time
import datetime
import sys

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


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

    date = []
    bids1, asks1 = [], []
    bids2, asks2 = [], []
    bids3, asks3 = [], []

    fig = plt.figure()
    fig.suptitle('Cryptocurriencies live tracking')

    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)

    axes = [ax1, ax2, ax3]

    line1, = ax1.plot_date(date, bids1, '.-', label='bids')
    line2, = ax1.plot_date(date, asks1, '.-', label='asks')
    line3, = ax2.plot_date(date, bids2, '.-', label='bids')
    line4, = ax2.plot_date(date, asks2, '.-', label='asks')
    line5, = ax3.plot_date(date, bids3, '.-', label='bids')
    line6, = ax3.plot_date(date, asks3, '.-', label='asks')

    def _update(frame):
        orders1 = get_bitbay_data('orderbook',
                                  CRYPTO_CURRENCIES[0]+MAIN_CURRENCY)
        orders2 = get_bitbay_data('orderbook',
                                  CRYPTO_CURRENCIES[1]+MAIN_CURRENCY)
        orders3 = get_bitbay_data('orderbook',
                                  CRYPTO_CURRENCIES[2]+MAIN_CURRENCY)

        date.append(datetime.datetime.now())

        bids1.append(orders1['bids'][0][0])
        asks1.append(orders1['asks'][0][0])
        bids2.append(orders2['bids'][0][0])
        asks2.append(orders2['asks'][0][0])
        bids3.append(orders3['bids'][0][0])
        asks3.append(orders3['asks'][0][0])

        line1.set_data(date, bids1)
        line2.set_data(date, asks1)
        line3.set_data(date, bids2)
        line4.set_data(date, asks2)
        line5.set_data(date, bids3)
        line6.set_data(date, asks3)

        for ax, crypto_currency in zip(axes, CRYPTO_CURRENCIES):
            ax.set(xlabel='Date', ylabel=f'Rate [{MAIN_CURRENCY}]',
                   title=crypto_currency+MAIN_CURRENCY)
            ax.relim()
            ax.autoscale_view()
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        plt.tight_layout()

        return line1, line2, line3, line4, line5, line6,

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
    INTERVAL = 1

    arg = sys.argv[1]
    if arg == '1':
        for currency in CRYPTO_CURRENCIES:
            resource = currency + MAIN_CURRENCY
            orders = get_bitbay_data('orderbook', resource)
            print_offers(orders, resource)
    elif arg == '2':
        monitor_offers(resource=CRYPTO_CURRENCIES[0]+MAIN_CURRENCY,
                       interval=INTERVAL, mode='CLI')
    elif arg == '3':
        monitor_offers(resource=CRYPTO_CURRENCIES[0]+MAIN_CURRENCY,
                       interval=INTERVAL, mode='plot')
