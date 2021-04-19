import matplotlib.pyplot as plt
import requests
from matplotlib.animation import FuncAnimation


url_1 = 'https://bitbay.net/API/Public/'
url_2 = '/ticker.json'
base = 'USD'
currencies = ['BCC', 'LTC', 'DASH']
frequency = 5


def data(currency):
    url = url_1 + currency + base + url_2
    response = requests.get(url).json()
    return response["ask"], response["bid"]


def plot_data(plot_1, plot_2, plot_3):
    ask_BTC, bid_BTC = data(currencies[0])
    ask_LTC, bid_LTC = data(currencies[1])
    ask_DASH, bid_DASH = data(currencies[2])
    plot_1.append(ask_BTC)
    plot_1.append(bid_BTC)
    plot_2.append(ask_LTC)
    plot_2.append(bid_LTC)
    plot_3.append(ask_DASH)
    plot_3.append(bid_DASH)

    return plot_1, plot_2, plot_3


def draw(a):
    plot1, plot2, plot3 = plot_data(plot_1, plot_2, plot_3)
    plt.cla()
    plt.title("Wykres ask i bid od czasu")
    plt.plot(plot1[::2], label='BCC ask')
    plt.plot(plot1[1::2], label='BCC bid')
    plt.plot(plot2[::2], label='LTC ask')
    plt.plot(plot2[1::2], label='LTC bid')
    plt.plot(plot3[::2], label='DASH ask')
    plt.plot(plot3[1::2], label='DASH bid')
    plt.ylabel('Kryptowaluty - wartosc')
    plt.xlabel('Czas')
    plt.legend(loc='upper right')


if __name__ == "__main__":
    plot_1 = []
    plot_2 = []
    plot_3 = []
    animation = FuncAnimation(plt.figure(), draw, interval=500)
    plt.show()

