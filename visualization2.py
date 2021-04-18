import matplotlib.pyplot as plt
import datetime
from matplotlib.animation import FuncAnimation
from matplotlib import style
from matplotlib.dates import DateFormatter


def currency_data(currency, category, file_ext):
    url = f"{BASE_URL}/{currency}/{category}.{file_ext}"

    try:
        response = requests.get(url)
        json = response.json()
        response = json
        sell_price = response['ask']
        buy_price = response['bid']
        return sell_price, buy_price, datetime.datetime.now()

    except requests.exceptions.ConnectionError:
        print("connection error")
        return None


def packaging_data(connect_type, file_ext):
    for item in CRYPTO_LIST:
        temp = (currency_data(item, connect_type, file_ext))
        dict_of_ask_bid_lists.update({item: temp})
    return dict_of_ask_bid_lists


def animated_chart():
    def data_update(i):
        print(f'Number of iterations is {i}')
        bid_results = packaging_data(CONNECTION_TYPE, FILE_EXTENSION)

        bidbtc_list.append(bid_results["btcpln"][0])
        askbtc_list.append(bid_results["btcpln"][1])
        bideth_list.append(bid_results["ethpln"][0])
        asketh_list.append(bid_results["ethpln"][1])
        bidzec_list.append(bid_results["zecpln"][0])
        askzec_list.append(bid_results["zecpln"][1])
        time_list.append(bid_results["btcpln"][2])

        lines[0][0].set_data(time_list, bidbtc_list)
        lines[1][0].set_data(time_list, askbtc_list)
        lines[2][0].set_data(time_list, bideth_list)
        lines[3][0].set_data(time_list, asketh_list)
        lines[4][0].set_data(time_list, bidzec_list)
        lines[5][0].set_data(time_list, askzec_list)

        axs[0].relim()
        axs[1].relim()
        axs[2].relim()
        axs[0].autoscale_view()
        axs[1].autoscale_view()
        axs[2].autoscale_view()

    fig, axs = plt.subplots(len(CRYPTO_LIST))
    lines = []

    lines.append(axs[0].plot(time_list, bidbtc_list, color='green', label='bid'))
    lines.append(axs[0].plot(time_list, askbtc_list, color='red', label='ask'))
    axs[0].set_title("Bitcoin values")
    axs[0].grid()
    axs[0].legend()
    axs[0].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    lines.append(axs[1].plot(time_list, bideth_list, color='green', label='bid'))
    lines.append(axs[1].plot(time_list, asketh_list, color='red', label='ask'))
    axs[1].set_title("Etherium values")
    axs[1].grid()
    axs[1].legend()
    axs[1].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    lines.append(axs[2].plot(time_list, bidzec_list, color='green', label='bid'))
    lines.append(axs[2].plot(time_list, askzec_list, color='red', label='ask'))
    axs[2].set_title("ZEC values")
    axs[2].grid()
    axs[2].legend()
    axs[2].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    fig.autofmt_xdate()
    _ = FuncAnimation(fig, func=data_update, interval=6000)
    plt.autoscale()
    plt.show()


if __name__ == "__main__":
    BASE_URL = "https://bitbay.net/API/Public/"
    FILE_EXTENSION = "json"
    CONNECTION_TYPE = "ticker"

    bidbtc_list = list()
    askbtc_list = list()
    bideth_list = list()
    asketh_list = list()
    bidzec_list = list()
    askzec_list = list()
    time_list = list()

    crypto_values = {"BTCpack": "btcpln", "ETHpack": "ethpln", "ZECpack": "zecpln"}
    CRYPTO_LIST = ["btcpln", "ethpln", "zecpln"]

    dict_of_ask_bid_lists = dict()
    for crypto in CRYPTO_LIST:
        dict_of_ask_bid_lists[crypto] = [list(), list(), list()]

    animated_chart()
    style.use('ggplot')