import requests
import time


def createURLS(market1, market2, market3):
    url1 = f"https://api.bittrex.com/api/v1.1/public/getticker?market={market1}"
    url2 = f"https://api.bittrex.com/api/v1.1/public/getticker?market={market2}"
    url3 = f"https://api.bittrex.com/api/v1.1/public/getticker?market={market3}"
    urls = [url1, url2, url3]
    return urls


def printMarket(market1, market2, market3):
    urls = createURLS(market1, market2, market3)
    while True:
        offers = []
        for url in urls:
            response = requests.get(url)
            data = response.json()['result']
            bid = data['Bid']
            ask = data['Ask']
            offers.append([bid, ask])
        allCalc = []
        for i in range(0, 3):
            calc = 1 - ((offers[i][0]-offers[i][1])/offers[i][1])
            allCalc.append(calc)
        print(f'{time.strftime("%H:%M:%S", time.localtime())} \n {market1} {allCalc[0]} \n {market2} {allCalc[1]} \n {market3} {allCalc[2]}')
        time.sleep(5)


printMarket('USD-BTC', 'EUR-YFL', 'USD-BAT')
