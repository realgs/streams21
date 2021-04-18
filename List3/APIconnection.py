import requests
from requests.exceptions import HTTPError
import time


def get_data(target_currency, base_currency, method):
    try:
        req = requests.get(f'https://bitbay.net/API/Public/{target_currency}{base_currency}/{method}.json')
        if req.status_code == 200:
            data = req.json()
        else:
            print("Wystapil blad podczas pobierania -",target_currency + base_currency)
    except HTTPError:
        print('Error:', HTTPError)
        return None
    return data


def main():
    CURR = ['BTC','DASH','LTC']
    BASE = ['USD']
    requestoffers(CURR, BASE)


if __name__ == '__main__':
    main()
