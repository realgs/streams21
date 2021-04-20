import requests
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as anim


def get_data(currency, p_currency):
    try:
        response = requests.get(f"https://bitbay.net/API/Public/{currency}{p_currency}/orderbook.json")
        response_json = response.json()
        bids = response_json['bids']
        asks = response_json['asks']

        return bids, asks

    except requests.exceptions.HTTPError:
        print("No connection to the server.")
        sys.exit()


def plot(currencies, bid, ask, times, k):

    for p in range(len(currencies)):
        y1 = []
        y2 = []
        for b in bid:
            y1.append(b[p][1])
        for a in ask:
            y2.append(a[p][1])
            x = [i for i in range(len(y1))]

        print(y1)
        print(y2)
        l = max(0, len(x)-20)
        r = (len(x))

        plt.subplot(len(currencies), 1, p+1)
        plt.plot(x, y2, "-", label=f"Asks of {currencies[p]}", color="#9467bd")
        plt.plot(x, y1, "-", label=f"Bids of {currencies[p]}", color="#1f77b4")

        plt.legend()
        plt.xticks(ticks=x, labels=times, rotation=50)
        plt.xlabel("Time")
        plt.ylabel(f"Bids, asks {currencies[p]} values [PLN]")
        plt.xlim(left=l, right=r)
    plt.tight_layout()
    plt.pause(k)
    plt.clf()


def plot_data(currencies, p_currency, k):
    bid = []
    ask = []
    times = []


    plt.subplots(nrows=len(currencies), figsize=(10, len(currencies) * 3.5))

    while True:
        b = []
        a = []
        for currency in currencies:
            bids, asks = get_data(currency, p_currency)
            b.append([currency, bids[0][0]])
            a.append([currency, asks[0][0]])

        bid.append(b)
        ask.append(a)
        times.append(datetime.now().strftime("%H:%M:%S"))
        # print(bid)
        # print(ask)
        # print(times)
        plot(currencies, bid, ask, times, k)


def main():
    currencies = ['BTC', 'ETH', 'DOT']
    p_currency = 'PLN'
    k = 0.5
    plot_data(currencies, p_currency, k)


if __name__ == '__main__':
    main()