import matplotlib.pyplot as plt
import requests
from matplotlib.animation import FuncAnimation
import time

url_1 = 'https://bitbay.net/API/Public/'
url_2 = '/ticker.json'
base = 'PLN'
currency = ['DASH', 'OMG', 'BTC']

volumen_list = []
ask_list = []
bid_list = []
avg_bid_list = []
avg_ask_list = []
rsi_bid = []
rsi_ask = []
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


def add_data(currency):
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
    ask_list, bid_list, volumen_list, avg_ask_graph, avg_bid_graph, rsi_ask, rsi_bid = add_data(currency[1])
    t.append(time.strftime("%H:%M:%S", time.localtime()))

    plt.subplot(311)
    plt.cla()
    plt.title(f'{currency[1]} chart')
    plt.plot(t, ask_list, label="buys", color="blue")
    plt.plot(t, bid_list, label="sells", color="red")
    plt.plot(t, avg_bid_graph, '--', label='buy avg', color='black')
    plt.plot(t, avg_ask_graph, '--', label='sell avg', color='green')
    plt.ylabel("Currency rate")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks([])

    plt.subplot(312)
    plt.title('Volume chart')
    plt.plot(t, volumen_list, "*-", color='orange')
    plt.xticks([])
    plt.ylabel("Volume values")

    plt.subplot(313)
    plt.cla()
    plt.title('RSI chart')
    plt.plot(t, rsi_bid, label='buy RSI', color='yellow')
    plt.plot(t, rsi_ask, ':', label='sell RSI', color='purple')
    plt.ylabel("RSI value")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(rotation='vertical')
    plt.xlabel("Time")
    plt.tight_layout()


if __name__ == '__main__':
    start = int(input('podaj dolną granicę z której chcesz liczyć rsi (od 0 do 20):'))
    stop = int(input('podaj górną granicę z której chcesz liczyć rsi (od 0 do 20):'))
    n = int(input("podaj ilość próbek:"))
    animation = FuncAnimation(plt.figure(), create_graph, interval=1000)
    plt.show()

