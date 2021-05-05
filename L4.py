import requests
import sys
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import time
import warnings

warnings.filterwarnings("ignore")


RSI_samples = 3
average_samples = 3
time_volume = 5
base_currency = "PLN"
first_currency = "LTC"
second_currency = "ETH"
third_currency = "LSK"

def calculate(buy_price, sell_price):
    output = round((1 - (sell_price - buy_price) / buy_price), 3)
    print(str(output) + " %")

def connect():
    try:
        urllib.request.urlopen('http://google.com')
    except:
        print("No internet connection")
        sys.exit()

def theGreatest(array):
    Lmax = max(array)
    return Lmax

def get_volume(fromCurrancy, toCurrancy, time):
    url = f"https://api.bitbay.net/rest/trading/transactions/{fromCurrancy}-{toCurrancy}"

    now = datetime.now()
    before = now - timedelta(0, time)
    before -= timedelta(0, time) - timedelta(0, time)
    querystring = {"from": int(before.timestamp()) * 1000, "to": int(now.timestamp()) * 1000}

    try:
        response = requests.request("GET", url, params=querystring)
        a = response.json()['items'][0]['a']
    except:
        a = 0
    return a

def average_calculate(arraySell, arrayBuy, samplesNumber):
    valueBuy = 0
    valueSell = 0
    if len(arrayBuy) > samplesNumber:
        for items in range(samplesNumber):
            valueBuy += arrayBuy[len(arrayBuy)-items-1]
        valueBuy /= samplesNumber
    else:
        for items in range(len(arrayBuy)):
            valueBuy += arrayBuy[items]
        valueBuy /= samplesNumber

    if len(arraySell) > samplesNumber:
        for items in range(samplesNumber):
            valueSell += arraySell[len(arraySell)-items-1]
        valueSell /= samplesNumber
    else:
        for items in range(len(arraySell)):
            valueSell += arraySell[items]
        valueSell /= samplesNumber
    return valueSell, valueBuy

def RSI_calculate(DecreaseArray, IncreaseArray, buyArray, samplesNumber):
    if len(buyArray) > samplesNumber:
        value = buyArray[len(buyArray)-1] - buyArray[len(buyArray)-samplesNumber]
        if value > 0:
            IncreaseArray.append(value)
        else:
            DecreaseArray.append(value)

        a = (sum(IncreaseArray) + 1) / (len(IncreaseArray) + 1)
        b = (sum(DecreaseArray) + 1) / (len(DecreaseArray) + 1)
    else:
        a = 1
        b = 1
    RSI = 100 - (100 / (1 + (a + 1/b + 1)))
    return RSI

def getCurrencyData(currency, category):
    connect()
    url = f"https://bitbay.net/API/Public/{currency}PLN/{category}.json"
    try:
        response = requests.get(url)
    except Exception as exception:
        print(exception)
        return False

    if response.status_code == 200:
        print(f"-----------{currency}-------------")
        json = response.json()
        response = json
        sell_price = response['ask']
        buy_price = response['bid']
        volume = response['volume']
        calculate(buy_price, sell_price)
        return buy_price, sell_price, volume
    else:
        print("Error when trying to fetch")
        sys.exit()

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

    BTCDecreaseArray = []
    BTCIncreaseArray = []
    BTCRSIArray = []
    # Ether
    ETHSellArray = []
    ETHBuyArray = []
    ETHVolumeArray = []
    ETHAverageArraySell = []
    ETHAverageArrayBuy = []

    ETHDecreaseArray = []
    ETHIncreaseArray = []
    ETHRSIArray = []
    # Lisk
    LSKSellArray = []
    LSKBuyArray = []
    LSKVolumeArray = []
    LSKAverageArraySell = []
    LSKAverageArrayBuy = []

    LSKDecreaseArray = []
    LSKIncreaseArray = []
    LSKRSIArray = []

    plt.show()
    fig, axes = plt.subplots(2, 3, figsize=(10, 4))
    fig.tight_layout(pad=2.0)

    plt.xlabel("Time")
    axes[0][0].set_title(first_currency)
    axes[0][1].set_title(second_currency)
    axes[0][2].set_title(third_currency)

    axes[1][0].set_title("Volume")
    axes[1][1].set_title("Volume")
    axes[1][2].set_title("Volume")

    axes[0][0].grid()
    axes[0][1].grid()
    axes[0][2].grid()

    while True:
        x.append(datetime.now().strftime("%H:%M:%S"))
        buyBTC, sellBTC, volumeBTC = getCurrencyData(first_currency, "ticker")
        buyETH, sellETH, volumeETH = getCurrencyData(second_currency, "ticker")
        buyLSK, sellLSK, volumeLSK = getCurrencyData(third_currency, "ticker")

        xLabels = x.copy()
        if len(xLabels) > 4:
            median = int(np.floor(np.median(np.arange(0, len(xLabels)))))
            xLabels = [xLabels[0], xLabels[median], xLabels[-1]]

        BTCSellArray.append(sellBTC)
        BTCBuyArray.append(buyBTC)
        BTCVolumeArray.append(get_volume(first_currency, "PLN", time_volume))

        valueBuyB, valueSellB = average_calculate(BTCSellArray, BTCBuyArray, average_samples)
        BTCAverageArraySell.append(valueSellB)
        BTCAverageArrayBuy.append(valueBuyB)

        RSIB = RSI_calculate(BTCDecreaseArray, BTCIncreaseArray, BTCSellArray, RSI_samples)
        BTCRSIArray.append(RSIB)



        ETHSellArray.append(sellETH)
        ETHBuyArray.append(buyETH)
        ETHVolumeArray.append(get_volume(second_currency, "PLN", time_volume))

        valueBuyE, valueSellE = average_calculate(ETHSellArray, ETHBuyArray, average_samples)
        ETHAverageArraySell.append(valueSellE)
        ETHAverageArrayBuy.append(valueBuyE)

        RSIE = RSI_calculate(ETHDecreaseArray, ETHIncreaseArray, ETHBuyArray, RSI_samples)
        ETHRSIArray.append(RSIE)



        LSKSellArray.append(sellLSK)
        LSKBuyArray.append(buyLSK)
        LSKVolumeArray.append(get_volume(third_currency, "PLN", time_volume))

        valueBuy, valueSell = average_calculate(LSKSellArray, LSKBuyArray, average_samples)
        LSKAverageArraySell.append(valueSell)
        LSKAverageArrayBuy.append(valueBuy)

        RSI = RSI_calculate(LSKDecreaseArray, LSKIncreaseArray, LSKSellArray, RSI_samples)
        LSKRSIArray.append(RSI)

        axes[0][0].plot(x, BTCSellArray, color='green')
        axes[0][0].plot(x, BTCBuyArray, color='magenta')
        axes[0][0].set_xticks(xLabels)
        axes[0][0].plot(x, BTCAverageArrayBuy, color='blue', linestyle='dashed')
        axes[0][0].plot(x, BTCAverageArraySell, color='orange', linestyle='dashed')
        axes[0][0].plot(x, BTCRSIArray, color='red', linestyle='dashed')

        axes[1][0].bar(x, BTCVolumeArray, color='green')
        axes[1][0].set_xticks(xLabels)

        axes[0][1].plot(x, ETHSellArray, color='green')
        axes[0][1].plot(x, ETHBuyArray, color='magenta')
        axes[0][1].set_xticks(xLabels)
        axes[0][1].plot(x, ETHAverageArrayBuy, color='blue', linestyle='dashed')
        axes[0][1].plot(x, ETHAverageArraySell, color='orange', linestyle='dashed')
        axes[0][1].plot(x, ETHRSIArray, color='red', linestyle='dashed')

        axes[1][1].bar(x, ETHVolumeArray, color='green')
        axes[1][1].set_xticks(xLabels)

        axes[0][2].plot(x, LSKSellArray, color='green', label='Sell' if i == 0 else "")
        axes[0][2].plot(x, LSKBuyArray, color='magenta', label='Buy' if i == 0 else "")
        axes[0][2].plot(x, LSKAverageArrayBuy, color='blue', linestyle='dashed', label='Ave.Buy' if i == 0 else "")
        axes[0][2].plot(x, LSKAverageArraySell, color='orange', linestyle='dashed', label='Ave.Sell' if i == 0 else "")
        axes[0][2].plot(x, LSKRSIArray, color='red', linestyle='dashed', label='RSI' if i == 0 else "")

        axes[0][2].set_xticks(xLabels)
        axes[0][2].legend(loc="upper right")

        axes[1][2].bar(x, LSKVolumeArray, color='green')
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
