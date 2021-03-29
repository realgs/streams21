import requests
from requests.exceptions import HTTPError
import time
from datetime import datetime

url_start='http://bitbay.net/API/Public/'
url_end='USD/ticker.json'
interval=10
def krypto_market(data):
    try:
        response = requests.get( url_start + data + url_end)
        response.raise_for_status()

    except HTTPError as error_with_http:
        print(f'Błąd z adresem HTTP : {error_with_http}')

    else:
        originalData = response.json()
        value = (100 - (1 - (float(originalData["ask"]) - float(originalData["bid"])) / float(originalData["bid"])) * 100 )
        print(f'{data} - Różnica procentowa pomiędzy kupnem a sprzedażą: {value}%')
        return value



while True:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Lokalny czas =", dt_string)

    krypto_market('BTC')
    krypto_market('DASH')
    krypto_market('LTC')
    print('____________________________________________')

    time.sleep(interval)
