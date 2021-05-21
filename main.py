import requests
import itertools
import warnings
import numpy as np
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import ConciseDateFormatter, AutoDateLocator
from matplotlib.widgets import Slider  # , TextBox

warnings.filterwarnings("ignore")


def _max(L):
    if not L:
        return 0
    return max(L)


def _min(L):
    if not L:
        return 0
    return min(L)


def get_bitbay_data(category, resource):
    URL = f'https://bitbay.net/API/Public/{resource}/{category}.json'
    try:
        response = requests.get(URL)
        return response.json()
    except Exception as e:
        print(e)


def dynamic_plotting(interval):
    global MAIN_CURRENCY, CRYPTO_CURRENCIES

    counter = itertools.count()
    N = len(CRYPTO_CURRENCIES)

    volume_chunk_size = 10
    hot_plot_mark = '⚑'
    uptrend_mark = '↗'
    downtrend_mark = '↘'

    date = []
    bids = [[] for _ in range(N)]
    asks = [[] for _ in range(N)]
    avg_bids = [[] for _ in range(N)]
    avg_asks = [[] for _ in range(N)]
    volumes = [[] for _ in range(N)]
    volume_chunks = [[] for _ in range(N)]
    RSI_values = [[] for _ in range(N)]
    bid_gains = [[] for _ in range(N)]
    bid_losses = [[] for _ in range(N)]
    curr_trend_marks = ['' for _ in range(N)]
    hot_plot_marks = ['' for _ in range(N)]

    fig = plt.figure(figsize=(15, 10), num='Please hire me',
                     constrained_layout=True)
    fig.suptitle('\nCryptocurriencies live tracking\n\n')
    fig_grid_spec = fig.add_gridspec(3*N, 1)

    ax_slider = plt.axes([0.78, 0.95, 0.18, 0.02])
    Y_slider = Slider(ax_slider, label='scan range\n(last days)',
                      valmin=1, valmax=2, valstep=1, valinit=1)

    main_axes = []
    volume_axes = []
    for i in range(2, 3*N+1, 3):
        main_axes.append(fig.add_subplot(fig_grid_spec[i-2:i, 0]))
        volume_axes.append(fig.add_subplot(fig_grid_spec[i:i+1, 0]))

    RSI_subaxes = []
    for ax in main_axes:
        RSI_subaxes.append(ax.twinx())

    ax_lines = []
    for i, ax in enumerate(main_axes):
        bids_line, = ax.plot_date(date, bids[i], '-', label='bids',
                                  color='royalblue')
        asks_line, = ax.plot_date(date, asks[i], '-', label='asks',
                                  color='darkorange')
        avg_bid_line, = ax.plot_date(date, avg_bids[i], '--',
                                     label="bids' avg", color='cornflowerblue')
        avg_ask_line, = ax.plot_date(date, avg_asks[i], '--',
                                     label="asks' avg", color='orange')
        RSI_line, = RSI_subaxes[i].plot_date(date, RSI_values[i], ':',
                                             label='RSI', color='lightgray')

        ax_lines.append((bids_line, asks_line, avg_bid_line,
                         avg_ask_line, RSI_line))

    # def submit(text):
    #     y = float(text)
    #     main_axes[0].scatter(date[-1], y, color='green')

    # ax_input = plt.axes([0.01, 0.8, 0.05, 0.05])
    # text_box = TextBox(ax_input, 'no\nkup\ncos')
    # text_box.on_submit(submit)

    def _update(frame):
        next_frame = next(counter)

        date.append(datetime.now() + timedelta(days=next_frame))

        if len(date) <= 50:
            Y_slider.valmax = len(date)
        ax_slider.set_xlim(Y_slider.valmin, Y_slider.valmax)

        orders = []
        for i in range(N):
            orders.append(get_bitbay_data('orderbook',
                                          CRYPTO_CURRENCIES[i]+MAIN_CURRENCY))

        for i in range(N):
            bids[i].append(orders[i]['bids'][0][0])
            asks[i].append(orders[i]['asks'][0][0])
            if len(bids[i]) >= Y_slider.val and \
                    Y_slider.val != Y_slider.valinit:
                last_Y_bids = bids[i][-Y_slider.val:]
                avg_bids[i].append(sum(last_Y_bids)/len(last_Y_bids))
            else:
                avg_bids[i].append(sum(bids[i])/len(bids[i]))
            if len(asks[i]) >= Y_slider.val and \
                    Y_slider.val != Y_slider.valinit:
                last_Y_asks = asks[i][-Y_slider.val:]
                avg_asks[i].append(sum(last_Y_asks)/len(last_Y_asks))
            else:
                avg_asks[i].append(sum(asks[i])/len(asks[i]))

        for i, ax in enumerate(volume_axes):
            if len(volumes[i]) < volume_chunk_size:
                volumes[i].append(orders[i]['bids'][0][1])

            if len(volumes[i]) >= volume_chunk_size:
                volume_chunk_val = sum(volumes[i])
                volume_chunks[i].append(volume_chunk_val)
                ax.bar(date[-1], volume_chunk_val, align='center',
                       width=0.95*volume_chunk_size, color='powderblue')
                ax.text(date[-1], volume_chunk_val/2,
                        round(volume_chunk_val, 2), ha='center', va='center',
                        fontsize='x-small')

            if len(volumes[i]) == volume_chunk_size:
                volumes[i] = []

        for i in range(N):
            if len(bids[i]) >= 2:
                if Y_slider.val != Y_slider.valinit and Y_slider.val >= 2:
                    last_Y_bids = bids[i][-Y_slider.val:]
                    diff = last_Y_bids[-2] - last_Y_bids[-1]
                else:
                    diff = bids[i][-2] - bids[i][-1]

                if diff < 0:
                    bid_gains[i].append(abs(diff))
                elif diff > 0:
                    bid_losses[i].append(diff)

            # https://en.wikipedia.org/wiki/Relative_strength_index
            if Y_slider.val != Y_slider.valinit:
                a = np.mean(bid_gains[i][-Y_slider.val:])
                b = np.mean(bid_losses[i][-Y_slider.val:])
            else:
                a, b = np.mean(bid_gains[i]), np.mean(bid_losses[i])
            RS = a / b
            RSI = 100 - (100 / (1+RS))

            nan_msg = None
            a_is_nan = np.isnan(a)
            b_is_nan = np.isnan(b)
            if a_is_nan and b_is_nan:
                nan_msg = 'Bid rate is stable'
            elif a_is_nan:
                nan_msg = "No bid rate growth recorded"
            elif b_is_nan:
                nan_msg = "No bid rate loss recorded"

            RSI_values[i].append(50 if nan_msg else RSI)

        for i, lines in enumerate(ax_lines):
            if bids[i]:
                lines[0].set_data(date, bids[i])
            if asks[i]:
                lines[1].set_data(date, asks[i])
            if avg_bids[i]:
                lines[2].set_data(date, avg_bids[i])
            if avg_asks[i]:
                lines[3].set_data(date, avg_asks[i])
            if RSI_values[i]:
                lines[4].set_data(date, RSI_values[i])

        for i, values in enumerate(RSI_values):
            if len(values) > 2:
                if values[-1] > values[-2]:
                    curr_trend_marks[i] = uptrend_mark
                elif values[-1] < values[-2]:
                    curr_trend_marks[i] = downtrend_mark

        canditate_indexes = []
        hot_plot_idx = None
        if all(volume_chunks):
            for i in range(N):
                if curr_trend_marks[i] != downtrend_mark:
                    canditate_indexes.append(i)

            if canditate_indexes:
                last_uptrend_records = []
                for i, ax_volumes in enumerate(volume_chunks):
                    if i in canditate_indexes:
                        last_uptrend_records.append((i, ax_volumes[-1]))

                max_volume = float('-inf')
                hot_plot_idx = None
                for i, volume in last_uptrend_records:
                    if volume > max_volume:
                        max_volume = volume
                        hot_plot_idx = i

                if hot_plot_idx:
                    hot_plot_marks[hot_plot_idx] = hot_plot_mark
                    for i in range(N):
                        if i != hot_plot_idx:
                            hot_plot_marks[i] = ''

        for i, (ax, crypto_currency) in enumerate(zip(main_axes,
                                                      CRYPTO_CURRENCIES)):
            xlocator = AutoDateLocator()
            ylocator = plt.LinearLocator(numticks=3)
            formatter = ConciseDateFormatter(xlocator, show_offset=False)
            ax_title = hot_plot_marks[i] + ' ' \
                + crypto_currency + ' ' \
                + curr_trend_marks[i]
            ax.set(ylabel=f'Rate [{MAIN_CURRENCY}]', title=ax_title)
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles+[RSI_line], labels+['RSI'], loc='upper left',
                      bbox_to_anchor=(1.08, 1.06))
            ax.yaxis.set_major_locator(ylocator)
            ax.xaxis.set_major_locator(xlocator)
            ax.xaxis.set_major_formatter(formatter)
            ax.relim()
            ax.autoscale_view()

        for ax in RSI_subaxes:
            ax.axhline(y=70, color='lightgray', linestyle='-', linewidth=0.4)
            ax.axhline(y=30, color='lightgray', linestyle='-', linewidth=0.4)
            ax.set(ylabel='RSI')
            ax.relim()
            ax.set_ylim(0, 100)
            ax.autoscale_view()

        for i, ax in enumerate(volume_axes):
            ax.set_ylabel('Volume', fontsize=8)
            xlocator = AutoDateLocator()
            ylocator = plt.LinearLocator(numticks=3)
            formatter = ConciseDateFormatter(xlocator)
            ax.yaxis.set_major_locator(ylocator)
            ax.set_yticklabels([])
            ax.xaxis.set_major_locator(xlocator)
            ax.xaxis.set_major_formatter(formatter)
            ax.xaxis.set_visible(False)
            ax.relim()
            ax.autoscale_view()

        plt.subplots_adjust(left=0.15, right=0.8,
                            bottom=0.02, top=0.92,
                            wspace=0.4, hspace=0.4)

        return ax_lines,

    mng = plt.get_current_fig_manager()
    mng.resize(1920, 1080)

    _ = FuncAnimation(fig, _update, interval=interval)
    plt.show()


if __name__ == '__main__':
    MAIN_CURRENCY = 'PLN'
    CRYPTO_CURRENCIES = ['BTC', 'LTC', 'DASH']
    INTERVAL_SEC = 1

    dynamic_plotting(INTERVAL_SEC*1000)
