import matplotlib.pyplot as plt
import currency
import datetime
import requests
from matplotlib import style
from matplotlib.dates import DateFormatter
from matplotlib.animation import FuncAnimation


def get_volume(url, pair):
    global LAST_VOLUME_LIST
    try:
        response = requests.get(url).json()
    except requests.exceptions.ConnectionError:
        print("Connection error has occurred")
        return 0

    if LAST_VOLUME_LIST[pair] is None:
        try:
            LAST_VOLUME_LIST[pair] = datetime.datetime.strptime(response[0]["executedAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            LAST_VOLUME_LIST[pair] = datetime.datetime.strptime(response[0]["executedAt"], "%Y-%m-%dT%H:%M:%SZ")
        return 0
    else:
        volume = 0
        for item in response:
            try:
                item_time = datetime.datetime.strptime(item["executedAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                item_time = datetime.datetime.strptime(item["executedAt"], "%Y-%m-%dT%H:%M:%SZ")

            if item_time <= LAST_VOLUME_LIST[pair]:
                try:
                    LAST_VOLUME_LIST[pair] = datetime.datetime.strptime(response[0]["executedAt"],
                                                                        "%Y-%m-%dT%H:%M:%S.%fZ")
                except ValueError:
                    LAST_VOLUME_LIST[pair] = datetime.datetime.strptime(response[0]["executedAt"], "%Y-%m-%dT%H:%M:%SZ")
                break
            volume += float(item["quantity"])
        return volume


def calculate_rsi(pair):
    global dict_of_ask_bid_lists, dict_of_changes
    global USER_PARAMETER
    if len(dict_of_ask_bid_lists[pair][1]) > USER_PARAMETER:
        value = dict_of_ask_bid_lists[pair][1][-1] - \
                dict_of_ask_bid_lists[pair][1][-USER_PARAMETER]
        if value > 0:
            dict_of_changes[pair][0].append(value)
        elif value < 0:
            dict_of_changes[pair][1].append(value)
        a = (sum(dict_of_changes[pair][0]) + 1) / (len(dict_of_changes[pair][0]) + 1)
        b = (sum(dict_of_changes[pair][1]) + 1) / (len(dict_of_changes[pair][1]) + 1)
    else:
        a = 1
        b = 1
    try:
        rsi_value = 100 - (100 / (1 + abs((a / b))))
    except ZeroDivisionError:
        return 50
    return rsi_value


def check_if_candidate(pair):
    global PAIRS, dict_of_ask_bid_lists
    highest_volume = 0
    highest_pair = None
    for pa in PAIRS:
        if sum(dict_of_ask_bid_lists[pa][5][-3:-1]) > highest_volume:
            highest_volume = dict_of_ask_bid_lists[pa][5][-1]
            highest_pair = pa
    if highest_pair == pair:
        return "Yes"
    else:
        return "No"


def get_x_last_transactions(n, pair):
    global VOLUME_URLS, dict_of_ask_bid_lists
    try:
        response = requests.get(VOLUME_URLS[list(dict_of_ask_bid_lists.keys()).index(pair)]).json()
    except requests.exceptions.ConnectionError:
        print("Connection error has occurred")
        return 0
    rates = []
    for g in range(n, -1, -1):
        rates.append(float(response[-g-1]["rate"]))
    return rates


def is_volatile(pair):
    global VOLATILE_EDGE, VOLATILE_NUMBER, dict_of_ask_bid_lists
    rate_list = get_x_last_transactions(VOLATILE_NUMBER, pair)
    difference = 0
    for k in range(len(rate_list), 0, -1):
        difference += abs(1 - (rate_list[-k]/rate_list[-k+1]))
    if difference > VOLATILE_EDGE:
        return ""
    else:
        return ",volatile asset"


def is_liquid(pair):
    global LIQUID_EDGE, dict_of_ask_bid_lists
    if (dict_of_ask_bid_lists[pair][3][-1] - dict_of_ask_bid_lists[pair][4][-1]) / dict_of_ask_bid_lists[pair][3][-1] \
            < LIQUID_EDGE:
        return ",liquid"
    else:
        return ""


def check_trend(pair, iteration):
    global dict_of_ask_bid_lists
    if iteration < 4:
        return "None", "No", "", ""
    rsi_values = dict_of_ask_bid_lists[pair][6]
    if rsi_values[-3] > rsi_values[-2] > rsi_values[-1]:
        return "downward", "No", "", ""
    if (rsi_values[-3] > rsi_values[-2] and rsi_values[-2] < rsi_values[-1]) or rsi_values[-3] < rsi_values[-2] and \
            rsi_values[-2] > rsi_values[-1]:
        return "sideways", check_if_candidate(pair), is_volatile(pair), is_liquid(pair)
    if rsi_values[-3] < rsi_values[-2] < rsi_values[-1]:
        return "rising", check_if_candidate(pair), is_volatile(pair), is_liquid(pair)
    return "None", "No", "", ""


def get_bid_ask(url: str, pair: str, i: int):
    global VOLUME_URLS

    result = currency.get_info([url], [pair], printing=False)
    if result is None:
        print("Data could not be retrieved")
        return False, False, False

    current_time = datetime.datetime.now()

    asks = result[0]['ask']
    best_ask_value = 0
    avg_ask_value = 0
    for ask in asks:
        avg_ask_value += float(ask['rate'])
        if float(ask['rate']) > best_ask_value:
            best_ask_value = float(ask['rate'])
    avg_ask_value /= len(asks)

    bids = result[0]['bid']
    best_bid_value = 0
    avg_bid_value = 0
    for bid in bids:
        avg_bid_value += float(bid['rate'])
        if float(bid['rate']) > best_bid_value:
            best_bid_value = float(bid['rate'])
    avg_bid_value /= len(bids)

    volume = get_volume(VOLUME_URLS[i], pair)

    result = {'time': current_time,
              'ask': best_ask_value,
              'bid': best_bid_value,
              'avg_ask': avg_ask_value,
              'avg_bid': avg_bid_value,
              'volume': volume}
    return result


def show_multiple_pairs():
    global URLS, PAIRS, FREQUENCY, dict_of_ask_bid_lists, TITLE_TEMPLATE, MOVING_AVERAGE_LENGTH

    def update_data(number):
        print(number)
        for i in range(len(PAIRS)):
            res = get_bid_ask(URLS[i], PAIRS[i], i)

            dict_of_ask_bid_lists[PAIRS[i]][0].append(res['time'])
            dict_of_ask_bid_lists[PAIRS[i]][1].append(res['ask'])
            dict_of_ask_bid_lists[PAIRS[i]][2].append(res['bid'])
            dict_of_ask_bid_lists[PAIRS[i]][3].append(res['avg_ask'])
            dict_of_ask_bid_lists[PAIRS[i]][4].append(res['avg_bid'])
            dict_of_ask_bid_lists[PAIRS[i]][5].append(res['volume'])

            # ask
            list_of_lines[i * 6 + 0].set_data(dict_of_ask_bid_lists[PAIRS[i]][0], dict_of_ask_bid_lists[PAIRS[i]][1])
            # bid
            list_of_lines[i * 6 + 1].set_data(dict_of_ask_bid_lists[PAIRS[i]][0], dict_of_ask_bid_lists[PAIRS[i]][2])

            #moving averages
            if len(dict_of_ask_bid_lists[PAIRS[i]][7]) < MOVING_AVERAGE_LENGTH:
                moving_average_ask = (sum(dict_of_ask_bid_lists[PAIRS[i]][7])+dict_of_ask_bid_lists[PAIRS[i]][3][-1]) \
                                     / (len(dict_of_ask_bid_lists[PAIRS[i]][7])+1)
                dict_of_ask_bid_lists[PAIRS[i]][7].append(moving_average_ask)
                list_of_lines[i * 6 + 2].set_data(dict_of_ask_bid_lists[PAIRS[i]][0],
                                                  dict_of_ask_bid_lists[PAIRS[i]][7])

                moving_average_bid = (sum(dict_of_ask_bid_lists[PAIRS[i]][8]) + dict_of_ask_bid_lists[PAIRS[i]][4][-1])\
                                     / (len(dict_of_ask_bid_lists[PAIRS[i]][8]) + 1)
                dict_of_ask_bid_lists[PAIRS[i]][8].append(moving_average_bid)
                list_of_lines[i * 6 + 3].set_data(dict_of_ask_bid_lists[PAIRS[i]][0],
                                                  dict_of_ask_bid_lists[PAIRS[i]][8])

            else:
                moving_average_ask = (sum(dict_of_ask_bid_lists[PAIRS[i]][7][-MOVING_AVERAGE_LENGTH:]) +
                                      dict_of_ask_bid_lists[PAIRS[i]][3][-1]) / (MOVING_AVERAGE_LENGTH+1)
                dict_of_ask_bid_lists[PAIRS[i]][7].append(moving_average_ask)
                list_of_lines[i * 6 + 2].set_data(dict_of_ask_bid_lists[PAIRS[i]][0],
                                                  dict_of_ask_bid_lists[PAIRS[i]][7])

                moving_average_bid = (sum(dict_of_ask_bid_lists[PAIRS[i]][8][-MOVING_AVERAGE_LENGTH:]) +
                                      dict_of_ask_bid_lists[PAIRS[i]][4][-1]) / (MOVING_AVERAGE_LENGTH+1)
                dict_of_ask_bid_lists[PAIRS[i]][8].append(moving_average_bid)
                list_of_lines[i * 6 + 3].set_data(dict_of_ask_bid_lists[PAIRS[i]][0],
                                                  dict_of_ask_bid_lists[PAIRS[i]][8])

            current_trend = check_trend(PAIRS[i], number)
            axs[0][i].set_title(TITLE_TEMPLATE.format(PAIRS[i], current_trend[0], current_trend[1], current_trend[2],
                                                      current_trend[3]))

            rsi = calculate_rsi(PAIRS[i])
            dict_of_ask_bid_lists[PAIRS[i]][6].append(rsi)
            list_of_lines[i * 6 + 4].set_data(dict_of_ask_bid_lists[PAIRS[i]][0], dict_of_ask_bid_lists[PAIRS[i]][6])

            list_of_lines[i * 6 + 5].set_data(dict_of_ask_bid_lists[PAIRS[i]][0], dict_of_ask_bid_lists[PAIRS[i]][5])

            axs[0][i].relim()
            axs[0][i].autoscale_view()

            axs[1][i].relim()
            axs[1][i].autoscale_view()

            axs[2][i].relim()
            axs[2][i].autoscale_view()

    fig, axs = plt.subplots(3, len(PAIRS), figsize=(30, 30), sharex='none')
    list_of_lines = list()

    for j in range(len(PAIRS)):
        ask_chart, = axs[0][j].plot(dict_of_ask_bid_lists[PAIRS[j]][0], dict_of_ask_bid_lists[PAIRS[j]][1],
                                    label='ask', color='red')
        bid_chart, = axs[0][j].plot(dict_of_ask_bid_lists[PAIRS[j]][0], dict_of_ask_bid_lists[PAIRS[j]][2],
                                    label='bid', color='green')
        avg_ask_chart, = axs[0][j].plot(dict_of_ask_bid_lists[PAIRS[j]][0], dict_of_ask_bid_lists[PAIRS[j]][3],
                                        label='ask avg', color='blue')
        avg_bid_chart, = axs[0][j].plot(dict_of_ask_bid_lists[PAIRS[j]][0], dict_of_ask_bid_lists[PAIRS[j]][4],
                                        label='bid avg', color='yellow')

        list_of_lines.append(ask_chart)
        list_of_lines.append(bid_chart)
        list_of_lines.append(avg_ask_chart)
        list_of_lines.append(avg_bid_chart)

        axs[0][j].set_title(TITLE_TEMPLATE.format(PAIRS[j], "None", "No", "", ""))
        axs[0][j].grid()
        axs[0][j].legend(loc=2)
        # axs[0][j].xaxis.set_major_formatter(DateFormatter('%d-%m-%y %H:%M:%S'))
        axs[0][j].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

        rsi_chart, = axs[2][j].plot(dict_of_ask_bid_lists[PAIRS[j]][0], dict_of_ask_bid_lists[PAIRS[j]][5],
                                    label='rsi', color='purple')
        list_of_lines.append(rsi_chart)

        axs[2][j].set_title(f"{PAIRS[j]} RSI")
        axs[2][j].grid()
        axs[2][j].legend(loc=2)
        # axs[2][j].xaxis.set_major_formatter(DateFormatter('%d-%m-%y %H:%M:%S'))
        axs[2][j].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

        volume_chart, = axs[1][j].plot(dict_of_ask_bid_lists[PAIRS[j]][0], dict_of_ask_bid_lists[PAIRS[j]][6],
                                       label="total volume", color='red')
        list_of_lines.append(volume_chart)

        axs[1][j].set_title(str(f"{PAIRS[j]} volume"))
        axs[1][j].grid()
        axs[1][j].legend(loc=2)
        # axs[1][j].xaxis.set_major_formatter(DateFormatter('%d-%m-%y %H:%M:%S'))
        axs[1][j].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    # fig.autofmt_xdate()
    plt.xticks(rotation='horizontal')
    _ = FuncAnimation(fig, update_data, interval=FREQUENCY * 1000)
    plt.show()


if __name__ == "__main__":
    FREQUENCY = 5  # seconds
    REPEAT = 20
    USER_PARAMETER = 4

    AVG_LENGTH = 10  # how many periods we want to analyse
    TITLE_TEMPLATE = "{}, TREND: {}, CANDIDATE: {} {} {}"
    VOLATILE_NUMBER = 4  # number of probes we go back
    VOLATILE_EDGE = 0.1  # %
    LIQUID_EDGE = 0.1  # %

    URL = "https://api.bittrex.com/v3/markets/{}/orderbook"
    PAIRS = ['BTC-USD',
             'ETH-USD',
             'LTC-USD']

    URLS = list()
    for p in range(len(PAIRS)):
        URLS.append(URL.format(PAIRS[p]))
    MOVING_AVERAGE_LENGTH = 10

    VOLUME_URL = "https://api.bittrex.com/v3/markets/{}/trades"
    VOLUME_URLS = list()
    for p in range(len(PAIRS)):
        VOLUME_URLS.append(VOLUME_URL.format(PAIRS[p]))

    # style.use('ggplot')
    style.use('seaborn-paper')

    LAST_VOLUME_LIST = {}
    for p in PAIRS:
        LAST_VOLUME_LIST[p] = None

    dict_of_ask_bid_lists = dict()
    for p in PAIRS:
        # time, ask, bid, ask_avg, bid_avg, volume, rsi, moving_avg_ask, moving_avg_bid
        dict_of_ask_bid_lists[p] = [list(), list(), list(), list(), list(), list(), list(), list(), list()]

    dict_of_changes = dict()
    for p in PAIRS:
        # increase, decrease
        dict_of_changes[p] = [list(), list()]

    show_multiple_pairs()

# okno przesuwne po best ask/bid po czasie
