import requests
import time
from requests.exceptions import HTTPError

url = {'BTCUSD': 'https://bitbay.net/API/Public/BTCUSD/orderbook.json',
       'LTCUSD': 'https://bitbay.net/API/Public/LTCUSD/orderbook.json',
       'DASHUSD': 'https://bitbay.net/API/Public/DASHUSD/orderbook.json'}


def getAlloffers():
    for u in url.keys():
        try:
            response = requests.get(url[u])
            if response.status_code == 200:
                print(70 * "_", u, 70 * "_")
                print(response.json())
                response.raise_for_status()
            else:
                print("Wystapil blad podczas pobierania.")
        except HTTPError:
            print('HTTP error:', HTTPError)


def getDifferencePercent():
    i = 1
    print(150*"-")
    while True:
        print("Roznica ceny kupna i sprzadarzy po", i, "odswiezeniu.")
        i += 1
        for u in url.keys():
            try:
                response = requests.get(url[u])
                if response.status_code == 200:
                    buy = response.json()['bids'][0][0]
                    sell = response.json()['asks'][0][0]
                    difference = round((1 - (sell - buy) / buy), 2)
                    print(u, difference, "%")
                else:
                    print("Wystapil blad podczas pobierania.")
            except HTTPError:
                print('HTTP error:', HTTPError)
        time.sleep(10)


getAlloffers()
getDifferencePercent()
