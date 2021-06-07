import requests
from requests.exceptions import HTTPError
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.animation import FuncAnimation
from numpy import *
import time
import json

URL = 'https://bitbay.net/API/Public/'
FILE_NAME = 'customer_transaction'

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
        return ask, bid

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

def get_volumen(currency1, currency2):
    url = f"https://api.bitbay.net/rest/trading/transactions/{currency1}-{currency2}"
    fromtime = (datetime.now() - timedelta(minutes=1))
    fromtime = int(fromtime.timestamp()) * 1000
    queryparams = {'fromTime': fromtime}
    response = requests.request("GET", url, params=queryparams)
    response = eval(response.text)
    return sum([float(response['items'][i]['a']) for i in range(len(response['items']))])


def trend_of_rsi(list_of_rsi_values):
    indicator_rsi = list_of_rsi_values[-1]
    if indicator_rsi >= 70:
        return 'Rising trend'
    elif indicator_rsi <= 30:
        return 'Falling trend'
    elif 70 > indicator_rsi > 30:
        return 'Sideways trend'


def candidate(list_of_trend, list_of_volume):
    list_of_currency = ['LSK-PLN', 'ETH-PLN', 'LTC-PLN']
    volumens_of_all = {}
    for i in range(len(list_of_currency)):
        if list_of_trend[i] == 'Rising trend' or 'Sideways trend':
            volumens_of_all[list_of_volume[i][-1]] = i
    if volumens_of_all:
        max_volumen = max(volumens_of_all)
        return list_of_currency[volumens_of_all[max_volumen]]
    else:
        return 'there is no stock'


def fluctuation(list_of_ask, x, y):
    fluctuation_list = list_of_ask[-y:]
    maxi = max(fluctuation_list)
    mini = min(fluctuation_list)
    fluctuation_value = (abs(maxi - mini) / maxi) * 100
    if fluctuation_value > x:
        return 'Volatile asset'
    else:
        return ''

def spread(list_of_ask, list_of_bid, s):
    purchase = list_of_ask[-1]
    sale = list_of_bid[-1]
    spread_value = ((purchase - sale) / purchase) * 100
    if spread_value < s:
        return 'Liquid asset'
    else:
        return ''



def plotting_graph(_):
    ask1, bid1 = get_data('LSK', 'PLN', 'ticker', 'json')
    ask2, bid2 = get_data('ETH', 'PLN', 'ticker', 'json')
    ask3, bid3 = get_data('LTC', 'PLN', 'ticker', 'json')

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

    volume1.append(get_volumen('LSK', 'PLN'))
    volume2.append(get_volumen('ETH', 'PLN'))
    volume3.append(get_volumen('LTC', 'PLN'))

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
        # while len(value) > 3:
            value.pop(0)


    trend_1_ask = trend_of_rsi(rsi_values_1_ask)
    trend_2_ask = trend_of_rsi(rsi_values_2_ask)
    trend_3_ask = trend_of_rsi(rsi_values_3_ask)

    trend_1_bid = trend_of_rsi(rsi_values_1_bid)
    trend_2_bid = trend_of_rsi(rsi_values_2_bid)
    trend_3_bid = trend_of_rsi(rsi_values_3_bid)

    if AB == 'A':
        candidate1 = candidate([trend_1_ask, trend_2_ask, trend_3_ask], [volume1, volume2, volume3])
    else:
        candidate1 = candidate([trend_1_bid, trend_2_bid, trend_3_bid], [volume1, volume2, volume3])

    title_of_candidate = f'- Candidate'
    list_of_currency = ['LSK-PLN', 'ETH-PLN', 'LTC-PLN']
    list_of_ask1 = [values_1_ask, values_2_ask, values_3_ask]
    list_of_bid1 = [values_1_bid, values_2_bid, values_3_bid]
    list_of_fluctuation = []
    list_of_spread = []
    list_of_title_candidate = []
    for i in range(len(list_of_currency)):
        if list_of_currency[i] == candidate1:
            spread0 = spread(list_of_ask1[i], list_of_bid1[i], S)
            fluctuation0 = fluctuation(list_of_ask1[i], X, Y)
            list_of_fluctuation.insert(i, spread0)
            list_of_spread.insert(i, fluctuation0)
            list_of_title_candidate.insert(i, title_of_candidate)
        else:
            list_of_fluctuation.insert(i, '')
            list_of_spread.insert(i, '')
            list_of_title_candidate.insert(i, '')

    fluctuation1, fluctuation2, fluctuation3 = list_of_fluctuation[0], list_of_fluctuation[1], list_of_fluctuation[2]
    spread1, spread2, spread3 = list_of_spread[0], list_of_spread[1], list_of_spread[2]
    title_candidate1, title_candidate2, title_candidate3 = list_of_title_candidate[0], list_of_title_candidate[1], list_of_title_candidate[2]

    f = open(f"C:\\Users\\Lenovo\\PycharmProjects\\L6\\{FILE_NAME}.json", "r")
    data = json.load(f)
    f.close()



    average_LSK_buy1 = [data['average_LSK_buy'][-1]] * len(t)
    average_ETH_buy1 = [data['average_ETH_buy'][-1]] * len(t)
    average_LTC_buy1 = [data['average_LTC_buy'][-1]] * len(t)

    profit_LSK = data['LSK_profit_loss1'][-1]
    profit_ETH = data['ETH_profit_loss1'][-1]
    profit_LTC = data['LTC_profit_loss1'][-1]

    plt.clf()
    plt.subplot(3, 3, 1)
    plt.title(f'Bid and ask LSK-PLN {title_candidate1} \n {fluctuation1} \n {spread1} \n {profit_LSK}', fontsize=8)
    plt.plot(t, values_1_bid, 'b-', label="bid")
    plt.plot(t, values_1_ask, 'g-', label="ask")
    plt.plot(t, avg_values_1_bid, 'r--', label="avg_bid")
    plt.plot(t, avg_values_1_ask, 'y--', label="avg_ask")
    plt.plot(t, average_LSK_buy1, 'c--', label="avg_cus")
    plt.ylabel('Currency rate LSK', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.xticks(rotation=70, fontsize=8)

    plt.subplot(3, 3, 2)
    plt.title(f'Bid and ask ETH-PLN {title_candidate2} \n {fluctuation2} \n {spread2} \n {profit_ETH}', fontsize=8)
    plt.plot(t, values_2_bid, 'b-', label="bid")
    plt.plot(t, values_2_ask, 'g-', label="ask")
    plt.plot(t, avg_values_2_bid, 'r--', label="avg_bid")
    plt.plot(t, avg_values_2_ask, 'y--', label="avg_ask")
    plt.plot(t, average_ETH_buy1, 'c--', label="avg_cus")
    plt.ylabel('Currency rate ETH', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.xticks(rotation=70, fontsize=8)

    plt.subplot(3, 3, 3)
    plt.title(f'Bid and ask LTC-PLN {title_candidate3} \n {fluctuation3} \n {spread3} \n {profit_LTC}', fontsize=8)
    plt.plot(t, values_3_bid, 'b-', label="bid")
    plt.plot(t, values_3_ask, 'g-', label="ask")
    plt.plot(t, avg_values_3_bid, 'r--', label="avg_bid")
    plt.plot(t, avg_values_3_ask, 'y--', label="avg_ask")
    plt.plot(t, average_LTC_buy1, 'c--', label="avg_cus")
    plt.ylabel('Currency rate LTC', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.xticks(rotation=70, fontsize=8)

    plt.subplot(3, 3, 4)
    plt.title('Volume LSK', fontsize=8)
    plt.bar(t, volume1, label="volume LSK")
    plt.ylabel('amount of volume', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    #  plt.xticks(rotation=70, fontsize=6)
    plt.xticks([])

    plt.subplot(3, 3, 5)
    plt.title('Volume ETH', fontsize=8)
    plt.bar(t, volume2, label="volume ETH")
    plt.ylabel('amount of volume', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    # plt.xticks(rotation=70, fontsize=6)
    plt.xticks([])

    plt.subplot(3, 3, 6)
    plt.title('Volume LTC', fontsize=8)
    plt.bar(t, volume3, label="volume LTC")
    plt.ylabel('amount of volume', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    # plt.xticks(rotation=70, fontsize=6)
    plt.xticks([])

    plt.subplot(3, 3, 7)
    plt.title(f'RSI LSK- {trend_1_ask}', fontsize=8)
    plt.plot(t, rsi_values_1_bid, 'b-', label="rsi_bid")
    plt.plot(t, rsi_values_1_ask, 'y-', label="rsi_ask")
    plt.ylabel('Value of RSI', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    # plt.xticks(rotation=70, fontsize=6)
    plt.xticks([])

    plt.subplot(3, 3, 8)
    plt.title(f'RSI ETH - {trend_2_ask}', fontsize=8)
    plt.plot(t, rsi_values_2_bid, 'b-', label="rsi_bid")
    plt.plot(t, rsi_values_2_ask, 'y-', label="rsi_ask")
    plt.ylabel('Value of RSI', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    # plt.xticks(rotation=70, fontsize=6)
    plt.xticks([])

    plt.subplot(3, 3, 9)
    plt.title(f'RSI LTC - {trend_3_ask}', fontsize=8)
    plt.plot(t, rsi_values_3_bid, 'b-', label="rsi_bid")
    plt.plot(t, rsi_values_3_ask, 'y-', label="rsi_ask")
    plt.ylabel('Value of RSI', fontsize=8)
    plt.xlabel('Time', fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    # plt.xticks(rotation=70, fontsize=6)
    plt.xticks([])
    plt.tight_layout()


if __name__ == '__main__':
    SIZE = 4  # int(input('Podaj wielkość przedziału do liczenia średniej ruchomej z zakresu <0,15>: '))
    FIRST = 1  # int(input('Podaj początek przedziału do liczenia RSI: '))
    LAST = 4  # int(input('Podaj koniec przedziału do liczenia RSI: '))
    X = 5
    Y = 3
    S = 8
    AB = 'A'  # str(input('if you want to classify the RSI indicator for ask write A, if for bid write B: '))
    INTERVAL = 3
    simulation = FuncAnimation(plt.figure(), plotting_graph, interval=1000*INTERVAL)
    plt.style.use('seaborn')
    plt.show()