import requests
import requests.exceptions
import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

#loop
t = 5

#collectingdata, collectingvolumen
x = "BTCPLN"
y = "LTCPLN"
z = "DASHPLN"
dat = [x, y, z]

#firstcalculating
vb = 0
vs = 0


def weight(a, b):
    if a > b:
        return a
    else:
        return b

def collectingdata():

        try:
            for i in dat:
                l = requests.get("https://bitbay.net/API/Public/" + i + "/orderbook.json").json()
                # print(l)

        except requests.HTTPError as error:
            print("Error:", error)



def collectingvolumen(time):

    for i in dat:
        l = requests.get("https://bitbay.net/API/Public/" + i + "/orderbook.json").json()
        # print(l)

        #timediff = dt.timedelta(0, time)
        now = datetime.now()
        then = now - timedelta(0, time)
        then -= timedelta(0, time) - timedelta(0, time)

        queue = {"from": int(then.timestamp()) * 1000, "to": int(now.timestamp()) * 1000}

        response = requests.request("GET", l, params = queue)
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

def loop():
        while 1:
            secbreak()
            time.sleep(t)
            print("Mineło %d sek" % (t))

if __name__=="__main__":


    #collectingdata()


    def secbreak():
        collectingdata()

        dict = requests.get("https://bitbay.net/API/Public/"+x+"/orderbook.json").json()
        bid1 = float(dict["bids"][0][0]) #Kupno
        ask1 = float(dict["asks"][0][0]) #Sprzedaż

        diff = float(((1 - (ask1 - bid1)) / ask1) * 100)
        print("Procentowa różnica między kupnem a sprzedażą to:", diff, "%")

        return bid1, ask1,
    secbreak()


    def plots(time):
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
        # Ether
        ETHSell = []
        ETHBuy = []
        ETHVolume = []
        ETHAverageSell = []
        ETHAverageBuy = []

        ETHDecrease = []
        ETHIncrease = []
        ETHRSI = []
        # Lisk
        LTCSell = []
        LTCBuy = []
        LTCVolume = []
        LTCAverageSell = []
        LTCAverageBuy = []

        LTCDecrease = []
        LTCIncrease = []
        LTCRSI = []

        plt.show()
        fig, axes = plt.subplots(2, 3, figsize=(10, 4))
        fig.tight_layout(pad=2.0)

        plt.xlabel("Time")
        axes[0][0].set_title(x)
        axes[0][1].set_title(y)
        axes[0][2].set_title(z)

        axes[1][0].set_title("Volume")
        axes[1][1].set_title("Volume")
        axes[1][2].set_title("Volume")

        axes[0][0].grid()
        axes[0][1].grid()
        axes[0][2].grid()

        while True:
            x.append(datetime.now().strftime("%H:%M:%S"))


            bBTC, sBTC, = secbreak()
            bETH, sETH, = secbreak()
            bLTC, sLTC, = secbreak()

            volumeBTC = collectingvolumen(time)
            volumeETH = collectingvolumen(time)
            volumeLCT = collectingvolumen(time)



            xLabels = x.copy()
            if len(xLabels) > 4:
                median = int(np.floor(np.median(np.arange(0, len(xLabels)))))
                xLabels = [xLabels[0], xLabels[median], xLabels[-1]]

            BTCSell.append(sBTC)
            BTCBuy.append(bBTC)
            BTCVolume.append(collectingvolumen(x, t))

            valueBuyB, valueSellB = firstcalculating(BTCSell, BTCBuy, len(dat))
            BTCAverageSell.append(valueSellB)
            BTCAverageBuy.append(valueBuyB)

            RSIB = calculateRSI(BTCDecrease, BTCIncrease, BTCSell, len(dat))
            BTCRSI.append(RSIB)

            ETHSell.append(sETH)
            ETHBuy.append(bETH)
            ETHVolume.append(collectingvolumen(y, t))

            valueBuyE, valueSellE = firstcalculating(ETHSell, ETHBuy, len(dat))
            ETHAverageSell.append(valueSellE)
            ETHAverageBuy.append(valueBuyE)

            RSIE = calculateRSI(ETHDecrease, ETHIncrease, ETHBuy, len(dat))
            ETHRSI.append(RSIE)

            LTCSell.append(sLTC)
            LTCBuy.append(bLTC)
            LTCVolume.append(collectingvolumen(z, t))

            valueBuy, valueSell = firstcalculating(LTCSell, LTCBuy, len(dat))
            LTCAverageSell.append(valueSell)
            LTCAverageBuy.append(valueBuy)

            RSI = calculateRSI(LTCDecrease, LTCIncrease, LTCSell, len(dat))
            LTCRSI.append(RSI)

            axes[0][0].plot(x, BTCSell, color='green')
            axes[0][0].plot(x, BTCBuy, color='magenta')
            axes[0][0].set_xticks(xLabels)
            axes[0][0].plot(x, BTCAverageBuy, color='blue', linestyle='dashed')
            axes[0][0].plot(x, BTCAverageSell, color='orange', linestyle='dashed')
            axes[0][0].plot(x, BTCRSI, color='red', linestyle='dashed')

            axes[1][0].bar(x, BTCVolume, color='green')
            axes[1][0].set_xticks(xLabels)

            axes[0][1].plot(x, ETHSell, color='green')
            axes[0][1].plot(x, ETHBuy, color='magenta')
            axes[0][1].set_xticks(xLabels)
            axes[0][1].plot(x, ETHAverageBuy, color='blue', linestyle='dashed')
            axes[0][1].plot(x, ETHAverageSell, color='orange', linestyle='dashed')
            axes[0][1].plot(x, ETHRSI, color='red', linestyle='dashed')

            axes[1][1].bar(x, ETHVolume, color='green')
            axes[1][1].set_xticks(xLabels)

            axes[0][2].plot(x, LTCSell, color='green', label='Sell' if i == 0 else "")
            axes[0][2].plot(x, LTCBuy, color='magenta', label='Buy' if i == 0 else "")
            axes[0][2].plot(x, LTCAverageBuy, color='blue', linestyle='dashed', label='Ave.Buy' if i == 0 else "")
            axes[0][2].plot(x, LTCAverageSell, color='orange', linestyle='dashed',
                            label='Ave.Sell' if i == 0 else "")
            axes[0][2].plot(x, LTCRSI, color='red', linestyle='dashed', label='RSI' if i == 0 else "")

            axes[0][2].set_xticks(xLabels)
            axes[0][2].legend(loc="upper right")

            axes[1][2].bar(x, LTCVolume, color='green')
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





plots(time)


