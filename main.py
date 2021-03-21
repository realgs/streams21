import requests
import time
from datetime import datetime

BITBAY_API_URL = 'https://bitbay.net/API/Public/CURRENCY_PAIR/orderbook.json'
FETCH_INTERVAL = 5


def fetch_orderbook(currency_pair):
    response = requests.get(BITBAY_API_URL.replace('CURRENCY_PAIR', currency_pair)).json()
    return {
        'bids': [offer[0] for offer in response['bids']],
        'asks': [offer[0] for offer in response['asks']]
    }


def print_offers(currency_pairs):
    for currency_pair in currency_pairs:
        orderbook = fetch_orderbook(currency_pair)
        print(f'Currency pair: {currency_pair}')
        print('Bids:')
        print(orderbook['bids'])
        print('Asks:')
        print(orderbook['asks'])
        print()


def calculate_pair_price_diff(currency_pair):
    orderbook = fetch_orderbook(currency_pair)
    price_diff = (orderbook['asks'][0] - orderbook['bids'][0]) / orderbook['bids'][0]

    return round(price_diff * 100, 2)


def log(message):
    print(f'[{datetime.now().strftime("%m/%d/%Y, %X")}] {message}')


def main():
    currency_pairs = ['BTCUSD', 'LTCUSD', 'DASHUSD']

    # TASK 1
    print_offers(currency_pairs)

    # TASK 2
    while True:
        for currency_pair in currency_pairs:
            log(f'Currency pair: {currency_pair}, bid and ask diff: {calculate_pair_price_diff(currency_pair)}%')

            time.sleep(FETCH_INTERVAL)


if __name__ == '__main__':
    main()
