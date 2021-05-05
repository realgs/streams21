import requests
import sys
from time import sleep
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animation
from statistics import mean
from matplotlib.widgets import TextBox

CURRIENCES = ['LTCPLN', 'ETHPLN', 'XRPPLN']
SLEEP_TIME = 5
URL_BEG = 'https://bitbay.net/API/Public/'
URL_END = '/ticker.json'
MEAN_PEROID = 5
RSI_PEROID = 10

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
    buy = float(data["bid"])
    sell = float(data["ask"])
    volume = float(data["volume"])
    return buy, sell, volume

def plotData(time_data, prices):
    for cur in CURRIENCES:
        buy, sell, volume = getData(cur)
        prices[cur]['buy'].append(buy)
        prices[cur]['sell'].append(sell)
        prices[cur]['volume'] = volume

        if len(prices[cur]['sell']) > 1:
            dif = float(sell) - float(prices[cur]['sell'][-2])
            if dif > 0:
                prices[cur]['growth_val'].append(dif)
            elif dif < 0:
                prices[cur]['dec_val'].append(dif*(-1))

        try:
            rsi = 100 - (100 / (1 + (mean(prices[cur]['growth_val'][-RSI_PEROID::])/mean(prices[cur]['dec_val'][-RSI_PEROID::]))))
        except:
            rsi = 0
        prices[cur]['rsi'] = rsi
        avg_buy = mean(prices[cur]['buy'][-MEAN_PEROID::])
        prices[cur]['buy_mean'] = avg_buy
        avg_sell = mean(prices[cur]['sell'][-MEAN_PEROID::])
        prices[cur]['sell_mean'] = avg_sell
    print(prices)
    time_data.append(datetime.now().strftime("%H:%M:%S"))

    return time_data, prices

def plotLoop(i):
    time_data_p, prices_p = plotData(time_data, prices)
    time_data_p = time_data_p[-5:]
    plt.style.use('ggplot')
    plt.subplots_adjust(hspace=0.3)
    for i,cur in enumerate(CURRIENCES):
        p = 311 + i
        plt.subplot(p).cla()
        plt.subplot(p)
        plt.title(cur)
        plt.plot(time_data_p, prices[cur]['buy'][-5:], label=f'Buy')
        plt.plot(time_data_p, prices[cur]['sell'][-5:], label=f'Sell')
        plt.axhline(prices[cur]['buy_mean'], color='k', linestyle='dashed', linewidth=1, label=f'Buy mean')
        plt.axhline(prices[cur]['sell_mean'], color='r', linestyle='dashed', linewidth=1, label=f'Sell mean')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
        plt.xticks(time_data_p)

        volume = prices[cur]['volume']
        tekst = f'Wartość wolumena:\n{round(volume,2)}'
        plt.annotate(tekst, xy=(1.01, 0.2), xycoords='axes fraction')

        rsi = prices[cur]['rsi']
        tekst = f'Rsi:{round(rsi,2)}'
        plt.annotate(tekst, xy=(1.01, 0), xycoords='axes fraction')


def dataFrame(CURRIENCES=CURRIENCES, prices = {}):
    for cur in CURRIENCES:
        prices[cur] = {'buy': [], 'sell': [], 'buy_mean':0, 'sell_mean':0, 'volume':0, 'growth_val':[], 'dec_val':[], 'rsi':0}
    return prices    


if __name__ == '__main__':
    time_data = []
    prices = dataFrame()
    f = plt.figure(figsize=(15, 13), dpi=80)
    T_animation=animation(f,plotLoop,interval=1000*SLEEP_TIME)
    plt.show()
