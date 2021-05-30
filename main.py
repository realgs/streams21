import requests
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta

def get_data(crypt):
    url = "https://bitbay.net/API/Public/{Currency}/{Category}.json".format(Currency=crypt,
                                                                                            Category= 'ticker')
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        buy = response['ask']
        sell = response['bid']
        return buy, sell
    else:
        print("Can't get data from API \n status code: ", response.status_code)


def get_volume(crypt):
    url = "https://api.bitbay.net/rest/trading/transactions/{currency}".format(currency= crypt)
    response = requests.get(url)
    response = response.json()
    if response['status'] == 'Ok':
        volume = float(response['items'][1]['a'])
        return volume
    else:
        print("Can't get data from API \n status code: ", response['status'])

def average(data_list, n):
    part_data = data_list[-n:]
    avg = sum(part_data)/len(part_data)
    return avg


def count_rsi(data_list, start, stop):
    sub_data = data_list[-10:]
    sub_data = sub_data[start:stop]
    rises = 0
    rises_counter = 0
    losses = 0
    losses_counter = 0
    for i in range(1, len(sub_data)):
        if sub_data[i - 1] < sub_data[i]:
            rise = sub_data[i] - sub_data[i - 1]
            rises += rise
            rises_counter += 1
        elif sub_data[i - 1] > sub_data[i]:
            loss = sub_data[i - 1] - sub_data[i]
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


def data_stream(crypt, buy_list, sell_list, avg_buy_list, avg_sell_list, volume_list, rsi_buy_list, rsi_sell_list):
    buy, sell = get_data(crypt)
    buy_list.append(buy)
    sell_list.append(sell)
    buy_avg = average(buy_list, N)
    sell_avg = average(sell_list, N)

    avg_buy_list.append(buy_avg)
    avg_sell_list.append(sell_avg)
    volume_list.append(get_volume(crypt))

    rsi_buy_list.append(count_rsi(buy_list, START, STOP))
    rsi_sell_list.append(count_rsi(sell_list, START, STOP))


    f = open('trades/{crypt}.json'.format(crypt= crypt), 'a')
    f.write(str(buy) + ' ' + str(sell) + '\n')
    f.close

    return buy_list, sell_list, avg_buy_list, avg_sell_list, volume_list, rsi_buy_list, rsi_sell_list


def trend(rsi_list):
    rsi = rsi_list[-1]
    if rsi >= 60:
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
    last_Y = buy_list[-Y:]
    value = abs(max(last_Y) - min(last_Y)) / min(last_Y) * 100
    if value > X:
        return ' - volatile asset'
    else:
        return ''


def is_liquid(buy_list, sell_list, S):
    sell = sell_list[-1]
    buy = buy_list[-1]
    spread = ((buy - sell) / buy ) * 100
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
    return l_title, v_title


def animate(i):
    global X, Y, S
    y1, y2, avg1, avg2, v, rsi1, rsi2 = data_stream(CURRENCY[0], buys0, sells0, avg_buy0, avg_sell0, volume0, rsi_buy_values0, rsi_sell_values0)
    y3, y4, avg3, avg4, v1, rsi3, rsi4 = data_stream(CURRENCY[1], buys1, sells1, avg_buy1, avg_sell1, volume1, rsi_buy_values1, rsi_sell_values1)
    y5, y6, avg5, avg6, v2, rsi5, rsi6 = data_stream(CURRENCY[2], buys2, sells2, avg_buy2, avg_sell2, volume2, rsi_buy_values2, rsi_sell_values2)
    t.append(time.strftime("%H:%M:%S", time.localtime()))
    for L in [y1, y2, avg1, avg2, v, rsi1, rsi2, t, y3, y4, avg3, avg4, v1, rsi3, rsi4, y5, y6, avg5, avg6, v2, rsi5, rsi6]:
        if len(L) > 10:
            L.pop(0)

    trend_0, trend_1, trend_2 = trend(rsi_buy_values0), trend(rsi_buy_values1), trend(rsi_buy_values2)
    candidate, subtitle = choose_candidate([trend_0, trend_1, trend_2], [v, v1, v2])
    [l_title1, l_title2, l_title3], [v_title1, v_title2, v_title3] = set_title(candidate, [y1, y3, y5], [y2, y4, y6], X, Y, S)
    
    plt.clf()
    plt.ion()
    plt.suptitle(subtitle, fontsize=18)
    plt.tight_layout()

# -----------------------------------------------------------------------
    plt.subplot(331)
    plt.title(f'{CURRENCY[0]} chart {l_title1} \n {v_title1}')
    plt.plot(t, y1, label="buys", color="blue")
    plt.plot(t, y2, label="sells", color="yellow")
    plt.plot(t, avg1, '--', label='buy avg', color='green')
    plt.plot(t, avg2, '--', label='sell avg', color='red')
    plt.ylabel("Currency rate")

    plt.xticks([])
    plt.subplot(334)
    plt.title('Volume chart')
    plt.bar(t, v, label='volume', color='gray')
    plt.xticks([])
    plt.ylabel("Volume values")

    plt.subplot(337)
    plt.title(f'RSI chart - {trend_0}')
    plt.plot(t, rsi1, label='buy RSI', color='orange')
    plt.plot(t, rsi2, ':', label='sell RSI', color='purple')
    plt.ylabel("RSI value")

    plt.xticks(rotation='vertical')


# -----------------------------------------------------------------------
    plt.subplot(332)
    plt.title(f'{CURRENCY[1]} chart {l_title2} \n {v_title2}')
    plt.plot(t, y3, label="buys", color="blue")
    plt.plot(t, y4, label="sells", color="yellow")
    plt.plot(t, avg3, '--', label='buy avg', color='green')
    plt.plot(t, avg4, '--', label='sell avg', color='red')

    plt.xticks([])
    plt.subplot(335)
    plt.title('Volume chart')
    plt.bar(t, v1, label='volume', color='gray')
    plt.xticks([])

    plt.subplot(338)
    plt.title(f'RSI chart - {trend_1}')
    plt.plot(t, rsi3, label='buy RSI', color='orange')
    plt.plot(t, rsi4, ':', label='sell RSI', color='purple')

    plt.xticks(rotation='vertical')
    plt.xlabel("Time")
    plt.tight_layout()
#-----------------------------------------------------------------------
    plt.subplot(333)
    plt.title(f'{CURRENCY[2]} chart {l_title3} \n {v_title3}')
    plt.plot(t, y5, label="buys", color="blue")
    plt.plot(t, y6, label="sells", color="yellow")
    plt.plot(t, avg5, '--', label='buy avg', color='green')
    plt.plot(t, avg6, '--', label='sell avg', color='red')

    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks([])
    plt.subplot(336)
    plt.title('Volume chart')
    plt.bar(t, v2, label='volume', color='gray')
    plt.xticks([])

    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.subplot(339)
    plt.title(f'RSI chart - {trend_2}')
    plt.plot(t, rsi5, label='buy RSI', color='orange')
    plt.plot(t, rsi6, ':', label='sell RSI', color='purple')

    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(rotation='vertical')

    plt.tight_layout()

def plot_data():
    global TIME_SLEEP
    animation = FuncAnimation(plt.figure(), func=animate, interval=TIME_SLEEP)
    plt.show()

if __name__ == "__main__":
    X, Y, S = 2, 5, 5
    TIME_SLEEP = 5000
    CURRENCY = ["OMG-PLN", "BTC-PLN", "ETH-PLN"]
    N = 5  # input("Liczba próbek do wyliczenia średniej: ")#average
    START = 0  # input("Początek przdziału do wyliczenia RSI: ") #rsi start
    STOP = 10  # input("Koniec przdziału do wyliczenia RSI: ") # rsi stop

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

    plot_data()



