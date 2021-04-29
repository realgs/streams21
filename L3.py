import requests
import requests.exceptions
import time
import matplotlib.pyplot as plt
import datetime


T = 5
x = "BTCPLN"
y = "LTCUSD"
z = "DASHUSD"
dat = [x, y, z]
P = []


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


def loop():
        while 1:
            secbreak()
            time.sleep(T)
            print("Mineło %d sek" % (T))

if __name__=="__main__":


    #collectingdata()


    def secbreak():
        collectingdata()

        dict = requests.get("https://bitbay.net/API/Public/"+x+"/orderbook.json").json()
        bid1 = float(dict["bids"][0][0]) #Kupno
        ask1 = float(dict["asks"][0][0]) #Sprzedaż
        diff = float(((1 - (ask1 - bid1)) / ask1) * 100)
        print("Procentowa różnica między kupnem a sprzedażą to:", diff, "%")

        return bid1, ask1
    secbreak()


    def plots():
        data = []


        BTCSell = []
        BTCBuy = []

        plt.show()
        axes = plt.gca()
        line1, = axes.plot(data, BTCSell, label='Sell BTC', color='green')
        line2, = axes.plot(data, BTCBuy, label='Buy BTC', color='grey')

        plt.legend()
        plt.title("Stock Plot")
        plt.xlabel("Time")
        plt.ylabel("Value")

        while True:
            data.append(datetime.datetime.now())

            bBTC, sBTC = secbreak()


            BTCSell.append(sBTC)
            BTCBuy.append(bBTC)

            axes.set_ylim(-10000, weight(bBTC, sBTC) + 50000)

            plt.plot(data, BTCSell, color='green')
            plt.plot(data, BTCBuy, color='grey')


            plt.draw()
            plt.pause(1e-17)
            time.sleep(5)

    plots()


#if __name__=="__main__":

