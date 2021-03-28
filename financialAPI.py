import time
import requests
from requests.exceptions import HTTPError


def data():
    currency_1 = ['BTC', 'LTC', 'DASH']
    currency_2 = 'USD'
    category = 'trades'
    while True:
        for i in currency_1:
            data = download_data(i, currency_2, category)
            print(data)
            calculate(data, i)
        time.sleep(5)
    return 'done'


def download_data(currency_1, currency_2, category):
    try:
        response = requests.get(url=f'https://bitbay.net/API/Public/{currency_1}{currency_2}/{category}.json')
        data = response.json()
    except HTTPError:
        print('HTTP error:', HTTPError)
    return(data)


def calculate(data, currency_1):
    sell_price = []
    buy_price = []
    for i in range(len(data)):
        if data[i]["type"] == "buy":
            buy_price.append(data[i]["price"])

        elif data[i]["type"] == "sell":
            sell_price.append(data[i]["price"])

        if (len(buy_price) != 0) and (len(sell_price) != 0):
            diffrence = 1 - ((buy_price[-1] - sell_price[-1]) / buy_price[-1])
            print({
                'valute': currency_1,
                'buy_price': buy_price[-1],
                'sell_price': sell_price[-1],
                'procent': diffrence})
    return 'thx'


if __name__ == "__main__":
    data()
