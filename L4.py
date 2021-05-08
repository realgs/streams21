import requests
import matplotlib.pyplot as plt
from sys import exit
import time
from matplotlib.animation import FuncAnimation

N=int(input('How many samples would you like to consider (max 20):' ))
upper=int(input('Input upper bount of the range in which you would like to calculate RSI (0, 20):'))
lower=int(input('Input lower bount of the range in which you would like to calculate RSI (0, 20):'))
curr=str(input('Choose the currency:'))

volumen_list = []
ask_list = []
bid_list = []
ask_graph = []
bid_graph = []
avg_bid_graph = []
avg_ask_graph = []
rsi_bid = []
rsi_ask = []
t = []


def connect(currency1, currency2):
    return f'https://bitbay.net/API/Public/{currency1}{currency2}/ticker.json'


def get_values(currency1):
    try:
        req = requests.get ( connect ( currency1, "PLN" ) ).json ()
        bid = req['bid']
        ask = req['ask']
        volume = req['volume']


    except Exception as e:
        print('ERROR:', e)
        return {}

    return bid, ask, volume


def calc_avg(data, n):
    sub_data = data[-n:]
    avg = sum(sub_data)/len(sub_data)

    return avg


def calc_RSI(data, lower, upper):
    sub_data = data[-20:]
    sub_data = sub_data[lower:upper]
    rises = 0
    rises_count = 0
    losses = 0
    losses_count = 0
    for i in range (1,len(sub_data)):
        if sub_data[i - 1] < sub_data[i]:
            rise = sub_data[i] - sub_data[i - 1]
            rises += rise
            rises_count += 1
        elif sub_data[i - 1] > sub_data[i]:
            loss = sub_data[i - 1] - sub_data[i]
            losses += loss
            losses_count += 1
    if rises_count == 0:
        a = 1
    else:
        a = rises / rises_count
    if losses_count == 0:
        b = 1
    else:
        b = losses / losses_count
    rsi = 100 - (100 / (1 + (a / b)))

    return rsi


def combine_values(currency):
    while True:
        i = currency

        bid, ask, volume = get_values (i)
        ask_list.append(ask)
        bid_list.append(bid)
        volumen_list.append(volume)

        bid_avg = calc_avg(bid_list, N)
        ask_avg = calc_avg(ask_list, N)
        avg_ask_graph.append(ask_avg)
        avg_bid_graph.append(bid_avg)

        rsi_ask.append(calc_RSI(ask_list, lower, upper))
        rsi_bid.append(calc_RSI(bid_list, lower, upper))

        ask_graph.append(ask_list)
        bid_graph.append(bid_list)

        return ask_list, bid_list, volumen_list, avg_ask_graph, avg_bid_graph, rsi_ask, rsi_bid


def create_graph():
    ask_list, bid_list, volumen_list, avg_ask_graph, avg_bid_graph, rsi_ask, rsi_bid = combine_values (curr)

    t.append(time.strftime("%H:%M:%S", time.localtime()))

    plt.subplot (311)
    plt.title(f'{curr} chart')
    plt.plot(t, ask_list, label="buys", color="blue")
    plt.plot(t, bid_list, label="sells", color="yellow")
    plt.plot(t, avg_bid_graph, '--', label='buy avg', color='black')
    plt.plot(t, avg_ask_graph, '--', label='sell avg', color='red')
    plt.ylabel("Currency rate")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks([])

    plt.subplot(312)
    plt.title('Volume chart')
    plt.plot(t, volumen_list, "*-", color='purple')
    plt.xticks([])
    plt.ylabel("Volume values")

    plt.subplot(313)
    plt.title('RSI chart')
    plt.plot(t, rsi_bid, label='buy RSI', color='orange')
    plt.plot(t, rsi_ask, ':', label='sell RSI', color='purple')
    plt.ylabel("RSI value")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(rotation='vertical')
    plt.xlabel("Time")
    plt.tight_layout ()


def animation():
    anim = FuncAnimation (plt.figure (), create_graph, interval=1000)
    plt.show ()


if __name__ == '__main__':

    currency1 = ["BTC", "LTC", "ETH"]
    currency2 = "PLN"

    while True:
        try:
            create_graph ()
            animation ()

        except KeyboardInterrupt:
            print ("Error due to user interuption")
            exit ()