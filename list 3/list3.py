import requests
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

URL = "https://api.bitbay.net/rest/trading/orderbook/"
FIRST_POSITION = 0
FIFE = 5
CURRENCY = ["ZEC-USD", "LTC-USD", "DASH-USD"]

ZEC_buy = []
ZEC_sell = []
LTC_buy = []
LTC_sell = []
DASH_buy = []
DASH_sell = []
t = []


def get_data(currency):
    temp_url = URL + currency
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", temp_url, headers=headers).json()

    try:
        buy = float(response['buy'][FIRST_POSITION]['ra'])
        sell = float(response['sell'][FIRST_POSITION]['ra'])
    except ValueError:
        print(">>> ValueError: could not convert string to float ")

    return buy, sell


def add_data(currency, buy_list, sell_list):
    buy, sell = get_data(currency)
    buy_list.append(buy)
    sell_list.append(sell)
    return buy_list, sell_list


def make_plot(a):
    y1, y2 = add_data(CURRENCY[0], ZEC_buy, ZEC_sell)
    y3, y4 = add_data(CURRENCY[1], LTC_buy, LTC_sell)
    y5, y6 = add_data(CURRENCY[2], DASH_buy, DASH_sell)
    t.append(time.strftime("%H:%M:%S", time.localtime()))
    plt.clf()
    plt.title("Wykres notowań kursu")
    plt.plot(t, y1, label="ZEC buy", color="blue")
    plt.plot(t, y2, label="ZEC sell", color="yellow")
    plt.plot(t, y3, label="LTC buy", color="red")
    plt.plot(t, y4, label="LTC sell", color="green")
    plt.plot(t, y5, label="DASH buy", color="pink")
    plt.plot(t, y6, label="DASH sell", color="grey")
    plt.xlabel("Czas")
    plt.ylabel("Kurs")
    plt.xticks(rotation='vertical')
    plt.subplots_adjust(bottom=0.2)
    plt.legend(loc="upper right")


def main():
    animation = FuncAnimation(plt.figure(), make_plot, interval=5000)
    plt.show()


if __name__ == '__main__':
    main()
