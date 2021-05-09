import matplotlib.pyplot as plt
import currency
import datetime
from matplotlib import style
from matplotlib.dates import DateFormatter
from matplotlib.animation import FuncAnimation


def get_bid_ask(url: str, pair: str):
    result = currency.get_info([url], [pair], printing=False)
    if result is None:
        print("Data could not be retrieved")
        return False, False, False

    current_time = datetime.datetime.now()

    asks = result[0]['ask']
    best_ask_value = 0
    for ask in asks:
        if float(ask['rate']) > best_ask_value:
            best_ask_value = float(ask['rate'])

    bids = result[0]['bid']
    best_bid_value = 0
    for bid in bids:
        if float(bid['rate']) > best_bid_value:
            best_bid_value = float(bid['rate'])

    result = {'time': current_time,
              'ask': best_ask_value,
              'bid': best_bid_value}
    # print(pair, result)
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

            list_of_lines[i*2].set_data(dict_of_ask_bid_lists[PAIRS[i]][0], dict_of_ask_bid_lists[PAIRS[i]][1])
            list_of_lines[i*2 + 1].set_data(dict_of_ask_bid_lists[PAIRS[i]][0], dict_of_ask_bid_lists[PAIRS[i]][2])

            axs[i].relim()
            axs[i].autoscale_view()

    fig, axs = plt.subplots(len(PAIRS), figsize=(30, 30), sharex='all')
    list_of_lines = []

    for j in range(len(PAIRS)):
        ask_chart, = axs[j].plot(dict_of_ask_bid_lists[PAIRS[j]][0], dict_of_ask_bid_lists[PAIRS[j]][1],
                                 label='ask', color='red')
        bid_chart, = axs[j].plot(dict_of_ask_bid_lists[PAIRS[j]][0], dict_of_ask_bid_lists[PAIRS[j]][2],
                                 label='bid', color='green')
        list_of_lines.append(ask_chart)
        list_of_lines.append(bid_chart)

        axs[j].set_title(PAIRS[j])
        # configure the grid lines
        axs[j].grid()
        axs[j].legend(loc=2)
        axs[j].xaxis.set_major_formatter(DateFormatter('%d-%m-%y %H:%M:%S'))
        # axs[j].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    fig.autofmt_xdate()
    plt.xticks(rotation='vertical')
    _ = FuncAnimation(fig, update_data, interval=FREQUENCY*1000)
    plt.show()


if __name__ == "__main__":
    FREQUENCY = 5  # seconds
    REPEAT = 20

    URL = "https://api.bittrex.com/v3/markets/{}/orderbook"
    PAIRS = ['BTC-USD',
             'ETH-USD',
             'LTC-USD']

    URLS = list()
    for p in range(len(PAIRS)):
        URLS.append(URL.format(PAIRS[p]))
    MAX_LENGTH = 20

    style.use('ggplot')
    # style.use('seaborn-paper')

    dict_of_ask_bid_lists = dict()
    for p in PAIRS:
        dict_of_ask_bid_lists[p] = [list(), list(), list()]
    show_multiple_pairs()
