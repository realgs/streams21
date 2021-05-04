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


def choiceState():
    f = open("D:\\Python\\projekty\\Przetwarzanie_strumieni_danych\\choice.txt", "r")
    data = json.load(f)
    return data

BITBAY_ADRES = 'https://bitbay.net/API/Public'
NEW_BITBAY_ADRES = 'https://api.bitbay.net/rest/trading'
FREQUENCY = 5
MOVING_AVR_SCALE = 3
Y_RSI = choiceState()['y']

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
            volume = 0
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

    if len(currencyList) > 3:
        currentAverage /= 3
        return currentAverage
    else:
        return currencyList[-1]

def animate(i):
    bidBTC, askBTC = dataPicker('ETH', 'PLN', 'ticker.json')
    bidLTC, askLTC = dataPicker('BSV', 'PLN', 'ticker.json')
    bidDASH, askDASH = dataPicker('XLM', 'PLN', 'ticker.json')
    volumeBTC = volumePicker('transactions', 'ETH-PLN', 60)
    volumeLTC = volumePicker('transactions', 'BSV-PLN', 60)
    volumeDASH = volumePicker('transactions', 'XLM-PLN', 60)
    print(volumeBTC, volumeLTC, volumeDASH)
    points_BTC_bid.append(bidBTC)
    points_BTC_ask.append(askBTC)
    points_BTC_volume.append(volumeBTC)
    points_LTC_bid.append(bidLTC)
    points_LTC_ask.append(askLTC)
    points_LTC_volume.append(volumeLTC)
    points_DASH_bid.append(bidDASH)
    points_DASH_ask.append(askDASH)
    points_DASH_volume.append(volumeDASH)
    points_x.append(datetime.now().strftime("%H:%M:%S"))

    left = max(0, len(points_x) - 6)
    right = (len(points_x))

    # Relative strength index RSI
    RSI_BTC.append(RSIcalculator(decrease_BTC, increase_BTC, points_BTC_bid, 3))
    RSI_LTC.append(RSIcalculator(decrease_LTC, increase_LTC, points_LTC_bid, 3))
    RSI_DASH.append(RSIcalculator(decrease_DASH, increase_DASH, points_DASH_bid, 3))

    # Moving Average
    points_BTC_bid_avr.append(movingAverage(points_BTC_bid))
    points_BTC_ask_avr.append(movingAverage(points_BTC_ask))

    points_LTC_bid_avr.append(movingAverage(points_LTC_bid))
    points_LTC_ask_avr.append(movingAverage(points_LTC_ask))

    points_DASH_bid_avr.append(movingAverage(points_DASH_bid))
    points_DASH_ask_avr.append(movingAverage(points_DASH_ask))


    # Plots
    with plt.style.context('seaborn'):
        plt.cla()

        ax1.plot(points_x, points_BTC_bid, color='#009933', linewidth=1.5, label='BTC Bids' if i == 0 else "")
        ax1.plot(points_x, points_BTC_ask, color='#ff0000', linewidth=1.5, label='BTC Asks' if i == 0 else "")
        ax1.plot(points_x, points_BTC_bid_avr, color='#003300', linestyle='--', linewidth=1.5, label='BTC Bids AVR' if i == 0 else "")
        ax1.plot(points_x, points_BTC_ask_avr, color='#4d0000', linestyle='--', linewidth=1.5, label='BTC Asks AVR' if i == 0 else "")
        ax1.set_xlim(left= left, right= right)
        ax1.set_xlabel('Czas', fontsize=12)
        ax1.set_ylabel('Wartość w złotówkach', fontsize=12)
        ax1.set_yscale('log')
        ax1.legend()

        ax2.plot(points_x, points_LTC_bid, color='#009933', linewidth=1.5, label='LTC Bids' if i == 0 else "")
        ax2.plot(points_x, points_LTC_ask, color='#ff0000', linewidth=1.5, label='LTC Asks' if i == 0 else "")
        ax2.plot(points_x, points_LTC_bid_avr, color='#003300', linestyle='--', linewidth=1.5, label='LTC Bids AVR' if i == 0 else "")
        ax2.plot(points_x, points_LTC_ask_avr, color='#4d0000', linestyle='--', linewidth=1.5, label='LTC Asks AVR' if i == 0 else "")
        ax2.set_xlim(left= left, right= right)
        ax2.set_xlabel('Czas', fontsize=12)
        ax2.set_yscale('log')
        ax2.legend()

        ax3.plot(points_x, points_DASH_bid, color='#009933', linewidth=1.5, label='DASH Bids' if i == 0 else "")
        ax3.plot(points_x, points_DASH_ask, color='#ff0000', linewidth=1.5, label='DASH Asks' if i == 0 else "")
        ax3.plot(points_x, points_DASH_bid_avr, color='#003300', linestyle='--', linewidth=1.5, label='DASH Bids AVR' if i == 0 else "")
        ax3.plot(points_x, points_DASH_ask_avr, color='#4d0000', linestyle='--', linewidth=1.5, label='DASH Asks AVR' if i == 0 else "")
        ax3.set_xlim(left= left, right= right)
        ax3.set_xlabel('Czas', fontsize=12)
        ax3.set_yscale('log')
        ax3.legend()

        if choiceState()['type'] == 'volume':
            ax4.plot(points_x, points_BTC_volume, color='#969696', alpha=0.5, label='Wolumen BTC' if i == 0 else "")
            ax4.set_xlim(left= left, right= right)
            ax4.set_ylabel('Ilość wolumenu', fontsize=12)
            ax4.set_xlabel('Czas', fontsize=12)
            ax4.legend()
            ax5.plot(points_x, points_LTC_volume, color='#969696', alpha=0.5)
            ax5.set_xlim(left= left, right= right)
            ax5.set_xlabel('Czas', fontsize=12)
            # ax5.legend()
            ax6.plot(points_x, points_DASH_volume, color='#969696', alpha=0.5)
            ax6.set_xlim(left= left, right= right)
            ax6.set_xlabel('Czas', fontsize=12)
            # ax6.legend()
        elif choiceState()['type'] == 'rsi':

            ax4.plot(points_x, RSI_BTC, color='#6600ff')
            ax4.set_xlim(left= left, right= right)
            ax4.set_ylabel('Wskaźnik siły względnej', fontsize=12)
            ax4.set_xlabel('Czas', fontsize=12)
            ax5.plot(points_x, RSI_LTC, color='#6600ff')
            ax5.set_xlim(left= left, right= right)
            ax5.set_xlabel('Czas', fontsize=12)
            ax6.plot(points_x, RSI_DASH, color='#6600ff')
            ax6.set_xlim(left= left, right= right)
            ax6.set_xlabel('Czas', fontsize=12)

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

    ani = FuncAnimation(fig, animate, interval=3000)
    plt.show()
