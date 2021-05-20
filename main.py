import numpy as np
from math import inf
import requests
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from itertools import count
import copy
import time



def get_data(crypt):
    url = "https://bitbay.net/API/Public/{Currency}/{Category}.json".format(Currency=crypt,
                                                                                            Category= 'ticker')
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        buy = response['ask']
        sell = response['bid']
        return buy, sell
    else:
        print("Can't get data from API \n status code: ", response.status_code)

def get_volume(crypt):
    url = "https://api.bitbay.net/rest/trading/transactions/{currency}".format(currency= crypt)
    response = requests.get(url)
    response = response.json()
    if response['status'] == 'Ok':
        volume = float(response['items'][1]['a'])
        return volume
    else:
        print("Can't get data from API \n status code: ", response['status'])


def average(data_list, n):
    sub_data = data_list[-n:]
    avg = sum(sub_data)/len(sub_data)
    return avg


def count_rsi(data_list, start, stop):
    sub_data = data_list[-10:]
    sub_data = sub_data[start:stop]
    rises = 0
    rises_counter = 0
    losses = 0
    losses_counter = 0
    for i in range(1, len(sub_data)):
        if sub_data[i - 1] < sub_data[i]:
            rise = sub_data[i] - sub_data[i - 1]
            rises += rise
            rises_counter += 1
        elif sub_data[i - 1] > sub_data[i]:
            loss = sub_data[i - 1] - sub_data[i]
            losses += loss
            losses_counter += 1
    if rises_counter == 0:
        a = 1
    else:
        a = rises/rises_counter
    if losses_counter == 0:
        b = 1
    else:
        b = losses/losses_counter
    rsi = 100 - (100 / (1 + (a / b)))
    return rsi

def data_stream(crypt, buy_list, sell_list, avg_buy_list, avg_sell_list, volume_list, rsi_buy_list, rsi_sell_list):
    buy, sell = get_data(crypt)
    buy_list.append(buy)
    sell_list.append(sell)
    buy_avg = average(buy_list, N)
    sell_avg = average(sell_list, N)

    avg_buy_list.append(buy_avg)
    avg_sell_list.append(sell_avg)
    volume_list.append(get_volume(crypt))

    rsi_buy_list.append(count_rsi(buy_list, START, STOP))
    rsi_sell_list.append(count_rsi(sell_list, START, STOP))
    return buy_list, sell_list, avg_buy_list, avg_sell_list, volume_list, rsi_buy_list, rsi_sell_list


def animate(i):
    global param
    buy, sell, avg1, avg2, vol, rsi_buy, rsi_sell = data_stream(CURRENCY[param], buys, sells, avg_buy, avg_sell, volume, rsi_buy_values, rsi_sell_values)
    t.append(time.strftime("%H:%M:%S", time.localtime()))
    for i in [buy, sell, avg1, avg2, vol, rsi_buy, rsi_sell, t]:
        if len(i) > 10:
            i.pop(0)
    plt.clf()
    plt.subplot(311)
    plt.title(f'{CURRENCY[param]} chart')
    plt.plot(t, buy, label="buys", color="green")
    plt.plot(t, sell, label="sells", color="red")
    plt.plot(t, avg1, '--', label='buy avg', color='yellow')
    plt.plot(t, avg2, '--', label='sell avg', color='pink')
    plt.ylabel("Currency rate")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks([])

    plt.subplot(312)
    plt.title('Volume chart')
    plt.bar(t, vol, label='volume', color='gray')
    plt.xticks([])
    plt.ylabel("Volume values")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

    plt.subplot(313)
    plt.title('RSI chart')
    plt.plot(t, rsi_buy, label='buy RSI', color='orange')
    plt.plot(t, rsi_sell, ':', label='sell RSI', color='purple')
    plt.ylabel("RSI value")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(rotation='vertical')
    plt.xlabel("Time")
    plt.tight_layout()


def plot_data():
    global TIME_SLEEP
    animation = FuncAnimation(plt.figure(), func=animate, interval=TIME_SLEEP)
    plt.show()


if __name__ == "__main__":
    TIME_SLEEP = 5000
    param = int(input("Wybierz walutę:"))
    CURRENCY = ["OMG-PLN", "BTC-PLN", "ETH-PLN"]
    N = 5 # input("Liczba próbek do wyliczenia średniej: ")#average
    START = 0 # input("Początek przdziału do wyliczenia RSI: ") #rsi start
    STOP = 10 # input("Koniec przdziału do wyliczenia RSI: ") # rsi stop
    buys = []
    sells = []
    avg_buy = []
    avg_sell = []
    volume = []
    rsi_buy_values = []
    rsi_sell_values = []
    t = []

    plot_data()

