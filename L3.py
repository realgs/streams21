import requests
import time
import sys
import urllib.request
import matplotlib.pyplot as plt
import datetime

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

def getCurrencyData(currency, category):
    connect()
    url = f"https://bitbay.net/API/Public/{currency}/{category}.json"
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
        calculate(buy_price, sell_price)
        return buy_price, sell_price
    else:
        print("Error when trying to fetch")
        sys.exit()

if __name__ == "__main__":
    x = []

    BTCSellArray = []
    BTCBuyArray = []

    ETHSellArray = []
    ETHBuyArray = []

    LTCSellArray = []
    LTCBuyArray = []

    plt.show()
    axes = plt.gca()
    line1, = axes.plot(x, BTCSellArray, label='Sell BTC', color='red')
    line2, = axes.plot(x, BTCBuyArray, label='Buy BTC', color='blue')
    line3, = axes.plot(x, ETHSellArray, label='Sell ETH', color='yellow')
    line4, = axes.plot(x, ETHBuyArray, label='Buy ETH', color='green')
    line5, = axes.plot(x, LTCSellArray, label='Sell LSK', color='black')
    line6, = axes.plot(x, LTCBuyArray, label='Buy LSK', color='magenta')
    plt.legend()
    plt.title("Finance Plot")
    plt.xlabel("Time")
    plt.ylabel("Data/Money")

    while True:
        x.append(datetime.datetime.now())

        buyBTC, sellBTC = getCurrencyData("BTC", "ticker")
        buyETH, sellETH = getCurrencyData("ETH", "ticker")
        buyLTC, sellLTC = getCurrencyData("LTC", "ticker")

        BTCSellArray.append(sellBTC)
        BTCBuyArray.append(buyBTC)

        ETHSellArray.append(sellETH)
        ETHBuyArray.append(buyETH)

        LTCSellArray.append(sellLTC)
        LTCBuyArray.append(buyLTC)

        axes.set_ylim(-10000, theGreatest(buyBTC, sellBTC) + 5000)

        plt.plot(x, BTCSellArray, 'r')
        plt.plot(x, BTCBuyArray, 'b')
        plt.plot(x, ETHSellArray, 'y')
        plt.plot(x, ETHBuyArray, 'g')
        plt.plot(x, LTCSellArray, 'k')
        plt.plot(x, LTCBuyArray, 'm')

        plt.draw()
        plt.pause(1e-17)
        time.sleep(5)
