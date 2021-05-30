import requests
import sys
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import time
import warnings
import json

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
S = 5
X = 5
Y = 3

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

def getVolumeNewAPI(fromCurrancy, toCurrancy, time):
    url = f'https://api.bitbay.net/rest/trading/transactions/{fromCurrancy}-{toCurrancy}'

    now = datetime.now()
    before = int((now - timedelta(0, time)).timestamp()) * 1000
    querystring = {"from": before}

    try:
        response = requests.request("GET", url, params=querystring)
        a = float(response.json()['items'][0]['a'])
    except:
        a = 0
    return a

def calculateAverage(arraySell, arrayBuy, samplesNumber):
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

def calculateRSI(DecreaseArray, IncreaseArray, buyArray, samplesNumber):
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
    RSI = 100 - (100 / (1 + ((a + 1)/(b + 1))))
    return RSI

def checkWhatTrend(RSIArray):

    downHillsPoints = []
    upHillsPoints = []

    for items in range(1, len(RSIArray) - 1):
        if (RSIArray[items - 1] > RSIArray[items]) and (RSIArray[items] < RSIArray[items + 1]):  # sprawdzam czy to dołek
            downHillsPoints.append(items)
        else:
            downHillsPoints.append(0)  # wyrównuję indeksy

        if (RSIArray[items - 1] < RSIArray[items]) and (RSIArray[items] > RSIArray[items + 1]):  # sprawdzam czy to wierzchołek
            upHillsPoints.append(items)
        else:
            upHillsPoints.append(0) # wyrównuję indeksy

    # Sprawdzam czy nastapił spadek
    if (downHillsPoints[len(downHillsPoints) - 1] < downHillsPoints[len(downHillsPoints) - 2]) and \
            (downHillsPoints[len(downHillsPoints) - 1] != 0 and downHillsPoints[len(downHillsPoints) - 2] != 0):
        print("down")
        return "Downward trend"
    # Sprawdzam czy nastapił wzrost
    elif (upHillsPoints[len(upHillsPoints) - 1] > upHillsPoints[len(upHillsPoints) - 2]) and \
            (upHillsPoints[len(upHillsPoints) - 1] != 0 and upHillsPoints[len(upHillsPoints) - 2] != 0):
        print("up")
        return "Rising trend"
    # Sprawdzam czy osięgnęliśmy trend boczny
    elif ((upHillsPoints[len(upHillsPoints) - 1] == upHillsPoints[len(upHillsPoints) - 2]) or (downHillsPoints[len(downHillsPoints) - 1] == downHillsPoints[len(downHillsPoints) - 2])) \
            and (upHillsPoints[len(upHillsPoints) - 1] != 0 and upHillsPoints[len(upHillsPoints) - 2] != 0) \
            and (downHillsPoints[len(downHillsPoints) - 1] != 0 and downHillsPoints[len(downHillsPoints) - 2] != 0):
        print("side")
        return "Sideways trend"
    else:
        print("Small amount of data")
        return "Small amount of data"

def defineCandidate(BTCTrend, ETHTrend, LSKTrend, BTCVolume, ETHVolume, LSKVolume):
    BTC = False
    ETH = False
    LSK = False

    TFArray = [BTC, ETH, LSK]

    BTCLastVolume = float(BTCVolume[len(BTCVolume) - 1])
    ETHLastVolume = float(ETHVolume[len(BTCVolume) - 1])
    LSKLastVolume = float(LSKVolume[len(BTCVolume) - 1])

    LastVolumeArray = [BTCLastVolume, ETHLastVolume, LSKLastVolume]
    max = ""

    if BTCTrend[len(BTCTrend) - 1] != "Downward trend":
        BTC = True
    if ETHTrend[len(ETHTrend) - 1] != "Downward trend":
        ETH = True
    if LSKTrend[len(LSKTrend) - 1] != "Downward trend":
        LSK = True

    maxArray = []
    for items in range(len(TFArray)):
        if TFArray[items] == True:
            maxArray.append(LastVolumeArray[items])
        else:
            maxArray.append(0)
    out = maxArray.index(np.max(maxArray))

    if out == 0:
        max = "BTC"
    elif out == 1:
        max = "ETH"
    else:
        max = "LSK"
    return max

def defineAsLiquid(buy, sell, S):
    if buy > sell:
        max = buy
        min = sell
    else:
        max = sell
        min = sell

    out = min * 100/max
    percent = 100 - out

    if percent < S:
        return True
    else:
        return False

def defineAsVolatile(samplesArray, Y, X):
    if len(samplesArray) > Y:
        Ysample = samplesArray[Y]
    else:
        Ysample = samplesArray[len(samplesArray) - 1]

    currentSample = samplesArray[0]

    if Ysample > currentSample:
        max = Ysample
        min = currentSample
    else:
        max = currentSample
        min = Ysample

    out = min * 100/max
    percent = 100 - out

    if percent > X:
        return True
    else:
        return False

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
        print(f"buy: {valueBuyB}")
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



        with open("data.json", 'r') as fp:
            data = json.load(fp)
            fp.close()

        data["BTC"] = valueSellB
        data["ETH"] = valueSellE
        data["LSK"] = valueSell

        file = open("data.json", "w")
        json.dump(data, file)
        file.close()

        with open('buysBTC.txt') as f:
            lines = f.readlines()

        count = 0
        number = 0

        for line in lines:
            number += 1
            count += float(line)
        AVERAGE_USER_BUY_PRICE_ETH.append(count / number)
        f.close()

        with open('buysETH.txt') as f:
            lines = f.readlines()

        count = 0
        number = 0

        for line in lines:
            number += 1
            count += float(line)
        AVERAGE_USER_BUY_PRICE_LSK.append(count / number)
        f.close()

        with open('buysLSK.txt') as f:
            lines = f.readlines()

        count = 0
        number = 0

        for line in lines:
            number += 1
            count += float(line)
        AVERAGE_USER_BUY_PRICE_BTC.append(count / number)
        f.close()





        axes[0][0].plot(x, BTCSellArray, color='red')
        axes[0][0].plot(x, BTCBuyArray, color='magenta')

        axes[0][0].plot(x, AVERAGE_USER_BUY_PRICE_BTC, color='green', linestyle='dashed')
        axes[0][0].set_xticks(xLabels)

        # axes[0][0].plot(x, BTCAverageArrayBuy, color='blue', linestyle='dashed')
        # axes[0][0].plot(x, BTCAverageArraySell, color='orange', linestyle='dashed')

        axes[1][0].bar(x, BTCVolumeArray, color='red')
        axes[1][0].set_xticks(xLabels)

        axes[0][1].plot(x, ETHSellArray, color='red')
        axes[0][1].plot(x, ETHBuyArray, color='magenta')

        axes[0][1].plot(x, AVERAGE_USER_BUY_PRICE_ETH, color='green', linestyle='dashed')

        axes[0][1].set_xticks(xLabels)
        # axes[0][1].plot(x, ETHAverageArrayBuy, color='blue', linestyle='dashed')
        # axes[0][1].plot(x, ETHAverageArraySell, color='orange', linestyle='dashed')

        axes[1][1].bar(x, ETHVolumeArray, color='red')
        axes[1][1].set_xticks(xLabels)

        axes[0][2].plot(x, LSKSellArray, color='red', label='Sell' if i == 0 else "")
        axes[0][2].plot(x, LSKBuyArray, color='magenta', label='Buy' if i == 0 else "")

        # axes[0][2].plot(x, AVERAGE_USER_BUY_PRICE_LSK, color='magenta', linestyle='dashed' if i == 0 else "")

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
