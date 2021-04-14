import time
import requests
from requests.exceptions import HTTPError

data_sells = []


def data():
    currency_1 = ['BTC', 'LTC', 'DASH']
    currency_2 = 'USD'
    category = 'orderbook'
    while True:
        for c in currency_1:
            data = download_data(c, currency_2, category)
            # print(data)
            if data is not None:
                pass
                diffrence = calculate(data, c)
        time.sleep(5)
    return diffrence


def download_data(currency_1, currency_2, category):
    try:
        response = requests.get(url=f'https://bitbay.net/API/Public/{currency_1}{currency_2}/{category}.json')
        data = response.json()
    except HTTPError:
        print('HTTP error:', HTTPError)
        return None
    return data


def calculate(data, currency_1):
    buy = data['bids'][0][0]
    sell = data['asks'][0][0]
    procenty = (1-(sell-buy)/sell) * 100
    diffrence = {
        'currency': currency_1,
        'buy_price': data['bids'][0][0],
        'sell_price': data['asks'][0][0],
        'procents': procenty,
    }

    data_sells.append(diffrence)
    print(diffrence)
    print('=========`======')
    return diffrence


if __name__ == "__main__":
    data()
