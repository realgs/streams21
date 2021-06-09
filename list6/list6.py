import requests
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta
import json

CURRENCY = ["BTC-PLN", "BCC-PLN", "ETH-PLN"]
N = int(input('Podaj z ilu ostatnich probek liczyć średnią (max 20):'))
START = int(input('Podaj poczatek przedziału y do wiliczenia rsi (zakres 0,20):'))
STOP = int(input('Podaj koniec przedziału y do wiliczenia rsi (zakres 0,20):'))
INTERVAL = 5000
FILE_NAME = str(input('Podaj nazwę pliku:')) + '.txt'

buys0 = []
sells0 = []
avg_buy0 = []
avg_sell0 = []
volume0 = []
rsi_buy_values0 = []
rsi_sell_values0 = []
avg_costumer0 = []
t = []

buys1 = []
sells1 = []
avg_buy1 = []
avg_sell1 = []
volume1 = []
rsi_buy_values1 = []
rsi_sell_values1 = []
avg_costumer1 = []

buys2 = []
sells2 = []
avg_buy2 = []
avg_sell2 = []
volume2 = []
rsi_buy_values2 = []
rsi_sell_values2 = []
avg_costumer2 = []


def get_data(currency):
    response = requests.get(f'https://bitbay.net/API/Public/{currency}/ticker.json')
    data = response.json()
    buy = data['ask']
    sell = data['bid']
    return buy, sell


def get_volumen(currency):
    fromtime = int((datetime.now() - timedelta(seconds=60)).timestamp()) * 1000
    queryparams = {'fromTime': fromtime}
    url = f"https://api.bitbay.net/rest/trading/transactions/{currency}"
    response = requests.get(url, params=queryparams)
    response = response.json()
    return sum([float(response['items'][i]['a']) for i in range(len(response['items']))])


def average(data_list, n):
    part_data = data_list[-n:]
    avg = sum(part_data) / len(part_data)
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
        a = rises / rises_counter
    if losses_counter == 0:
        b = 1
    else:
        b = losses / losses_counter
    rsi = 100 - (100 / (1 + (a / b)))
    return rsi


def add_data(currency, buy_list, sell_list, avg_buy_list, avg_sell_list, volumen_list, rsi_buy_list, rsi_sell_list, costumer_avg_list):
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
    costumer_avg_list.append(get_costumer_avg(currency, FILE_NAME))
    return buy_list, sell_list, avg_buy_list, avg_sell_list, volumen_list, rsi_buy_list, rsi_sell_list, costumer_avg_list


def trend(rsi_list):
    rsi = rsi_list[-1]
    if rsi >= 70:
        return 'upward trend'
    elif rsi <= 30:
        return 'downward trend'
    else:
        return 'sideways trend'


def choose_candidate(trends_list, volume_list):
    volume_compare = {}
    for i in range(3):
        if trends_list[i] != 'downward trend':
            volume_compare[volume_list[i][-1]] = i
    if len(volume_compare) != 0:
        max_volume = max(volume_compare)
        return CURRENCY[volume_compare[max_volume]], f' Current candidate is: {CURRENCY[volume_compare[max_volume]]}'
    else:
        return None, 'There is no candidate at the moment'


def is_volatile(buy_list, X, Y):
    Y_list = buy_list[-Y:]
    value = (abs(max(Y_list) - min(Y_list)) / max(Y_list)) * 100
    if value > X:
        return ' - volatile asset'
    else:
        return ''


def is_liquid(buy_list, sell_list, S):
    bid = sell_list[-1]
    ask = buy_list[-1]
    spread = ((ask - bid) / ask) * 100
    if spread < S:
        return ' - liquid asset'
    return ''


def set_title(candidate, buy_list, sell_list, X, Y, S):
    l_title = []
    v_title = []
    for i in range(len(CURRENCY)):
        if CURRENCY[i] == candidate:
            title_l = is_liquid(buy_list[i], sell_list[i], S)
            title_v = is_volatile(buy_list[i], X, Y)
            l_title.insert(i, title_l)
            v_title.insert(i, title_v)
        else:
            l_title.insert(i, '')
            v_title.insert(i, '')
    return l_title[0], l_title[1], l_title[2], v_title[0], v_title[1], v_title[2]


def get_costumer_avg(currency, path="database.txt"):
    currency = currency[:3]
    f = open(path, 'r')
    data = json.load(f)
    avg = data[f'average_{currency}_json']
    f.close()
    return avg


def get_saldo(currency, path="database.txt"):
    currency = currency[0:3]
    f = open(path, 'r')
    data = json.load(f)
    saldo = data[f'saldo_{currency}_json']
    f.close()
    return saldo


def make_plot(a):
    y1, y2, avg1, avg2, v, rsi1, rsi2, avg_c1 = add_data(CURRENCY[0], buys0, sells0, avg_buy0, avg_sell0, volume0,
                                                 rsi_buy_values0, rsi_sell_values0, avg_costumer0)
    y3, y4, avg3, avg4, v1, rsi3, rsi4, avg_c2 = add_data(CURRENCY[1], buys1, sells1, avg_buy1, avg_sell1, volume1,
                                                  rsi_buy_values1, rsi_sell_values1, avg_costumer1)
    y5, y6, avg5, avg6, v2, rsi5, rsi6, avg_c3 = add_data(CURRENCY[2], buys2, sells2, avg_buy2, avg_sell2, volume2,
                                                  rsi_buy_values2, rsi_sell_values2, avg_costumer2)
    t.append(time.strftime("%H:%M:%S", time.localtime()))
    for i in [y1, y2, avg1, avg2, v, rsi1, rsi2, t, y3, y4, avg3, avg4, v1, rsi3, rsi4, y5, y6, avg5, avg6, v2, rsi5,
              rsi6, avg_c1, avg_c2, avg_c3]:
        if len(i) > 20:
            i.pop(0)
    trend_BTC = trend(rsi_buy_values0)
    trend_BCC = trend(rsi_buy_values1)
    trend_ETH = trend(rsi_buy_values2)
    candidate, subtitle = choose_candidate([trend_BTC, trend_BCC, trend_ETH], [v, v1, v2])
    title1, title2, title3, title4, title5, title6 = set_title(candidate, [y1, y3, y5], [y2, y4, y6], 5, 3, 5)
    saldo1, saldo2, saldo3 = get_saldo(CURRENCY[0], FILE_NAME), get_saldo(CURRENCY[1], FILE_NAME), get_saldo(CURRENCY[2], FILE_NAME)
    plt.clf()
    plt.ion()
    plt.suptitle(subtitle, fontsize=18)
    plt.tight_layout()
    plt.subplot(331)
    plt.title(f'{CURRENCY[0]} chart {title1} \n {title4}')
    plt.plot(t, y1, label="buys", color="blue")
    plt.plot(t, y2, label="sells", color="yellow")
    plt.plot(t, avg1, '--', label='buy avg', color='green')
    plt.plot(t, avg2, '--', label='sell avg', color='red')
    plt.plot(t, avg_c1, '--', label='costumer avg', color='black')
    plt.autoscale(True, 'y')
    plt.ylabel("Currency rate")
    if saldo1 < 0:
        plt.xlabel(f'Saldo:{saldo1}', color='red')
    else:
        plt.xlabel(f'Saldo:{saldo1}', color='green')
    plt.xticks([])
    plt.subplot(334)
    plt.autoscale(True, 'y')
    plt.title('Volume chart')
    plt.bar(t, v, label='volume', color='gray')
    plt.xticks([])
    plt.ylabel("Volume values")
    plt.subplot(337)
    plt.autoscale(True, 'y')
    plt.title(f'RSI chart - {trend_BTC}')
    plt.plot(t, rsi1, label='buy RSI', color='orange')
    plt.plot(t, rsi2, ':', label='sell RSI', color='purple')
    plt.ylabel("RSI value")
    plt.xticks(rotation='vertical')

    plt.subplot(332)
    plt.autoscale(True, 'y')
    plt.title(f'{CURRENCY[1]} chart {title2} \n {title5}')
    plt.plot(t, y3, label="buys", color="blue")
    plt.plot(t, y4, label="sells", color="yellow")
    plt.plot(t, avg3, '--', label='buy avg', color='green')
    plt.plot(t, avg4, '--', label='sell avg', color='red')
    plt.plot(t, avg_c2, '--', label='costumer avg', color='black')
    if saldo2 < 0:
        plt.xlabel(f'Saldo:{saldo2}', color='red')
    else:
        plt.xlabel(f'Saldo:{saldo2}', color='green')
    plt.xticks([])
    plt.subplot(335)
    plt.autoscale(True, 'y')
    plt.title('Volume chart')
    plt.bar(t, v1, label='volume', color='gray')
    plt.xticks([])
    plt.subplot(338)
    plt.autoscale(True, 'y')
    plt.title(f'RSI chart - {trend_BCC}')
    plt.plot(t, rsi3, label='buy RSI', color='orange')
    plt.plot(t, rsi4, ':', label='sell RSI', color='purple')
    plt.xticks(rotation='vertical')
    plt.xlabel("Time")
    plt.tight_layout()

    plt.subplot(333)
    plt.autoscale(True, 'y')
    plt.title(f'{CURRENCY[2]} chart {title3} \n {title6}')
    plt.plot(t, y5, label="buys", color="blue")
    plt.plot(t, y6, label="sells", color="yellow")
    plt.plot(t, avg5, '--', label='buy avg', color='green')
    plt.plot(t, avg6, '--', label='sell avg', color='red')
    plt.plot(t, avg_c3, '--', label='costumer avg', color='black')
    if saldo3 < 0:
        plt.xlabel(f'Saldo:{saldo3}', color='red')
    else:
        plt.xlabel(f'Saldo:{saldo3}', color='green')
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks([])
    plt.subplot(336)
    plt.autoscale(True, 'y')
    plt.title('Volume chart')
    plt.bar(t, v2, label='volume', color='gray')
    plt.xticks([])
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.subplot(339)
    plt.autoscale(True, 'y')
    plt.title(f'RSI chart - {trend_ETH}')
    plt.plot(t, rsi5, label='buy RSI', color='orange')
    plt.plot(t, rsi6, ':', label='sell RSI', color='purple')
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(rotation='vertical')
    plt.tight_layout()


def main():
    animation = FuncAnimation(plt.figure(), make_plot, interval=INTERVAL)
    plt.show()


if __name__ == '__main__':
    main()
