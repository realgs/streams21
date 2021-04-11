import requests
import time
import matplotlib.pyplot as plt
from matplotlib import gridspec

hist = []


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
    val = (1 - (sell - buy) / buy)*100
    return val


def addData(market):
    url = createURL(market)
    buy, sell = getData(url)
    diff = calc(buy, sell)
    xlab = time.strftime("%H:%M:%S", time.localtime())
    hist.append([market, buy, sell, xlab])
    # print(f'{time.strftime("%H:%M:%S", time.localtime())} \n {market} {sell} \n {buy} \n {diff}')


def prepareData(market):
    buyL = []
    sellL = []
    timeL = []
    for i in range(0, len(hist)):
        if hist[i][0] == market:
            buyL.append(hist[i][1])
            sellL.append(hist[i][2])
            timeL.append(hist[i][3])
    return buyL, sellL, timeL


def drawPlot(market):
    buyL, sellL, timeL = prepareData(market)
    plt.title(f'Wykres notowań kursu {market}')
    plt.plot(timeL, sellL, label='Sell', color='green')
    plt.plot(timeL, buyL, label='Buy', color='red')
    plt.ylabel(f'Wartość {market[:3]}')
    plt.xlabel('Czas [s]', loc='right')
    plt.xticks(rotation=45)



def showPlots(markets):
    fig = plt.figure(figsize=(14, 10))
    plt.subplot(3, 1, 1)
    drawPlot(markets[0])
    fig.legend(framealpha=1, frameon=True, prop={'size': 15})
    plt.subplot(3, 1, 2)
    drawPlot(markets[1])
    plt.subplot(3, 1, 3)
    drawPlot(markets[2])
    fig.tight_layout()
    plt.show(block=False)
    plt.pause(5)
    plt.close()


def run(markets):
    while True:
        for market in markets:
            addData(market)
        showPlots(markets)


markets = ['EUR-USD', 'USD-BTC', 'USD-BAT']

if __name__ == '__main__':
    run(markets)
