import requests
import time
import sys


def fetchBitbayAPI(category, resource):
    URL = f'https://bitbay.net/API/Public/{resource}/{category}.json'
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()


def printOffers(orders, resource):
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


def monitorOffers(resource):
    while 1:
        orders = fetchBitbayAPI(category='orderbook', resource='BTCUSD')
        bid_rate = orders['bids'][0][0]
        ask_rate = orders['asks'][0][0]
        diff = (ask_rate-bid_rate) / bid_rate
        if diff < 0:
            print('-', abs(diff))
        else:
            print('+', abs(diff))

        time.sleep(FREQUENCY)


if __name__ == '__main__':

    RESOURCES = ['BTCUSD', 'LTCUSD', 'DASHUSD']
    FREQUENCY = 5

    arg = sys.argv[1]
    if arg == '1':
        for R in RESOURCES:
            orders = fetchBitbayAPI(category='orderbook', resource=R)
            printOffers(orders, R)
    elif arg == '2':
        monitorOffers(resource='BTCUSD')
