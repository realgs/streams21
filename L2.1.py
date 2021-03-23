import requests
from requests.exceptions import HTTPError
import time

def krypto_market(data):
    try:
        response = requests.get('http://bitbay.net/API/Public/' + data + 'USD/ticker.json')
        response.raise_for_status()
    except HTTPError as error_with_http:
        print(f'Błąd z adresem HTTP : {error_with_http}')


while True:
    krypto_market('BTC')
    time.sleep(10)
