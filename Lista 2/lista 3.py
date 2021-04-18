import time

import numpy as np
import requests
from requests.exceptions import HTTPError
import matplotlib.pyplot as plt


def get_data(currency_l, url_l):
    try:
        response = requests.get(url=url_l + f'{currency_l}{"USD"}/{"trades"}.json')
        return response.json()
    except HTTPError:
        print('HTTP error:', HTTPError)
        return []


def import_values(currency_l, buy_prices_l, sell_prices_l, url_l, index_l):
    print(currency_l)

    new_data = []
    new_data += get_data(currency_l, url_l)

    if new_data:
        for data_row in new_data:
            if data_row["type"] == "buy":
                buy_prices_l[index_l].append(data_row["price"])
            elif data_row["type"] == "sell":
                sell_prices_l[index_l].append(data_row["price"])


def draw_values(currency_l, buy_prices_l, sell_prices_l, plt_l, index_l):
    values_amount = min(len(buy_prices_l[index_l]), len(sell_prices_l[index_l]))

    x = range(values_amount)
    y1_np = np.array(buy_prices_l[index_l])
    y2_np = np.array(sell_prices_l[index_l])
    y1 = y1_np[0:values_amount]
    y2 = y2_np[0:values_amount]

    plt.subplot(3, 1, index_l + 1)
    plt_l.plot(x, y1, label="Buy price " + currency_l)
    plt_l.plot(x, y2, label="Sell price " + currency_l)
    plt_l.title(currency_l)

    plt_l.legend(loc='upper left')
    plt_l.draw()


if __name__ == "__main__":
    currencies = ["BTC", "LTC", "DASH"]
    buy_prices = [[], [], []]
    sell_prices = [[], [], []]
    URL = f'https://bitbay.net/API/Public/'

    plt.ion()
    plt.show()

    while True:
        for currency in currencies:
            import_values(currency, buy_prices, sell_prices, URL, currencies.index(currency))
            draw_values(currency, buy_prices, sell_prices, plt, currencies.index(currency))

        plt.pause(0.0001)
        plt.clf()
        time.sleep(5)
