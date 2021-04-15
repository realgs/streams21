import requests
from requests.exceptions import HTTPError
import time
from datetime import datetime


URL_START='http://bitbay.net/API/Public/'
URL_END='USD/ticker.json'
INTERVAL=5

def crypto_get(data):
    try:
        response = requests.get( URL_START + data + URL_END)
        response.raise_for_status()

    except HTTPError as error_with_http:
        print(f'Błąd z adresem HTTP : {error_with_http}')

    else:
        originalData = response.json()
        return originalData["bid"], originalData["ask"]

def animate(i):
    bid_LSK, ask_LSK = crypto_get(f'LSK', 'USD', 'ticker.json')
    bid_BAT, ask_BAT = crypto_get(f'BAT', 'USD', 'ticker.json')
    bid_ZRX, ask_ZRX = crypto_get(f'ZRX', 'USD', 'ticker.json')

    x_axis.append(datetime.now().strftime("%H:%M:%S"))

    crypto_bid_LSK.append(ask_LSK)
    crypto_ask_LSK.append(bid_LSK)
    crypto_bid_BAT.append(ask_BAT)
    crypto_ask_BAT.append(bid_BAT)
    crypto_bid_ZRX.append(ask_ZRX)
    crypto_ask_ZRX.append(bid_ZRX)

while True:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Lokalny czas =", dt_string)
    crypto_get('BTC')
    crypto_get('DASH')
    crypto_get('LTC')
    print('____________________________________________')
    time.sleep(INTERVAL)
