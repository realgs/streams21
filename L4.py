import requests
from requests.exceptions import HTTPError
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.animation import FuncAnimation
from numpy import *


URL = 'https://bitbay.net/API/Public/'

values_1_bid, values_1_ask = [], []
values_2_bid, values_2_ask = [], []
values_3_bid, values_3_ask = [], []

avg_values_1_bid, avg_values_1_ask = [], []
avg_values_2_bid, avg_values_2_ask = [], []
avg_values_3_bid, avg_values_3_ask = [], []

rsi_values_1_bid, rsi_values_1_ask = [], []
rsi_values_2_bid, rsi_values_2_ask = [], []
rsi_values_3_bid, rsi_values_3_ask = [], []

volume1, volume2, volume3 = [], [], []

t = []


def get_data(currency1, currency2, category1, format1):
    try:
        response = requests.get(f'{URL}/{currency1}-{currency2}/{category1}.{format1}')
        response.raise_for_status()
    except HTTPError as http_error:
        print(f'Error! Operation failed:{http_error}')
    except Exception as error:
        print(f'Error! Operation failed:{error}')
    else:
        data = eval(response.text)
        ask = data['ask']
        bid = data['bid']
        volume = data['volume']
        return ask, bid, volume

def moving_average(data, compartment):
    data_to_average = data[len(data) - compartment:]
    mov_average = sum(data_to_average)/len(data_to_average)
    return mov_average


def calculate_rsi(values_of_bid_or_ask, first, last):
    data_to_rsi = values_of_bid_or_ask[first:last]
    growth, count_growth, loss, count_loss = 0, 0, 0, 0
    for i in range(1, len(data_to_rsi)):
        if data_to_rsi[i-1] < data_to_rsi[i]:
            growth_0 = data_to_rsi[i] - data_to_rsi[i-1]
            growth = growth + growth_0
            count_growth += 1
        elif data_to_rsi[i-1] > data_to_rsi[i]:
            loss_0 = data_to_rsi[i - 1] - data_to_rsi[i]
            loss += loss_0
            count_loss += 1
    if count_growth == 0:
        a = 1
    else:
        a = growth/count_growth
    if count_loss == 0:
        b = 1
    else:
        b = loss/count_loss
    value_of_rsi = 100 - (100/(1+(a/b)))
    return value_of_rsi


def plotting_graph(_):
    ask1, bid1, volume11 = get_data('LSK', 'PLN', 'ticker', 'json')
    ask2, bid2, volume22 = get_data('ETH', 'PLN', 'ticker', 'json')
    ask3, bid3, volume33 = get_data('LTC', 'PLN', 'ticker', 'json')

    values_1_bid.append(bid1)
    values_2_bid.append(bid2)
    values_3_bid.append(bid3)

    values_1_ask.append(ask1)
    values_2_ask.append(ask2)
    values_3_ask.append(ask3)

    avg_values_1_bid.append(moving_average(values_1_bid, SIZE))
    avg_values_2_bid.append(moving_average(values_2_bid, SIZE))
    avg_values_3_bid.append(moving_average(values_3_bid, SIZE))

    avg_values_1_ask.append(moving_average(values_1_ask, SIZE))
    avg_values_2_ask.append(moving_average(values_2_ask, SIZE))
    avg_values_3_ask.append(moving_average(values_3_ask, SIZE))

    volume1.append(volume11)
    volume2.append(volume22)
    volume3.append(volume33)

    rsi_values_1_bid.append(calculate_rsi(values_1_bid, FIRST, LAST))
    rsi_values_2_bid.append(calculate_rsi(values_2_bid, FIRST, LAST))
    rsi_values_3_bid.append(calculate_rsi(values_3_bid, FIRST, LAST))

    rsi_values_1_ask.append(calculate_rsi(values_1_ask, FIRST, LAST))
    rsi_values_2_ask.append(calculate_rsi(values_2_ask, FIRST, LAST))
    rsi_values_3_ask.append(calculate_rsi(values_3_ask, FIRST, LAST))

    timepiece = datetime.now()
    t.append(timepiece.strftime('%X'))

    values_of_all = [
        values_1_bid, values_1_ask,
        values_2_bid, values_2_ask,
        values_3_bid, values_3_ask,

        avg_values_1_bid, avg_values_1_ask,
        avg_values_2_bid, avg_values_2_ask,
        avg_values_3_bid, avg_values_3_ask,

        rsi_values_1_bid, rsi_values_1_ask,
        rsi_values_2_bid, rsi_values_2_ask,
        rsi_values_3_bid, rsi_values_3_ask,

        volume1, volume2, volume3,
        t
    ]

    for value in values_of_all:
        if len(value) > 15:
            value.pop(0)

    plt.clf()
    plt.subplot(3, 3, 1)
    plt.title('Chart bid and ask LSK', fontsize=8)
    plt.plot(t, values_1_bid, 'b-', label="bid")
    plt.plot(t, values_1_ask, 'g-', label="ask")
    plt.plot(t, avg_values_1_bid, 'r--', label="avg_bid")
    plt.plot(t, avg_values_1_ask, 'y--', label="avg_ask")
    plt.ylabel('Currency rate LSK', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.xticks(rotation=70, fontsize=8)

    plt.subplot(3, 3, 2)
    plt.title('Chart bid and ask ETH', fontsize=8)
    plt.plot(t, values_2_bid, 'b-', label="bid")
    plt.plot(t, values_2_ask, 'g-', label="ask")
    plt.plot(t, avg_values_2_bid, 'r--', label="avg_bid")
    plt.plot(t, avg_values_2_ask, 'y--', label="avg_ask")
    plt.ylabel('Currency rate ETH', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.xticks(rotation=70, fontsize=8)

    plt.subplot(3, 3, 3)
    plt.title('Chart bid and ask LTC', fontsize=8)
    plt.plot(t, values_3_bid, 'b-', label="bid")
    plt.plot(t, values_3_ask, 'g-', label="ask")
    plt.plot(t, avg_values_3_bid, 'r--', label="avg_bid")
    plt.plot(t, avg_values_3_ask, 'y--', label="avg_ask")
    plt.ylabel('Currency rate LTC', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.xticks(rotation=70, fontsize=8)

    plt.subplot(3, 3, 4)
    plt.title('Chart of volume LSK', fontsize=8)
    plt.bar(t, volume1, label="volume LSK")
    plt.ylabel('amount of volume', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    #plt.xticks(rotation=70, fontsize=6)
    plt.xticks([])

    plt.subplot(3, 3, 5)
    plt.title('Chart of volume ETH', fontsize=8)
    plt.bar(t, volume2, label="volume ETH")
    plt.ylabel('amount of volume', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    #plt.xticks(rotation=70, fontsize=6)
    plt.xticks([])

    plt.subplot(3, 3, 6)
    plt.title('Chart of volume LTC', fontsize=8)
    plt.bar(t, volume3, label="volume LTC")
    plt.ylabel('amount of volume', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    #plt.xticks(rotation=70, fontsize=6)
    plt.xticks([])

    plt.subplot(3, 3, 7)
    plt.title('Chart of RSI LSK', fontsize=8)
    plt.plot(t, rsi_values_1_bid, 'b-', label="rsi_bid")
    plt.plot(t, rsi_values_1_ask, 'y--', label="rsi_ask")
    plt.ylabel('Value of RSI', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    #plt.xticks(rotation=70, fontsize=6)
    plt.xticks([])

    plt.subplot(3, 3, 8)
    plt.title('Chart of RSI ETH', fontsize=8)
    plt.plot(t, rsi_values_2_bid, 'b-', label="rsi_bid")
    plt.plot(t, rsi_values_2_ask, 'y--', label="rsi_ask")
    plt.ylabel('Value of RSI', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    #plt.xticks(rotation=70, fontsize=6)
    plt.xticks([])

    plt.subplot(3, 3, 9)
    plt.title('Chart of RSI LTC', fontsize=8)
    plt.plot(t, rsi_values_3_bid, 'b-', label="rsi_bid")
    plt.plot(t, rsi_values_3_ask, 'y--', label="rsi_ask")
    plt.ylabel('Value of RSI', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    #plt.xticks(rotation=70, fontsize=6)
    plt.xticks([])
    plt.tight_layout()


if __name__ == '__main__':
    SIZE = int(input('Podaj wielkość przedziału do liczenia średniej ruchomej z zakresu <0,15>: '))
    FIRST = int(input('Podaj początek przedziału do liczenia RSI: '))
    LAST = int(input('Podaj koniec przedziału do liczenia RSI: '))

    INTERVAL = 5
    simulation = FuncAnimation(plt.figure(), plotting_graph, interval=1000*INTERVAL)
    plt.style.use('seaborn')
    plt.show()