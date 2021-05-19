import requests
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

waluty = ['ZEC', 'LTC', 'DASH']
url1 = "https://bitbay.net/API/Public/"
url2 = "USD/ticker.json"


def downloadData(currency, url1, url2):
    url = url1 + currency + url2
    data = requests.get(url).json()
    return data['ask'], data['bid']


def plotData(plt1, plt2, plt3):
    ask_BTC, bid_BTC = downloadData(waluty[0], url1, url2)
    ask_LTC, bid_LTC = downloadData(waluty[1], url1, url2)
    ask_DASH, bid_DASH = downloadData(waluty[2], url1, url2)
    plt1.append(ask_BTC)
    plt1.append(bid_BTC)
    plt2.append(ask_LTC)
    plt2.append(bid_LTC)
    plt3.append(ask_DASH)
    plt3.append(bid_DASH)

    return plt1, plt2, plt3


def drawPlot(i):
    plt1_a, plt2_a, plt3_a = plotData(plt1, plt2, plt3,)
    plt.cla()
    plt.title("Wykres zmiany ask/bid wybranych kryptowalut")
    plt.plot(plt1_a[::2], label='ZEC_ask')
    plt.plot(plt1_a[1::2], label='ZEC_bid')
    plt.plot(plt2_a[::2], label='LTC_ask')
    plt.plot(plt2_a[1::2], label='LTC_bid')
    plt.plot(plt3_a[::2], label='DASH_ask')
    plt.plot(plt3_a[1::2], label='DASH_bid')
    plt.ylabel('Kryptowaluty - wartosc')
    plt.xlabel('Czas')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5))


if __name__ == "__main__":
    godzina = []
    plt1 = []
    plt2 = []
    plt3 = []
    animacja = FuncAnimation(plt.figure(), drawPlot, interval=5000)
    plt.show()
