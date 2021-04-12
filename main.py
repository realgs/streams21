import requests
from datetime import datetime

BITBAY_API_URL = 'https://api.bitbay.net/rest/trading/orderbook-limited/CURRENCY_PAIR/10'


def fetch_best_offers(currency_pair):
    try:
        response = requests.get(BITBAY_API_URL.replace('CURRENCY_PAIR', currency_pair)).json()

        return {
            'sell': float(response['sell'][0]['ra']),
            'buy': float(response['buy'][0]['ra']),
            'time': datetime.now()
        }
    except Exception as e:
        print('fetch_best_offers(): Something went wrong during fetching best offers from orderbook.')
        print(f'Error: {e}\n')
        return False
