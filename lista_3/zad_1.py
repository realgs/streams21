import requests
from requests.exceptions import HTTPError
import time

ADRESS = {
    'BTC-PLN' : 'https://bitbay.net/API/Public/BTCPLN/orderbook.json',
    'LTC-PLN' : 'https://bitbay.net/API/Public/LTCPLN/orderbook.json',
    'ZRX-PLN' : 'https://bitbay.net/API/Public/ZRXPLN/orderbook.json',
    'BCC-PLN' : 'https://bitbay.net/API/Public/BCCPLN/orderbook.json',
    'OMG-PLN' : 'https://bitbay.net/API/Public/OMGPLN/orderbook.json'
}

def market():
    counter = 1
    while True:
        print(counter, "survey of buy - sell difference:")
        for key in ADRESS.keys():
            try:
                request = requests.get(ADRESS[key])
                if request.status_code == 200:
                    bids = request.json()['bids'][0][0]
                    asks = request.json()['asks'][0][0]
                    print(key,'->',calc(bids, asks),"%")
                else:
                    print('ERROR')
            except HTTPError:
                print('ERROR: ',HTTPError)
        counter += 1
        print('------------------')
        time.sleep(5)


def calc(bids, asks):
    return round(((1 - (asks - bids)/bids)*100),2)

market()
