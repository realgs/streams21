import requests
import numpy as np
import matplotlib.pyplot as plt
from sys import exit

def connect(currency1, currency2):
    return f'https://bitbay.net/API/Public/{currency1}{currency2}/orderbook.json'


def calculate_diff(buy, sell):
    return round ( (1 - (sell - buy) / buy), 3 )


def get_values(currency1):
    try:
        req = requests.get(connect(currency1, "USD")).json()
        bid = req['bids']
        ask = req['asks']

    except Exception as e:
        print('ERROR:', e)
        return {}

    return bid, ask


def calc_rate(currency1):
    bids, asks = get_values ( currency1 )
    if len (bids) == 0:
        print("There is no value to show")
    elif len (asks) == 0:
        print("There is no value to show")
    else:
        bid = bids[0][0]
        ask = asks[0][0]
        diff = calculate_diff (bid, ask)
        print("The difference between bids and asks for", currency1, "equals", diff)
        return diff, bid, ask


def create_graph(currency1, interval):
    data1 = []
    data2 = []
    while True:
        lista1 = []
        lista2 = []
        for i in currency1:
            diff, ask, bid = calc_rate (i)
            lista1.append ([i, ask])
            lista2.append ([i, bid])
        data1.append(lista1)
        data2.append(lista2)
        generate_graph(data1, data2, interval)


def generate_graph(data1, data2, interval):
    plt.ion()

    t= np.arange (0,5 * (len (data1)),5)
    number=len(data1[0])

    for i in range (number):

        label1 = str (data1[0][i][0] + "asks")
        label2 = str (data1[0][i][0] + "bids")
        y1 = []
        y2 = []

        for j in data1:
            y1.append (j[i][1])

        for j in data2:
            y2.append ( j[i][1] )

        plt.plot (t, y1, "--o", label=label1)
        plt.plot (t, y2, "--*", label=label2)

    plt.legend (bbox_to_anchor=(1.04, 1), borderaxespad=0)
    plt.xlabel ("bids/ asks")
    plt.ylabel ("time")
    plt.xlim ([-0.1, t[-1] + 1])
    plt.yscale ('log')
    plt.draw ()
    plt.pause (interval)


def animation():
    anim = FuncAnimation (plt.figure (), make_plot, interval=5000)
    plt.show ()


if __name__ == '__main__':
    interval = 5
    currency1 = ["BTC", "LTC", "ETH"]
    currency2 = "USD"

    while True:
        try:
            create_graph (currency1, interval)
            animation ()

        except KeyboardInterrupt:
            print ("Error due to user interuption")
            exit ()