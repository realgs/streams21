import matplotlib.pyplot as plt
import currency
import datetime
from matplotlib import style
from matplotlib.dates import DateFormatter
from matplotlib.animation import FuncAnimation


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
    rsi_value = 100 - (100 / (1 + abs((a / b))))
    return rsi_value


def get_bid_ask(url: str, pair: str):
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

    volume = 0
    for item in result[0]['ask']:
        volume += float(item['quantity'])
    for item in result[0]['bid']:
        volume += float(item['quantity'])

    result = {'time': current_time,
              'ask': best_ask_value,
              'bid': best_bid_value,
              'avg_ask': avg_ask_value,
              'avg_bid': avg_bid_value,
              'volume': volume}
    return result


def show_multiple_pairs():
    global URLS, PAIRS, FREQUENCY, dict_of_ask_bid_lists

    def update_data(number):
        print(number)
        for i in range(len(PAIRS)):
            res = get_bid_ask(URLS[i], PAIRS[i])

            dict_of_ask_bid_lists[PAIRS[i]][0].append(res['time'])
            dict_of_ask_bid_lists[PAIRS[i]][1].append(res['ask'])
            dict_of_ask_bid_lists[PAIRS[i]][2].append(res['bid'])
            dict_of_ask_bid_lists[PAIRS[i]][3].append(res['avg_ask'])
            dict_of_ask_bid_lists[PAIRS[i]][4].append(res['avg_bid'])
            dict_of_ask_bid_lists[PAIRS[i]][5].append(res['volume'])

            list_of_lines[i * 6 + 0].set_data(dict_of_ask_bid_lists[PAIRS[i]][0], dict_of_ask_bid_lists[PAIRS[i]][1])
            list_of_lines[i * 6 + 1].set_data(dict_of_ask_bid_lists[PAIRS[i]][0], dict_of_ask_bid_lists[PAIRS[i]][2])
            list_of_lines[i * 6 + 2].set_data(dict_of_ask_bid_lists[PAIRS[i]][0], dict_of_ask_bid_lists[PAIRS[i]][3])
            list_of_lines[i * 6 + 3].set_data(dict_of_ask_bid_lists[PAIRS[i]][0], dict_of_ask_bid_lists[PAIRS[i]][4])

            rsi = calculate_rsi(PAIRS[i])
            dict_of_ask_bid_lists[PAIRS[i]][6].append(rsi)
            list_of_lines[i * 6 + 4].set_data(dict_of_ask_bid_lists[PAIRS[i]][0], dict_of_ask_bid_lists[PAIRS[i]][6])

            list_of_lines[i * 6 + 5].set_data(dict_of_ask_bid_lists[PAIRS[i]][0], dict_of_ask_bid_lists[PAIRS[i]][5])

            axs[0][i].relim()
            axs[0][i].autoscale_view()

            axs[1][i].relim()
            axs[1][i].autoscale_view()

    fig, axs = plt.subplots(2, len(PAIRS), figsize=(30, 30), sharex='none')
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
        rsi_chart, = axs[0][j].plot(dict_of_ask_bid_lists[PAIRS[j]][0], dict_of_ask_bid_lists[PAIRS[j]][5],
                                        label='rsi', color='purple')

        list_of_lines.append(ask_chart)
        list_of_lines.append(bid_chart)
        list_of_lines.append(avg_ask_chart)
        list_of_lines.append(avg_bid_chart)
        list_of_lines.append(rsi_chart)

        axs[0][j].set_title(PAIRS[j])
        axs[0][j].grid()
        axs[0][j].legend(loc=2)
        # axs[0][j].xaxis.set_major_formatter(DateFormatter('%d-%m-%y %H:%M:%S'))
        axs[0][j].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

        volume_chart, = axs[1][j].plot(dict_of_ask_bid_lists[PAIRS[j]][0], dict_of_ask_bid_lists[PAIRS[j]][6],
                                       label="total volume", color='red')
        list_of_lines.append(volume_chart)

        axs[1][j].set_title(str(f"{PAIRS[j]} volume"))
        axs[1][j].grid()
        axs[1][j].legend(loc=2)
        # axs[1][j].xaxis.set_major_formatter(DateFormatter('%d-%m-%y %H:%M:%S'))
        axs[1][j].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    #fig.autofmt_xdate()
    plt.xticks(rotation='horizontal')
    _ = FuncAnimation(fig, update_data, interval=FREQUENCY*1000)
    plt.show()


if __name__ == "__main__":
    FREQUENCY = 5  # seconds
    REPEAT = 20
    USER_PARAMETER = 4
    AVG_LENGTH = 3

    URL = "https://api.bittrex.com/v3/markets/{}/orderbook"
    PAIRS = ['BTC-USD',
             'ETH-USD',
             'LTC-USD']

    URLS = list()
    for p in range(len(PAIRS)):
        URLS.append(URL.format(PAIRS[p]))
    MAX_LENGTH = 20

    # style.use('ggplot')
    style.use('seaborn-paper')

    dict_of_ask_bid_lists = dict()
    for p in PAIRS:
        # time, ask, bid, ask_avg, bid_avg, volume, rsi
        dict_of_ask_bid_lists[p] = [list(), list(), list(), list(), list(), list(), list()]

    dict_of_changes = dict()
    for p in PAIRS:
        # increase, decrease
        dict_of_changes[p] = [list(), list()]

    show_multiple_pairs()
