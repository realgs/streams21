import matplotlib.pyplot as plt
import datetime
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter
import requests
import json


def currency_data(currency, category, file_ext):
    url = f"{BASE_URL}/{currency}/{category}.{file_ext}"

    try:
        response = requests.get(url)
        json_data = response.json()
        response = json_data
        sell_price = response['ask']
        buy_price = response['bid']
        return sell_price, buy_price, datetime.datetime.now()

    except requests.exceptions.ConnectionError:
        print("connection error")
        return None


def volumen_data(currency, seconds):
    url = f"https://api.bitbay.net/rest/trading/transactions/{currency}"

    now = datetime.datetime.now()
    before = int((now - datetime.timedelta(seconds=seconds)).timestamp())

    querystring = {"from": before}
    try:
        response = requests.request("GET", url, params=querystring)
        volume = float(response.json()['items'][0]['a'])
    except requests.exceptions.ConnectionError:
        print("connection error")
        return None
    return volume


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
        value = bid_values[-1] - bid_values[-parameter]
        if value > 0:
            increases.append(value)
        else:
            decreases.append(value)
        a = (sum(increases)) + 1 / (len(increases) + 1)
        b = (sum(decreases)) + 1 / (len(decreases) + 1)
    else:
        a = 1
        b = 1
    try:
        RSI = 100 - (100 / (1 + abs((a / b))))
    except ZeroDivisionError:
        return 50
    print(RSI)
    return RSI


def check_trend(rsi_data):
    if len(rsi_data) < 3:
        return "No data yet"
    else:
        if rsi_data[-3] > rsi_data[-2] > rsi_data[-1]:
            return "Downward trend"
        if (rsi_data[-3] > rsi_data[-2] and rsi_data[-2] < rsi_data[-1]) or rsi_data[-3] < rsi_data[-2] and \
                rsi_data[-2] > rsi_data[-1]:
            return "Sideways trend"
        if rsi_data[-3] < rsi_data[-2] < rsi_data[-1]:
            return "Rising trend"
        else:
            return "No trend"


def check_if_candidate(btc_volume, eth_volume, zec_volume, btc_trending, eth_trending, zec_trending):
    last_btc = btc_volume[-1]
    last_eth = eth_volume[-1]
    last_zec = zec_volume[-1]

    max_volume = list()

    if btc_trending == "Downward trend":
        max_volume.append(0)
    else:
        max_volume.append(last_btc)

    if eth_trending == "Downward trend":
        max_volume.append(0)
    else:
        max_volume.append(last_eth)

    if zec_trending == "Downward trend":
        max_volume.append(0)
    else:
        max_volume.append(last_zec)

    if sum(max_volume) == 0:
        return "NO", "NO", "NO"

    crypto_id = max_volume.index(np.max(max_volume))

    if crypto_id == 0:
        return "YES", "NO", "NO"
    if crypto_id == 1:
        return "NO", "YES", "NO"
    if crypto_id == 2:
        return "NO", "NO", "YES"


def is_volatile(data, lenght, edge_value):
    diff = 0

    if len(data) < lenght:
        return "Waiting for data"
    else:
        for i in range(lenght):
            diff += abs(((float(data[-i]) - data[-i - 1]) / data[-i - 1]) * 100)
    if diff > edge_value:
        return "Volatile asset"
    else:
        return "Stable asset"


def is_liquid(buy, sell, S):
    perc = ((buy[-1] - sell[-1]) / sell[-1]) * 100
    if perc < S:
        return ", Liquid asset"

    else:
        return ""


def get_filename():
    file = open('file_name.txt', 'r')
    filename = file.read()
    return filename


def avg_from_json(filename):
    with open(filename, 'r') as openfile:
        data = json.load(openfile)

    pricing_list_btc = list()
    pricing_list_eth = list()
    pricing_list_zec = list()
    quantity_list_btc = list()
    quantity_list_eth = list()
    quantity_list_zec = list()

    for i in range(len(data["BTC"])):
        price_of_one = data["BTC"][i][1] * data["BTC"][i][0]
        quantity_list_btc.append(data["BTC"][i][0])
        pricing_list_btc.append(price_of_one)
    if len(pricing_list_btc) < 1:
        our_btc_mean = None
    else:
        our_btc_mean = (sum(pricing_list_btc)) / (sum(quantity_list_btc))

    for i in range(len(data["ETH"])):
        price_of_one = data["ETH"][i][1] * data["ETH"][i][0]
        quantity_list_eth.append((data["ETH"][i][0]))
        pricing_list_eth.append(price_of_one)
    if len(pricing_list_eth) < 1:
        our_eth_mean = None
    else:
        our_eth_mean = (sum(pricing_list_eth)) / (sum(quantity_list_eth))

    for i in range(len(data["ZEC"])):
        price_of_one = data["ZEC"][i][1] * data["ZEC"][i][0]
        quantity_list_zec.append((data["ZEC"][i][0]))
        pricing_list_zec.append(price_of_one)
    if len(pricing_list_zec) < 1:
        our_zec_mean = None
    else:
        our_zec_mean = (sum(pricing_list_zec)) / (sum(quantity_list_zec))

    openfile.close()

    return our_btc_mean, our_eth_mean, our_zec_mean


def profit_value_json():
    with open('sell_values_json.json', 'r') as openfile:
        profit_data = json.load(openfile)

        btc_profit = profit_data["BTC"]
        eth_profit = profit_data["ETH"]
        zec_profit = profit_data["ZEC"]
        return sum(btc_profit), sum(eth_profit), sum(zec_profit)


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

        vol_btc_list.append(volumen_data("BTC-PLN", 10))
        vol_eth_list.append(volumen_data("ETH-PLN", 10))
        vol_zec_list.append(volumen_data("ZEC-PLN", 10))

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

        averages = avg_from_json(FILE_NAME)
        our_btc_average.append(averages[0])
        our_eth_average.append(averages[1])
        our_zec_average.append(averages[2])

        crypto_profits = profit_value_json()
        btc_profit_label = crypto_profits[0]
        eth_profit_label = crypto_profits[1]
        zec_profit_label = crypto_profits[2]

        avg_lines[0][0].set_data(time_list, bidbtc_avg)
        avg_lines[1][0].set_data(time_list, askbtc_avg)
        avg_lines[2][0].set_data(time_list, our_btc_average[-1])
        avg_lines[3][0].set_data(time_list, bideth_avg)
        avg_lines[4][0].set_data(time_list, asketh_avg)
        avg_lines[5][0].set_data(time_list, our_eth_average[-1])
        avg_lines[6][0].set_data(time_list, bidzec_avg)
        avg_lines[7][0].set_data(time_list, askzec_avg)
        avg_lines[8][0].set_data(time_list, our_zec_average[-1])

        rsi_lines[0][0].set_data(time_list, rsi_btc)
        rsi_lines[1][0].set_data(time_list, rsi_eth)
        rsi_lines[2][0].set_data(time_list, rsi_zec)

        axs[0][0].relim()
        axs[0][1].relim()
        axs[0][2].relim()
        axs[1][0].relim()
        axs[1][1].relim()
        axs[1][2].relim()
        axs[2][0].relim()
        axs[2][1].relim()
        axs[2][2].relim()
        axs[0][0].autoscale_view()
        axs[0][1].autoscale_view()
        axs[0][2].autoscale_view()
        axs[1][0].autoscale_view()
        axs[1][1].autoscale_view()
        axs[1][2].autoscale_view()
        axs[2][0].autoscale_view()
        axs[2][1].autoscale_view()
        axs[2][2].autoscale_view()

        trending_btc = check_trend(rsi_btc)
        trending_eth = check_trend(rsi_eth)
        trending_zec = check_trend(rsi_zec)

        candidate_info = check_if_candidate(vol_btc_list, vol_eth_list, vol_zec_list, trending_btc, trending_eth,
                                            trending_zec)

        btc_volatile = (is_volatile(askbtc_list, VOLATILE_LENGTH, VOLATILE_VALUE))
        eth_volatile = (is_volatile(asketh_list, VOLATILE_LENGTH, VOLATILE_VALUE))
        zec_volatile = (is_volatile(askzec_list, VOLATILE_LENGTH, VOLATILE_VALUE))

        btc_liquid = is_liquid(bidbtc_list, askbtc_list, LIQUID_VALUE)
        eth_liquid = is_liquid(bideth_list, asketh_list, LIQUID_VALUE)
        zec_liquid = is_liquid(bidzec_list, askzec_list, LIQUID_VALUE)

        if trending_btc == "Downward trend":
            cl_btc = 'red'
        elif trending_btc == "Rising trend":
            cl_btc = 'green'
        elif trending_btc == "Sideways trend":
            cl_btc = 'purple'
        else:
            cl_btc = 'black'

        if trending_eth == "Downward trend":
            cl_eth = 'red'
        elif trending_eth == "Rising trend":
            cl_eth = 'green'
        elif trending_eth == "Sideways trend":
            cl_eth = 'purple'
        else:
            cl_eth = 'black'

        if trending_zec == "Downward trend":
            cl_zec = 'red'
        elif trending_zec == "Rising trend":
            cl_zec = 'green'
        elif trending_zec == "Sideways trend":
            cl_zec = 'purple'
        else:
            cl_zec = 'black'

        axs[0][0].set_title(f'Bitcoin values, profit is: {btc_profit_label}')
        axs[0][1].set_title(f'Bitcoin values, profit is: {eth_profit_label}')
        axs[0][2].set_title(f'Bitcoin values, profit is: {zec_profit_label}')

        axs[1][0].set_title(f'Bitcoin RSI, Trend: {trending_btc}', color=cl_btc)
        axs[1][1].set_title(f'Eth RSI, Trend: {trending_eth}', color=cl_eth)
        axs[1][2].set_title(f'ZEC RSI, Trend: {trending_zec}', color=cl_zec)

        axs[2][0].set_title(f'Bitcoin volume - Candidate?:{candidate_info[0]}, {btc_volatile} {btc_liquid}')
        axs[2][1].set_title(f'Eth volume - Candidate?:{candidate_info[1]}, {eth_volatile} {eth_liquid}')
        axs[2][2].set_title(f'ZEC volume - Candidate?:{candidate_info[2]}, {zec_volatile} {zec_liquid}')

    fig, axs = plt.subplots(3, 3, figsize=(18, 12))

    lines.append(axs[0][0].plot(time_list, bidbtc_list, color='green', label='bid'))
    lines.append(axs[0][0].plot(time_list, askbtc_list, color='red', label='ask'))
    avg_lines.append(axs[0][0].plot(time_list, bidbtc_avg, color='orange', label='bid avg', linestyle='dotted'))
    avg_lines.append(axs[0][0].plot(time_list, askbtc_avg, color='pink', label='ask avg', linestyle='dotted'))
    avg_lines.append(axs[0][0].plot(time_list, our_btc_average, color='blue', label='my avg', linestyle='dotted'))
    axs[0][0].set_title("Bitcoin values")
    axs[0][0].grid()
    axs[0][0].legend(loc=1)
    axs[0][0].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    rsi_lines.append(axs[1][0].plot(time_list, rsi_btc, color='red', label='RSI BTC value'))
    axs[1][0].set_title("Bitcoin RSI")
    axs[1][0].legend(loc=1)
    axs[1][0].grid()
    axs[1][0].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    volumen_lines.append(axs[2][0].plot(time_list, vol_btc_list, color='blue', label='BTC volume'))
    axs[2][0].set_title("Bitcoin volume")
    axs[2][0].legend(loc=1)
    axs[2][0].grid()
    axs[2][0].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    lines.append(axs[0][1].plot(time_list, bideth_list, color='green', label='bid'))
    lines.append(axs[0][1].plot(time_list, asketh_list, color='red', label='ask'))
    avg_lines.append(axs[0][1].plot(time_list, bideth_avg, color='orange', label='bid avg', linestyle='dotted'))
    avg_lines.append(axs[0][1].plot(time_list, asketh_avg, color='pink', label='ask avg', linestyle='dotted'))
    avg_lines.append(axs[0][1].plot(time_list, our_eth_average, color='blue', label='my avg', linestyle='dotted'))
    axs[0][1].set_title("Etherium values")
    axs[0][1].grid()
    axs[0][1].legend(loc=1)
    axs[0][1].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    rsi_lines.append(axs[1][1].plot(time_list, rsi_eth, color='red', label='RSI ETH value'))
    axs[1][1].set_title("Etherium RSI")
    axs[1][1].legend(loc=1)
    axs[1][1].grid()
    axs[1][1].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    volumen_lines.append(axs[2][1].plot(time_list, vol_eth_list, color='blue', label='ETH volume'))
    axs[2][1].set_title("Etherium volume")
    axs[2][1].legend(loc=1)
    axs[2][1].grid()
    axs[2][1].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    lines.append(axs[0][2].plot(time_list, bidzec_list, color='green', label='bid'))
    lines.append(axs[0][2].plot(time_list, askzec_list, color='red', label='ask'))
    avg_lines.append(axs[0][2].plot(time_list, bidzec_avg, color='orange', label='bid avg', linestyle='dotted'))
    avg_lines.append(axs[0][2].plot(time_list, askzec_avg, color='pink', label='ask avg', linestyle='dotted'))
    avg_lines.append(axs[0][2].plot(time_list, our_zec_average, color='blue', label='my avg', linestyle='dotted'))
    axs[0][2].set_title("ZEC values")
    axs[0][2].grid()
    axs[0][2].legend(loc=1)
    axs[0][2].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    rsi_lines.append(axs[1][2].plot(time_list, rsi_zec, color='red', label='RSI ZEC value'))
    axs[1][2].set_title("ZEC RSI")
    axs[1][2].legend(loc=1)
    axs[1][2].grid()
    axs[1][2].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    volumen_lines.append(axs[2][2].plot(time_list, vol_eth_list, color='blue', label='ZEC volume'))
    axs[2][2].set_title("ZEC volume")
    axs[2][2].legend(loc=1)
    axs[2][2].grid()
    axs[2][2].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    fig.autofmt_xdate()
    _ = FuncAnimation(fig, func=data_update, interval=6000)
    plt.autoscale()
    plt.show()


if __name__ == "__main__":
    BASE_URL = "https://bitbay.net/API/Public/"
    FILE_EXTENSION = "json"
    CONNECTION_TYPE = "ticker"
    FILE_NAME = get_filename()
    print(FILE_NAME)

    our_btc_average = list()
    our_eth_average = list()
    our_zec_average = list()

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

    VOLATILE_VALUE = 0.2
    VOLATILE_LENGTH = 3
    LIQUID_VALUE = 0.2

    dict_of_ask_bid_lists = dict()
    for crypto in CRYPTO_LIST:
        dict_of_ask_bid_lists[crypto] = [list(), list(), list()]

    animated_chart()
