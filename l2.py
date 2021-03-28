import requests as r
import time

def currencies(url):
    for key in url.keys():
        resp = r.get(url[key])
        print(f'{key}')
        print(resp.json())

def percentage_results(url):
    i=1
    while True:
        print('---------------------------------- ' + str(i) + ' ----------------------------------')
        i += 1
        for key in url.keys():
            resp = r.get(url[key])
            result = 100 * (1 - (resp.json()['asks'][0][0] - resp.json()['bids'][0][0]) / resp.json()['bids'][0][0])
            print(f'{key}:', round(result, 4))
        time.sleep(5)

urls = {'BTCUSD': 'https://bitbay.net/API/Public/BTCUSD/orderbook.json',
        'LTCUSD': 'https://bitbay.net/API/Public/LTCUSD/orderbook.json',
        'DASHUSD': 'https://bitbay.net/API/Public/DASHUSD/orderbook.json'}

currencies(urls)
percentage_results(urls)
