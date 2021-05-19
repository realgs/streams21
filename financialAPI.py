import time
import requests
import statistics
import numpy as np
from requests.exceptions import HTTPError
import matplotlib.pyplot as plt


data_currency = {
    "LSK": [],
    "BCP": [],
    "GNT": [],
}

data_currency_extra = {
    "LSK": [],
    "BCP": [],
    "GNT": [],
}

data_currency_extra1 = {
    "LSK": [],
    "BCP": [],
    "GNT": [],
}

S = 5
X = 5
Y = 3


def data(lines, window, zakres):
    currency_1 = ['LSK', 'BCP', 'GNT']
    currency_2 = 'PLN'
    category = 'orderbook'
    iterator = 0
    while True:
        iterator += 1
        for c in currency_1:
            data = download_data(c, currency_2, category)
            if data is not None:
                diffrence = calculate(data, c, window, zakres)
        create_graph(iterator, lines)
        candidate = find_candidate(currency_1[0], currency_1[1], currency_1[2])
        define_liquid(candidate)
        define_volatile(candidate)
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


def get_volumen(currency):
    try:
        response = requests.get(url=f'https://api.bitbay.net/rest/trading/transactions/{currency}-PLN')
        data = response.json()

    except HTTPError:
        print('HTTP error:', HTTPError)
        return None
    return data['items'][1]['a']


def calculate_averange(currency, window_len):
    data = data_currency[currency]
    data_points_ctr = len(data)
    if window_len >= data_points_ctr:
        window_len = data_points_ctr

    window = data[-window_len:]

    b_avg = statistics.mean([dp["buy_price"] for dp in window])
    s_avg = statistics.mean([dp["sell_price"] for dp in window])

    return b_avg, s_avg


def calculate_RSI(currency, window_len):
    average_price_increase = []
    average_price_decrease = []
    data = data_currency[currency]
    data_points_ctr = len(data)

    if len(data) >= window_len:
        value = data[-1]["buy_price"] - data[data_points_ctr-window_len]["buy_price"]
        if value > 0:
            average_price_increase.append(value)
        elif value <= 0:
            average_price_decrease.append(value)
        a = (sum(average_price_increase) + 1)/(len(average_price_increase) + 1)
        b = (sum(average_price_decrease) + 1)/(len(average_price_decrease) + 1)
    else:
        a = 1
        b = 1
    RSI = 100 - (100 / (1 + (a/b)))
    return RSI


def check_trend(currency):
    down_hills_points = []
    up_hills_points = []
    data = data_currency_extra[currency]

    for items in range(1, len(data)-1):

        if (data[items - 1]["RSI"] > data[items]["RSI"]) and (data[items]["RSI"] < data[items + 1]["RSI"]):  # sprawdzam czy to dołek and (data[items]["RSI"] < data[items + 1]["RSI"])
            down_hills_points.append(data[items]["RSI"])
            print(down_hills_points, '-')
        else:
            down_hills_points.append(0)

        if (data[items - 1]["RSI"] < data[items]["RSI"]) and (data[items]["RSI"] > data[items + 1]["RSI"]):  # sprawdzam czy to wierzchołek and (data[items]["RSI"] > data[items + 1]["RSI"])
            up_hills_points.append(data[items]["RSI"])
            print(up_hills_points, '+')
        else:
            up_hills_points.append(0)

    if (down_hills_points[-1] < down_hills_points[len(down_hills_points) - 2]) and \
            (down_hills_points[len(down_hills_points) - 2] != 0):
        print("down")
        return "Downward"

    elif (up_hills_points[-1] > up_hills_points[len(up_hills_points) - 2]) and \
            (up_hills_points[-1] != 0):
        print("up")
        return "Rising"

    elif ((up_hills_points[-1] == up_hills_points[len(up_hills_points) - 2])
            or (down_hills_points[-1] == down_hills_points[len(down_hills_points) - 2])) \
            and (up_hills_points[-1] != 0 and up_hills_points[len(up_hills_points) - 2] != 0) \
            and (down_hills_points[-1] != 0 and down_hills_points[len(down_hills_points) - 2] != 0):
        print("side")
        return "Sideways"

    else:
        print("insufficient amount of data")
        return "Insufficient amount of data"


def find_candidate(c1, c2, c3):
    currency1 = False
    currency2 = False
    currency3 = False

    c1_trend = data_currency_extra1[c1][-1]["trend"]
    c2_trend = data_currency_extra1[c2][-1]["trend"]
    c3_trend = data_currency_extra1[c3][-1]["trend"]

    print(c1_trend, c2_trend, c3_trend)
    bool_array = [currency1, currency2, currency3]

    LastVolumen_c1 = data_currency_extra[c1][-1]['volumen']
    LastVolumen_c2 = data_currency_extra[c2][-1]['volumen']
    LastVolumen_c3 = data_currency_extra[c3][-1]['volumen']

    LastVolumeArray = [LastVolumen_c1, LastVolumen_c2, LastVolumen_c3]
    
    max = ""

    if c1_trend !=  "Downward":
        currency1 = True
    if c2_trend != "Downward":
        currency2 = True
    if c3_trend != "Downward":
        currency3 = True

    print(bool_array, ' ------- ')

    max_array = []
    for items in bool_array:
        if items is True:
            max_array.append(LastVolumeArray[items])
        else:
            max_array.append(0)
    out = max_array.index(np.max(max_array))

    if out == 0:
        max = c1
    elif out == 1:
        max = c2
    else:
        max = c3

    data_currency_extra1[max][-1]['candidate'] = 'C'
    return max


def define_liquid(currency):

    buy = data_currency[currency][-1]["buy_price"]
    sell = data_currency[currency][-1]["sell_price"]

    maximum = max(buy, sell)
    minimum = min(buy, sell)

    out = maximum * 100/minimum
    distance = 100 - out

    if distance < 5:
        data_currency_extra1[currency][-1]['liquid']='L'
        return True
    else:
        return False


def define_volatile(currency):
    buy_array = []
    for i in range(len(data_currency[currency])):
        data = data_currency[currency][i]["buy_price"]
        buy_array.append(data)

    if Y < len(buy_array):
        value_Y = buy_array[len(buy_array)-Y]
    else:
        value_Y = buy_array[-1]

    current = buy_array[0]

    maximum = max(value_Y, current)
    minimum = min(value_Y, current)

    out = minimum * 100/maximum
    distance = 100 - out

    if distance > X:
        data_currency_extra1[currency][-1]['volatile'] = 'V'
        return True
    else:
        return False


def calculate(data, currency, beginning, end):
    buy = data['bids'][0][0]
    sell = data['asks'][0][0]
    procent = (1-(sell-buy)/sell) * 100
    t = time.strftime("%H:%M:%S", time.localtime())

    diffrence = {
        'buy_price': data['bids'][0][0],
        'sell_price': data['asks'][0][0],
        'procents': procent,
        'time': str(t),
    }
    print(currency, '-----', procent)
    data_currency[currency].append(diffrence)
    value_buy, value_sell = calculate_averange(currency, window)
    RSI = calculate_RSI(currency, zakres)

    volumen = get_volumen(currency)
    diffrence2 = {
        'buy_averange': value_buy,
        'sell_averange': value_sell,
        'RSI': RSI,
        'volumen': volumen,
    }

    data_currency_extra[currency].append(diffrence2)
    if len(data_currency_extra[currency]) >= 3:
        trend = check_trend(currency)

    else:
        trend = None

    diffrence3 = {
        'trend': trend,
        'candidate': '-',
        'volatile': '-',
        'liquid': '-',
        }
    data_currency_extra1[currency].append(diffrence3)
    return diffrence


xrang = 8


def create_graph(j, lines):
    for c, l in lines.items():
        data = data_currency[c]
        data2 = data_currency_extra[c]
        data3 = data_currency_extra1[c]
        buy = []
        sell = []
        tim = []
        buy_average = []
        sell_average = []
        RSI = []
        volumen = []
        trend = []
        candidate = []
        volatile = []
        liquid = []
        width = 0.35
        if len(data) > 0:
            itr = range(xrang)
            if len(data) < xrang:
                itr = range(len(data))
            for i in itr:
                buy.append(data[i-len(itr)]["buy_price"])
                sell.append(data[i-len(itr)]["sell_price"])
                tim.append(data[i-len(itr)]["time"])
                buy_average.append(data2[i-len(itr)]["buy_averange"])
                sell_average.append(data2[i-len(itr)]["sell_averange"])
                RSI.append(data2[i-len(itr)]["RSI"])
                volumen.append(float(data2[i-len(itr)]["volumen"]))
                trend.append(data3[i-len(itr)]["trend"])
                candidate.append(data3[i-len(itr)]["candidate"])
                volatile.append(data3[i-len(itr)]["volatile"])
                liquid.append(data3[i-len(itr)]["liquid"])

            l[0].set_data(itr, buy)
            l[1].set_data(itr, sell)
            l[2].set_data(itr, buy_average)
            l[3].set_data(itr, sell_average)
            plts[c].set_xticklabels(tim, rotation='horizontal', fontsize=7)
            plts[c].set_xlim(0, xrang-1)
            plts[c].set_title(f"{c} - PLN, {candidate[0]}, {volatile[0]}, {liquid[0]}")

            if min(buy) >= min(buy_average):
                bottom = min(buy_average)
            else:
                bottom = min(buy)

            if max(sell) <= max(sell_average):
                top = max(sell_average)
            else:
                top = max(sell)
            plts[c].set_ylim([bottom*0.95, top*1.05])

            br1 = itr
            br2 = [x + width for x in br1]
            plts_ex[c].bar(br1, volumen, width, align='center', color='blue', label=volumen)
            plts_ex[c].bar(br2, RSI, width, align='center', color='orange', label=RSI)

            plts_ex[c].set_xticklabels(tim, rotation='horizontal', fontsize=7)
            plts_ex[c].set_xlim(0, xrang-1)
            plts_ex[c].set_title(f"{c} - PLN, trend:{trend[-1]}")

            if min(RSI) >= min(volumen):
                bottom1 = min(volumen)
            else:
                bottom1 = min(RSI)

            if max(RSI) <= max(volumen):
                top1 = max(volumen)
            else:
                top1 = max(RSI)
            plts_ex[c].legend(labels=[f'Volumen: {volumen[-1]}', f'RSI: {RSI[-1]}'])
            plts_ex[c].set_ylim([bottom1*0.85, top1*1.15])

    plt.draw()
    plt.pause(1e-17)


if __name__ == "__main__":

    window = int(input("podaj długość zakresu z którego chcesz otrzymać średnią: "))
    zakres = int(input("podaj długość zakresu z którego chcesz otrzymać RSI: "))
    plt.ion()

    plts = {}
    plts_ex = {}
    lines = {}
    lines_ex = {}

    fig1 = plt.figure()
    fig2 = plt.figure()

    itr = 1
    itr2 = 1

    for c in data_currency.keys():
        plts[c] = fig1.add_subplot(len(data_currency), 1, itr)
        buy_line, = plts[c].plot([0], [0], label='buy')
        sell_line, = plts[c].plot([0], [0], label='sell')
        buy_average, = plts[c].plot([0], [0], color='blue', linestyle='dashed', label='buy_average')
        sell_average, = plts[c].plot([0], [0], color='orange', linestyle='dashed', label='sell_average')
        lines[c] = [buy_line, sell_line, buy_average, sell_average]

        plts[c].set_ylim([1, 5])
        plts[c].set_title(f"{c} - PLN")

        plts[c].set_xlabel("time")
        plts[c].set_ylabel("value")

        plts[c].legend()

        itr += 1

    fig1.tight_layout(h_pad=0.5)

    for c in data_currency.keys():
        plts_ex[c] = fig2.add_subplot(len(data_currency), 1, itr2)

        volumen, = plts_ex[c].plot([0], [0], label='Volumen')
        RSI, = plts_ex[c].plot([0], [0], label='RSI')
        lines_ex[c] = [volumen, RSI]

        plts_ex[c].set_ylim([1, 5])
        plts_ex[c].set_title(f"{c} - PLN")

        plts_ex[c].set_xlabel("time")
        plts_ex[c].set_ylabel("value")

        plts_ex[c].legend()

        itr2 += 1

    fig2.tight_layout(h_pad=0.5)

    data(lines, window, zakres)
