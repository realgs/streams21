import requests
import time

BITBAY_API_URL = 'https://bitbay.net/API/Public/CURRENCY_PAIR/orderbook.json'


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


def main():
    currency_pairs = ['BTCUSD', 'LTCUSD', 'DASHUSD']
    print_offers(currency_pairs)


if __name__ == '__main__':
    main()
