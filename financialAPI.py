import time
import requests
from requests.exceptions import HTTPError
import matplotlib.pyplot as plt


data_currency = {
    "BTC": [],
    "LTC": [],
    "DASH": [],
}


def data(lines):
    currency_1 = ['BTC', 'LTC', 'DASH']
    currency_2 = 'USD'
    category = 'orderbook'
    iterator = 0
    while True:
        iterator += 1
        for c in currency_1:
            data = download_data(c, currency_2, category)
            if data is not None:
                diffrence = calculate(data, c)
        create_graph(iterator, lines)
        time.sleep(5)
    return diffrence


def download_data(currency_1, currency_2, category):
    try:
        response = requests.get(url=f'https://bitbay.net/API/Public/{currency_1}{currency_2}/{category}.json')
        data = response.json()
    except HTTPError:
        print('HTTP error:', HTTPError)
        return None
    return data


def calculate(data, currency_1):
    buy = data['bids'][0][0]
    sell = data['asks'][0][0]
    procenty = (1-(sell-buy)/sell) * 100
    t = time.strftime("%H:%M:%S", time.localtime())
    diffrence = {
        'buy_price': data['bids'][0][0],
        'sell_price': data['asks'][0][0],
        'procents': procenty,
        'time': str(t),
    }

    data_currency[f"{currency_1}"].append(diffrence)
    print(diffrence)
    return diffrence


def create_graph(iterator, lines):

    for c, l in lines.items():
        data = data_currency[c][0:iterator]
        buy = []
        sell = []
        t = []
        for i in range(len(data)):
            buy.append(data[i]["buy_price"])
            sell.append(data[i]["sell_price"])
            tim = data[i]["time"]
            t.append(i+1)

        l[0].set_data(t, buy)
        l[1].set_data(t, sell)
        plts[c].set_xticklabels(tim, rotation='horizontal', fontsize=7)
        plts[c].set_xlim([max(iterator-8, 1), iterator+3])
        plts[c].set_ylim([min(buy)*0.95, max(sell)*1.05])

    plt.draw()
    plt.pause(1e-17)


if __name__ == "__main__":

    plt.ion()

    plts = {}
    lines = {}

    fig = plt.figure()

    itr = 1
    for c in data_currency.keys():
        plts[c] = fig.add_subplot(len(data_currency), 1, itr)
        buy_line, = plts[c].plot([0], [0])
        sell_line, = plts[c].plot([0], [0])
        lines[c] = [buy_line, sell_line]

        plts[c].set_ylim([1, 5])
        plts[c].set_title(f"{c} - USD")

        plts[c].set_xlabel("time")
        plts[c].set_ylabel("value")

        itr += 1

    fig.tight_layout(h_pad=0.5)

    data(lines)
