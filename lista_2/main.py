import requests
import requests.exceptions
import time

ADRESS = {
    'btcpln' : 'https://bitbay.net/API/Public/BTCPLN/orderbook.json',
    'ltcusd' : 'https://bitbay.net/API/Public/LTCPLN/orderbook.json',
    'dashusd': 'https://bitbay.net/API/Public/DASHPLN/orderbook.json'
}

def market():
