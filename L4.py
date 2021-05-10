import requests
import requests.exceptions
import time
import matplotlib.pyplot as plt
import datetime as dt


T = 5
x = "BTCPLN"
y = "LTCPLN"
z = "DASHPLN"
dat = [x, y, z]
P = []
#timediff = dt.timedelta(0, time)gg

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

        timediff = dt.timedelta(0, time)
        now = dt.datetime.now()
        then = now - timediff
        then -= timediff - timediff

        queue = {"from": int(then.timestamp()) * 1000, "to": int(now.timestamp()) * 1000}

        response = requests.request("GET", l, params = queue)
        r = response.json()['items'][0]['a']

    return r



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

        ETHSell = []
        ETHBuy = []

        LTCSell = []
        LTCBuy = []

        plt.figure(figsize=(15, 8))

        plt.suptitle('Vertically stacked subplots')
        plt.plot(data, BTCSell, label='Sell BTC', color='green')
        plt.plot(data, BTCBuy, label='Buy BTC', color='grey')
        plt.plot(data, ETHSell, label='Sell ETH', color='yellow')
        plt.plot(data, ETHBuy, label='Buy ETH', color='green')
        plt.plot(data, LTCSell, label='Sell LSK', color='black')
        plt.plot(data, LTCBuy, label='Buy LSK', color='magenta')

        plt.legend()
        plt.title("Stock Plot")
        plt.xlabel("Time")
        plt.ylabel("Value")

        while True:
            data.append(dt.datetime.now())
            #plt.xticks(data, data, rotation= 45)

            bBTC, sBTC = secbreak()
            bETH, sETH = secbreak()
            bLTC, sLTC = secbreak()

            BTCSell.append(sBTC)
            BTCBuy.append(bBTC)

            ETHSell.append(sETH)
            ETHBuy.append(bETH)

            LTCSell.append(sLTC)
            LTCBuy.append(bLTC)

            plt.figure(figsize=(15, 8))
            plt.ylim(40000, weight(bBTC, sBTC) + 50000)

            plt.plot(data, BTCSell, color='green')
            plt.plot(data, BTCBuy, color='grey')
            plt.plot(data, ETHSell, color='green')
            plt.plot(data, ETHBuy, color='grey')
            plt.plot(data, LTCSell, color='green')
            plt.plot(data, LTCBuy, color='grey')


            #plt.draw()
            plt.pause(1e-17)
            time.sleep(5)





plots()

#if __name__=="__main__":

