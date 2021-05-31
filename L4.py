import requests
import sys
import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

#main
t = 5

#main
x1 = "PLN"
y1 = "BTC"
y2 = "ETH"
y3 = "LTC"
daty = [y1, y2, y3]




def calculate(buy, sell):
    o = round((1 - (sell - buy) / buy), 3)
    print(str(o) + " %")


def theGreatest(array):
    Lmax = max(array)
    return Lmax

def get_volume(firstCurrancy, secondCurrancy, time):
    url = f"https://api.bitbay.net/rest/trading/transactions/{firstCurrancy}-{secondCurrancy}"

    #timediff = dt.timedelta(0, time)
    now = datetime.now()
    before = now - timedelta(0, time)
    before -= timedelta(0, time) - timedelta(0, time)
    querystring = {"from": int(before.timestamp()) * 1000, "to": int(now.timestamp()) * 1000}


    response = requests.request("GET", url, params=querystring)
    r = response.json()['items'][0]['a']

    return r

def firstcalculating(Sell, Buy, Samples):
    vb = 0
    vs = 0

    if len(Buy) > Samples:
        for items in range(Samples):
            vb += Buy[len(Buy) - items - 1]
        vb /= Samples

    else:
        for items in range(len(Buy)):
            vb += Buy[items]
        vb /= Samples


    if len(Sell) > Samples:
        for items in range(Samples):
            vs += Sell[len(Sell) - items - 1]
        vs /= Samples

    else:
        for items in range(len(Sell)):
            vs += Sell[items]
        vs /= Samples

    return vs, vb

def calculateRSI(Decrease, Increase, Buy, Sample):

    if len(Buy) > Sample:
        value = Buy[len(Buy)-1] - Buy[len(Buy)-Sample]

        if value > 0:
            Increase.append(value)

        else:
            Decrease.append(value)

        a = (sum(Increase) + 1) / (len(Increase) + 1)
        b = (sum(Decrease) + 1) / (len(Decrease) + 1)

    else:
        a = 1
        b = 1
    RSI = 100 - (100 / (1 + (a + 1/b + 1)))

    return RSI

def getCurrencyData(firstCurrency,secondCurrency, Category):

    url = f"https://bitbay.net/API/Public/{firstCurrency}{secondCurrency}/{Category}.json"

    response = requests.get(url)


    if response.status_code == 200:
        print(f"{firstCurrency}:")
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

    BTCSell = []
    BTCBuy = []
    BTCVolume = []
    BTCAverageSell = []
    BTCAverageBuy = []

    BTCDecrease = []
    BTCIncrease = []
    BTCRSI = []

    ETHSell = []
    ETHBuy = []
    ETHVolume = []
    ETHAverageSell = []
    ETHAverageBuy = []

    ETHDecrease = []
    ETHIncrease = []
    ETHRSI = []

    LTCSell = []
    LTCBuy = []
    LTCVolume = []
    LTCAverageSell = []
    LTCAverageBuy = []

    LTCDecrease = []
    LTCIncrease = []
    LTCRSI = []

    plt.show()
    fig, ax1 = plt.subplots(2, 3, figsize=(17, 6), squeeze=False)
    fig.tight_layout(pad=2.0)

    ax20 = ax1[0][0].twinx()
    ax21 = ax1[0][1].twinx()
    ax22 = ax1[0][2].twinx()

    plt.xlabel("Time")
    ax1[0][0].set_title(y1)
    ax1[0][1].set_title(y2)
    ax1[0][2].set_title(y3)

    ax1[1][0].set_title("Volume")
    ax1[1][1].set_title("Volume")
    ax1[1][2].set_title("Volume")

    ax1[0][0].grid()
    ax1[0][1].grid()
    ax1[0][2].grid()

    while True:
        x.append(datetime.now().strftime("%H:%M:%S"))
        buyBTC, sellBTC, volumeBTC = getCurrencyData(y1, x1, "ticker")
        buyETH, sellETH, volumeETH = getCurrencyData(y2, x1, "ticker")
        buyLTC, sellLTC, volumeLTC = getCurrencyData(y3, x1, "ticker")

        xLabels = x.copy()
        if len(xLabels) > 4:
            median = int(np.floor(np.median(np.arange(0, len(xLabels)))))
            xLabels = [xLabels[0], xLabels[median], xLabels[-1]]

        BTCSell.append(sellBTC)
        BTCBuy.append(buyBTC)
        BTCVolume.append(get_volume(y1, x1, t))

        valueBuyB, valueSellB = firstcalculating(BTCSell, BTCBuy, len(daty))
        BTCAverageSell.append(valueSellB)
        BTCAverageBuy.append(valueBuyB)

        RSIB = calculateRSI(BTCDecrease, BTCIncrease, BTCSell, len(daty))
        BTCRSI.append(RSIB)



        ETHSell.append(sellETH)
        ETHBuy.append(buyETH)
        ETHVolume.append(get_volume(y2, x1, t))

        valueBuyE, valueSellE = firstcalculating(ETHSell, ETHBuy, len(daty))
        ETHAverageSell.append(valueSellE)
        ETHAverageBuy.append(valueBuyE)

        RSIE = calculateRSI(ETHDecrease, ETHIncrease, ETHBuy, len(daty))
        ETHRSI.append(RSIE)



        LTCSell.append(sellLTC)
        LTCBuy.append(buyLTC)
        LTCVolume.append(get_volume(y3, x1, t))

        valueBuy, valueSell = firstcalculating(LTCSell, LTCBuy, len(daty))
        LTCAverageSell.append(valueSell)
        LTCAverageBuy.append(valueBuy)

        RSI = calculateRSI(LTCDecrease, LTCIncrease, LTCSell, len(daty))
        LTCRSI.append(RSI)

        ax1[0][0].plot(x, BTCSell, color='green')
        ax1[0][0].plot(x, BTCBuy, color='grey')
        ax1[0][0].set_xticks(xLabels)
        ax1[0][0].plot(x, BTCAverageBuy, color='#59981A', linestyle = '--')
        ax1[0][0].plot(x, BTCAverageSell, color='black', linestyle = '--')
        #ax1[0][0].plot(x, BTCRSI, color='red', linestyle = '--')
        ax20.plot(x, BTCRSI, color ='red', linestyle = '--')


        ax1[1][0].bar(x, BTCVolume, color='green')
        ax1[1][0].set_xticks(xLabels)

        ax1[0][1].plot(x, ETHSell, color='green')
        ax1[0][1].plot(x, ETHBuy, color='grey')
        ax1[0][1].set_xticks(xLabels)
        ax1[0][1].plot(x, ETHAverageBuy, color='#59981A', linestyle = '--')
        ax1[0][1].plot(x, ETHAverageSell, color='black', linestyle = '--')
        #ax1[0][1].plot(x, ETHRSI, color='red', linestyle = '--')
        ax21.plot(x, ETHRSI, color ='red', linestyle = '--')

        ax1[1][1].bar(x, ETHVolume, color='green')
        ax1[1][1].set_xticks(xLabels)

        ax1[0][2].plot(x, LTCSell, color='green', label='Sell' if i == 0 else "")
        ax1[0][2].plot(x, LTCBuy, color='grey', label='Buy' if i == 0 else "")
        ax1[0][2].plot(x, LTCAverageBuy, color='#59981A', linestyle = '--', label='Ave.Buy' if i == 0 else "")
        ax1[0][2].plot(x, LTCAverageSell, color='black', linestyle = '--', label='Ave.Sell' if i == 0 else "")
        #ax1[0][2].plot(x, LTCRSI, color='red', linestyle = '--', label='RSI' if i == 0 else "")
        ax22.plot(x, LTCRSI, color='red', linestyle = '--',label = 'RSI' if i == 0 else "")

        ax1[0][2].set_xticks(xLabels)
        ax1[0][2].legend(loc="upper right")
        ax22.legend(loc="lower right")
        ax1[1][2].bar(x, LTCVolume, color='green')
        ax1[1][2].set_xticks(xLabels)

        ax20.set_ylabel('RSI',color='red')
        ax21.set_ylabel('RSI',color='red')
        ax22.set_ylabel('RSI',color='red')


        i += 1
        plt.draw()

        plt.pause(1e-17)
        time.sleep(5)