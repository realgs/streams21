import requests as r
import time


def crypto(currencies, category):
    result = []
    for currency in currencies:
        URL = f'https://bitbay.net/API/Public/{currency}/{category}.json'
        request = r.get(URL).json()
        buy_price = request['ask']
        sell_price = request['bid']
        print(f'Currency: {currency} Sell price: {sell_price} Buy price: {buy_price}')
        result.append([currency,buy_price,sell_price])
    return result
    

currencies = ['BTCUSD', 'LTCUSD', 'DASHUSD']
category = 'ticker'
crypto(currencies, category)
