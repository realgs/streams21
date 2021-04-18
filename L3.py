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

def draw_graph(all_data, interval):
    plt.ion()
    freq = np.arange(0, 5 * (len(all_data)), 5)
    iteration = len(all_data[0])
    for i in range(iteration):
        y = []
        for part in all_data:
            y.append(part[i][1])
        plt.plot(freq, y, '-h', label = all_data[0][i][0])
    plt.legend(loc='upper right')
    plt.title('Bids vs. asks', color='r')
    plt.xlabel('time')
    plt.ylabel('value')
    plt.xlim([-0.1,freq[-1]+1])
    plt.draw()
    plt.pause(interval)
    plt.clf()

def make_graph(currency1, currency2, interval):
    all_data = []
    while True:
        temp_list = []
        for i in currency1:
            temp_list.append([i +' | '+ currency2, calc_diffrence(i)])
        all_data.append(temp_list)
        draw_graph(all_data, interval)

if __name__ == '__main__':
    interval = 5
    currency1 = ['BTC', 'LTC', 'TRX']
    currency2 = 'USD'
    try:
        make_graph(currency1, currency2, interval)
    except KeyboardInterrupt:
        print('User hit the interrupt key')
        sys.exit()
