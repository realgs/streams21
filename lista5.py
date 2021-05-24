import matplotlib.pyplot as plt
import requests
from matplotlib.animation import FuncAnimation
import time
from datetime import datetime, timedelta

url_1 = 'https://bitbay.net/API/Public/'
url_2 = '/ticker.json'
base = 'PLN'
currency = ['DASH', 'ETH', 'BTC']

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
    fromtime = int((datetime.now() - timedelta(seconds=60)).timestamp()) * 1000
    url = f"https://api.bitbay.net/rest/trading/transactions/{currency}-PLN"
    queryparams = {'fromTime': fromtime}
    response = requests.request("GET", url, params=queryparams)
    response = eval(response.text)

    return sum([float(response['items'][i]['a']) for i in range(len(response['items']))])


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


def trend(rsi_list):
    rsi = rsi_list[-1]
    if rsi >= 70:
        return 'upward trend'
    elif rsi <= 30:
        return 'downward trend'
    else:
        return 'sideways trend'


def find_candidate(trends_list, volume_list):
    volume_compare = {}
    for i in range(3):
        if trends_list[i] != 'downward trend':
            volume_compare[volume_list[i][-1]] = i
    if len(volume_compare) != 0:
        max_volume = max(volume_compare)
        return currency[volume_compare[max_volume]], f' Current candidate is: {currency[volume_compare[max_volume]]}'
    else:
        return None, 'There is no candidate at the moment'


def is_volatile(buy_list, X, Y):
    Y_list = buy_list[-Y:]

    value = (abs(max(Y_list)-min(Y_list)) / max(Y_list)) * 100
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

    for i in range(len(currency)):
        if currency[i] == candidate:
            title_l = is_liquid(buy_list[i], sell_list[i], S)
            title_v = is_volatile(buy_list[i], X, Y )
            l_title.insert(i,title_l)
            v_title.insert(i, title_v)
        else:
            l_title.insert(i, '')
            v_title.insert(i, '')
    return l_title[0], l_title[1], l_title[2], v_title[0], v_title[1], v_title[2]


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
    trend_DASH = trend(rsibid0)
    trend_ETH = trend(rsibid1)
    trend_BTC = trend(rsibid2)
    candidate, subtitle = find_candidate([trend_DASH, trend_ETH, trend_BTC], [volumen0, volumen1, volumen2])
    title1, title2, title3, title4, title5, title6 = set_title(candidate, [ask0, ask1, ask2], [bid0, bid1, bid2], X, Y, S)
    ticks = list()

    if len(t) > 5:
        ticks.append(t[0])
        middle = int(len(t)/2)
        ticks.append(t[middle])
        ticks.append(t[-1])
    else:
        ticks = t
    plt.ion()
    plt.clf()
    plt.suptitle(subtitle)
    plt.subplot(331)
    plt.title(f'{currency[0]} chart {title1} \n {title4}')
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
    plt.title(f'RSI chart - {trend_DASH}')
    plt.plot(t, rsibid0, label='buy RSI', color='yellow')
    plt.plot(t, rsiask0, ':', label='sell RSI', color='purple')
    plt.ylabel("RSI value")
    plt.xticks(ticks=ticks, rotation='vertical')
    plt.xlabel("Time")
    plt.tight_layout()

    plt.subplot(332)
    plt.title(f'{currency[1]} chart {title2} \n {title5}')
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
    plt.title(f'RSI chart - {trend_ETH}')
    plt.plot(t, rsibid1, label='buy RSI', color='yellow')
    plt.plot(t, rsiask1, ':', label='sell RSI', color='purple')
    plt.ylabel("RSI value")
    plt.xticks(ticks=ticks, rotation='vertical')
    plt.xlabel("Time")
    plt.tight_layout()

    plt.subplot(333)
    plt.title(f'{currency[2]} chart {title3} \n {title6}')
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
    plt.title(f'RSI chart - {trend_BTC}')
    plt.plot(t, rsibid2, label='buy RSI', color='yellow')
    plt.plot(t, rsiask2, ':', label='sell RSI', color='purple')
    plt.ylabel("RSI value")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(ticks=ticks, rotation='vertical')
    plt.xlabel("Time")
    plt.tight_layout()


if __name__ == '__main__':
    start = int(input('podaj dolną granicę z której chcesz liczyć rsi:'))
    stop = int(input('podaj górną granicę z której chcesz liczyć rsi:'))
    n = int(input("podaj ilość próbek:"))
    S = 4
    X = 5
    Y = 4
    animation = FuncAnimation(plt.figure(), create_graph, interval=1000)
    plt.show()
    