import requests
import matplotlib.pyplot as plt
import numpy as np


def link(currency_type):
    return f'https://bitbay.net/API/Public/{currency_type}/orderbook.json'

def get_data(currency_type):
    try:
        req = requests.get(link(currency_type)).json()
        bid = req['bids']
        ask = req['asks']
    except Exception as e: # obsługa błęów
        print(e)
        return {}

    return bid, ask

def print_offers(offers):
    if len(offers) > 6:
        short_offers = offers[:3] + ['...'] + offers[-3:]
    for offer in short_offers:
       print(offer)

def min_max_values(lists_list):
    min_ = []
    max_ = []
    for element in lists_list:
       min_.append(min(element))
       max_.append(max(element))
    return min(min_), max(max_) 

if __name__ == '__main__':
    SLEEPING_TIME = 5
    CURRENCIES = ['ETHPLN', 'BTCPLN', 'LTCPLN']

    bids = [[],[],[]]
    asks = [[],[],[]]

    plt.ion()
    fig, ax = plt.subplots()
    x, lines = [],[]
    for c in CURRENCIES:
        line_b, = ax.plot([],[], label= c + '_bids', marker='o')
        line_a, = ax.plot([],[], label= c + '_asks', marker='o')
        lines.append([line_b,line_a])

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_yscale("log")
    ax.set_title('Cryptocurrencies buy and sell price')
    ax.set_xlabel('time [s]')
    ax.set_ylabel('value')
    ax.legend()

    i = 0
    while True:
        print(i)
        x.append(i * SLEEPING_TIME)
        
        for j, c in enumerate(CURRENCIES):
            dataset = get_data(c)
            if len(dataset):
                all_bid, all_ask = dataset
                asks[j].append(all_bid [0] [0])
                print("ask: ", asks[j])
                bids[j].append(all_ask [0] [0]) 
                print("bid: ", bids[j])

            else:
                print("nie")
                bids[j].append(None)
                asks[j].append(None)

            if i != 0:            
                min_a, max_a = min_max_values(asks)
                min_b, max_b = min_max_values(bids)

              #  plt.subplot( f"{len(CURRENCIES)}1{j}")

                ax.set_xlim(min(x) * 0.9  , max(x) * 1.1 )
                ax.set_ylim(min(min_a, min_b) * 0.9 , max(max_a, max_b) *1.1 )

                lines[j][0].set_xdata(x)
                lines[j][0].set_ydata(asks[j][i])
                lines[j][1].set_xdata(x)
                lines[j][1].set_ydata(bids[j][i])
            
            else:
                ax.set_xlim(0, 1)
                ax.set_ylim(0.9 * min(bids[0][0], asks[0][0]), 1.1 * max(bids[0][0], asks[0][0]))
                lines[0][0].set_xdata(x)
                lines[0][0].set_ydata(asks[0][0])
                lines[0][1].set_xdata(x)
                lines[0][1].set_ydata(bids[0][0])

            plt.pause(0.1) 
        i += 1
        plt.pause(SLEEPING_TIME)