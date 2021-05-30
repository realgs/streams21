import requests
import matplotlib.pyplot as plt
import numpy as np
from sys import exit
from datetime import datetime, timedelta

def link(currency_type, type): #sklejone wszystkie url
    if type == 'ticker':
        return f'https://bitbay.net/API/Public/{currency_type}/ticker.json'
    if type == 'transactions':
        return f'https://api.bitbay.net/rest/trading/transactions/{currency_type}'

def get_data(currency_type):
    try:
        req = requests.get(link(currency_type, 'ticker'))
        req_json = req.json()
        bid = req_json['bid']
        ask = req_json['ask']
        print (req.status_code)
    except Exception as e: # obsługa błęów błędy obsługi -> status code
        print(e)
        print (req.status_code)
        return {}

    return bid, ask


def get_volumen(currency_type):
    fromtime = int((datetime.now() - timedelta(seconds=60)).timestamp()) * 1000
    queryparams = {'fromTime': fromtime}
    response = requests.request("GET", link(currency_type, 'transactions'), params=queryparams)
    response = eval(response.text)
    return sum([float(response['items'][i]['a']) for i in range(len(response['items']))])



def list_average(list_, elements_a):# blad krotkosci - nie ma: jezeli probek jest mniej, to używamy wszytskie które są
    data = list_[-elements_a:]
    if elements_a > len (list_) - 3:
        print ("The number of elements is smaller than list length, but it doesn't matter bcs we use all we have")
        print(data)
    return sum(data) / len(data)

def RSI_value(list_, elements_r):
    data = list_[- elements_r:]
    up = 0
    up_c = 0
    down = 0
    down_c = 0
    for i in range(1, len(data)):
        if data[i - 1] < data[i]:
            up += data[i] - data[i - 1]
            up_c += 1
        elif data[i - 1] > data[i]:
            down+= data[i - 1] - data[i]
            down_c += 1
    if up_c == 0:
        a = 1
    else:
        a = up/up_c
    if down_c == 0:
        b = 1
    else:
        b = down/down_c
    RSI = 100 - (100 / (1 + (a / b)))
    return RSI

def draw_axes():
    fig, axs = plt.subplots(3, 3, figsize=(12, 5), constrained_layout=True)
    for i, currency_type in enumerate(CURRENCIES):
        plt.suptitle('Cryptocurrencies traiding',fontsize=24)
        axs[0][i].set_title(currency_type)
        axs[0][i].set_xlabel('Time')
        axs[0][i].set_ylabel('Value')
        axs[1][i].set_title('Volume')
        axs[1][i].set_xlabel('Time')
        axs[1][i].set_ylabel('Value')
        axs[2][i].set_title('RSI')
        axs[2][i].set_xlabel('Time')
        axs[2][i].set_ylabel('Value')
    return fig, axs


def add_avgRSI(buy_list, sell_list, avg_buy_list, avg_sell_list, RSI_buy_list, RSI_sell_list, currency_type):
    buy, sell = get_data(currency_type)
    buy_list.append(buy)
    sell_list.append(sell)
    buy_avg = list_average(buy_list, elements_a)
    sell_avg = list_average(sell_list, elements_a)
    avg_buy_list.append(buy_avg)
    avg_sell_list.append(sell_avg)
    RSI_buy_list.append(RSI_value(buy_list, elements_r))
    RSI_sell_list.append(RSI_value(sell_list, elements_r))
    return avg_buy_list, avg_sell_list, RSI_buy_list, RSI_sell_list


def add_values(buy, sell, volume, currency_type):
    data = get_data(currency_type)
    buy.append(data[0])
    sell.append(data[1])
    volume.append(get_volumen(currency_type))
    return buy, sell, volume

def check_trend(list):
    avg = list_average(list, len(list))
    trend = list[-1]
    if avg > trend:
        return 'Upward trend'
    elif avg < trend:
        return 'Downward trend'
    else:
        return 'Sideways trend'

def check_voltaile(buy_list, X, Y):
    if len(buy_list) < Y:
        return '---'
    y_samples = buy_list[-Y:]
    oscilation = ((max(y_samples) - min(y_samples))/max(y_samples)) * 100
    if oscilation > X:
        return 'Volatile asset'
    else:
        return '---'


def check_liquid(buy_list, sell_list, S):
    difference = ((buy_list[-1] - sell_list[-1])/buy_list[-1]) * 100
    if difference < S:
        return 'Liquid asset'
    else:
        return '---'

def draw_plot(time_interval):

    fig, axs = draw_axes()
    buy, sell, volume, buy_list, sell_list, avg_buy_list, avg_sell_list, rsi_buy_list, rsi_sell_list = [], [], [], [], [], [], [], [], []
    i = 0
    while True:
        for a, currency_type in enumerate(CURRENCIES):
            add_values(buy, sell, volume, currency_type)
            avg_buy, avg_sell, buy_RSI, sell_RSI = add_avgRSI(buy_list, sell_list, avg_buy_list, avg_sell_list, rsi_buy_list, rsi_sell_list, currency_type)
            if len(buy) and len(sell) and len(buy_RSI) and len(sell_RSI) >= 2:
        
                x = [(i - 1) * time_interval, i * time_interval]
                selling_cost = [sell[-2], sell[-1]]
                purchase_cost = [buy[-2], buy[-1]]
                volume_value = [volume[-2], volume[-1]]
                avg_buy_value = [avg_buy[-2], avg_buy[-1]]
                avg_sell_value = [avg_sell[-2], avg_sell[-1]]
                RSI_buy_value = [buy_RSI[-2], buy_RSI[-1]]
                RSI_sell_value = [sell_RSI[-2], sell_RSI[-1]]
                axs[0][a].plot(x, selling_cost, label="Selling cost", color='red')
                axs[0][a].plot(x, purchase_cost, label="Purchase cost", color='yellow')
                axs[0][a].plot(x, avg_buy_value, '--', label='Average Buy Cost', color='darkred')
                axs[0][a].plot(x, avg_sell_value, '--', label='Average Sell Cost', color='#9B870C')

                axs[1][a].bar(x, volume_value, label='Volume ', color='purple')
                axs[1][a].set_xticks([])

                axs[2][a].plot(x, RSI_buy_value, label='RSI buy', color='lightgreen' )
                axs[2][a].plot(x, RSI_sell_value, label='RSI sell', color='darkgreen')

                if len(buy) and len(sell) and len(buy_RSI) and len(sell_RSI) == 2:
                    axs[0][2].legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
                    axs[1][2].legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
                    axs[2][2].legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
                
        i += 1
        plt.pause(time_interval)


def check_value(name):
    if str(name) == 'c':
        if name not in [0, 1, 2]:
            print("Niepoprawny format")
            exit()
    if str(name) == 'elements_a_start' or str(name) == 'elements_r' or str(name) == 'elements_a_stop':
        if name.type != int:
            print("Niepoprawny format")
            exit()
            
        if name > 30:
            print("Niepoprawny format")
            exit()


if __name__ == '__main__':
    SLEEPING_TIME = 5
    CURRENCIES = ['ETH-PLN', 'BTC-PLN', 'LTC-PLN']

    # c = int(input("Wybierz walutę: 0 - ethereum, 1 - bitcoin, 2 - litecoin "))
    # check_value(c)
    # currency_type = CURRENCIES[c]
    # # elements_a_start = int(input("Podaj początek przedziału wyliczania średniej "))
    # # check_value(elements_a_start)
    # a
    # # elements_a_stop = int(input("Podaj koniec przedziału wyliczania średniej "))
    # # check_value(elements_a_stop)
    # # if elements_a_start > elements_a_stop:
    #     # print("Niepoprawny format")
    #     # exit()
    # elements_r = int(input("Podaj liczbę próbek do wyliczania espolczynnika RSI "))
    # check_value(elements_r)

   # currency_type = "ETH-PLN"
    elements_a = 10
    elements_a_start = 10
    elements_a_stop = 15
    elements_r = 15

    draw_plot(SLEEPING_TIME)
