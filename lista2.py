import requests
from requests.exceptions import HTTPError
import time

frequency = 5

def dataPicker(resource):
    try:
        adres = 'https://bitbay.net/API/Public/' + resource + 'USD/ticker.json'
        response = requests.get(adres)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        data = response.json()
        score = round((1 - (data["ask"] - data["bid"]) / data["bid"]) * 100,6)
        print(f'{resource} - Różnica pomiędzy kupnem a sprzedażą: {score}%')
        return score

while True:
    dataPicker('BTC')
    dataPicker('LTC')
    dataPicker('DASH')
    print('---------------------------------------------------------')
    time.sleep(frequency)










