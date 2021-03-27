import requests
import pprint
import time

urls = {'BTCUSD': 'https://bitbay.net/API/Public/BTCUSD/orderbook.json',
        'LTCUSD': 'https://bitbay.net/API/Public/LTCUSD/orderbook.json',
        'DASHUSD': 'https://bitbay.net/API/Public/DASHUSD/orderbook.json'}


def orderbook(url):
    for key in url.keys():
        try:
            r = requests.get(url[key])
            r.raise_for_status()
            print(f'{key} -----------------------------------')
            # pprint.pprint(r.json())
            print(r.json())

        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)


def data_stream(url):
    while True:
        for key in url.keys():
            try:
                r = requests.get(url[key])
                r.raise_for_status()
                result = 1 - (r.json()['asks'][0][0] - r.json()['bids'][0][0]) / r.json()['bids'][0][0]
                print(f'{key}: ', round(result, 4))

            except requests.exceptions.HTTPError as err:
                raise SystemExit(err)

        print('\n')
        time.sleep(5)


orderbook(urls)
data_stream(urls)
