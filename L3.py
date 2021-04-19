from requests import get
import sys
import matplotlib.pyplot as plt
import numpy as np

def connection(currency1, currency2):
    return f'https://bitbay.net/API/Public/{currency1}{currency2}/orderbook.json'

def get_values(currency1):
    try:
        req = get(connection(currency1, 'USD')).json()
        bid = req['bids']
        ask = req['asks']
    except Exception as e:
        print(e)
    return bid, ask

def print_offers(offers):
    offer_parts = offers[:1] + ['...'] + offers[-1:]
    for offer in offer_parts:
        print(offer)
    return offer

def calc_diffrence(currency1):
    bids, asks = get_values(currency1)
    bid = bids[0][0]
    ask = asks[0][0]
    difference = (1 - (ask - bid) / bid)
    print(currency1)
    print('bid: ', bid, '\nask: ', ask, '\ndifference: ', round(difference, 3), '%', '\n')
    return difference

def draw_graph(datas, interval):
    plt.ion()
    freq = [i for i in range(0,5 * len(datas), 5)]
    for i in range(len(datas[0])):
        y_label = []
        for part in datas:
            y_label.append(part[i][1])
        plt.plot(freq, y_label, '-h', label = datas[0][i][0])
    plt.legend(loc='upper right')
    plt.title('Bids vs. asks', color='r')
    plt.xlabel('time')
    plt.ylabel('value')
    plt.xlim([-1,freq[-1]+1])
    plt.draw()
    plt.pause(interval)
    plt.clf()

def make_graph(currency1, currency2, interval):
    datas = []
    while True:
        temp_list = []
        for i in currency1:
            temp_list.append([i +' | '+ currency2, calc_diffrence(i)])
        datas.append(temp_list)
        draw_graph(datas, interval)

