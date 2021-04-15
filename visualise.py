import requests as r
from time import sleep
from matplotlib import pyplot as plt
from requests.exceptions import HTTPError
from datetime import datetime
from matplotlib.animation import FuncAnimation

SLEEP_VALUE = 1


def add_currency_to_currencies(currencies, currency):
    result = []
    for c in currencies:
        result.append(c+currency)
    return result


def download_data(currency, caregory):
    URL = f'https://bitbay.net/API/Public/{currency}/{category}.json'
    try:
        response = r.get(URL)
        response.raise_for_status()

    except HTTPError:
        print(f'Error: : {HTTPError}')

    else:
        return response.json()
    return r.get(URL).json()


def fetchFromAPI(currencies, category):
    result = []
    for currency in currencies:
        data = download_data(currency, category)
        sleep(SLEEP_VALUE)
        buy_price = data['ask']
        sell_price = data['bid']
        result.append([currency, buy_price, sell_price])
    return result


def calculate_percentage_diffrence_of_buy_and_sell_price(buy_price, sell_price):
    return round(100*(1-sell_price/buy_price), 3)


def split_data_into_packages(data):
    names = []
    result = {}
    for val in data:
        names.append(val[0])
        ask = val[1]
        bid = val[2]
        time = datetime.now().strftime("%H:%M:%S")
        result.setdefault('ask', []).append(ask)
        result.setdefault('bid', []).append(bid)
    return names, result


def animation_frame(i):
    data = fetchFromAPI(currencies, category)
    names, splitted_data = split_data_into_packages(data)
    asks = splitted_data['ask']
    bids = splitted_data['bid']
    x_data.append(datetime.now().strftime("%H:%M:%S"))
    x_data_labels = x_data.copy()

    for i in range(len(names)):
        y_ask_data.setdefault(names[i], []).append(asks[i])
        y_bid_data.setdefault(names[i], []).append(bids[i])

    for i in range(len(names)):
        plt.plot(x_data, y_ask_data[names[i]],
                 linewidth=1, label='Asks of ' + names[i])
        plt.plot(x_data, y_bid_data[names[i]],
                 linewidth=1, label='Bids of ' + names[i])

    plt.subplots_adjust(bottom=0.2, left=0.2, right=0.9)
    plt.xticks(x_data_labels)

    plt.xlabel('Time')
    plt.ylabel('Value in USD')
    plt.legend()


if __name__ == "__main__":
    currencies = ['LSK', 'LTC', 'DASH']
    colors = ['blue', 'orange', 'black', 'green', 'yellow', 'purple']
    currency = 'USD'
    currencies = add_currency_to_currencies(currencies, currency)
    category = 'ticker'
    x_data = []
    y_ask_data = {}
    y_bid_data = {}

    ani = FuncAnimation(plt.gcf(), animation_frame, interval=5000)
    plt.legend()
    plt.show()
