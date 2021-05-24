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
first_currency = "BTC"
second_currency = "ETH"
third_currency = "LSK"
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

def get_volume(fromCurrancy, toCurrancy, time):
    url = f"https://api.bitbay.net/rest/trading/transactions/{fromCurrancy}-{toCurrancy}"

    now = datetime.now()
    before = int((now - timedelta(0, time)).timestamp()) * 1000
    querystring = {"from": before}

    try:
        response = requests.request("GET", url, params=querystring)
        a = float(response.json()['items'][0]['a'])
    except:
        a = 0
    return a

def average_calculate(arraySell, arrayBuy, samplesNumber):
    BuyValue = 0
    SellValue = 0
    if len(arrayBuy) > samplesNumber:
        for items in range(samplesNumber):
            BuyValue += arrayBuy[len(arrayBuy)-items-1]
        BuyValue /= samplesNumber
    else:
        for items in range(len(arrayBuy)):
            BuyValue += arrayBuy[items]
        BuyValue /= samplesNumber

    if len(arraySell) > samplesNumber:
        for items in range(samplesNumber):
            SellValue += arraySell[len(arraySell)-items-1]
        SellValue /= samplesNumber
    else:
        for items in range(len(arraySell)):
            SellValue += arraySell[items]
        SellValue /= samplesNumber
    return SellValue, BuyValue

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

def checkWhatTrend(RSIArray):
    PointsDownTrend = []
    PointsUpTrend = []

    for items in range(1, len(RSIArray) - 1):
        if (RSIArray[items - 1] > RSIArray[items]) and (RSIArray[items] < RSIArray[items + 1]):
            PointsDownTrend.append(items)
        else:
            PointsDownTrend.append(0)

        if (RSIArray[items - 1] < RSIArray[items]) and (RSIArray[items] > RSIArray[items + 1]):
            PointsUpTrend.append(items)
        else:
            PointsUpTrend.append(0)

    # trend spadkowy
    if (PointsDownTrend[len(PointsDownTrend) - 1] < PointsDownTrend[len(PointsDownTrend) - 2]) and \
            (PointsDownTrend[len(PointsDownTrend) - 1] != 0 and PointsDownTrend[len(PointsDownTrend) - 2] != 0):
        print("spadek")
        return "Trend spadkowy"
    # trend wzrostowy
    elif (PointsUpTrend[len(PointsUpTrend) - 1] > PointsUpTrend[len(PointsUpTrend) - 2]) and \
            (PointsUpTrend[len(PointsUpTrend) - 1] != 0 and PointsUpTrend[len(PointsUpTrend) - 2] != 0):
        print("wzrost")
        return "Trend wzrostowy"
    # trend boczny
    elif ((PointsUpTrend[len(PointsUpTrend) - 1] == PointsUpTrend[len(PointsUpTrend) - 2]) or (PointsDownTrend[len(PointsDownTrend) - 1] == PointsDownTrend[len(PointsDownTrend) - 2])) \
            and (PointsUpTrend[len(PointsUpTrend) - 1] != 0 and PointsUpTrend[len(PointsUpTrend) - 2] != 0) \
            and (PointsDownTrend[len(PointsDownTrend) - 1] != 0 and PointsDownTrend[len(PointsDownTrend) - 2] != 0):
        print("boczny")
        return "Trend boczny"
    else:
        print("Za mało danych do zdefiniowania trendu")
        return "Za mało danych do zdefiniowania trendu"

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

    if BTCTrend[len(BTCTrend) - 1] != "Trend spadkowy":
        BTC = True
    if ETHTrend[len(ETHTrend) - 1] != "Trend spadkowy":
        ETH = True
    if LSKTrend[len(LSKTrend) - 1] != "Trend spadkowy":
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
    print(f'Naszym kandydatem jest: {max}')
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
    if Y > len(samplesArray):
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
    fig, axes = plt.subplots(2, 3, figsize=(15, 7), squeeze=False)
    fig.tight_layout(pad=2.0)

    ax20 = axes[0][0].twinx()
    ax21 = axes[0][1].twinx()
    ax22 = axes[0][2].twinx()

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

        if len(LSKRSIArray) > 3 and len(ETHRSIArray) > 3 and len(BTCRSIArray) > 3:
            trendB = checkWhatTrend(BTCRSIArray)
            BTCTrendArray.append(trendB)
            axes[0][0].set_title(f'{first_currency}|Trend: {trendB}')

            trendE = checkWhatTrend(ETHRSIArray)
            ETHTrendArray.append(trendE)
            axes[0][1].set_title(f'{second_currency}|Trend: {trendE}')

            trendL = checkWhatTrend(LSKRSIArray)
            LSKTrendArray.append(trendL)
            axes[0][2].set_title(f'{third_currency}|Trend: {trendL}')

            out = defineCandidate(trendB, trendE, trendL, BTCVolumeArray, ETHVolumeArray, LSKVolumeArray)
            if out == "BTC":
                axes[0][0].set_title(f'{first_currency}|Trend: {trendB} [K]')
                if defineAsLiquid(buyBTC, sellBTC, 5):
                    axes[0][0].set_title(f'{first_currency}|Trend: {trendB} [K][L]')
                if defineAsVolatile(BTCBuyArray, Y, X):
                    axes[0][0].set_title(f'{first_currency}|Trend: {trendB} [K][L][V]')
            elif out == "ETH":
                axes[0][1].set_title(f'{second_currency}|Trend: {trendE} [K]')
                if defineAsLiquid(buyETH, sellETH, 5):
                    axes[0][1].set_title(f'{second_currency}|Trend: {trendE} [K][L]')
                if defineAsVolatile(ETHBuyArray, Y, X):
                    axes[0][1].set_title(f'{second_currency}|Trend: {trendE} [K][L][V]')
            else:
                axes[0][2].set_title(f'{third_currency}|Trend: {trendL} [K]')
                if defineAsLiquid(buyLSK, sellLSK, 5):
                    axes[0][2].set_title(f'{third_currency}|Trend: {trendL} [K][L]')
                if defineAsVolatile(LSKBuyArray, Y, X):
                    axes[0][1].set_title(f'{third_currency}|Trend: {trendL} [K][L][V]')

        axes[0][0].plot(x, BTCSellArray, color='green')
        axes[0][0].plot(x, BTCBuyArray, color='magenta')
        axes[0][0].set_xticks(xLabels)
        axes[0][0].plot(x, BTCAverageArrayBuy, color='blue', linestyle='dashed')
        axes[0][0].plot(x, BTCAverageArraySell, color='orange', linestyle='dashed')
        ax20.plot(x, BTCRSIArray, color ='red', linestyle='dashed')


        axes[1][0].bar(x, BTCVolumeArray, color='green')
        axes[1][0].set_xticks(xLabels)

        axes[0][1].plot(x, ETHSellArray, color='green')
        axes[0][1].plot(x, ETHBuyArray, color='magenta')
        axes[0][1].set_xticks(xLabels)
        axes[0][1].plot(x, ETHAverageArrayBuy, color='blue', linestyle='dashed')
        axes[0][1].plot(x, ETHAverageArraySell, color='orange', linestyle='dashed')
        ax21.plot(x, ETHRSIArray, color ='red', linestyle='dashed')

        axes[1][1].bar(x, ETHVolumeArray, color='green')
        axes[1][1].set_xticks(xLabels)

        axes[0][2].plot(x, LSKSellArray, color='green', label='Sell' if i == 0 else "")
        axes[0][2].plot(x, LSKBuyArray, color='magenta', label='Buy' if i == 0 else "")
        axes[0][2].plot(x, LSKAverageArrayBuy, color='blue', linestyle='dashed', label='Ave.Buy' if i == 0 else "")
        axes[0][2].plot(x, LSKAverageArraySell, color='orange', linestyle='dashed', label='Ave.Sell' if i == 0 else "")
        ax22.plot(x, LSKRSIArray, color='red', linestyle='dashed',label='RSI')

        axes[0][2].set_xticks(xLabels)
        axes[0][2].legend(loc="upper right")

        axes[1][2].bar(x, LSKVolumeArray, color='green')
        axes[1][2].set_xticks(xLabels)

        ax20.set_ylabel('RSI',color='red')
        ax21.set_ylabel('RSI',color='red')
        ax22.set_ylabel('RSI',color='red')


        i += 1
        plt.draw()
        plt.waitforbuttonpress()
        plt.pause(1e-17)
        time.sleep(5)
