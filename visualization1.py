import requests
import time
import matplotlib.pyplot as plt
import datetime
from matplotlib.animation import FuncAnimation
from matplotlib import style


def currency_data(currency, category, file_extensions):
    url = f"{BASE_URL}/{currency}/{category}.{file_extensions}"

    try:
        response = requests.get(url)
        json = response.json()
        response = json
        sell_price = response['ask']
        buy_price = response['bid']
        return sell_price, buy_price

    except requests.exceptions.ConnectionError:
        print("connection error")
        return None


def packaging_data(crypto, connect_type, file_ext):
    temp = currency_data(crypto, connect_type, file_ext)
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    bids = temp[0]
    asks = temp[1]
    return bids, asks, current_time


def animated_chart(i):
    print(f'Number of iterations is {i}')
    bid_results = packaging_data(crypto_to_char, connection_type, file_extension)

    bids_list.append(bid_results[0])
    asks_list.append(bid_results[1])
    time_list.append(bid_results[2])

    plt.title(f'Crypto {crypto_to_char} plot')
    plt.plot(time_list, bids_list, color='green', label='bid')
    plt.plot(time_list, asks_list, color='red', label='ask')


if __name__ == "__main__":
    BASE_URL = "https://bitbay.net/API/Public/"

    bids_list = list()
    asks_list = list()
    time_list = list()

    file_extension = {"Json_stream": "json", "Txt_file": "txt"}
    connection_types = {"Ticker": "ticker", "Orderbook": "orderbook"}
    crypto_values = {"BTCpack": "btcpln", "ETHpack": "ethpln", "ZECpack": "zecpln"}

    crypto_to_char = crypto_values["ZECpack"]
    file_extension = file_extension["Json_stream"]
    connection_type = connection_types["Ticker"]

    style.use('ggplot')
    ani = FuncAnimation(plt.gcf(), func=animated_chart, interval=6000)
    # plt.yscale("log")

    plt.tight_layout()
    plt.show()
    time.sleep(6)
