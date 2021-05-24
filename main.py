import requests
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter

URL = 'https://api.bitbay.net/rest/trading/orderbook-limited/CURRENCY_PAIR/10'
FETCH_INTERVAL = 5000


def fetch_best_offers(currency_pair):
    try:
        response = requests.get(URL.replace('CURRENCY_PAIR', currency_pair)).json()

        return {
            'sell': float(response['sell'][0]['ra']),
            'buy': float(response['buy'][0]['ra']),
            'volume': float(response['sell'][0]['ca']) + float(response['buy'][0]['ca']),
            'time': datetime.now()
        }
    except Exception as e:
        print(f'Error: {e}\n')
        return False


def arr(n):
    return [[] for  n in range(n)]


def calculate_RSI(data_chunk):
    ups_mean, ups_counter, downs_mean, downs_counter = 0, 0, 0, 0
    for i in range(1, len(data_chunk)):
        if data_chunk[i-1] > data_chunk[i]:
            downs_mean += data_chunk[i-1] - data_chunk[i]
            downs_counter += 1
        elif data_chunk[i-1] < data_chunk[i]:
            ups_mean += data_chunk[i] - data_chunk[i-1]
            ups_counter += 1

    if ups_counter:
        ups_mean /= ups_counter

    if downs_counter:
        downs_mean /= downs_counter
    else:
        downs_mean = 1

    return 100 - (100 / (1 + (ups_mean / downs_mean)))


def show_plots(currency_pairs, sma_buy_per, sma_sell_per, rsi_buy_per, rsi_sell_per):
    def update(_):
        for i in range(n):
            currency_pair = currency_pairs[i]
            orderbook = fetch_best_offers(currency_pair)
            if not orderbook:
                print('print_offers(): Something went wrong during fetching orderbook.')
                return

            time[i].append(orderbook['time'])
            buy[i].append(orderbook['buy'])
            sell[i].append(orderbook['sell'])
            volume[i].append(orderbook['volume'])

            if len(time[i]) >= sma_buy_per:
                tmp = buy[i][-sma_buy_per:]
                sma_buy[i].append(sum(tmp) / len(tmp))
                lines[7 * (i + 1) - 5].set_data(time[i][-len(sma_buy[i]):], sma_buy[i])

            if len(time[i]) >= sma_sell_per:
                tmp = sell[i][-sma_sell_per:]
                sma_sell[i].append(sum(tmp) / len(tmp))
                lines[7 * (i + 1) - 4].set_data(time[i][-len(sma_sell[i]):], sma_sell[i])

            if len(time[i]) >= rsi_buy_per:
                buy_chunk = buy[i][-rsi_buy_per:]
                rsi_buy[i].append(calculate_RSI(buy_chunk))
                lines[7 * (i + 1) - 2].set_data(time[i][-len(rsi_buy[i]):], rsi_buy[i])

            if len(time[i]) >= rsi_sell_per:
                sell_chunk = sell[i][-rsi_sell_per:]
                rsi_sell[i].append(calculate_RSI(sell_chunk))
                lines[7 * (i + 1) - 1].set_data(time[i][-len(rsi_sell[i]):], rsi_sell[i])

            lines[7 * (i + 1) - 7].set_data(time[i], buy[i])
            lines[7 * (i + 1) - 6].set_data(time[i], sell[i])
            lines[7 * (i + 1) - 3].set_data(time[i], volume[i])

            for j in [2, 3]:
                axs[3 * (i + 1) - j].relim()
                axs[3 * (i + 1) - j].autoscale_view()

        return lines

    mpl.use('TKAgg')
    plt.style.use('seaborn-dark')
    n = len(currency_pairs)
    time, buy, sell, volume, sma_buy, sma_sell, rsi_buy, rsi_sell = arr(n), arr(n), arr(n), \
                                                                    arr(n), arr(n), arr(n), \
                                                                    arr(n), arr(n)

    ratios = [2, 1, 2]
    fig, axs = plt.subplots(nrows=n*3, gridspec_kw={'height_ratios': ratios*n}, sharex=True)
    fig.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0.4)


    lines = []
    for i in range(len(currency_pairs)):
        line_buy, = axs[3 * (i + 1) - 3].plot([], [], label=f'Best buy offer', color='blue')
        line_sell, = axs[3 * (i + 1) - 3].plot([], [], label=f'Best sell offer', color='orange')
        line_sma_buy, = axs[3 * (i + 1) - 3].plot([], [], '--', label=f'SMA {sma_buy_per} buy', color='red')
        line_sma_sell, = axs[3 * (i + 1) - 3].plot([], [], '--', label=f'SMA {sma_buy_per} sell', color='green')
        dot_volume, = axs[3 * (i + 1) - 2].plot([], [], 'o', markersize=3)
        line_rsi_buy, = axs[3 * (i + 1) - 1].plot([], [], label=f'RSI {rsi_buy_per} buy')
        line_rsi_sell, = axs[3 * (i + 1) - 1].plot([], [], label=f'RSI {rsi_sell_per} sell')
        lines.extend([line_buy, line_sell, line_sma_buy, line_sma_sell, dot_volume, line_rsi_buy, line_rsi_sell])

        axs[3*(i+1)-3].set_title(currency_pairs[i])
        axs[3*(i+1)-3].grid()
        axs[3*(i+1)-3].legend()
        axs[3*(i+1)-3].xaxis.set_major_formatter(DateFormatter('%d-%m-%y %H:%M:%S'))

        axs[3*(i+1)-2].set_ylabel(f'Volume [{currency_pairs[i].split("-")[0]}]')
        axs[3*(i+1)-2].grid()

        axs[3*(i+1)-1].set_ylabel('RSI')
        axs[3*(i+1)-1].set_ylim(-5, 105)
        axs[3*(i+1)-1].legend()
        axs[3*(i+1)-1].grid()

    fig.autofmt_xdate()
    anim = FuncAnimation(fig, update, interval=FETCH_INTERVAL)
    plt.show()


def main():
    currency_pairs = ['BTC-PLN', 'ETH-PLN', 'LTC-PLN']
    show_plots(currency_pairs, sma_buy_per=5, sma_sell_per=5, rsi_buy_per=10, rsi_sell_per=10)


if __name__ == '__main__':
    main()
