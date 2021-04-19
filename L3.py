import requests
import numpy as np
import matplotlib.pyplot as plt


def connect(currency1, currency2):
    return f'https://bitbay.net/API/Public/{currency1}{currency2}/orderbook.json'

def calculate_diff(buy, sell):
    return round ( (1 - (sell - buy) / buy), 3 )

def get_values(currency1):
    try:
        req = requests.get (connect(currency1, "USD")).json()
        bid = req['bids']
        ask = req['asks']

    except Exception as e:
        print('ERROR:', e)
        return {}

    return bid, ask

def calc_rate(currency1):

    bids, asks = get_values (currency1)
    if len (bids) == 0:
        print("There is no value to show")
    elif len (asks) == 0:
        print("There is no value to show")
    else:
        bid = bids[0][0]
        ask = asks[0][0]
        diff = calculate_diff (bid, ask)
        print("The difference between bids and asks for", currency1, "equals", diff)
        return diff

def create_graph(currency1, currency2, interval):

    data = []
    while True:
        lista = []
        for i in currency1:
            lista.append ([i + currency2, calc_rate (i)])
        data.append (lista)
        generate_graph (data, interval)

def generate_graph(data, interval):

    plt.ion ()
    t = np.arange (0,5 *(len(data)), 5)
    number = len(data[0])

    for i in range (number):
        y = []
        for j in data:
            y.append (j[i][1])
        plt.plot (t, y, "--*", label=data[0][i][0])

    plt.legend ()
    plt.xlabel ("time")
    plt.ylabel ("difference")
    plt.xlim ([-0.1, t[-1] + 1])
    plt.draw ()
    plt.pause (interval)
    plt.clf ()

if __name__ == '__main__':
    interval = 5
    currency1 = ["BTC", "LTC", "ETH"]
    currency2 = "USD"
    create_graph (currency1, currency2, interval)
