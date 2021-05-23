import requests
import matplotlib.pyplot as plt
from sys import exit
import time
from datetime import datetime, timedelta
from matplotlib.animation import FuncAnimation
import matplotlib.patches as mpatches

N=int(input('How many samples would you like to consider (max 20):' ))
upper=int(input('Input upper bount of the range in which you would like to calculate RSI (0, 20):'))
lower=int(input('Input lower bount of the range in which you would like to calculate RSI (0, 20):'))

def connect(currency1, currency2):

    return f'https://bitbay.net/API/Public/{currency1}{currency2}/ticker.json'

def get_values(currency1):

    try:
        req = requests.get (connect(currency1, "PLN")).json()
        bid = req['bid']
        ask = req['ask']

    except Exception as e:
        print('ERROR:', e)
        return {}

    return bid, ask


def get_volumen(currency):

    fromtime = int ( (datetime.now () - timedelta ( seconds=60 )).timestamp () ) * 1000
    url = f"https://api.bitbay.net/rest/trading/transactions/{currency}"
    queryparams = {'fromTime': fromtime}
    response = requests.request("GET", url, params=queryparams)
    response = eval(response.text)

    return sum([float(response['items'][i]['a'] ) for i in range(len(response['items']))])


def calc_avg(data, n):

    sub_data = data[-n:]
    avg = sum (sub_data) / len(sub_data)
    return avg


def calc_RSI(data, lower, upper):
    sub_data = data[-20:]
    sub_data = sub_data[lower:upper]
    rises = 0
    rises_count = 0
    losses = 0
    losses_count = 0
    for i in range ( 1, len ( sub_data ) ):
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


def combine_values(currency, ask_list, bid_list, volumen_list, avg_ask_graph, avg_bid_graph, rsi_ask, rsi_bid):
    while True:
        i = currency

        bid, ask = get_values (i)
        ask_list.append (ask)
        bid_list.append (bid)

        volume = get_volumen(f'{i}-PLN')
        volumen_list.append(volume)

        bid_avg = calc_avg(bid_list, N)
        ask_avg = calc_avg (ask_list, N)
        avg_ask_graph.append (ask_avg)
        avg_bid_graph.append (bid_avg)

        rsi_ask.append (calc_RSI (ask_list, lower, upper))
        rsi_bid.append (calc_RSI (bid_list, lower, upper))

        return ask_list, bid_list, volumen_list, avg_ask_graph, avg_bid_graph, rsi_ask, rsi_bid


def trend(rsi_list):
    rsi = rsi_list[-1]

    if rsi>= 70:
        return 'Strefa wyprzedarzy'

    elif rsi<= 30:
        return 'Strefa wykupienia'

    else:
        return 'Boczny trend'


def find_candidate(trends_list, volume_list):
    volume_compare = list ()

    for i in range ( 3 ):

        if trends_list[i] != 'Strefa wykupienia':
            volume_compare.append (volume_list[i][-1])

    if len (volume_compare) != 0:
        max_volume = max (volume_compare)
        ind = volume_compare.index (max_volume)

        return currency1[ind], f'Current candidate is:{currency1[ind]}'

    else:
        return None, 'There is no candidate at the moment'


def is_volatile(buy_list, X, Y):
    Y_list = buy_list[-Y:]

    value = (abs(max( Y_list )-min(Y_list)) / max(Y_list)) * 100
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

    for i in range ( len(currency1)):
        if currency1[i] == candidate:
            title_l = is_liquid (buy_list[i], sell_list[i], S)
            title_v = is_volatile ( buy_list[i], X, Y )
            l_title.insert (i,title_l)
            v_title.insert (i, title_v)
        else:
            l_title.insert (i, '')
            v_title.insert (i, '')
    return l_title[0], l_title[1], l_title[2], v_title[0], v_title[1], v_title[2]


def create_graph():
    ask1, bid1, vol1, avg_ask1, avg_bid1, rsi_a1, rsi_b1 = combine_values ( currency1[0], ask_list1, bid_list1,
                                                                            volumen_list1, avg_ask_graph1,
                                                                            avg_bid_graph1, rsi_ask1, rsi_bid1 )
    ask2, bid2, vol2, avg_ask2, avg_bid2, rsi_a2, rsi_b2 = combine_values ( currency1[1], ask_list2, bid_list2,
                                                                            volumen_list2, avg_ask_graph2,
                                                                            avg_bid_graph2, rsi_ask2, rsi_bid2 )
    ask3, bid3, vol3, avg_ask3, avg_bid3, rsi_a3, rsi_b3 = combine_values ( currency1[2], ask_list3, bid_list3,
                                                                            volumen_list3, avg_ask_graph3,
                                                                            avg_bid_graph3, rsi_ask3, rsi_bid3 )

    t.append ( time.strftime ( "%H:%M:%S", time.localtime () ) )

    trend_BTC = trend (rsi_b1)
    trend_LTC = trend (rsi_b2)
    trend_ETH = trend (rsi_b3)

    candidate, subtitle = find_candidate ( [trend_BTC, trend_LTC, trend_ETH], [vol1, vol2, vol3] )

    title1, title2, title3, title4, title5, title6 = set_title (candidate, [ask1, ask2, ask3], [bid1, bid2, bid3], X,
                                                                 Y, S)

    ticks = list ()

    if len (t) > 4:
        ticks.append (t[0])
        middle = int (len(t)/2)
        ticks.append (t[middle])
        ticks.append (t[-1])

    else:
        ticks = t

    plt.clf ()
    plt.ion ()
    plt.suptitle (subtitle, fontsize=10)
    plt.tight_layout ()

    plt.subplot (331)
    plt.title (f'{currency1[0]} chart {title1} \n {title4}', size=7)

    plt.plot (t, ask1, label="buys", color="blue")
    plt.plot (t, bid1, label="sells", color="yellow")

    plt.plot (t, avg_ask1, '--', label='buy avg', color='black')
    plt.plot (t, avg_bid1, '--', label='sell avg', color='red')
    plt.ylabel ("Currency rate")
    plt.xticks ([])
    plt.yticks (fontsize=6)

    plt.subplot ( 334 )
    plt.title ('Volume chart', size=6)
    plt.plot (t, vol1, "--", color='purple')
    plt.xticks ([])
    plt.ylabel ("Volume values")
    plt.yticks (fontsize=6)

    plt.subplot (337)
    plt.title (f'RSI chart - {trend_BTC}', size=7)
    plt.plot (t, rsi_b1, label='buy RSI', color='orange')
    plt.plot (t, rsi_a1, ':', label='sell RSI', color='purple')
    plt.ylabel ("RSI value")
    plt.xticks (ticks=ticks, rotation='vertical', size=7)
    plt.xlabel ("Time", size=8)
    plt.yticks (fontsize=6)

    plt.subplot (332)
    plt.title (f'{currency1[1]} chart {title2} \n {title5}', size=7)

    plt.plot (t, ask2, label="buys", color="blue")
    plt.plot (t, bid2, label="sells", color="yellow")
    plt.plot (t, avg_ask2, '--', label='buy avg', color='black')
    plt.plot (t, avg_bid2, '--', label='sell avg', color='red')
    plt.xticks ([])
    plt.yticks (fontsize=6)

    plt.subplot (335)
    plt.title ('Volume chart', size=7)
    plt.plot (t, vol2, "--", color='purple')
    plt.xticks ([])
    plt.yticks (fontsize=6)

    plt.subplot (338)
    plt.title (f'RSI chart - {trend_LTC}', size=7)
    plt.plot (t, rsi_b2, label='buy RSI', color='orange')
    plt.plot (t, rsi_a2, ':', label='sell RSI', color='purple')
    plt.xticks (ticks=ticks, rotation='vertical', size=7)
    plt.xlabel ("Time", size=8)
    plt.yticks (fontsize=6)

    plt.subplot (333)
    plt.title (f'{currency1[2]} chart {title3} \n {title6}', size=7)

    plt.plot (t, ask3, label="buys", color="blue" )
    plt.plot (t, bid3, label="sells", color="yellow" )

    plt.plot (t, avg_ask3, '--', label='buy avg', color='black')
    plt.plot (t, avg_bid3, '--', label='sell avg', color='red')
    plt.legend (bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks ([])
    plt.yticks (fontsize=6)

    plt.subplot (336)
    plt.title ('Volume chart', size=7)
    plt.plot (t, vol3, "--", color='purple')
    plt.xticks ([])
    plt.yticks (fontsize=6)

    vol_lab = mpatches.Patch (color='purple', label='volume')
    plt.legend (handles=[vol_lab], bbox_to_anchor=(1.05, 1.0), loc='upper left')

    plt.subplot (339)
    plt.title (f'RSI chart - {trend_BTC}', size=7)
    plt.plot (t, rsi_b3, label='buy RSI', color='orange')
    plt.plot (t, rsi_a3, ':', label='sell RSI', color='purple')
    plt.legend (bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks (ticks=ticks, rotation='vertical', size=7)
    plt.xlabel ("Time", size=8)
    plt.yticks (fontsize=6)


def animation():
    anim = FuncAnimation (plt.figure (), create_graph, interval=1000)
    plt.show ()


if __name__ == '__main__':

    currency1 = ["BTC", "LTC", "ETH"]
    currency2 = "PLN"

    t = []

    volumen_list1 = []
    ask_list1 = []
    bid_list1 = []
    ask_graph1 = []
    bid_graph1 = []
    avg_bid_graph1 = []
    avg_ask_graph1 = []
    rsi_bid1 = []
    rsi_ask1 = []

    volumen_list2 = []
    ask_list2 = []
    bid_list2 = []
    ask_graph2 = []
    bid_graph2 = []
    avg_bid_graph2 = []
    avg_ask_graph2 = []
    rsi_bid2 = []
    rsi_ask2 = []

    volumen_list3 = []
    ask_list3 = []
    bid_list3 = []
    ask_graph3 = []
    bid_graph3 = []
    avg_bid_graph3 = []
    avg_ask_graph3 = []
    rsi_bid3 = []
    rsi_ask3 = []

    S = 5
    X = 5
    Y = 3

    while True:
        try:
            create_graph ()
            animation ()

        except KeyboardInterrupt:
            print ("Error due to user interuption")
            exit ()
