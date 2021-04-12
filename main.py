import requests
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter

BITBAY_API_URL = 'https://api.bitbay.net/rest/trading/orderbook-limited/CURRENCY_PAIR/10'
FETCH_INTERVAL = 5000


def fetch_best_offers(currency_pair):
    try:
        response = requests.get(BITBAY_API_URL.replace('CURRENCY_PAIR', currency_pair)).json()

        return {
            'sell': float(response['sell'][0]['ra']),
            'buy': float(response['buy'][0]['ra']),
            'time': datetime.now()
        }
    except Exception as e:
        print('fetch_best_offers(): Something went wrong during fetching best offers from orderbook.')
        print(f'Error: {e}\n')
        return False


def gen_empty_arrays(n):
    return [[] for _ in range(n)]


def show_plots(currency_pairs):
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

            lines[i*2].set_data(time[i], buy[i])
            lines[i*2+1].set_data(time[i], sell[i])

            axs[i].relim()
            axs[i].autoscale_view()

        return lines

    plt.style.use('seaborn-dark')
    n = len(currency_pairs)
    time, buy, sell = gen_empty_arrays(n), gen_empty_arrays(n), gen_empty_arrays(n)

    fig, axs = plt.subplots(n, figsize=(15, 10), sharex=True)
    lines = []

    for i in range(len(currency_pairs)):
        line_buy, = axs[i].plot([], [], label=f'Best buy offer')
        line_sell, = axs[i].plot([], [], label=f'Best sell offer')
        lines.append(line_buy)
        lines.append(line_sell)

        axs[i].set_title(currency_pairs[i])
        axs[i].grid()
        axs[i].legend()
        axs[i].xaxis.set_major_formatter(DateFormatter('%d-%m-%y %H:%M:%S'))

    fig.autofmt_xdate()
    anim = FuncAnimation(fig, update, interval=FETCH_INTERVAL)
    plt.show()


def main():
    currency_pairs = ['BTC-USD', 'LTC-USD', 'DASH-USD']
    show_plots(currency_pairs)


if __name__ == '__main__':
    main()
