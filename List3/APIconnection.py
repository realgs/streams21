import requests
from requests.exceptions import HTTPError
import time

def requestoffers():
    for key in url.keys():
        try:
            req = requests.get(url[key])
            if req.status_code == 200:
                print(key)
                print(req.json(),'\n')
            else:
                print("Wystapil blad podczas pobierania -",key)
        except HTTPError:
            print('Error:', HTTPError)


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


url = {'BTCUSD': 'https://bitbay.net/API/Public/BTCUSD/orderbook.json',
       'DASHUSD': 'https://bitbay.net/API/Public/DASHUSD/orderbook.json',
       'LTCUSD': 'https://bitbay.net/API/Public/LTCUSD/orderbook.json',\
       }
# requestoffers()
markettracking()