import requests
import time
import matplotlib.pyplot as plt

URL = "https://api.bitbay.net/rest/trading/orderbook/"
FIRST_POSITION = 0
FIFE = 5
CURRENCY = ["BTC-USD", "LTC-USD", "DASH-USD"]

def get_data (currency):
    temp_url = URL + currency
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", temp_url, headers=headers).json()

    try:
        buy = float(response['buy'][FIRST_POSITION]['ra'])
        sell = float(response['sell'][FIRST_POSITION]['ra'])
    except ValueError:
        print(">>> ValueError: could not convert string to float ")

    return buy, sell

def add_data (currency, buy_list, sell_list, time_list):
    buy, sell = get_data(currency)
    buy_list.append(buy)
    sell_list.append(sell)
    time_list.append(time.strftime("%H:%M:%S", time.localtime()))

    return buy_list, sell_list, time_list

def make_plot (currency):
    y1 = []
    y2 = []
    t = []

    while True:
        y1, y2, t = add_data(currency, y1, y2, t)
        plt.title(f"Wykres notowań kursu {currency}")
        plt.plot(t, y1, label="Najlepszy kurs kupna", color="blue")
        plt.plot(t, y2, label="Najlepszy kurs sprzedaży", color="yellow")
        plt.xlabel("Czas")
        plt.ylabel("Kurs")
        plt.xlim(0, 10)
        plt.xticks(rotation='vertical')
        plt.subplots_adjust(bottom=0.2)
        plt.show()
        time.sleep(FIFE)

def main():
    make_plot(CURRENCY[0])

if __name__ == '__main__':
    main()
