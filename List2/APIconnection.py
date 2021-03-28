import requests
from requests.exceptions import HTTPError


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


url = {'BTCUSD': 'https://bitbay.net/API/Public/BTCUSD/orderbook.json',
       'LTCUSD': 'https://bitbay.net/API/Public/LTCUSD/orderbook.json',
       'DASHUSD': 'https://bitbay.net/API/Public/DASHUSD/orderbook.json'}
requestoffers()
