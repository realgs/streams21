import requests
import time
import matplotlib.pyplot as plt
import datetime
from matplotlib.animation import FuncAnimation
from matplotlib import style


def currency_data(currency, category, file_ext):
    url = f"{BASE_URL}/{currency}/{category}.{file_ext}"

    try:
        response = requests.get(url)
        json = response.json()
        response = json
        sell_price = response['ask']
        buy_price = response['bid']
        return sell_price, buy_price, datetime.datetime.now().strftime("%H:%M:%S")

    except requests.exceptions.ConnectionError:
        print("connection error")
        return None


def packaging_data(connect_type, file_ext):
    for item in CRYPTO_LIST:
        temp = (currency_data(item, connect_type, file_ext))
        print(item)
        print(temp)
        dict_of_ask_bid_lists.update({item: temp})
    return dict_of_ask_bid_lists


def animated_chart():
    def data_update(i):
        print(f'Number of iterations is {i}')
        bid_results = packaging_data(connection_type, file_extension)

        bidbtc_list.append(bid_results["btcpln"][0])
        askbtc_list.append(bid_results["btcpln"][1])
        bideth_list.append(bid_results["ethpln"][0])
        asketh_list.append(bid_results["ethpln"][1])
        bidzec_list.append(bid_results["zecpln"][0])
        askzec_list.append(bid_results["zecpln"][1])
        time_list.append(bid_results["btcpln"][2])

        axs[0].plot(time_list, bidbtc_list, color='green', label='bid')
        axs[0].plot(time_list, askbtc_list, color='red', label='ask')
        axs[0].set_title("Bitcoin values")
        axs[1].plot(time_list, bideth_list, color='green', label='ask')
        axs[1].plot(time_list, asketh_list, color='red', label='ask')
        axs[1].set_title("Etherium values")
        axs[2].plot(time_list, bidzec_list, color='green', label='ask')
        axs[2].plot(time_list, askzec_list, color='red', label='ask')
        axs[2].set_title("ZEC values")

    fig, axs = plt.subplots(3)
    _ = FuncAnimation(fig, func=data_update, interval=6000)
    plt.autoscale()
    plt.show()


if __name__ == "__main__":
    BASE_URL = "https://bitbay.net/API/Public/"

    bidbtc_list = list()
    askbtc_list = list()
    bideth_list = list()
    asketh_list = list()
    bidzec_list = list()
    askzec_list = list()
    time_list = list()

    file_extensions = {"Json_stream": "json", "Txt_file": "txt"}
    connection_types = {"Ticker": "ticker", "Orderbook": "orderbook"}
    crypto_values = {"BTCpack": "btcpln", "ETHpack": "ethpln", "ZECpack": "zecpln"}
    CRYPTO_LIST = ["btcpln", "ethpln", "zecpln"]

    dict_of_ask_bid_lists = dict()
    for crypto in CRYPTO_LIST:
        dict_of_ask_bid_lists[crypto] = [list(), list(), list()]

    file_extension = file_extensions["Json_stream"]
    connection_type = connection_types["Ticker"]
    animated_chart()
    style.use('ggplot')
    plt.tight_layout()

    time.sleep(6)
