import requests
import sys
from time import sleep
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animation
from statistics import mean
from matplotlib.widgets import TextBox
import json

CURRIENCES = ['LTCPLN', 'ETHPLN', 'XRPPLN']
SLEEP_TIME = 5
URL_BEG = 'https://bitbay.net/API/Public/'
URL_END = '/ticker.json'
URL_TRAN = 'https://api.bitbay.net/rest/trading/transactions/'
MEAN_PEROID = 5
RSI_PEROID = 10
volume_hist = []

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

def getTransa(currency):
    url = URL_TRAN + currency + '-USD'
    try:
        response = requests.get(url)
        response.raise_for_status()
        response = response.json()
        return response['items']
    except requests.HTTPError as exception:
        print(exception)
        sys.exit()

def volatile_asset(cur, X, Y):
    cur = cur[:3]
    transa = getTransa(cur)
    data = []

    for i,t in enumerate(transa):
        if i > Y:
            break
        else:
            data.append(float(t['a'])*float(t['r']))

    minimum = min(data)
    maximum = max(data)

    dif = (abs(maximum - minimum) / maximum) * 100
    if dif > X:
        return '<- Volatile asset'
    else:
        return ''

def liquid_asset(cur, S):
    cur = cur[:3]
    transa = getTransa(cur)
    buy_data = []
    sell_data = []

    for t in transa:
        if t['ty'] == 'Buy':
            buy_data.append(float(t['a'])*float(t['r']))
        else:
            sell_data.append(float(t['a'])*float(t['r']))

    buy = mean(buy_data)
    sell = mean(sell_data)
    dif = (abs(buy-sell)/buy)*100

    if dif < S:
        return '<- Liquid asset'
    else:
        return ''

def plotData(time_data, prices):
    max_volume = 0
    max_cur =  False
    for cur in CURRIENCES:
        buy, sell, volume = getData(cur)
        
        if prices[cur]['prev_volume'] != 0:
            current_vol = abs(prices[cur]['prev_volume']-volume)
        else:
            current_vol = False

        prices[cur]['volume'].append(current_vol)
        prices[cur]['buy'].append(buy)
        prices[cur]['sell'].append(sell)
        prices[cur]['candidate'] = 0
        prices[cur]['prev_volume'] = volume

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

        prices[cur]['rsi'].append(rsi)
        avg_buy = mean(prices[cur]['buy'][-MEAN_PEROID::])
        prices[cur]['buy_mean'] = avg_buy
        avg_sell = mean(prices[cur]['sell'][-MEAN_PEROID::])
        prices[cur]['sell_mean'] = avg_sell

        trend = getTrend(rsi)
        prices[cur]['trend'] = trend

        if current_vol > max_volume and trend[0] != -1:
            max_volume = current_vol
            max_cur = cur

    if max_volume > 0:
        prices[max_cur]['candidate'] =  1
        
    time_data.append(datetime.now().strftime("%H:%M:%S"))

    return time_data, prices

def getTrend(rsi):
    if rsi > 60:
        return(1, 'Wzrostowy')
    
    elif rsi < 40:
        return(-1, 'Spadkowy')
    
    else:
        return(0, "Boczny")

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
        ax = plt.twinx()
        ax = plt.plot(time_data_p, prices[cur]['volume'][-5:], label=f'Buy')

        volume = prices[cur]['volume'][-1]
        tekst = f'Wartość wolumena:\n{round(volume,2)}'
        plt.annotate(tekst, xy=(1.01, 0.4), xycoords='axes fraction')

        rsi = prices[cur]['rsi']
        tekst = f'Rsi:{round(rsi[-1],2)}'
        plt.annotate(tekst, xy=(1.01, 0.6), xycoords='axes fraction')
        
        if rsi[-1] != 0:
            trend = prices[cur]['trend'][1]
            tekst = f'Trend: {trend}'
            plt.annotate(tekst, xy=(1.01, 0.2), xycoords='axes fraction')

        if prices[cur]['candidate'] == 1:
            tekst = '<- Kandydat'
            plt.annotate(tekst, xy=(1.01, 0.1), xycoords='axes fraction')
            volatile = volatile_asset(cur, 0, 10)
            plt.annotate(volatile, xy=(1.01, 0.05), xycoords='axes fraction')
            liquid = liquid_asset(cur, 50)
            plt.annotate(liquid, xy=(1.01, 0), xycoords='axes fraction')

def calculate_mean(wallet, amount = False):
    try:
        sum_val = 0
        sum_am = 0
        for trans in wallet:
            sum_val += float(trans[1])*float(trans[0])
            sum_am += float(trans[0])
        if amount:
            if sum_am == 0:
                return 0, 0
            else:
                return sum_val/sum_am, sum_am
        else:
            if sum_am == 0:
                return 0
            else:
                return sum_val/sum_am
    except:
        return 0

def dataFrame(CURRIENCES=CURRIENCES, prices = {}):
    for cur in CURRIENCES:
        prices[cur] = {'buy': [], 'sell': [], 'buy_mean':0, 'sell_mean':0, 'volume':[], 'prev_volume':0, 'growth_val':[], 'dec_val':[], 'rsi':[], 'trend':0, 'candidate':0, 'wallet_amount':0, 'mean_buy_price':0}
    return prices

def save_to_jsn(new_data, filename='user_data.json'):
    with open(filename,'w') as file:
        json.dump(new_data, file, indent = 4)
        

def read_from_js(filename='user_data.json'):
    with open(filename,'r+') as file:
        file = json.load(file)
        try:
            file['LTCPLN']
            return file, 1
        except:
            return {'LTCPLN':[], 'ETHPLN':[], 'XRPPLN':[]}, 0
    

if __name__ == '__main__':
    
    time_data = []
    prices = dataFrame()
    f = plt.figure(figsize=(15, 13), dpi=80)
    T_animation=animation(f,plotLoop,interval=1000*SLEEP_TIME)
    plt.show()
