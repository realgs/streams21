import requests
from time import time_ns
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.animation import FuncAnimation

BITBAY_LAST_TRANS_API_URL = 'https://api.bitbay.net/rest/trading/transactions/CURRENCY_PAIR?fromTime=TIMESTAMP_MILLIS&limit=10'
BITBAY_OFFERS_API_URL = 'https://api.bitbay.net/rest/trading/orderbook-limited/CURRENCY_PAIR/10'

CANDIDATE_LABEL = '[*]'
VOLATILE_ASSET_LABEL = '[VA]'
LIQUID_ASSET_LABEL = '[LA]'

latest_transaction_fetches_ts = {}


def print_warning(message):
    print(f'[WARNING] {message}')


def print_error(message):
    print(f'[ERROR] {message}')


def current_timestamp_millis():
    return time_ns() // 1_000_000


def fetch_avg_last_transaction(currency_pair):
    try:
        latest_fetch = 0
        if currency_pair in latest_transaction_fetches_ts:
            latest_fetch = latest_transaction_fetches_ts[currency_pair]

        response = requests.get(BITBAY_LAST_TRANS_API_URL
                                .replace('CURRENCY_PAIR', currency_pair)
                                .replace('TIMESTAMP_MILLIS', str(latest_fetch))).json()

        latest_transaction_fetches_ts[currency_pair] = current_timestamp_millis()
        transactions = response['items']

        if not transactions:
            return False

        volume, avg_price = 0, 0
        for transaction in transactions:
            tmp_volume = float(transaction['a'])
            volume += tmp_volume
            avg_price += float(transaction['r']) * tmp_volume

        avg_price /= volume

        return {
            'avg_rate': avg_price,
            'volume': volume,
            'size': len(transactions),
            'time': datetime.fromtimestamp(latest_transaction_fetches_ts[currency_pair] // 1000)
        }
    except Exception as e:
        print_error(f'Something went wrong during fetching avg latest transaction!')
        print_error(f'Message: {e}')
        return False


def fetch_best_offers(currency_pair):
    try:
        response = requests.get(BITBAY_OFFERS_API_URL.replace('CURRENCY_PAIR', currency_pair)).json()

        return {
            'sell': float(response['sell'][0]['ra']),
            'buy': float(response['buy'][0]['ra']),
            'time': datetime.now()
        }
    except Exception as e:
        print('Something went wrong during fetching best offers from orderbook.')
        print(f'Error: {e}\n')
        return False


def gen_arr(n):
    return [[] for _ in range(n)]


def calculate_RSI(data_chunk):
    ups_mean, ups_counter, downs_mean, downs_counter = 0, 0, 0, 0
    for i in range(1, len(data_chunk)):
        if data_chunk[i - 1] > data_chunk[i]:
            downs_mean += data_chunk[i - 1] - data_chunk[i]
            downs_counter += 1
        elif data_chunk[i - 1] < data_chunk[i]:
            ups_mean += data_chunk[i] - data_chunk[i - 1]
            ups_counter += 1

    if ups_counter:
        ups_mean /= ups_counter

    if downs_counter:
        downs_mean /= downs_counter
    else:
        downs_mean = 1

    return 100 - (100 / (1 + (ups_mean / downs_mean)))


def is_volatile(data, X, Y):
    if len(data) < Y:
        return False

    data_chunk = data[-Y:]
    chunk_min, chunk_max = min(data_chunk), max(data_chunk)

    return ((chunk_max - chunk_min) / chunk_min) * 100 > X


def is_liquid(data_sell, data_buy, S):
    if not data_sell or not data_buy:
        return False

    return (abs(data_sell[-1] - data_buy[-1]) / data_sell[-1]) * 100 < S


def get_trend_type(rsi_data, period):
    if len(rsi_data) < period:
        return None

    rsi_chunk = rsi_data[-period:]
    rsi_mean = sum(rsi_chunk) / len(rsi_chunk)

    if rsi_mean > 70:
        return 'UP'
    elif rsi_mean < 30:
        return 'DOWN'
    else:
        return 'SIDE'


def show_plots(currency_pairs, fetch_interval, rsi_per, volume_per, rsi_trend_per,
               volatile_asset_per, volatile_asset_percentage, spread_percentage):
    n = len(currency_pairs)
    time, avg_trans_time, avg_trans, buy, sell, volume, rsi = gen_arr(n), gen_arr(n), gen_arr(n), gen_arr(n), \
                                                              gen_arr(n), gen_arr(n), gen_arr(n)
    trends = {}

    def update(_):
        ######
        # per currency_pair plot update
        ######
        for i in range(n):
            currency_pair = currency_pairs[i]
            orderbook = fetch_best_offers(currency_pair)
            last_avg_transaction = fetch_avg_last_transaction(currency_pair)
            # print(f'{currency_pair}: {last_avg_transaction}')

            if not orderbook:
                print_error(f'Something went wrong during fetching {currency_pair} orderbook.')
                continue

            time[i].append(orderbook['time'])
            buy[i].append(orderbook['buy'])
            sell[i].append(orderbook['sell'])

            if last_avg_transaction:
                avg_trans_time[i].append(orderbook['time'])
                avg_trans[i].append(last_avg_transaction['avg_rate'])
                volume[i].append(last_avg_transaction['volume'])

                lines[4 * (i + 1) - 2].set_data(avg_trans_time[i], avg_trans[i])

                # rsi chunk
                if len(avg_trans_time[i]) >= rsi_per:
                    avg_trans_chunk = avg_trans[i][-rsi_per:]
                    rsi[i].append(calculate_RSI(avg_trans_chunk))
                    lines[4 * (i + 1) - 1].set_data(avg_trans_time[i][-len(rsi[i]):], rsi[i])

                # volume chunk
                if len(avg_trans_time[i]) >= volume_per:
                    volume_chunk = volume[i][-volume_per:]
                    axs[2 * (i + 1) - 1].bar(avg_trans_time[i][-1], sum(volume_chunk),
                                             width=0.8 * (fetch_interval / 1000 / 24 / 60 / 60),
                                             color='gray', alpha=0.7)

                trend = get_trend_type(rsi[i], 2)
                if trend:
                    trends[i] = trend
                    axs[2 * (i + 1) - 2].set_title(f'{currency_pair} {f"({trend})" if trend else ""}')

            lines[4 * (i + 1) - 4].set_data(time[i], buy[i])
            lines[4 * (i + 1) - 3].set_data(time[i], sell[i])

            for j in [1, 2]:
                axs[2 * (i + 1) - j].relim()
                axs[2 * (i + 1) - j].autoscale_view()

        ######
        # candidate, trends, volatile asset and liquid asset
        ######
        highest_volume = -1
        candidate_index = -1
        for i in range(n):
            trend = trends[i]

            if not trend:
                continue

            if trend == 'DOWN':
                continue

            vol = sum(volume[i][-rsi_trend_per:])
            if vol > highest_volume:
                highest_volume = vol
                candidate_index = i

        for i in range(n):
            if not trends[i]:
                continue

            title_ax = axs[2 * (i + 1) - 2]

            if CANDIDATE_LABEL in title_ax.get_title():
                if i != candidate_index:
                    title_ax.set_title(title_ax.get_title().replace(CANDIDATE_LABEL, ''))
            else:
                if i == candidate_index:
                    title_ax.set_title(CANDIDATE_LABEL + title_ax.get_title())

            volatile = is_volatile(avg_trans[i], volatile_asset_percentage, volatile_asset_per)
            if VOLATILE_ASSET_LABEL in title_ax.get_title():
                if not (i == candidate_index and volatile):
                    title_ax.set_title(title_ax.get_title().replace(VOLATILE_ASSET_LABEL, ''))
            else:
                if i == candidate_index and volatile:
                    title_ax.set_title(VOLATILE_ASSET_LABEL + title_ax.get_title())

            liquid = is_liquid(sell[i], buy[i], spread_percentage)
            if LIQUID_ASSET_LABEL in title_ax.get_title():
                if not (i == candidate_index and liquid):
                    title_ax.set_title(title_ax.get_title().replace(LIQUID_ASSET_LABEL, ''))
            else:
                if i == candidate_index and liquid:
                    title_ax.set_title(LIQUID_ASSET_LABEL + title_ax.get_title())

        return lines

    # matplotlib init
    mpl.use('TKAgg')
    plt.style.use('seaborn-dark')

    ratios = [2, 1]
    fig, axs = plt.subplots(nrows=n * 2, gridspec_kw={'height_ratios': ratios * n}, sharex=True)
    fig.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0.4)
    fig.canvas.manager.full_screen_toggle()

    lines, rsi_axs = [], []
    for i in range(n):
        currency_pair = currency_pairs[i]
        first_ax, second_ax = axs[2 * (i + 1) - 2], axs[2 * (i + 1) - 1]

        line_buy, = first_ax.plot([], [], label=f'Best buy offer', color='blue')
        line_sell, = first_ax.plot([], [], label=f'Best sell offer', color='orange')
        line_transactions, = first_ax.plot([], [], label=f'Avg transaction', color='green')
        rsi_axs.append(first_ax.twinx())
        line_rsi, = rsi_axs[-1].plot([], [], '--', label=f'RSI ({rsi_per})', color='gray', alpha=0.7)
        lines.extend([line_buy, line_sell, line_transactions, line_rsi])

        first_ax.set_ylabel(f'Price [{currency_pair.split("-")[1]}]')
        first_ax.set_title(currency_pair)
        first_ax.grid()
        first_ax.legend(lines[:4], [tmp.get_label() for tmp in lines[:4]])
        first_ax.xaxis_date()

        second_ax.set_ylabel(f'Volume [{currency_pair.split("-")[0]}]')
        second_ax.grid()
        second_ax.xaxis_date()

        trends[i] = None

    for rsi_ax in rsi_axs:
        rsi_ax.set_ylim(-5, 105)
        rsi_ax.set_ylabel(f'RSI')

    anim = FuncAnimation(fig, update, interval=fetch_interval)
    plt.show()


def main():
    currency_pairs = ['BTC-PLN', 'ETH-PLN']
    show_plots(currency_pairs,
               fetch_interval=5000,
               rsi_per=5,
               volume_per=5,
               rsi_trend_per=1,
               volatile_asset_per=5,
               volatile_asset_percentage=0.5,
               spread_percentage=5)


if __name__ == '__main__':
    main()
