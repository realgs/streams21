import requests
import sys
from time import sleep
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animation


CURRIENCES = ['ZEC', 'ETH', 'XRP']
SLEEP_TIME = 5
URL_BEG = 'https://bitbay.net/API/Public/'
URL_END = '/ticker.json'


def getPath(currency, category):
    return f'{URL_BEG}{currency}/{category}{URL_END}'

def getOffers(currency, category):
    try:
        response = requests.get(getPath(currency,category))
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as exception:
        print(exception)
        sys.exit()

def getData(currency):
    data = getOffers(currency, 'ticker')
    buy = data["bid"]
    sell = data["ask"]
    return buy, sell

def plotData(time_data, prices):
    for cur in CURRIENCES:
        buy, sell = getData(cur)
        prices[cur]['buy'].append(buy)
        prices[cur]['sell'].append(sell)

    time_data.append(datetime.now().strftime("%H:%M:%S"))

    return time_data, prices

def plotLoop(i):
    time_data_p, prices_p = plotData(time_data, prices)
    time_data_p = time_data_p[-5:]
    plt.cla()
    for cur in CURRIENCES:
        plt.plot(time_data_p, prices[cur]['buy'][-5:], label=f'{cur} buy')
        plt.plot(time_data_p, prices[cur]['sell'][-5:], label=f'{cur} sell')

    plt.xticks(time_data_p, rotation=35)

    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()

def dataFrame(CURRIENCES=CURRIENCES, prices = {}):
    for cur in CURRIENCES:
        buy, sell = getData(cur)
        prices[cur] = {'buy': [], 'sell': []}
    return prices    
    

if __name__ == '__main__':
    time_data = []
    prices = dataFrame()
    T_animation=animation(plt.figure(),plotLoop,interval=1000*SLEEP_TIME)
    plt.show()

