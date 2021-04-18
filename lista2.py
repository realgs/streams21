import requests
import time
from requests.exceptions import HTTPError

url_1 = 'https://bitbay.net/API/Public/'
url_2 = '/orderbook.json'
base = 'USD'
currencies = ['BTC', 'LTC', 'DASH']
frequency = 5

def data(currency):
    try:
        response = requests.get(url_1 + currency + base + url_2)
        response.raise_for_status()
        return response.json()
    except HTTPError:
        print('HTTP error:', HTTPError)
    except Exception:
        print('Other error:', Exception)

def offers():
    for currency in currencies:
        response = data(currency)
        print(currency, response)

    while True:
        for currency in currencies:
            response = data(currency)
            buy = response['bids'][0][0]
            sell = response['asks'][0][0]
            difference = 1 - (sell - buy) / sell
            print(currency, difference)
        time.sleep(frequency)


offers()
