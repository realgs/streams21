import requests
import time
import sys


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


def monitor_offers(resource, freq):
    while 1:
        orders = get_bitbay_data(category='orderbook', resource='BTCUSD')
        bid_rate = orders['bids'][0][0]
        ask_rate = orders['asks'][0][0]
        diff = (ask_rate-bid_rate) / bid_rate
        if diff < 0:
            print('-', abs(diff))
        else:
            print('+', abs(diff))

        time.sleep(freq)


if __name__ == '__main__':
    MAIN_CURRENCY = 'USD'
    CRYPTO_CURRENCY = ['BTC', 'LTC', 'DASH']
    FREQUENCY = 5

    arg = sys.argv[1]
    if arg == '1':
        for currency in CRYPTO_CURRENCY:
            resource = currency + MAIN_CURRENCY
            orders = get_bitbay_data('orderbook', resource)
            print_offers(orders, resource)
    elif arg == '2':
        monitor_offers(resource='BTCUSD', freq=FREQUENCY)
