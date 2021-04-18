import requests
from requests.exceptions import HTTPError
import time


def get_data(currency_pair, method):
    try:
        req = requests.get(f'https://bitbay.net/API/Public/{currency_pair}/{method}.json')
        if req.status_code == 200:
            data = req.json()
        else:
            print("Wystapil blad podczas pobierania -",currency_pair)
    except HTTPError:
        print('Error:', HTTPError)
        return None
    return data

def create_pairs(BASE, CURR):
    pairs = []
    for i in BASE:
        for j in CURR:
            pairs.append[i+j]
    return pairs

def draw_graphs(currency_pairs):
    pass

def update():
    pass

def main():
    CURR = ['BTC','DASH','LTC']
    BASE = ['USD']
    requestoffers(create_pairs(BASE, CURR))


if __name__ == '__main__':
    main()
