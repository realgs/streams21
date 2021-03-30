import requests
import time


def printMarket(market1, market2, market3):
    url1 = f"https://api.bittrex.com/api/v1.1/public/getticker?market={market1}"
    url2 = f"https://api.bittrex.com/api/v1.1/public/getticker?market={market2}"
    url3 = f"https://api.bittrex.com/api/v1.1/public/getticker?market={market3}"
    urls = [url1, url2, url3]

    offers = []
    for url in urls:
        response = requests.get(url)
        data = response.json()['result']
        offers.append(data)
    print(f'{time.strftime("%H:%M:%S", time.localtime())} \n {market1} {offers[0]} \n {market2} {offers[1]} \n {market3} {offers[2]}')


printMarket('USD-BTC', 'EUR-YFL', 'USD-BAT')
