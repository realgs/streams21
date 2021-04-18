import requests
import time
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


def monitor_offers(resource, interval, mode):
    def _update_plot(_):
        # :(
        global MAIN_CURRENCY, CRYPTO_CURRENCY

        btc_orders = get_bitbay_data('orderbook',
                                     CRYPTO_CURRENCY[0]+MAIN_CURRENCY)
        ltc_orders = get_bitbay_data('orderbook',
                                     CRYPTO_CURRENCY[1]+MAIN_CURRENCY)
        dash_orders = get_bitbay_data('orderbook',
                                      CRYPTO_CURRENCY[2]+MAIN_CURRENCY)

        btc_bid_rate = btc_orders['bids'][0][0]
        btc_ask_rate = btc_orders['asks'][0][0]
        ltc_bid_rate = ltc_orders['bids'][0][0]
        ltc_ask_rate = ltc_orders['asks'][0][0]
        dash_bid_rate = dash_orders['bids'][0][0]
        dash_ask_rate = dash_orders['asks'][0][0]

        btc_bids.append(btc_bid_rate)
        btc_asks.append(btc_ask_rate)
        ltc_bids.append(ltc_bid_rate)
        ltc_asks.append(ltc_ask_rate)
        dash_bids.append(dash_bid_rate)
        dash_asks.append(dash_ask_rate)
        t2 = time.time()
        T.append(int(t2 - t1))

        plt.cla()
        plt.plot(T, btc_bids, '.-',
                 label=CRYPTO_CURRENCY[0]+MAIN_CURRENCY+' bids')
        plt.plot(T, btc_asks, '.-',
                 label=CRYPTO_CURRENCY[0]+MAIN_CURRENCY+' asks')
        plt.plot(T, ltc_bids, '.-',
                 label=CRYPTO_CURRENCY[1]+MAIN_CURRENCY+' bids')
        plt.plot(T, ltc_asks, '.-',
                 label=CRYPTO_CURRENCY[1]+MAIN_CURRENCY+' asks')
        plt.plot(T, dash_bids, '.-',
                 label=CRYPTO_CURRENCY[2]+MAIN_CURRENCY+' bids')
        plt.plot(T, dash_asks, '.-',
                 label=CRYPTO_CURRENCY[2]+MAIN_CURRENCY+' asks')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()

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
        btc_bids = []
        btc_asks = []
        ltc_bids = []
        ltc_asks = []
        dash_bids = []
        dash_asks = []
        T = []
        t1 = time.time()

        _ = FuncAnimation(plt.gcf(), _update_plot, interval=interval*1000) \
            # noqa: F841
        plt.show()


if __name__ == '__main__':
    MAIN_CURRENCY = 'PLN'
    CRYPTO_CURRENCY = ['BTC', 'LTC', 'DASH']
    INTERVAL = 1

    arg = sys.argv[1]
    if arg == '1':
        for currency in CRYPTO_CURRENCY:
            resource = currency + MAIN_CURRENCY
            orders = get_bitbay_data('orderbook', resource)
            print_offers(orders, resource)
    elif arg == '2':
        monitor_offers(resource=CRYPTO_CURRENCY[0]+MAIN_CURRENCY,
                       interval=INTERVAL, mode='CLI')
    elif arg == '3':
        monitor_offers(resource=CRYPTO_CURRENCY[0]+MAIN_CURRENCY,
                       interval=INTERVAL, mode='plot')
