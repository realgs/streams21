import requests
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

database = []

def createURL(market):
    url = f"https://api.bittrex.com/api/v1.1/public/getticker?market={market}"
    return url


def getData(url):
    resp = getResponse(url)
    data = resp['result']
    buy = data['Bid']
    sell = data['Ask']
    return buy, sell


def getResponse(url):
    global response
    try:
        response = requests.get(url)
    except Exception as e:
        print(e)

    if response.status_code == 200:
        respJson = response.json()
        return respJson


def calc(buy, sell):
    val = (1 - (sell - buy) / buy) * 100
    return val


def addData(market):
    url = createURL(market)
    buy, sell = getData(url)
    xTime = time.strftime("%H:%M:%S", time.localtime())
    database.append([market, buy, sell, xTime])


def prepareData(market):
    buyL = []
    sellL = []
    timeL = []
    for i in range(0, len(database)):
        if database[i][0] == market:
            buyL.append(database[i][1])
            sellL.append(database[i][2])
            timeL.append(database[i][3])
    return buyL, sellL, timeL
import requests
import time
import matplotlib.pyplot as plt


def createURL(market):
    url = f"https://api.bittrex.com/api/v1.1/public/getticker?market={market}"
    return url


def getData(url):
    resp = getResponse(url)
    data = resp['result']
    buy = data['Bid']
    sell = data['Ask']
    return buy, sell

    # try:
    #     response = requests.get(url)
    #     data = response.json()['result']
    #     buy = data['Bid']
    #     sell = data['Ask']
    #     return buy, sell
    # except Exception as e:
    #     print(e)


def getResponse(url):
    global response
    try:
        response = requests.get(url)
    except Exception as e:
        print(e)

    if response.status_code == 200:
        respJson = response.json()
        return respJson


def calc(buy, sell):
    val = (1 - (sell - buy) / buy) * 100
    return val


def addData(market):
    url = createURL(market)
    buy, sell = getData(url)
    xTime = time.strftime("%H:%M:%S", time.localtime())
    database.append([market, buy, sell, xTime])


def prepareData(market):
    buyL = []
    sellL = []
    timeL = []
    for i in range(0, len(database)):
        if database[i][0] == market:
            buyL.append(database[i][1])
            sellL.append(database[i][2])
            timeL.append(database[i][3])
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
    fig = plt.figure(figsize=(12, 8))

    for i in range(0, len(markets)):
        plt.subplot(3, 1, i + 1)
        drawPlot(markets[i])

    fig.legend(['Sell', 'Buy'], frameon=True, prop={'size': 15})
    fig.tight_layout()
    animate = animation.FuncAnimation(fig, addData, frames=markets, interval=5000)
    plt.show()


def run(markets):
    global database
    hist = []
    while True:
        for market in markets:
            addData(market)
        showPlots(markets)


markets = ['EUR-USD', 'USD-BTC', 'USD-BAT']

if __name__ == '__main__':
    run(markets)
