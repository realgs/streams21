import numpy as np
import pandas as pd
import requests
from requests.exceptions import HTTPError
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta
import json

plt.style.use('fivethirtyeight')
params = {'legend.fontsize': 'x-small',
         'axes.labelsize': 'x-small',
         'xtick.labelsize':'x-small',
         'ytick.labelsize':'x-small'}
pylab.rcParams.update(params)
plt.rcParams['legend.numpoints'] = 1

# if elem['currency'] == sellingElem['currency'] and elem['amountInitial'] == sellingElem['amountInitial'] and elem['cost'] == sellingElem['cost']
def choiceState():
    f = open("D:\\Python\\projekty\\Przetwarzanie_strumieni_danych\\choice.txt", "r")
    data = json.load(f)
    return data

BITBAY_ADRES = 'https://bitbay.net/API/Public'
NEW_BITBAY_ADRES = 'https://api.bitbay.net/rest/trading'
FREQUENCY = 6
MOVING_AVR_SCALE = choiceState()['yMovAv']
Y_RSI = choiceState()['yRsi']
Y = 3
X = 0.1 # 10%
S = 0.1 # 10%

def dataPicker(resource, currency, format):
    try:
        _ADRES = f'{BITBAY_ADRES}/{resource}/{currency}/{format}'
        response = requests.get(_ADRES)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        _DATA = response.json()
        print(_DATA)
        return _DATA["bid"], _DATA["ask"]

def volumePicker(resource, currency, fromTime):
    try:
        _ADRES = f'{NEW_BITBAY_ADRES}/{resource}/{currency}'

        now = datetime.now()
        before = int((now - timedelta(0, fromTime)).timestamp()) * 1000
        headers = {'content-type': 'application/json'}
        querystring = {"fromTime": before, "limit": 1}

        response = requests.request("GET", _ADRES, headers=headers, params=querystring)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        _DATA = response.json()
        try:
            volume = _DATA['items'][0]['a']
        except IndexError:
            volume = str(0.0)
        return volume

def RSIcalculator(decrease, increase, buyArray, period):
    if len(buyArray) > period:
        value = buyArray[len(buyArray) - 1] - buyArray[len(buyArray) - period]
        if value > 0:
            increase.append(value)
        else:
            decrease.append(value)

        a = (sum(increase) + 1) / (len(increase) + 1)
        b = (sum(decrease) + 1) / (len(decrease) + 1)
    else:
        a = 1
        b = 1
    RSI = 100 - (100 / (1 + (a/b)))
    return RSI

def movingAverage(currencyList):
    currentAverage = 0
    for i in range(len(currencyList) - MOVING_AVR_SCALE, len(currencyList)):
        if i >= 0:
            currentAverage += currencyList[i]

    if len(currencyList) > MOVING_AVR_SCALE:
        currentAverage /= MOVING_AVR_SCALE
        return currentAverage
    else:
        return currencyList[-1]

def typeOfVolume(volumes, types):
    volumeDataBase = {types[0]: '', types[1]: '', types[2]: ''}
    for volumeIndex in range(len(volumes)):
        if len(volumes[volumeIndex]) > 3:
            avr = 0
            for index in range(len(volumes[volumeIndex]) - 1, len(volumes[volumeIndex]) - 4, -1):
                avr += volumes[volumeIndex][index]
            avr /= 3
            if round(avr - volumes[volumeIndex][-4], 6) == 0:
                volumeDataBase[types[volumeIndex]] += f'Wolumen {types[volumeIndex]} horyzontalny'
            elif avr <= volumes[volumeIndex][-4]:
                volumeDataBase[types[volumeIndex]] += f'Wolumen {types[volumeIndex]} malejący'
            else:
                volumeDataBase[types[volumeIndex]] += f'Wolumen {types[volumeIndex]} wzrostowy'
        else:
            volumeDataBase[types[volumeIndex]] += f'Wolumen {types[volumeIndex]}'

    theBiggestVolume = 0
    candidateIndex = -1
    candidate = 0
    liqAsset = False
    for i in range(3):
        if volumes[i][-1] > theBiggestVolume and ('malejący' not in volumeDataBase[types[i]]):
            theBiggestVolume = volumes[i][-1]
            candidateIndex = i
            candidate = volumes[i].copy()
    if candidateIndex > -1:
        volumeDataBase[types[candidateIndex]] += '(C)'
        liqAsset = types[candidateIndex]

        if len(candidate) > Y and candidate[-Y] > 0 and candidate[-1] > 0 and abs(1 - candidate[-Y] / candidate[-1]) > X:
            volumeDataBase[types[candidateIndex]] += f' VA'

    return volumeDataBase, liqAsset

def averageOfCustomerBids(bidArray, askArray):
    if len(bidArray) != 0:
        howMany = 0
        btcSum = 0
        notEmptyAskArray = [elem for elem in askArray if elem['amountLeft'] != 0]
        if notEmptyAskArray != []:
            for elem in notEmptyAskArray:
                selling(elem)
        for bidValue in bidArray:
            if bidValue['amountLeft'] != 0:
                btcSum += bidValue['amountLeft'] * bidValue['cost']
                howMany += bidValue['amountLeft']
        try:
            btcSum /= howMany
        except ZeroDivisionError:
            btcSum = 0
        return round(btcSum, 2)
    return None

def selling(sellingObject):
    f = open("D:\\Python\\projekty\\Przetwarzanie_strumieni_danych\\choice.txt", "r")
    data = json.load(f)
    currentSellingObjectIndex = data['asks'].index(sellingObject)
    sellingCurrency = data['asks'][currentSellingObjectIndex]['currency']
    for elem in data['bids']:
        if elem['currency'] == sellingCurrency and elem['amountLeft'] > 0:
            amountAfterSelling = elem['amountLeft'] - data['asks'][currentSellingObjectIndex]['amountLeft']
            if amountAfterSelling == 0:
                cost = elem['amountLeft'] * elem['cost']
                profit = data['asks'][currentSellingObjectIndex]['amountLeft'] * data['asks'][currentSellingObjectIndex]['cost']
                data['profit'][sellingCurrency] += profit - cost
                elem['amountLeft'] = 0
                data['asks'][currentSellingObjectIndex]['amountLeft'] = 0
                break
            elif amountAfterSelling < 0:
                cost = elem['amountLeft'] * elem['cost']
                profit = elem['amountLeft'] * data['asks'][currentSellingObjectIndex]['cost']
                data['profit'][sellingCurrency] += profit - cost
                elem['amountLeft'] = 0
                data['asks'][currentSellingObjectIndex]['amountLeft'] = abs(amountAfterSelling)
            elif amountAfterSelling > 0:
                cost = data['asks'][currentSellingObjectIndex]['amountLeft'] * elem['cost']
                profit = data['asks'][currentSellingObjectIndex]['amountLeft'] * data['asks'][currentSellingObjectIndex]['cost']
                data['profit'][sellingCurrency] += profit - cost
                elem['amountLeft'] = amountAfterSelling
                data['asks'][currentSellingObjectIndex]['amountLeft'] = 0
                break
    f.close()
    g = open("D:\\Python\\projekty\\Przetwarzanie_strumieni_danych\\choice.txt", "w")
    json.dump(data, g)
    g.close()


def animate(i):
    bidBTC, askBTC = dataPicker('BTC', 'PLN', 'ticker.json')
    bidLTC, askLTC = dataPicker('BSV', 'PLN', 'ticker.json')
    bidDASH, askDASH = dataPicker('XLM', 'PLN', 'ticker.json')
    volumeBTC = volumePicker('transactions', 'ETH-PLN', 60)
    volumeLTC = volumePicker('transactions', 'BSV-PLN', 60)
    volumeDASH = volumePicker('transactions', 'XLM-PLN', 60)
    points_BTC_bid.append(bidBTC)
    points_BTC_ask.append(askBTC)
    points_BTC_volume.append(float(volumeBTC))
    points_LTC_bid.append(bidLTC)
    points_LTC_ask.append(askLTC)
    points_LTC_volume.append(float(volumeLTC))
    points_DASH_bid.append(bidDASH)
    points_DASH_ask.append(askDASH)
    points_DASH_volume.append(float(volumeDASH))
    points_x.append(datetime.now().strftime("%H:%M:%S"))

    left = max(0, len(points_x) - 6)
    right = (len(points_x))

    # Relative strength index RSI
    RSI_BTC.append(RSIcalculator(decrease_BTC, increase_BTC, points_BTC_bid, Y_RSI))
    RSI_LTC.append(RSIcalculator(decrease_LTC, increase_LTC, points_LTC_bid, Y_RSI))
    RSI_DASH.append(RSIcalculator(decrease_DASH, increase_DASH, points_DASH_bid, Y_RSI))

    # Moving Average
    points_BTC_bid_avr.append(movingAverage(points_BTC_bid))
    points_BTC_ask_avr.append(movingAverage(points_BTC_ask))

    points_LTC_bid_avr.append(movingAverage(points_LTC_bid))
    points_LTC_ask_avr.append(movingAverage(points_LTC_ask))

    points_DASH_bid_avr.append(movingAverage(points_DASH_bid))
    points_DASH_ask_avr.append(movingAverage(points_DASH_ask))

    volumeDataBase, liqAsset = typeOfVolume([points_BTC_volume, points_LTC_volume, points_DASH_volume], ['BTC', 'LTC', 'DASH'])
    if liqAsset is not False:
        liqAssetBid, liqAssetAsk = [], []
        if liqAsset == 'BTC':
            liqAssetBid, liqAssetAsk = points_BTC_bid, points_BTC_ask
        elif liqAsset == 'LTC':
            liqAssetBid, liqAssetAsk = points_LTC_bid, points_LTC_ask
        elif liqAsset == 'DASH':
            liqAssetBid, liqAssetAsk = points_DASH_bid, points_DASH_ask

        liqDiff = sum(liqAssetBid[-Y:]) / sum(liqAssetAsk[-Y:])
        if abs(1 - liqDiff) > S:
            volumeDataBase[liqAsset] += f' LA'

    # Customer values
    bidsDataBase = {"BTC": 0, "BSV": 0, "XLM": 0}
    if len(choiceState()['bids']) != 0:
        btcBidList = [elem for elem in choiceState()['bids'] if elem["currency"] == "BTC"]
        bsvBidList = [elem for elem in choiceState()['bids'] if elem["currency"] == "BSV"]
        xlmBidList = [elem for elem in choiceState()['bids'] if elem["currency"] == "XLM"]
        btcAskList = [elem for elem in choiceState()['asks'] if elem["currency"] == "BTC"]
        bsvAskList = [elem for elem in choiceState()['asks'] if elem["currency"] == "BSV"]
        xlmAskList = [elem for elem in choiceState()['asks'] if elem["currency"] == "XLM"]
        bidsDataBase['BTC'] = averageOfCustomerBids(btcBidList, btcAskList)
        bidsDataBase['BSV'] = averageOfCustomerBids(bsvBidList, bsvAskList)
        bidsDataBase['XLM'] = averageOfCustomerBids(xlmBidList, xlmAskList)
    print(f'\nbidsDataBase: {bidsDataBase}\n')

    askBTCleft = sum([elem["amountLeft"] for elem in choiceState()["bids"] if elem["currency"] == "BTC"])
    askBSVleft = sum([elem["amountLeft"] for elem in choiceState()["bids"] if elem["currency"] == "BSV"])
    askXLMleft = sum([elem["amountLeft"] for elem in choiceState()["bids"] if elem["currency"] == "XLM"])

    # Plots
    with plt.style.context('seaborn'):
        plt.cla()

        ax1.plot(points_x, points_BTC_bid, color='#009933', linewidth=1.5, label='BTC Bids' if i == 1 else "")
        ax1.plot(points_x, points_BTC_ask, color='#ff0000', linewidth=1.5, label='BTC Asks' if i == 1 else "")
        ax1.plot(points_x, points_BTC_bid_avr, color='#003300', linestyle='--', linewidth=1.5, label='BTC Bids AVR' if i == 1 else "")
        ax1.plot(points_x, points_BTC_ask_avr, color='#4d0000', linestyle='--', linewidth=1.5, label='BTC Asks AVR' if i == 1 else "")
        ax1.plot(points_x, [bidsDataBase['BTC'] for i in range(len(points_x))], color='#6600ff', linestyle='-.', linewidth=1.5, label='BTC AVR Customer' if i == 1 else "")
        ax1.set_xlim(left= left, right= right)
        ax1.set_xlabel(f'Obecny bilans: {choiceState()["profit"]["BTC"]}, pozostało {askBTCleft} jednostek', fontsize=12)
        ax1.set_ylabel('Wartość w złotówkach', fontsize=12)
        ax1.set_yscale('log')
        ax1.legend()

        ax2.plot(points_x, points_LTC_bid, color='#009933', linewidth=1.5, label='LTC Bids' if i == 1 else "")
        ax2.plot(points_x, points_LTC_ask, color='#ff0000', linewidth=1.5, label='LTC Asks' if i == 1 else "")
        ax2.plot(points_x, points_LTC_bid_avr, color='#003300', linestyle='--', linewidth=1.5, label='LTC Bids AVR' if i == 1 else "")
        ax2.plot(points_x, points_LTC_ask_avr, color='#4d0000', linestyle='--', linewidth=1.5, label='LTC Asks AVR' if i == 1 else "")
        ax2.plot(points_x, [bidsDataBase['BSV'] for i in range(len(points_x))], color='#6600ff', linestyle='-.', linewidth=1.5, label='LTC AVR Customer' if i == 1 else "")
        ax2.set_xlim(left= left, right= right)
        ax2.set_xlabel(f'Obecny bilans: {choiceState()["profit"]["BSV"]}, pozostało {askBSVleft} jednostek', fontsize=12)
        ax2.set_yscale('log')
        ax2.legend()

        ax3.plot(points_x, points_DASH_bid, color='#009933', linewidth=1.5, label='DASH Bids' if i == 1 else "")
        ax3.plot(points_x, points_DASH_ask, color='#ff0000', linewidth=1.5, label='DASH Asks' if i == 1 else "")
        ax3.plot(points_x, points_DASH_bid_avr, color='#003300', linestyle='--', linewidth=1.5, label='DASH Bids AVR' if i == 1 else "")
        ax3.plot(points_x, points_DASH_ask_avr, color='#4d0000', linestyle='--', linewidth=1.5, label='DASH Asks AVR' if i == 1 else "")
        ax3.plot(points_x, [bidsDataBase['XLM'] for i in range(len(points_x))], color='#6600ff', linestyle='-.', linewidth=1.5, label='LTC AVR Customer' if i == 1 else "")
        ax3.set_xlim(left= left, right= right)
        ax3.set_xlabel(f'Obecny bilans: {choiceState()["profit"]["XLM"]}, pozostało {askXLMleft} jednostek', fontsize=12)
        ax3.set_yscale('log')
        ax3.legend()

        if choiceState()['type'] == 'volume':
            ax4.bar(points_x, points_BTC_volume, color='#969696', alpha=0.5, label='BTC' if i == 1 else "")
            ax4.set_ylabel('Ilość wolumenu', fontsize=12)
            ax4.set_title(volumeDataBase['BTC'])
            ax5.bar(points_x, points_LTC_volume, color='#969696', alpha=0.5, label='LTC' if i == 1 else "")
            ax5.set_title(volumeDataBase['LTC'])
            ax6.bar(points_x, points_DASH_volume, color='#969696', alpha=0.5, label='DASH' if i == 1 else "")
            ax6.set_title(volumeDataBase['DASH'])
        elif choiceState()['type'] == 'rsi':
            ax4.plot(points_x, RSI_BTC, color='#6600ff', label='RSI BTC' if i == 1 else "")
            ax4.set_ylabel('Wskaźnik siły względnej', fontsize=12)
            ax5.plot(points_x, RSI_LTC, color='#6600ff', label='RSI LTC' if i == 1 else "")
            ax6.plot(points_x, RSI_DASH, color='#6600ff', label='RSI DASH' if i == 1 else "")

        ax4.set_xlim(left= left, right= right)
        ax4.set_xlabel('Czas', fontsize=12)
        ax4.legend()
        ax5.set_xlim(left= left, right= right)
        ax5.set_xlabel('Czas', fontsize=12)
        ax5.legend()
        ax6.set_xlim(left= left, right= right)
        ax6.set_xlabel('Czas', fontsize=12)
        ax6.legend()

        plt.suptitle("Najlepsze kursy kupna oraz sprzedaży")


if __name__ == '__main__':
    points_x = []
    points_BTC_bid = []
    points_BTC_ask = []
    points_BTC_bid_avr = []
    points_BTC_ask_avr = []
    points_BTC_volume = []
    decrease_BTC = []
    increase_BTC = []
    RSI_BTC = []
    points_LTC_bid = []
    points_LTC_ask = []
    points_LTC_bid_avr = []
    points_LTC_ask_avr = []
    points_LTC_volume = []
    decrease_LTC = []
    increase_LTC = []
    RSI_LTC = []
    points_DASH_bid = []
    points_DASH_ask = []
    points_DASH_bid_avr = []
    points_DASH_ask_avr = []
    points_DASH_volume = []
    decrease_DASH = []
    increase_DASH = []
    RSI_DASH = []

    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3)
    fig.tight_layout(pad=1.0)

    ani = FuncAnimation(fig, animate, interval=FREQUENCY)
    plt.show()
