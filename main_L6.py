import requests
import matplotlib.pyplot as plt
from sys import exit
import time
from datetime import datetime, timedelta
from matplotlib.animation import FuncAnimation
import matplotlib.patches as mpatches
import json

N = 20
upper = 20
lower = 1
T = 5
profit = []


def connect(currency1, currency2):
    return f'https://bitbay.net/API/Public/{currency1}{currency2}/ticker.json'


def read_file_buy():
    while True:
        with open ( "buy.json", 'r' ) as handle:
            json_buy = [json.loads ( line ) for line in handle]
            return json_buy
            time.sleep ( T )


def read_file_sell():
    while True:
        with open ( "sell.json", 'r' ) as handle:
            json_sell = [json.loads ( line ) for line in handle]
            return json_sell
            time.sleep ( T )


def print_file_values():
    print(read_file_buy ())
    print(read_file_sell ())


def file_values_buy():
    data = read_file_buy ()

    amt_BTC = []
    amt_LTC = []
    amt_ETH = []
    price_BTC = []
    price_LTC = []
    price_ETH = []
    time_BTC = []
    time_LTC = []
    time_ETH = []

    for i in data:

        if len ( i ) != 0:
            if i['currency'] == 'BTC':
                amt_BTC.append ( i['amount'] )
                price_BTC.append ( i['price'] )

                time_BTC.append ( i['time'] )

            elif i['currency'] == 'LTC':

                amt_LTC.append ( i['amount'] )
                price_LTC.append ( i['price'] )
                time_LTC.append ( i['time'] )

            elif i['currency'] == 'ETH':
                amt_ETH.append ( i['amount'] )
                price_ETH.append ( i['price'] )
                time_ETH.append ( i['time'] )

            else:
                continue

    return amt_BTC, amt_LTC, amt_ETH, price_BTC, price_LTC, price_ETH, time_BTC, time_LTC, time_ETH


def file_values_sell():
    data = read_file_sell ()

    amt_BTC_sell = []
    amt_LTC_sell = []
    amt_ETH_sell = []
    price_BTC_sell = []
    price_LTC_sell = []
    price_ETH_sell = []
    time_BTC_sell = []
    time_LTC_sell = []
    time_ETH_sell = []

    for i in data:

        if len ( i ) != 0:
            if i['currency'] == 'BTC':
                amt_BTC_sell.append ( i['amount'] )
                price_BTC_sell.append ( i['price'] )
                time_BTC_sell.append ( i['time'] )

            elif i['currency'] == 'LTC':

                amt_LTC_sell.append ( i['amount'] )
                price_LTC_sell.append ( i['price'] )
                time_LTC_sell.append ( i['time'] )

            elif i['currency'] == 'ETH':
                amt_ETH_sell.append ( i['amount'] )
                price_ETH_sell.append ( i['price'] )
                time_ETH_sell.append ( i['time'] )

            else:
                continue

    return amt_BTC_sell, amt_LTC_sell, amt_ETH_sell, price_BTC_sell, price_LTC_sell, price_ETH_sell, time_BTC_sell, time_LTC_sell, time_ETH_sell


def after_sell(sell_list, amt_sell_list, buy_list, amt_buy_list):
    avg = []
    current = []
    fifo = []

    if len ( sell_list ) != 0:

        if sum ( amt_buy_list ) >= sum ( amt_sell_list ):

            x = len ( amt_sell_list )

            latest_amt = amt_sell_list[-1]
            for num1, num2 in zip ( buy_list, amt_buy_list ):
                fifo.append ( [num1] * num2 )

            flat_list = [item for sublist in fifo for item in sublist]

            amt_sold = amt_sell_list[:(x - 1)]
            sum_sold = sum ( amt_sold )

            del_sells = flat_list[sum_sold:]
            cut_fifo = del_sells[latest_amt:]
            ann_cut = del_sells[:latest_amt]

            products = []

            part_profit = (latest_amt * sell_list[-1]) - (sum ( ann_cut ))
            current.append ( part_profit )
            avg.append ( new_average ( cut_fifo ) )


    else:

        if len ( buy_list ) == 0:
            current.append ( 0 )
            avg.append ( 0 )

        else:

            products = []
            avg.append ( new_average ( buy_list ) )
            for num1, num2 in zip ( buy_list, amt_buy_list ):
                products.append ( num1 * num2 )

            current.append ( (-1) * sum ( products ) )

    return current, avg


def new_average(list):
    if len ( list ) == 0:
        avg = 0

    else:

        avg = (sum ( list ) / len ( list ))

    return avg


def calc_new_avg(new_avg_BTC, new_avg_LTC, new_avg_ETH, label_btc, label_eth, label_ltc):
    amt_BTC, amt_LTC, amt_ETH, price_BTC, price_LTC, price_ETH, time_BTC, time_LTC, time_ETH = file_values_buy ()
    amt_BTC_sell, amt_LTC_sell, amt_ETH_sell, price_BTC_sell, price_LTC_sell, price_ETH_sell, time_BTC_sell, time_LTC_sell, time_ETH_sell = file_values_sell ()

    cur1, avg1 = after_sell ( price_BTC_sell, amt_BTC_sell, price_BTC, amt_BTC )
    cur2, avg2 = after_sell ( price_LTC_sell, amt_LTC_sell, price_LTC, amt_LTC )
    cur3, avg3 = after_sell ( price_ETH_sell, amt_ETH_sell, price_ETH, amt_ETH )

    new_avg_BTC.append ( avg1 )
    new_avg_LTC.append ( avg2 )
    new_avg_ETH.append ( avg3 )

    label_btc.append ( cur1 )
    label_ltc.append ( cur2 )
    label_eth.append ( cur3 )

    return new_avg_BTC, new_avg_ETH, new_avg_LTC, label_btc, label_eth, label_ltc


def get_values(currency1):
    try:
        req = requests.get ( connect ( currency1, "PLN" ) ).json ()
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

    response = requests.request ( "GET", url, params=queryparams )

    response = eval ( response.text )

    return sum ( [float ( response['items'][i]['a'] ) for i in range ( len ( response['items'] ) )] )


def calc_avg(data, n):
    sub_data = data[-n:]
    avg = sum ( sub_data ) / len ( sub_data )

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

        bid, ask = get_values ( i )
        ask_list.append ( ask )
        bid_list.append ( bid )

        volume = get_volumen ( f'{i}-PLN' )
        volumen_list.append ( volume )

        bid_avg = calc_avg ( bid_list, N )
        ask_avg = calc_avg ( ask_list, N )
        avg_ask_graph.append ( ask_avg )
        avg_bid_graph.append ( bid_avg )

        rsi_ask.append ( calc_RSI ( ask_list, lower, upper ) )
        rsi_bid.append ( calc_RSI ( bid_list, lower, upper ) )

        return ask_list, bid_list, volumen_list, avg_ask_graph, avg_bid_graph, rsi_ask, rsi_bid


def trend(rsi_list):
    rsi = rsi_list[-1]

    if rsi >= 70:
        return 'Strefa wyprzedarzy'

    elif rsi <= 30:
        return 'Strefa wykupienia'

    else:
        return 'Boczny trend'


def find_candidate(trends_list, volume_list):
    volume_compare = list ()

    for i in range ( 3 ):

        if trends_list[i] != 'Strefa wykupienia':
            volume_compare.append ( volume_list[i][-1] )

    if len ( volume_compare ) != 0:
        max_volume = max ( volume_compare )
        ind = volume_compare.index ( max_volume )

        return currency1[ind], f' Current candidate is: {currency1[ind]}'

    else:
        return None, 'There is no candidate at the moment'


def is_volatile(buy_list, X, Y):
    Y_list = buy_list[-Y:]

    value = (abs ( max ( Y_list ) - min ( Y_list ) ) / max ( Y_list )) * 100

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

    for i in range ( len ( currency1 ) ):
        if currency1[i] == candidate:
            title_l = is_liquid ( buy_list[i], sell_list[i], S )
            title_v = is_volatile ( buy_list[i], X, Y )
            l_title.insert ( i, title_l )
            v_title.insert ( i, title_v )
        else:
            l_title.insert ( i, '' )
            v_title.insert ( i, '' )
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

    amt_BTC, amt_LTC, amt_ETH, price_BTC, price_LTC, price_ETH, time_BTC, time_LTC, time_ETH = file_values_buy ()
    new_BTC, new_ETH, new_LTC, label_BTC, label_ETH, label_LTC = calc_new_avg ( new_avg_BTC, new_avg_LTC, new_avg_ETH,
                                                                                label_btc, label_eth, label_ltc )

    t.append ( time.strftime ( "%H:%M:%S", time.localtime () ) )

    trend_BTC = trend ( rsi_b1 )
    trend_LTC = trend ( rsi_b2 )
    trend_ETH = trend ( rsi_b3 )

    candidate, subtitle = find_candidate ( [trend_BTC, trend_LTC, trend_ETH], [vol1, vol2, vol3] )

    title1, title2, title3, title4, title5, title6 = set_title ( candidate, [ask1, ask2, ask3], [bid1, bid2, bid3], X,
                                                                 Y, S )

    suma1 = []
    suma2 = []
    suma3 = []

    for i in label_BTC:
        for j in label_BTC:
            for k in j:
                suma1.append ( k )

    for i in label_LTC:
        for j in label_LTC:
            for k in j:
                suma2.append ( k )

    for i in label_ETH:
        for j in label_ETH:
            for k in j:
                suma3.append ( k )

    sumaBTC = sum ( suma1 )
    sumaLTC = sum ( suma2 )
    sumaETH = sum ( suma3 )

    if sumaBTC < 0:
        title1_words = f'Your loss on BTC equals {sumaBTC}'
    elif sumaBTC == 0:
        title1_words = 0
    else:
        title1_words = f'Your gain on BTC equals {sumaBTC}'

    if sumaLTC < 0:
        title2_words = f'Your loss on BTC equals {sumaLTC}'
    elif sumaLTC == 0:
        title2_words = 0
    else:
        title2_words = f'Your gain on BTC equals {sumaLTC}'

    if sumaETH < 0:
        title3_words = f'Your loss on BTC equals {sumaETH}'
    elif sumaETH == 0:
        title3_words = 0
    else:
        title3_words = f'Your gain on BTC equals {sumaETH}'

    ticks = list ()

    if len ( t ) > 3:
        ticks.append ( t[0] )
        middle = int ( len ( t ) / 2 )
        middle1 = int ( middle / 2 )
        middle2 = middle + middle1
        ticks.append ( t[middle] )
        ticks.append ( t[middle1] )
        ticks.append ( t[middle2] )
        ticks.append ( t[-1] )

    else:
        ticks = t

    plt.clf ()
    plt.ion ()
    plt.suptitle ( subtitle, fontsize=10 )
    plt.tight_layout ()

    plt.subplot ( 331 )
    plt.title ( f'{currency1[0]} {title1} \n {title4}', size=7 )

    plt.plot ( t, ask1, label="buys", color="blue" )
    plt.plot ( t, bid1, label="sells", color="yellow" )
    plt.plot ( time_BTC, price_BTC, '*', color="purple" )
    plt.plot ( new_BTC, "--", label="new avg", color='pink' )

    plt.plot ( t, avg_ask1, '--', label='buy avg', color='black' )
    plt.plot ( t, avg_bid1, '--', label='sell avg', color='red' )

    plt.ylabel ( "Currency rate" )
    plt.xticks ( [] )
    plt.yticks ( fontsize=6 )
    plt.yscale ( 'log' )

    plt.subplot ( 334 )
    plt.title ( 'Volume', size=7 )
    plt.plot ( t, vol1, "--", color='purple' )
    plt.xticks ( [] )
    plt.ylabel ( "Volume" )
    plt.yticks ( fontsize=6 )

    plt.subplot ( 337 )
    plt.title ( f'RSI - {trend_BTC}', size=7 )
    plt.plot ( t, rsi_b1, label='buy RSI', color='orange' )
    plt.plot ( t, rsi_a1, ':', label='sell RSI', color='purple' )
    plt.ylabel ( "RSI " )
    plt.xticks ( ticks=ticks, rotation='vertical', size=7 )
    plt.xlabel ( "Time", size=8 )
    plt.yticks ( fontsize=6 )

    plt.subplot ( 332 )
    plt.title ( f'{currency1[1]} {title2} \n {title5}', size=7 )

    plt.plot ( t, ask2, label="buys", color="blue" )
    plt.plot ( t, bid2, label="sells", color="yellow" )
    plt.plot ( time_LTC, price_LTC, '*', label="new", color="purple" )
    plt.plot ( t, new_LTC, "--", label="new avg", color='pink' )
    plt.plot ( t, avg_ask2, '--', label='buy avg', color='black' )
    plt.plot ( t, avg_bid2, '--', label='sell avg', color='red' )
    plt.xticks ( [] )
    plt.yticks ( fontsize=6 )

    plt.subplot ( 335 )
    plt.title ( 'Volume ', size=7 )
    plt.plot ( t, vol2, "--", color='purple' )
    plt.xticks ( [] )
    plt.yticks ( fontsize=6 )

    plt.subplot ( 338 )
    plt.title ( f'RSI  - {trend_LTC}', size=7 )
    plt.plot ( t, rsi_b2, label='buy RSI', color='orange' )
    plt.plot ( t, rsi_a2, ':', label='sell RSI', color='purple' )
    plt.xticks ( ticks=ticks, rotation='vertical', size=7 )
    plt.xlabel ( "Time", size=8 )
    plt.yticks ( fontsize=6 )

    plt.subplot ( 333 )
    plt.title ( f'{currency1[2]} {title3} \n {title6}', size=7 )

    plt.plot ( t, ask3, label="buys", color="blue" )
    plt.plot ( t, bid3, label="sells", color="yellow" )
    plt.plot ( time_ETH, price_ETH, '*', label="new", color="purple" )
    plt.plot ( t, new_ETH, "--", label="new avg", color='pink' )

    plt.plot ( t, avg_ask3, '--', label='buy avg', color='black' )
    plt.plot ( t, avg_bid3, '--', label='sell avg', color='red' )
    plt.legend ( bbox_to_anchor=(1.05, 1.0), loc='upper left' )
    plt.xticks ( [] )
    plt.yticks ( fontsize=6 )

    plt.subplot ( 336 )
    plt.title ( 'Volume', size=7 )
    plt.plot ( t, vol3, "--", color='purple' )
    plt.xticks ( [] )
    plt.yticks ( fontsize=6 )

    btc_lab = mpatches.Patch ( label=title1_words )
    ltc_lab = mpatches.Patch ( label=title2_words )
    eth_lab = mpatches.Patch ( label=title3_words )

    plt.legend ( handles=[btc_lab, ltc_lab, eth_lab], bbox_to_anchor=(1.05, 1.0), loc='upper left' )

    plt.subplot ( 339 )
    plt.title ( f'RSI - {trend_BTC}', size=7 )
    plt.plot ( t, rsi_b3, label='buy RSI', color='orange' )
    plt.plot ( t, rsi_a3, ':', label='sell RSI', color='purple' )
    plt.legend ( bbox_to_anchor=(1.05, 1.0), loc='upper left' )
    plt.xticks ( ticks=ticks, rotation='vertical', size=7 )
    plt.xlabel ( "Time", size=8 )
    plt.yticks ( fontsize=6 )


def animation():
    anim = FuncAnimation ( plt.figure (), create_graph, interval=1000 )
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

    new_avg_BTC = []
    new_avg_LTC = []
    new_avg_ETH = []
    label_btc = []
    label_eth = []
    label_ltc = []

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
