import requests
from requests.exceptions import HTTPError
import time
from datetime import datetime

def krypto_market(data):
    try:
        response = requests.get('http://bitbay.net/API/Public/' + data + 'USD/ticker.json')
        response.raise_for_status()

    except HTTPError as error_with_http:
        print(f'Błąd z adresem HTTP : {error_with_http}')

    # else:
    #     originalData = response.content.decode()
    #     Cooked_Data = {}
    #     for elem in originalData[slice(1,-1)].split(","):
    #         part = elem.split(":")
    #         key = part[0]
    #         Cooked_Data[key[slice(1,-1)]] = part[1]
    #     value =(1-(float(Cooked_Data["ask"]) - float(Cooked_Data["bid"])) / float(Cooked_Data["bid"])*100)
    #     # print(f'Request status: {response.status_code}')
    #     print(f'{data} : Różnica procentowa pomiędzy ceną kupna, a sprzedarzy {value}%')
    #     return value
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

    time.sleep(10)
