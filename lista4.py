import matplotlib.pyplot as plt
import requests
from matplotlib.animation import FuncAnimation
import time

url_1 = 'https://bitbay.net/API/Public/'
url_2 = '/ticker.json'
base = 'PLN'
currency = ['DASH', 'OMG', 'BTC']

volumen_list0 = []
ask_list0 = []
bid_list0 = []
avg_bid_list0 = []
avg_ask_list0 = []
rsi_bid0 = []
rsi_ask0 = []

volumen_list1 = []
ask_list1 = []
bid_list1 = []
avg_bid_list1 = []
avg_ask_list1 = []
rsi_bid1 = []
rsi_ask1 = []

volumen_list2 = []
ask_list2 = []
bid_list2 = []
avg_bid_list2 = []
avg_ask_list2 = []
rsi_bid2 = []
rsi_ask2 = []
t = []


def get_data(currency):
    response = requests.get(url_1 + currency + base + url_2).json()
    return response["ask"], response["bid"]


def get_volumen(currency):
    response = requests.get(url=f'https://api.bitbay.net/rest/trading/transactions/{currency}-PLN')
    data = response.json()
    return data['items'][1]['a']


def calculate_rsi(data_list, start, stop):
    data = data_list[-20:]
    data = data[start:stop]
    rise = 0
    r_count = 0
    loss = 0
    l_count = 0
    for i in range(1, len(data)):
        if data[i - 1] < data[i]:
            rise += data[i] - data[i - 1]
            r_count += 1
        elif data[i - 1] > data[i]:
            loss += data[i - 1] - data[i]
            l_count += 1
    if r_count == 0:
        a = 1
    else:
        a = rise / r_count
    if l_count == 0:
        b = 1
    else:
        b = loss / l_count
    rsi = 100 - (100 / (1 + (a / b)))
    return rsi


def calculate_averange(data, n):
    interval_data = data[-n:]
    avg = sum(interval_data) / len(interval_data)
    return avg


def add_data(currency,ask_list, bid_list, volumen_list, avg_ask_list, avg_bid_list, rsi_ask, rsi_bid):
    bid, ask = get_data(currency)
    volumen = get_volumen(currency)
    ask_list.append(ask)
    bid_list.append(bid)
    volumen_list.append(volumen)
    bid_avg = calculate_averange(bid_list, n)
    ask_avg = calculate_averange(ask_list, n)
    avg_bid_list.append(bid_avg)
    avg_ask_list.append(ask_avg)
    rsi_bid.append(calculate_rsi(bid_list, start, stop))
    rsi_ask.append(calculate_rsi(ask_list, start, stop))
    return ask_list, bid_list, volumen_list, avg_ask_list, avg_bid_list, rsi_ask, rsi_bid


def create_graph(a):
    ask0, bid0, volumen0, avg_ask0, avg_bid0, rsiask0, rsibid0 = add_data(currency[0],ask_list0, bid_list0, volumen_list0, avg_ask_list0, avg_bid_list0, rsi_ask0, rsi_bid0)
    ask1, bid1, volumen1, avg_ask1, avg_bid1, rsiask1, rsibid1 = add_data(currency[1],ask_list1, bid_list1, volumen_list1, avg_ask_list1, avg_bid_list1, rsi_ask1, rsi_bid1)
    ask2, bid2, volumen2, avg_ask2, avg_bid2, rsiask2, rsibid2 = add_data(currency[1],ask_list2, bid_list2, volumen_list2, avg_ask_list2, avg_bid_list2, rsi_ask2, rsi_bid2)
    t.append(time.strftime("%H:%M:%S", time.localtime()))

    plt.subplot(331)
    plt.cla()
    plt.title(f'{currency[0]} chart')
    plt.plot(t, ask0, label="buys", color="blue")
    plt.plot(t, bid0, label="sells", color="red")
    plt.plot(t, avg_bid0, '--', label='buy avg', color='black')
    plt.plot(t, avg_ask0, '--', label='sell avg', color='green')
    plt.ylabel("Currency rate")
    plt.xticks([])

    plt.subplot(334)
    plt.title('Volume chart')
    plt.plot(t, volumen0, "*-", color='orange')
    plt.xticks([])
    plt.ylabel("Volume values")

    plt.subplot(337)
    plt.cla()
    plt.title('RSI chart')
    plt.plot(t, rsibid0, label='buy RSI', color='yellow')
    plt.plot(t, rsiask0, ':', label='sell RSI', color='purple')
    plt.ylabel("RSI value")
    plt.xticks(rotation='vertical')
    plt.xlabel("Time")
    plt.tight_layout()

    plt.subplot(332)
    plt.cla()
    plt.title(f'{currency[1]} chart')
    plt.plot(t, ask1, label="buys", color="blue")
    plt.plot(t, bid1, label="sells", color="red")
    plt.plot(t, avg_bid1, '--', label='buy avg', color='black')
    plt.plot(t, avg_ask1, '--', label='sell avg', color='green')
    plt.ylabel("Currency rate")
    plt.xticks([])

    plt.subplot(335)
    plt.title('Volume chart')
    plt.plot(t, volumen1, "*-", color='orange')
    plt.xticks([])
    plt.ylabel("Volume values")

    plt.subplot(338)
    plt.cla()
    plt.title('RSI chart')
    plt.plot(t, rsibid1, label='buy RSI', color='yellow')
    plt.plot(t, rsiask1, ':', label='sell RSI', color='purple')
    plt.ylabel("RSI value")
    plt.xticks(rotation='vertical')
    plt.xlabel("Time")
    plt.tight_layout()

    plt.subplot(333)
    plt.cla()
    plt.title(f'{currency[2]} chart')
    plt.plot(t, ask2, label="buys", color="blue")
    plt.plot(t, bid2, label="sells", color="red")
    plt.plot(t, avg_bid2, '--', label='buy avg', color='black')
    plt.plot(t, avg_ask2, '--', label='sell avg', color='green')
    plt.ylabel("Currency rate")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks([])

    plt.subplot(336)
    plt.title('Volume chart')
    plt.plot(t, volumen2, "*-", color='orange')
    plt.xticks([])
    plt.ylabel("Volume values")

    plt.subplot(339)
    plt.cla()
    plt.title('RSI chart')
    plt.plot(t, rsibid2, label='buy RSI', color='yellow')
    plt.plot(t, rsiask2, ':', label='sell RSI', color='purple')
    plt.ylabel("RSI value")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(rotation='vertical')
    plt.xlabel("Time")
    plt.tight_layout()


if __name__ == '__main__':
    start = int(input('podaj dolną granicę z której chcesz liczyć rsi:'))
    stop = int(input('podaj górną granicę z której chcesz liczyć rsi:'))
    n = int(input("podaj ilość próbek:"))
    animation = FuncAnimation(plt.figure(), create_graph, interval=1000)
    plt.show()
