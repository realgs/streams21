import requests
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta

CURRENCY = ["BTC-PLN", "BCC-PLN", "ETH-PLN"]
N = int(input('Podaj z ilu ostatnich probek liczyć średnią (max 20):'))
START = int(input('Podaj poczatek przedziału y do wiliczenia rsi (zakres 0,20):'))
STOP = int(input('Podaj koniec przedziału y do wiliczenia rsi (zakres 0,20):'))
INTERVAL = 5000

buys0 = []
sells0 = []
avg_buy0 = []
avg_sell0 = []
volume0 = []
rsi_buy_values0 = []
rsi_sell_values0 = []
t = []

buys1 = []
sells1 = []
avg_buy1 = []
avg_sell1 = []
volume1 = []
rsi_buy_values1 = []
rsi_sell_values1 = []

buys2 = []
sells2 = []
avg_buy2 = []
avg_sell2 = []
volume2 = []
rsi_buy_values2 = []
rsi_sell_values2 = []


def get_data(currency):
    URL = f'https://bitbay.net/API/Public/{currency}/ticker.json'
    response = requests.get(URL)
    response = eval(response.text)
    buy = response['ask']
    sell = response['bid']
    return buy, sell


def get_volumen(currency):
    fromtime = datetime.now() - timedelta(minutes=5)
    fromtime = int(fromtime.timestamp()) * 1000
    url = f"https://api.bitbay.net/rest/trading/transactions/{currency}"
    queryparams = {'fromTime': fromtime}
    response = requests.request("GET", url, params=queryparams)
    response = eval(response.text)
    return sum([float(response['items'][i]['a']) for i in range(len(response['items']))])


def average(data_list, n):
    part_data = data_list[-n:]
    avg = sum(part_data)/len(part_data)
    return avg


def count_rsi(data_list, start, stop):
    part_data = data_list[-20:]
    part_data = part_data[start:stop]
    rises = 0
    rises_counter = 0
    losses = 0
    losses_counter = 0
    for i in range(1, len(part_data)):
        if part_data[i - 1] < part_data[i]:
            rise = part_data[i] - part_data[i - 1]
            rises += rise
            rises_counter += 1
        elif part_data[i - 1] > part_data[i]:
            loss = part_data[i - 1] - part_data[i]
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


def add_data(currency, buy_list, sell_list, avg_buy_list, avg_sell_list, volumen_list, rsi_buy_list, rsi_sell_list):
    buy, sell = get_data(currency)
    buy_list.append(buy)
    sell_list.append(sell)
    buy_avg = average(buy_list, N)
    sell_avg = average(sell_list, N)
    avg_buy_list.append(buy_avg)
    avg_sell_list.append(sell_avg)
    volumen_list.append(get_volumen(currency))
    rsi_buy_list.append(count_rsi(buy_list, START, STOP))
    rsi_sell_list.append(count_rsi(sell_list, START, STOP))
    return buy_list, sell_list, avg_buy_list, avg_sell_list, volumen_list, rsi_buy_list, rsi_sell_list


def make_plot(a):
    y1, y2, avg1, avg2, v, rsi1, rsi2 = add_data(CURRENCY[0], buys0, sells0, avg_buy0, avg_sell0, volume0, rsi_buy_values0, rsi_sell_values0)
    y3, y4, avg3, avg4, v1, rsi3, rsi4 = add_data(CURRENCY[1], buys1, sells1, avg_buy1, avg_sell1, volume1, rsi_buy_values1, rsi_sell_values1)
    y5, y6, avg5, avg6, v2, rsi5, rsi6 = add_data(CURRENCY[2], buys2, sells2, avg_buy2, avg_sell2, volume2, rsi_buy_values2, rsi_sell_values2)
    t.append(time.strftime("%H:%M:%S", time.localtime()))
    for i in [y1, y2, avg1, avg2, v, rsi1, rsi2, t, y3, y4, avg3, avg4, v1, rsi3, rsi4, y5, y6, avg5, avg6, v2, rsi5, rsi6]:
        if len(i) > 20:
            i.pop(0)
    plt.clf()
    plt.ion()
    plt.subplot(331)
    plt.title(f'{CURRENCY[0]} chart')
    plt.plot(t, y1, label="buys", color="blue")
    plt.plot(t, y2, label="sells", color="yellow")
    plt.plot(t, avg1, '--', label='buy avg', color='green')
    plt.plot(t, avg2, '--', label='sell avg', color='red')
    plt.ylabel("Currency rate")
    # plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks([])
    plt.subplot(334)
    plt.title('Volume chart')
    plt.bar(t, v, label='volume', color='gray')
    plt.xticks([])
    plt.ylabel("Volume values")
    # plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.subplot(337)
    plt.title('RSI chart')
    plt.plot(t, rsi1, label='buy RSI', color='orange')
    plt.plot(t, rsi2, ':', label='sell RSI', color='purple')
    plt.ylabel("RSI value")
    # plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(rotation='vertical')
    # plt.xlabel("Time")
    plt.tight_layout()

    plt.subplot(332)
    plt.title(f'{CURRENCY[1]} chart')
    plt.plot(t, y3, label="buys", color="blue")
    plt.plot(t, y4, label="sells", color="yellow")
    plt.plot(t, avg3, '--', label='buy avg', color='green')
    plt.plot(t, avg4, '--', label='sell avg', color='red')
    # plt.ylabel("Currency rate")
    # plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks([])
    plt.subplot(335)
    plt.title('Volume chart')
    plt.bar(t, v1, label='volume', color='gray')
    plt.xticks([])
    # plt.ylabel("Volume values")
    # plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.subplot(338)
    plt.title('RSI chart')
    plt.plot(t, rsi3, label='buy RSI', color='orange')
    plt.plot(t, rsi4, ':', label='sell RSI', color='purple')
    # plt.ylabel("RSI value")
    # plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(rotation='vertical')
    plt.xlabel("Time")
    plt.tight_layout()

    plt.subplot(333)
    plt.title(f'{CURRENCY[2]} chart')
    plt.plot(t, y5, label="buys", color="blue")
    plt.plot(t, y6, label="sells", color="yellow")
    plt.plot(t, avg5, '--', label='buy avg', color='green')
    plt.plot(t, avg6, '--', label='sell avg', color='red')
    # plt.ylabel("Currency rate")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks([])
    plt.subplot(336)
    plt.title('Volume chart')
    plt.bar(t, v2, label='volume', color='gray')
    plt.xticks([])
    # plt.ylabel("Volume values")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.subplot(339)
    plt.title('RSI chart')
    plt.plot(t, rsi5, label='buy RSI', color='orange')
    plt.plot(t, rsi6, ':', label='sell RSI', color='purple')
    # plt.ylabel("RSI value")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(rotation='vertical')
    # plt.xlabel("Time")
    plt.tight_layout()



def main():
    animation = FuncAnimation(plt.figure(), make_plot, interval=INTERVAL)
    plt.show()


if __name__ == '__main__':
    main()
