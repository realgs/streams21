import requests
import time


def createURL(market):
    url = f"https://api.bittrex.com/api/v1.1/public/getticker?market={market}"
    return url


def getData(url):
    response = requests.get(url)
    data = response.json()['result']
    buy = data['Bid']
    sell = data['Ask']
    return buy, sell


def calc(buy, sell):
    val = 1 - (sell - buy) / buy
    return val


def main(market):
    url = createURL(market)
    buy, sell = getData(url)
    diff = calc(buy, sell)
    print(f'{time.strftime("%H:%M:%S", time.localtime())} \n {market} {sell} \n {buy} \n {diff}')

markets = ['USD-BTC', 'EUR-YFL', 'USD-BAT']

while True:
    for market in markets:
        main(market)
    time.sleep(5)

