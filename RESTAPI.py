import requests
import time
import sys
import urllib.request
import matplotlib.pyplot as plt
import datetime
import numpy as np

def calculate(buy_price, sell_price):
    output = round((1 - (sell_price - buy_price) / buy_price), 3)
    print(str(output) + " %")

def connect():
    try:
        urllib.request.urlopen('http://google.com')
    except:
        print("No internet connection")
        sys.exit()

def theGreatest(a, b):
    if a > b:
        return a
    else:
        return b

def calculateAverage(arraySell, arrayBuy, samplesNumber):
    valueBuy = 0
    valueSell = 0
    if len(arrayBuy) >= samplesNumber:
        for items in range(samplesNumber):
            valueBuy += arrayBuy[items]
        valueBuy /= samplesNumber
    else:
        for items in range(len(arrayBuy)):
            valueBuy += arrayBuy[items]
        valueBuy /= samplesNumber

    if len(arraySell) >= samplesNumber:
        for items in range(samplesNumber):
            valueSell += arraySell[items]
        valueSell /= samplesNumber
    else:
        for items in range(len(arraySell)):
            valueSell += arraySell[items]
        valueSell /= samplesNumber
    return valueSell, valueBuy

def calculateRSI(buyArray, samplesNumber):
    if len(buyArray) > samplesNumber:
        value = buyArray[len(buyArray)-1] - buyArray[len(buyArray)-samplesNumber]
        if value > 0:
            MeanIncreaseArray.append(value)
        else:
            MeanDecreaseArray.append(value)

        a = (sum(MeanIncreaseArray) + 1)/(len(MeanIncreaseArray) + 1)
        b = (sum(MeanDecreaseArray) + 1)/(len(MeanDecreaseArray) + 1)
    else:
        a = 1
        b = 1
    RSI = 100 - (100 / (1 + (a/b)))
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
        print(f'Volume {volume}')
        calculate(buy_price, sell_price)
        return buy_price, sell_price, volume
    else:
        print("Error when trying to fetch")
        sys.exit()

if __name__ == "__main__":
    i = 0
    x = []
    xLabels = []

    BTCSellArray = []
    BTCBuyArray = []
    BTCVolumeArray = []
    BTCAverageArray = []

    ETHSellArray = []
    ETHBuyArray = []
    ETHVolumeArray = []
    ETHAverageArray = []

    LSKSellArray = []
    LSKBuyArray = []
    LSKVolumeArray = []
    LSKAverageArraySell = []
    LSKAverageArrayBuy = []

    MeanDecreaseArray = []
    MeanIncreaseArray = []
    RSIArray = []

    plt.show()
    fig, axes = plt.subplots(2, 3, figsize=(10, 4))
    fig.tight_layout(pad=2.0)

    plt.xlabel("Time")

    axes[0][0].set_title("GNT")
    axes[0][1].set_title("ETH")
    axes[0][2].set_title("LSK")

    axes[1][0].set_title("Volume")
    axes[1][1].set_title("Volume")
    axes[1][2].set_title("Volume")

    axes[0][0].grid()
    axes[0][1].grid()
    axes[0][2].grid()

    while True:
        x.append(datetime.datetime.now().strftime("%H:%M:%S"))
        buyBTC, sellBTC, volumeBTC = getCurrencyData("BTC", "ticker")
        buyETH, sellETH, volumeETH = getCurrencyData("ETH", "ticker")
        buyLSK, sellLSK, volumeLSK = getCurrencyData("LSK", "ticker")

        xLabels = x.copy()
        if len(xLabels) > 4:
            median = int(np.floor(np.median(np.arange(0, len(xLabels)))))
            xLabels = [xLabels[0], xLabels[median], xLabels[-1]]

        BTCSellArray.append(sellBTC)
        BTCBuyArray.append(buyBTC)
        BTCVolumeArray.append(volumeBTC)

        ETHSellArray.append(sellETH)
        ETHBuyArray.append(buyETH)
        ETHVolumeArray.append(volumeETH)

        LSKSellArray.append(sellLSK)
        LSKBuyArray.append(buyLSK)
        LSKVolumeArray.append(volumeLSK)

        valueBuy, valueSell = calculateAverage(LSKSellArray, LSKBuyArray, 3)
        LSKAverageArraySell.append(valueSell)
        LSKAverageArrayBuy.append(valueBuy)

        RSI = calculateRSI(LSKSellArray, 2)
        RSIArray.append(RSI)

        axes[0][0].plot(x, BTCSellArray, color='red')
        axes[0][0].plot(x, BTCBuyArray, color='magenta')
        axes[0][0].set_xticks(xLabels)

        axes[1][0].bar(x, BTCVolumeArray, color='red')
        axes[1][0].set_xticks(xLabels)

        axes[0][1].plot(x, ETHSellArray, color='red')
        axes[0][1].plot(x, ETHBuyArray, color='magenta')
        axes[0][1].set_xticks(xLabels)

        axes[1][1].bar(x, ETHVolumeArray, color='red')
        axes[1][1].set_xticks(xLabels)

        axes[0][2].plot(x, LSKSellArray, color='red', label='Sell' if i == 0 else "")
        axes[0][2].plot(x, LSKBuyArray, color='magenta')
        axes[0][2].plot(x, LSKAverageArrayBuy, color='blue', linestyle='dashed')
        axes[0][2].plot(x, LSKAverageArraySell, color='orange', linestyle='dashed')
        axes[0][2].plot(x, RSIArray, color='green', linestyle='dashed')
        axes[0][2].set_xticks(xLabels)
        axes[0][2].legend(loc="upper right")

        axes[1][2].bar(x, LSKVolumeArray, color='red')
        axes[1][2].set_xticks(xLabels)
        i += 1
        plt.draw()
        plt.pause(1e-17)
        time.sleep(5)
