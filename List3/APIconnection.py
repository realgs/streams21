import requests
from requests.exceptions import HTTPError
import time


def get_data(target_currency, base_currency ):
    try:
        req = requests.get(f'https://bitbay.net/API/Public/{target_currency}{base_currency}/orderbook.json')
        if req.status_code == 200:
            data = req.json()
        else:
            print("Wystapil blad podczas pobierania -",key)
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
    time_counter = 1
    while True:
        print(time_counter, "- Różnica pomiędzy kupnem a sprzedażą.")
        for key in url.keys():
            try:
                response = requests.get(url[key])
                if response.status_code == 200:
                    bids = response.json()['bids'][0][0]
                    asks = response.json()['asks'][0][0]
                    difference = calc_diff(bids, asks)
                    print(key, difference, "%")
                else:
                    print("Wystapil blad podczas pobierania.")
            except HTTPError:
                print('HTTP error:', HTTPError)
        time_counter += 1
        time.sleep(10)


# URL = {'BTCUSD': 'https://bitbay.net/API/Public/BTCUSD/orderbook.json',
#        'DASHUSD': 'https://bitbay.net/API/Public/DASHUSD/orderbook.json',
#        'LTCUSD': 'https://bitbay.net/API/Public/LTCUSD/orderbook.json',\
#        }
CURR = ['BTC','DASH','LTC']
BASE = 'USD'
requestoffers()
# markettracking()