import requests
from requests.exceptions import HTTPError
import time


def get_data(target_currency, base_currency ):
    try:
        req = requests.get(f'https://bitbay.net/API/Public/{target_currency}{base_currency}/orderbook.json')
        if req.status_code == 200:
            data = req.json()
        else:
            print("Wystapil blad podczas pobierania -",target_currency)
    except HTTPError:
        print('Error:', HTTPError)
        return None
    return data


def requestoffers():
    for currency in CURR:
        print(currency + BASE)
        print(get_data(currency, BASE) , '\n')


def calc_diff(bids, asks):
    return round((1 - (asks - bids) / bids), 4)


def markettracking():
    while True:
        print(time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()), "- Różnica pomiędzy kupnem a sprzedażą.")
        for currency in CURR:
            data = get_data(currency, BASE)
            bids = data['bids'][0][0]
            asks = data['asks'][0][0]
            difference = calc_diff(bids, asks)
            print(currency, difference, "%")
        time.sleep(10)


# URL = {'BTCUSD': 'https://bitbay.net/API/Public/BTCUSD/orderbook.json',
#        'DASHUSD': 'https://bitbay.net/API/Public/DASHUSD/orderbook.json',
#        'LTCUSD': 'https://bitbay.net/API/Public/LTCUSD/orderbook.json',\
#        }
CURR = ['BTC','DASH','LTC']
BASE = 'USD'
# requestoffers()
markettracking()