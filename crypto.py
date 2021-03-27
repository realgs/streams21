import requests as r
import time


def crypto(currencies, category):  # 1
    result = []
    for currency in currencies:
        URL = f'https://bitbay.net/API/Public/{currency}/{category}.json'
        request = r.get(URL).json()
        buy_price = request['ask']
        sell_price = request['bid']
        print(
            f'Currency: {currency} Sell price: {sell_price} Buy price: {buy_price}')
        result.append([currency, buy_price, sell_price])
    return result


def calculate(buy_price, sell_price):
    return round(100*(1-sell_price/buy_price), 2)


def refreshing_results(currencies, category):  # 2
    while(True):
        data = crypto(currencies, category)
        print(
            f'BTCUSD % diffrence between sell and buy price: {calculate(data[0][1],data[0][2])}')
        print(
            f'LTCUSD % diffrence between sell and buy price: {calculate(data[1][1],data[1][2])}')
        print(
            f'DASHUSD % diffrence between sell and buy price: {calculate(data[2][1],data[2][2])}')
        time.sleep(5)


currencies = ['BTCUSD', 'LTCUSD', 'DASHUSD']
category = 'ticker'
refreshing_results(currencies, category)
