import matplotlib.pyplot as plt
import datetime
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter
import requests


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


def volumen_data(currency):
    url = f"https://api.bitbay.net/rest/trading/transactions/{currency}"
    try:
        response = requests.get(url)
        json = response.json()
        response = json
        volume = float(response['items'][1]['a'])
        return volume

    except requests.exceptions.ConnectionError:
        print("connection error")
        return None


def packaging_data(connect_type, file_ext):
    for item in CRYPTO_LIST:
        temp = (currency_data(item, connect_type, file_ext))
        dict_of_ask_bid_lists.update({item: temp})
    return dict_of_ask_bid_lists


def avg_values(ask_values, bid_values, parameter):
    buy = list()
    sell = list()
    if len(ask_values) <= parameter:
        for i in ask_values:
            sell.append(i)
        for i in bid_values:
            buy.append(i)
        sell_avg = sum(sell) / len(sell)
        buy_avg = sum(buy) / len(buy)
        return sell_avg, buy_avg
    else:
        for i in range(-1, -parameter, -1):
            buy.append(bid_values[i])
            sell.append(ask_values[i])
        sell_avg = sum(sell) / len(sell)
        buy_avg = sum(buy) / len(buy)
        return sell_avg, buy_avg


def rsi_values(bid_values, parameter):
    increases = list()
    decreases = list()
    if len(bid_values) > parameter:
        temp = bid_values[len(bid_values) - 1] - bid_values[len(bid_values) - parameter]
        if temp > 0:
            increases.append(temp)
        else:
            decreases.append(temp)

        a = (sum(increases) + 1) / (len(increases) + 1)
        b = (sum(decreases) + 1) / (len(decreases) + 1)

    else:
        a = 1
        b = 1
    RSI = 100 - (100 / (1 + (a / b)))
    print(RSI)
    return RSI


def animated_chart():
    def data_update(i):
        print(f'Number of iterations is {i}')
        bid_results = packaging_data(CONNECTION_TYPE, FILE_EXTENSION)

        bidbtc_list.append(bid_results["BTC-PLN"][0])
        askbtc_list.append(bid_results["BTC-PLN"][1])
        bideth_list.append(bid_results["ETH-PLN"][0])
        asketh_list.append(bid_results["ETH-PLN"][1])
        bidzec_list.append(bid_results["ZEC-PLN"][0])
        askzec_list.append(bid_results["ZEC-PLN"][1])
        time_list.append(bid_results["BTC-PLN"][2])

        vol_btc_list.append(volumen_data("BTC-PLN"))
        vol_eth_list.append(volumen_data("ETH-PLN"))
        vol_zec_list.append(volumen_data("ZEC-PLN"))

        sell_avg, buy_avg = avg_values(askbtc_list, bidbtc_list, 50)
        bidbtc_avg.append(buy_avg)
        askbtc_avg.append(sell_avg)
        sell_avg, buy_avg = avg_values(asketh_list, bideth_list, 50)
        bideth_avg.append(buy_avg)
        asketh_avg.append(sell_avg)
        sell_avg, buy_avg = avg_values(askzec_list, bidzec_list, 50)
        bidzec_avg.append(buy_avg)
        askzec_avg.append(sell_avg)

        rsi_btc.append(rsi_values(bidbtc_list, 5))
        rsi_eth.append(rsi_values(bideth_list, 5))
        rsi_zec.append(rsi_values(bidzec_list, 5))

        lines[0][0].set_data(time_list, bidbtc_list)
        lines[1][0].set_data(time_list, askbtc_list)
        lines[2][0].set_data(time_list, bideth_list)
        lines[3][0].set_data(time_list, asketh_list)
        lines[4][0].set_data(time_list, bidzec_list)
        lines[5][0].set_data(time_list, askzec_list)

        volumen_lines[0][0].set_data(time_list, vol_btc_list)
        volumen_lines[1][0].set_data(time_list, vol_eth_list)
        volumen_lines[2][0].set_data(time_list, vol_zec_list)

        avg_lines[0][0].set_data(time_list, bidbtc_avg)
        avg_lines[1][0].set_data(time_list, askbtc_avg)
        avg_lines[2][0].set_data(time_list, bideth_avg)
        avg_lines[3][0].set_data(time_list, asketh_avg)
        avg_lines[4][0].set_data(time_list, bidzec_avg)
        avg_lines[5][0].set_data(time_list, askzec_avg)

        rsi_lines[0][0].set_data(time_list, rsi_btc)
        rsi_lines[1][0].set_data(time_list, rsi_eth)
        rsi_lines[2][0].set_data(time_list, rsi_zec)

        axs[0][0].relim()
        axs[0][1].relim()
        axs[0][2].relim()
        axs[1][0].relim()
        axs[1][1].relim()
        axs[1][2].relim()
        axs[0][0].autoscale_view()
        axs[0][1].autoscale_view()
        axs[0][2].autoscale_view()
        axs[1][0].autoscale_view()
        axs[1][1].autoscale_view()
        axs[1][2].autoscale_view()

    fig, axs = plt.subplots(2, 3, figsize=(18, 8))

    lines.append(axs[0][0].plot(time_list, bidbtc_list, color='green', label='bid'))
    lines.append(axs[0][0].plot(time_list, askbtc_list, color='red', label='ask'))
    avg_lines.append(axs[0][0].plot(time_list, bidbtc_avg, color='orange', label='bid avg', linestyle='dotted'))
    avg_lines.append(axs[0][0].plot(time_list, askbtc_avg, color='pink', label='ask avg', linestyle='dotted'))
    axs[0][0].set_title("Bitcoin values")
    axs[0][0].grid()
    axs[0][0].legend()
    axs[0][0].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    volumen_lines.append(axs[1][0].plot(time_list, vol_btc_list, color='blue', label='BTC volume'))
    rsi_lines.append(axs[1][0].plot(time_list, rsi_btc, color='red', label='RSI BTC value'))
    axs[1][0].set_title("Bitcoin volume and RSI")
    axs[1][0].legend()
    axs[1][0].grid()
    axs[1][0].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    axs[1][0].set_yscale('log')

    lines.append(axs[0][1].plot(time_list, bideth_list, color='green', label='bid'))
    lines.append(axs[0][1].plot(time_list, asketh_list, color='red', label='ask'))
    avg_lines.append(axs[0][1].plot(time_list, bideth_avg, color='orange', label='bid avg', linestyle='dotted'))
    avg_lines.append(axs[0][1].plot(time_list, asketh_avg, color='pink', label='ask avg', linestyle='dotted'))
    axs[0][1].set_title("Etherium values")
    axs[0][1].grid()
    axs[0][1].legend()
    axs[0][1].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    volumen_lines.append(axs[1][1].plot(time_list, vol_eth_list, color='blue', label='ETH volume'))
    rsi_lines.append(axs[1][1].plot(time_list, rsi_eth, color='red', label='RSI ETH value'))
    axs[1][1].set_title("Etherium volume and RSI")
    axs[1][1].legend()
    axs[1][1].grid()
    axs[1][1].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    axs[1][1].set_yscale('log')

    lines.append(axs[0][2].plot(time_list, bidzec_list, color='green', label='bid'))
    lines.append(axs[0][2].plot(time_list, askzec_list, color='red', label='ask'))
    avg_lines.append(axs[0][2].plot(time_list, bidzec_avg, color='orange', label='bid avg', linestyle='dotted'))
    avg_lines.append(axs[0][2].plot(time_list, askzec_avg, color='pink', label='ask avg', linestyle='dotted'))
    axs[0][2].set_title("ZEC values")
    axs[0][2].grid()
    axs[0][2].legend()
    axs[0][2].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    volumen_lines.append(axs[1][2].plot(time_list, vol_eth_list, color='blue', label='ZEC volume'))
    rsi_lines.append(axs[1][2].plot(time_list, rsi_zec, color='red', label='RSI ZEC value'))
    axs[1][2].set_title("ZEC volume and RSI")
    axs[1][2].legend()
    axs[1][2].grid()
    axs[1][2].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    axs[1][2].set_yscale('log')

    fig.autofmt_xdate()
    _ = FuncAnimation(fig, func=data_update, interval=6000)
    plt.autoscale()
    plt.show()


if __name__ == "__main__":
    BASE_URL = "https://bitbay.net/API/Public/"
    FILE_EXTENSION = "json"
    CONNECTION_TYPE = "ticker"

    bidbtc_list = list()
    bidbtc_avg = list()
    askbtc_list = list()
    askbtc_avg = list()
    vol_btc_list = list()
    rsi_btc = list()

    bideth_list = list()
    bideth_avg = list()
    asketh_list = list()
    asketh_avg = list()
    vol_eth_list = list()
    rsi_eth = list()

    bidzec_list = list()
    bidzec_avg = list()
    askzec_list = list()
    askzec_avg = list()
    vol_zec_list = list()
    rsi_zec = list()

    time_list = list()
    lines = list()
    volumen_lines = list()
    avg_lines = list()
    rsi_lines = list()

    crypto_values = {"BTCpack": "btcpln", "ETHpack": "ethpln", "ZECpack": "zecpln"}
    CRYPTO_LIST = ["BTC-PLN", "ETH-PLN", "ZEC-PLN"]

    dict_of_ask_bid_lists = dict()
    for crypto in CRYPTO_LIST:
        dict_of_ask_bid_lists[crypto] = [list(), list(), list()]

    animated_chart()
