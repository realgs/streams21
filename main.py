import requests
from time import time_ns
from datetime import datetime

BITBAY_LAST_TRANS_API_URL = 'https://api.bitbay.net/rest/trading/transactions/CURRENCY_PAIR?fromTime=TIMESTAMP_MILLIS&limit=10'
BITBAY_OFFERS_API_URL = 'https://api.bitbay.net/rest/trading/orderbook-limited/CURRENCY_PAIR/10'

latest_transaction_fetches_ts = {}


def print_warning(message):
    print(f'[WARNING] {message}')


def print_error(message):
    print(f'[ERROR] {message}')


def current_timestamp_millis():
    return time_ns() // 1_000_000


def fetch_avg_last_transaction(currency_pair):
    try:
        latest_fetch = 0
        if currency_pair in latest_transaction_fetches_ts:
            latest_fetch = latest_transaction_fetches_ts[currency_pair]

        response = requests.get(BITBAY_LAST_TRANS_API_URL
                                .replace('CURRENCY_PAIR', currency_pair)
                                .replace('TIMESTAMP_MILLIS', str(latest_fetch))).json()

        latest_transaction_fetches_ts[currency_pair] = current_timestamp_millis()
        transactions = response['items']

        if not transactions:
            return False

        volume, avg_price = 0, 0
        for transaction in transactions:
            tmp_volume = float(transaction['a'])
            volume += tmp_volume
            avg_price += float(transaction['r']) * tmp_volume

        avg_price /= volume

        return {
            'avg_rate': avg_price,
            'volume': volume,
            'size': len(transactions),
            'time': datetime.fromtimestamp(latest_transaction_fetches_ts[currency_pair] // 1000)
        }
    except Exception as e:
        print_error(f'Something went wrong during fetching avg latest transaction!')
        print_error(f'Message: {e}')
        return False


def fetch_best_offers(currency_pair):
    try:
        response = requests.get(BITBAY_OFFERS_API_URL.replace('CURRENCY_PAIR', currency_pair)).json()

        return {
            'sell': float(response['sell'][0]['ra']),
            'buy': float(response['buy'][0]['ra']),
            'time': datetime.now()
        }
    except Exception as e:
        print('Something went wrong during fetching best offers from orderbook.')
        print(f'Error: {e}\n')
        return False
