import requests
from requests.exceptions import HTTPError
import time

def krypto_market(data):
    try:
        response = requests.get('http://bitbay.net/API/Public/' + data + 'USD/ticker.json')
        response.raise_for_status()
    except HTTPError as error_with_http:
        print(f'Błąd z adresem HTTP : {error_with_http}')
    else:
        originalData = response.content.decode()
        Cooked_Data = {}
        for elem in originalData[slice(1,-1)].split(","):
            part = elem.split(":")
            key = part[0]
            Cooked_Data[key[slice(1,-1)]] = part[1]
        value =(1-(float(Cooked_Data["ask"]) - float(Cooked_Data["bid"])) / float(Cooked_Data["bid"])*100)
        print(f'{data} : Różnica procentowa pomiędzy ceną kupna, a sprzedarzy {value}%')

while True:
    krypto_market('BTC')
    time.sleep(10)
