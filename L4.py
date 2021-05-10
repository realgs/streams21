import requests
from requests.exceptions import HTTPError
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.animation import FuncAnimation
from numpy import *

URL = 'https://bitbay.net/API/Public/'

def get_data(currency1, currency2, category1, format1):
    try:
        response = requests.get(f'{URL}/{currency1}-{currency2}/{category1}.{format1}')
        response.raise_for_status()
    except HTTPError as http_error:
        print(f'Error! Operation failed:{http_error}')
    except Exception as error:
        print(f'Error! Operation failed:{error}')
    else:
        #  data = eval(response.text)
        data = response.json()
        return data

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
    values_1_bid.append(y1['bid'])
    values_1_ask.append(y1['ask'])
    values_2_bid.append(y2['bid'])
    values_2_ask.append(y2['ask'])
    values_3_bid.append(y3['bid'])
    values_3_ask.append(y3['ask'])

    avg_values_1_bid.append(moving_average(values_1_bid, SIZE))
    avg_values_1_ask.append(moving_average(values_1_ask, SIZE))
    avg_values_2_bid.append(moving_average(values_2_bid, SIZE))
    avg_values_2_ask.append(moving_average(values_2_ask, SIZE))
    avg_values_3_bid.append(moving_average(values_3_bid, SIZE))
    avg_values_3_ask.append(moving_average(values_3_ask, SIZE))

    volume1.append(y1['volume'])
    volume2.append(y2['volume'])
    volume3.append(y3['volume'])

    rsi_values_1_bid.append(calculate_rsi(values_1_bid, FIRST, LAST))
    rsi_values_1_ask.append(calculate_rsi(values_1_ask, FIRST, LAST))
    rsi_values_2_bid.append(calculate_rsi(values_2_bid, FIRST, LAST))
    rsi_values_2_ask.append(calculate_rsi(values_2_ask, FIRST, LAST))
    rsi_values_3_bid.append(calculate_rsi(values_3_bid, FIRST, LAST))
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

    for elem in values_of_all:
        if len(elem) > 3:
            elem.pop(0)

    plt.clf()
    plt.subplot(3, 3, 1)
    plt.title('chart bid and ask LSK', fontsize=8)
    plt.plot(t, values_1_bid, 'b-', label="bid")
    plt.plot(t, values_1_ask, 'g-', label="ask")
    plt.plot(t, avg_values_1_bid, 'r--', label="avg_bid")
    plt.plot(t, avg_values_1_ask, 'y--', label="avg_ask")
    plt.ylabel('price LSK', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')

    plt.subplot(3, 3, 2)
    plt.title('chart bid and ask ETH', fontsize=8)
    plt.plot(t, values_2_bid, 'b-', label="bid")
    plt.plot(t, values_2_ask, 'g-', label="ask")
    plt.plot(t, avg_values_2_bid, 'r--', label="avg_bid")
    plt.plot(t, avg_values_2_ask, 'y--', label="avg_ask")
    plt.ylabel('price ETH', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')

    plt.subplot(3, 3, 3)
    plt.title('chart bid and ask LTC', fontsize=8)
    plt.plot(t, values_3_bid, 'b-', label="bid")
    plt.plot(t, values_3_ask, 'g-', label="ask")
    plt.plot(t, avg_values_3_bid, 'r--', label="avg_bid")
    plt.plot(t, avg_values_3_ask, 'y--', label="avg_ask")
    plt.ylabel('price LTC', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')

    plt.subplot(3, 3, 4)
    plt.title('chart of volume LSK', fontsize=8)
    plt.bar(t, volume1, label="volume LSK")
    plt.ylabel('amount of volume', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')

    plt.subplot(3, 3, 5)
    plt.title('chart of volume ETH', fontsize=8)
    plt.bar(t, volume2, label="volume ETH")
    plt.ylabel('amount of volume', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')

    plt.subplot(3, 3, 6)
    plt.title('chart of volume LTC', fontsize=8)
    plt.bar(t, volume3, label="volume LTC")
    plt.ylabel('amount of volume', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')

    plt.subplot(3, 3, 7)
    plt.title('chart of RSI LSK', fontsize=8)
    plt.plot(t, rsi_values_1_bid, 'b-', label="rsi_bid")
    plt.plot(t, rsi_values_1_ask, 'y--', label="rsi_ask")
    plt.ylabel('Value of RSI', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')

    plt.subplot(3, 3, 8)
    plt.title('chart of RSI ETH', fontsize=8)
    plt.plot(t, rsi_values_2_bid, 'b-', label="rsi_bid")
    plt.plot(t, rsi_values_2_ask, 'y--', label="rsi_ask")
    plt.ylabel('Value of RSI', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')

    plt.subplot(3, 3, 9)
    plt.title('chart of RSI LTC', fontsize=8)
    plt.plot(t, rsi_values_3_bid, 'b-', label="rsi_bid")
    plt.plot(t, rsi_values_3_ask, 'y--', label="rsi_ask")
    plt.ylabel('Value of RSI', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.tight_layout()


if __name__ == '__main__':
    SIZE = int(input('Podaj wielkość przedziału do liczenia średniej ruchomej z zakresu <5,20>: '))
    FIRST = int(input('Podaj początek przedziału do liczenia RSI: '))
    LAST = int(input('Podaj koniec przedziału do liczenia RSI: '))

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

    y1 = get_data('LSK', 'PLN', 'ticker', 'json')
    y2 = get_data('ETH', 'PLN', 'ticker', 'json')
    y3 = get_data('LTC', 'PLN', 'ticker', 'json')

    t = []

    INTERVAL = 5
    simulation = FuncAnimation(plt.figure(), plotting_graph, interval=1000*INTERVAL)
    plt.style.use('seaborn')
    plt.show()
