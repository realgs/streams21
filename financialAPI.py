import time
import requests
import statistics
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


def calculate(data, currency, beginning, end):
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

    print(diffrence, diffrence2)
    return diffrence


xrang = 8


def create_graph(j, lines):
    for c, l in lines.items():
        data = data_currency[c]
        data2 = data_currency_extra[c]
        buy = []
        sell = []
        tim = []
        buy_average = []
        sell_average = []
        RSI = []
        volumen = []
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
            # dodać przerywane linie
            l[0].set_data(itr, buy)
            l[1].set_data(itr, sell)
            l[2].set_data(itr, buy_average)
            l[3].set_data(itr, sell_average)
            plts[c].set_xticklabels(tim, rotation='horizontal', fontsize=7)
            plts[c].set_xlim(0, xrang-1)

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

            if min(RSI) >= min(volumen):
                bottom1 = min(volumen)
            else:
                bottom1 = min(RSI)

            if max(RSI) <= max(volumen):
                top1 = max(volumen)
            else:
                top1 = max(RSI)
            plts_ex[c].legend(labels=[f'Volumen: {volumen[-1]}', f'RSI: {RSI[-1]}'])
            plts_ex[c].set_ylim([bottom1*0.95, top1*1.05])

    plt.draw()
    plt.pause(1e-17)


if __name__ == "__main__":

    window = int(input("podaj koniec zakresu z którego chcesz otrzymać średnią: "))
    zakres = int(input("podaj koniec zakresu z którego chcesz otrzymać RSI: "))
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
        buy_average, = plts[c].plot([0], [0], label='buy_average')
        sell_average, = plts[c].plot([0], [0], label='sell_average')
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
