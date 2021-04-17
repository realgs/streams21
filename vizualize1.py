import matplotlib.pyplot as plt
import currency
from matplotlib.animation import FuncAnimation
from matplotlib import style
import datetime


def get_bid_ask(url: str, pair: str):
    result = currency.get_info([url], [pair], printing=False)
    if result is None:
        print("Data could not be retrieved")
        return False, False, False

    current_time = datetime.datetime.now().strftime("%H:%M:%S")

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

    return best_ask_value, best_bid_value, current_time


def change_single_pair(number):
    print(f"Number of iteration: {number}")
    global ask_values, bid_values, times_list, URL, PAIR, is_legend

    res = get_bid_ask(URL, PAIR)
    ask_values.append(res[0])
    bid_values.append(res[1])
    times_list.append(res[2])

    current_time_labels = times_list.copy()

    if len(current_time_labels) > 12:
        current_time_labels = current_time_labels[::4]

    plt.title(PAIR)

    plt.plot(times_list, ask_values, color='green', label='ask')
    plt.plot(times_list, bid_values, color='red', label='bid')

    plt.xticks(current_time_labels, rotation='vertical')
    if not is_legend:
        plt.legend(loc=2)
        is_legend = True


if __name__ == "__main__":
    FREQUENCY = 5  # seconds
    REPEAT = 20

    PAIR = 'BTC-USD'
    #PAIR = 'ETH-USD'
    #PAIR = 'LTC-USD'
    URL = "https://api.bittrex.com/v3/markets/{}/orderbook".format(PAIR)
    MAX_LENGTH = 20
    is_legend = False

    ask_values = list()
    bid_values = list()
    times_list = list()

    style.use('ggplot')
    animation = FuncAnimation(plt.gcf(), func=change_single_pair, interval=FREQUENCY*1000)
    plt.show()
