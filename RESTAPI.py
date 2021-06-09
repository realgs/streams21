import requests
import sys
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import time
import warnings
import json

from VolatileLiquid.Liquid import defineAsLiquid
from VolatileLiquid.Volatile import defineAsVolatile
from RSIandAverage.Average import calculateAverage
from RSIandAverage.RSI import calculateRSI
from CandidateandTrend.Trend import checkWhatTrend
from CandidateandTrend.Candidate import defineCandidate
from API.newAPI import getVolumeNewAPI
from API.oldAPI import getCurrencyData

warnings.filterwarnings("ignore")

RSI_SAMPLES_NUMBER = 3
AVERAGE_SAMPLES_NUMBER = 3
TIME_IN_VOLUME = 5
BASE_CURRENCY = "PLN"
FIRST_CRYPTO = "LTC"
SECOND_CRYPTO = "ETH"
THIRD_CRYPTO = "LSK"

AVERAGE_USER_BUY_PRICE_BTC = []
AVERAGE_USER_BUY_PRICE_ETH = []
AVERAGE_USER_BUY_PRICE_LSK = []

AVERAGE_USER_SELL_PRICE_BTC = []
AVERAGE_USER_SELL_PRICE_ETH = []
AVERAGE_USER_SELL_PRICE_LSK = []

S = 5
X = 5
Y = 3

def theGreatest(array):
    Lmax = max(array)
    return Lmax

if __name__ == "__main__":
    i = 0
    x = []
    xLabels = []
    # GNT
    BTCSellArray = []
    BTCBuyArray = []
    BTCVolumeArray = []
    BTCAverageArraySell = []
    BTCAverageArrayBuy = []
    BTCTrendArray = []

    BTCDecreaseArray = []
    BTCIncreaseArray = []
    BTCRSIArray = []
    # Ether
    ETHSellArray = []
    ETHBuyArray = []
    ETHVolumeArray = []
    ETHAverageArraySell = []
    ETHAverageArrayBuy = []
    ETHTrendArray = []

    ETHDecreaseArray = []
    ETHIncreaseArray = []
    ETHRSIArray = []
    # Lisk
    LSKSellArray = []
    LSKBuyArray = []
    LSKVolumeArray = []
    LSKAverageArraySell = []
    LSKAverageArrayBuy = []
    LSKTrendArray = []

    LSKDecreaseArray = []
    LSKIncreaseArray = []
    LSKRSIArray = []

    plt.show()
    fig, axes = plt.subplots(2, 3, figsize=(10, 4))
    fig.tight_layout(pad=2.0)

    plt.xlabel("Time")
    axes[0][0].set_title(FIRST_CRYPTO)
    axes[0][1].set_title(SECOND_CRYPTO)
    axes[0][2].set_title(THIRD_CRYPTO)

    axes[1][0].set_title("Volume")
    axes[1][1].set_title("Volume")
    axes[1][2].set_title("Volume")

    axes[0][0].grid()
    axes[0][1].grid()
    axes[0][2].grid()

    while True:
        x.append(datetime.now().strftime("%H:%M:%S"))
        buyBTC, sellBTC, volumeBTC = getCurrencyData(FIRST_CRYPTO, "ticker")
        buyETH, sellETH, volumeETH = getCurrencyData(SECOND_CRYPTO, "ticker")
        buyLSK, sellLSK, volumeLSK = getCurrencyData(THIRD_CRYPTO, "ticker")

        xLabels = x.copy()

        if len(xLabels) > 4:
            median = int(np.floor(np.median(np.arange(0, len(xLabels)))))
            xLabels = [xLabels[0], xLabels[median], xLabels[-1]]

        BTCSellArray.append(sellBTC)
        BTCBuyArray.append(buyBTC)
        BTCVolumeArray.append(getVolumeNewAPI(FIRST_CRYPTO, BASE_CURRENCY, TIME_IN_VOLUME))

        valueBuyB, valueSellB = calculateAverage(BTCSellArray, BTCBuyArray, AVERAGE_SAMPLES_NUMBER)
        BTCAverageArraySell.append(valueSellB)
        BTCAverageArrayBuy.append(valueBuyB)

        RSIB = calculateRSI(BTCDecreaseArray, BTCIncreaseArray, BTCSellArray, RSI_SAMPLES_NUMBER)
        BTCRSIArray.append(RSIB)

        # Ether
        ETHSellArray.append(sellETH)
        ETHBuyArray.append(buyETH)
        ETHVolumeArray.append(getVolumeNewAPI(SECOND_CRYPTO, BASE_CURRENCY, TIME_IN_VOLUME))

        valueBuyE, valueSellE = calculateAverage(ETHSellArray, ETHBuyArray, AVERAGE_SAMPLES_NUMBER)
        ETHAverageArraySell.append(valueSellE)
        ETHAverageArrayBuy.append(valueBuyE)

        RSIE = calculateRSI(ETHDecreaseArray, ETHIncreaseArray, ETHBuyArray, RSI_SAMPLES_NUMBER)
        ETHRSIArray.append(RSIE)

        # Lisk
        LSKSellArray.append(sellLSK)
        LSKBuyArray.append(buyLSK)
        LSKVolumeArray.append(getVolumeNewAPI(THIRD_CRYPTO, BASE_CURRENCY, TIME_IN_VOLUME))

        valueBuy, valueSell = calculateAverage(LSKSellArray, LSKBuyArray, AVERAGE_SAMPLES_NUMBER)
        LSKAverageArraySell.append(valueSell)
        LSKAverageArrayBuy.append(valueBuy)

        RSI = calculateRSI(LSKDecreaseArray, LSKIncreaseArray, LSKSellArray, RSI_SAMPLES_NUMBER)
        LSKRSIArray.append(RSI)

        # BUY
        # Buy BTC
        f = open('Buys/buysBTC.json')
        data = json.load(f)

        count = 1
        number = 1
        down = 1
        equesionSum = 0

        for line in range(len(data["data"])):
            down += data['data'][line]['count']
            number = data['data'][line]['count']
            count = data['data'][line]['value']
            equesionSum += number * count
        equesionSum = equesionSum / down
        print(f'Obecna średnia cena zakupy {FIRST_CRYPTO} to: {equesionSum}')
        AVERAGE_USER_BUY_PRICE_BTC.append(equesionSum)
        f.close()

        # Buy ETH
        f = open('Buys/buysETH.json')
        data = json.load(f)

        count = 1
        number = 1
        down = 1
        equesionSum = 0

        for line in range(len(data["data"])):
            down += data['data'][line]['count']
            number = data['data'][line]['count']
            count = data['data'][line]['value']
            equesionSum += number * count
        equesionSum = equesionSum / down
        print(f'Obecna średnia cena zakupy {SECOND_CRYPTO} to: {equesionSum}')
        AVERAGE_USER_BUY_PRICE_ETH.append(equesionSum)
        f.close()

        # Buy LSK
        f = open('Buys/buysLSK.json')
        data = json.load(f)

        count = 1
        number = 1
        down = 1
        equesionSum = 0

        for line in range(len(data["data"])):
            down += data['data'][line]['count']
            number = data['data'][line]['count']
            count = data['data'][line]['value']
            equesionSum += number * count
        equesionSum = equesionSum / down
        print(f'Obecna średnia cena zakupy {THIRD_CRYPTO} to: {equesionSum}')
        AVERAGE_USER_BUY_PRICE_LSK.append(equesionSum)
        f.close()

        # SELL
        # Sell BTC
        f = open('Sells/sellsBTC.json')
        data = json.load(f)

        count = 1
        number = 1

        for line in range(len(data["data"])):
            number += 1
            count += data['data'][line]['value']

        AVERAGE_USER_SELL_PRICE_BTC.append(count / number)
        f.close()

        # Sell ETH
        f = open('Sells/sellsETH.json')
        data = json.load(f)

        count = 1
        number = 1

        for line in range(len(data["data"])):
            number += 1
            count += data['data'][line]['value']

        AVERAGE_USER_SELL_PRICE_ETH.append(count / number)
        f.close()

        # Sell LSK
        f = open('Sells/sellsLSK.json')
        data = json.load(f)

        count = 1
        number = 1

        for line in range(len(data["data"])):
            number += 1
            count += data['data'][line]['value']

        AVERAGE_USER_SELL_PRICE_LSK.append(count / number)
        f.close()

        # if revenue or loss
        f = open('Revenue/revenueBTC.json')
        data = json.load(f)
        if data['data'][0]['revenue'] > 0:
            axes[0][0].set_title(f'{FIRST_CRYPTO} | ZYSK')
        else:
            axes[0][0].set_title(f'{FIRST_CRYPTO} | STRATA')

        f = open('Revenue/revenueETH.json')
        data = json.load(f)
        if data['data'][0]['revenue'] > 0:
            axes[0][1].set_title(f'{SECOND_CRYPTO} | ZYSK')
        else:
            axes[0][1].set_title(f'{SECOND_CRYPTO} | STRATA')

        f = open('Revenue/revenueLSK.json')
        data = json.load(f)
        if data['data'][0]['revenue'] > 0:
            axes[0][2].set_title(f'{THIRD_CRYPTO} | ZYSK')
        else:
            axes[0][2].set_title(f'{THIRD_CRYPTO} | STRATA')


        # axes[0][0].plot(x, BTCSellArray, color='red')
        # axes[0][0].plot(x, BTCBuyArray, color='magenta')
        axes[0][0].plot(x, AVERAGE_USER_BUY_PRICE_BTC, color='green', linestyle='dashed')
        axes[0][0].plot(x, AVERAGE_USER_SELL_PRICE_BTC, color='blue', linestyle='dashed')
        axes[0][0].set_xticks(xLabels)

        # axes[0][0].plot(x, BTCAverageArrayBuy, color='blue', linestyle='dashed')
        # axes[0][0].plot(x, BTCAverageArraySell, color='orange', linestyle='dashed')

        axes[1][0].bar(x, BTCVolumeArray, color='red')
        axes[1][0].set_xticks(xLabels)

        # axes[0][1].plot(x, ETHSellArray, color='red')
        # axes[0][1].plot(x, ETHBuyArray, color='magenta')

        axes[0][1].plot(x, AVERAGE_USER_BUY_PRICE_ETH, color='green', linestyle='dashed')
        axes[0][1].plot(x, AVERAGE_USER_SELL_PRICE_ETH, color='blue', linestyle='dashed')

        axes[0][1].set_xticks(xLabels)
        # axes[0][1].plot(x, ETHAverageArrayBuy, color='blue', linestyle='dashed')
        # axes[0][1].plot(x, ETHAverageArraySell, color='orange', linestyle='dashed')

        axes[1][1].bar(x, ETHVolumeArray, color='red')
        axes[1][1].set_xticks(xLabels)

        # axes[0][2].plot(x, LSKSellArray, color='red', label='Sell' if i == 0 else "")
        # axes[0][2].plot(x, LSKBuyArray, color='magenta', label='Buy' if i == 0 else "")

        axes[0][2].plot(x, AVERAGE_USER_BUY_PRICE_LSK, color='green', linestyle='dashed', label='AVG.Buy' if i == 0 else "")
        axes[0][2].plot(x, AVERAGE_USER_SELL_PRICE_LSK, color='blue', linestyle='dashed', label='AVG.Sell' if i == 0 else "")

        # axes[0][2].plot(x, LSKAverageArrayBuy, color='blue', linestyle='dashed', label='Ave.Buy' if i == 0 else "")
        # axes[0][2].plot(x, LSKAverageArraySell, color='orange', linestyle='dashed', label='Ave.Sell' if i == 0 else "")

        axes[0][2].set_xticks(xLabels)
        axes[0][2].legend(loc="upper right")

        axes[1][2].bar(x, LSKVolumeArray, color='red')
        axes[1][2].set_xticks(xLabels)

        axes[0][0].set_yscale('log')
        axes[0][1].set_yscale('log')
        axes[0][2].set_yscale('log')
        axes[1][0].set_yscale('log')
        axes[1][1].set_yscale('log')
        axes[1][2].set_yscale('log')

        i += 1
        plt.draw()
        plt.pause(1e-17)
        time.sleep(5)
