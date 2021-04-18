import requests
import sys
from datetime import datetime
import matplotlib.pyplot as plt


def diff(purchase, sale):
    return round(((1 - (sale[0][0] - purchase[0][0])/purchase[0][0])*100), 2)


def get_data(currency, p_currency):
    try:
        response = requests.get(f"https://bitbay.net/API/Public/{currency}{p_currency}/orderbook.json")
        response_json = response.json()
        bids = response_json['bids']
        asks = response_json['asks']

        # print(f"{currency}:\n "
        #       f"Purchase price: {bids[0][0]},\n"
        #       f"Selling price: {asks[0][0]},\n "
        #       f"Difference between purchase and selling price: {diff(bids, asks)} %")
        return bids, asks

    except requests.exceptions.HTTPError:
        print("No connection to the server.")
        sys.exit()


def plot(currencies, data, times, k):

    plots = len(data[0])
    for p in range(plots):
        y = []

        for d in data:
            y.append(d[p][1])
            x = [i for i in range(len(y))]
        l = max(0, len(x)-20)
        r = (len(x))
        plt.plot(x, y, "-", label=currencies[p])

    plt.legend()
    plt.xticks(ticks=x, labels=times, rotation=50)
    plt.xlabel("Time")
    plt.ylabel("Bids-asks difference [%]")
    plt.xlim(left=l, right=r)
    plt.pause(k)
    plt.clf()


def plot_data(currencies, p_currency, k):
    data = []
    times = []
    while True:
        d = []
        for currency in currencies:
            bids, asks = get_data(currency, p_currency)
            d.append([currency, diff(bids, asks)])

        data.append(d)
        times.append(datetime.now().strftime("%H:%M:%S"))

        print(data)
        print(times)

        plot(currencies, data, times, k)
