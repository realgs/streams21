import requests
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

currency= ['BTC-USD', 'ETH-USD', 'LTC-USD']
BIT_URL = "https://bitbay.net/API/Public/Place_Holder/ticker.json"
Interwal=5000

def get_value(currency):
    url = BIT_URL.replace('Place_Holder', currency)
    data = requests.get(url).json()
    return data['ask'], data['bid']

def intial_plot(plt1, plt2, plt3):
    ask_1, bid_1 = get_value(currency[0])
    ask_2, bid_2 = get_value(currency[1])
    ask_3, bid_3 = get_value(currency[2])
    plt1.append(ask_1)
    plt1.append(bid_1)
    plt2.append(ask_2)
    plt2.append(bid_2)
    plt3.append(ask_3)
    plt3.append(bid_3)

    return plt1, plt2, plt3


def plots(i):

    plt1_a, plt2_a, plt3_a = intial_plot(plt1, plt2, plt3,)
    plt.cla()
    plt.title("Cryptos on one graf")
    plt.plot(plt1_a[::2], label=currency[0]+'/ask')
    plt.plot(plt1_a[1::2], label=currency[0]+'/bid')
    plt.plot(plt2_a[::2], label=currency[1]+'/ask')
    plt.plot(plt2_a[1::2], label=currency[1]+'/bid')
    plt.plot(plt3_a[::2], label=currency[2]+'/ask')
    plt.plot(plt3_a[1::2], label=currency[2]+'/bid')
    plt.ylabel('value')
    plt.xlabel('Time')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5))





if __name__ == "__main__":
    plt1 = []
    plt2 = []
    plt3 = []
    animacja = FuncAnimation(plt.figure(), plots, Interwal)
    plt.show()