import requests
import itertools
import warnings
import json
import numpy as np
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import ConciseDateFormatter, AutoDateLocator
from matplotlib.widgets import Slider, TextBox, Button

warnings.filterwarnings("ignore")


def get_bitbay_data(category, crypto_currency, main_currency):
    if category == 'transactions':
        resource = f'{crypto_currency}-{main_currency}'
        URL = f'https://api.bitbay.net/rest/trading/{category}/{resource}'
        response = requests.get(URL)
        return response.json()

    resource = crypto_currency + main_currency
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
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

    ASSET_SCAN_LIMIT = 5
    TREND_SCAN_LIMIT = 5
    RSI_DEFAULT_LIMIT = 10
    VOLATILE_BOUND = 0.05
    LIQUID_BOUND = 0.05
    VOLUME_CHUNK_SIZE = 10
    HOT_PLOT_MARK = '⚑'
    UPTREND_MARK = '↗'
    DOWNTREND_MARK = '↘'

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
    transactions = [[] for _ in range(N)]
    user_buy_history = [[] for _ in range(N)]
    user_buy_history_avg = [[] for _ in range(N)]
    crypto_amount = [0 for _ in range(N)]
    buyings = [[] for _ in range(N)]
    sells = [[] for _ in range(N)]

    BALANCE = [100_000, MAIN_CURRENCY]

    load_wallet_data = input('\
Do you want to load your wallet data from JSON file? [Y/n]\n>> ')
    if load_wallet_data.lower() == 'y':
        file_path = input('Please enter relative file path\n>> ')

        with open(file_path, 'r') as f:
            data = json.load(f)
            date = list(map(lambda x: datetime.strptime(x, DATE_FORMAT),
                            data['date']))
            BALANCE = data['BALANCE']
            bids = data['bids']
            asks = data['asks']
            avg_bids = data['avg_bids']
            avg_asks = data['avg_asks']
            volumes = data['volumes']
            volume_chunks = data['volume_chunks']
            RSI_values = data['RSI_values']
            bid_gains = data['bid_gains']
            bid_losses = data['bid_losses']
            curr_trend_marks = data['curr_trend_marks']
            hot_plot_marks = data['hot_plot_marks']
            transactions = data['transactions']
            user_buy_history = data['user_buy_history']
            user_buy_history_avg = data['user_buy_history_avg']
            crypto_amount = data['crypto_amount']

    fig = plt.figure(figsize=(15, 10), num='Please hire me',
                     constrained_layout=True)
    fig.suptitle('\nCryptocurriencies live tracking\n\n')
    fig_grid_spec = fig.add_gridspec(3*N, 1)

    ax_slider = plt.axes([0.78, 0.95, 0.18, 0.02])
    ax_slider.set_axis_off()
    ax_slider.set_visible(False)
    Y_slider = Slider(ax_slider, label='',
                      valmin=1, valmax=2, valstep=1, valinit=1,
                      initcolor='none')

    fig.text(x=0.025, y=0.865, s='My wallet', fontweight='semibold')
    crypto_amount_txt = []
    for i, currency in enumerate(CRYPTO_CURRENCIES):
        curr_text = fig.text(x=0.01, y=0.835-(i/50), s=f'{currency}: ')
        curr_amount_text = fig.text(x=0.01+(len(curr_text.get_text()))*0.004,
                                    y=0.835-(i/50),
                                    s=crypto_amount[i])

        crypto_amount_txt.append(curr_amount_text)

    fig.text(x=0.01, y=0.835-((1/50)*(len(CRYPTO_CURRENCIES)+0.25)),
             s='Balance:')
    BALANCE_TXT = fig.text(x=0.045,
                           y=0.835-((1/50)*(len(CRYPTO_CURRENCIES)+0.25)),
                           s=f'{BALANCE[0]:,.2f} {BALANCE[1]}')

    currency_textbox_ax = plt.axes([0.04, 0.65, 0.033, 0.025])
    currency_amount_textbox_ax = plt.axes([0.04, 0.62, 0.033, 0.025])
    price_textbox_ax = plt.axes([0.04, 0.59, 0.033, 0.025])
    buy_button_ax = plt.axes([0.02, 0.55, 0.033, 0.025])
    sell_button_ax = plt.axes([0.06, 0.55, 0.033, 0.025])
    save_button_ax = plt.axes([0.005, 0.975, 0.025, 0.02])

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
        transactions_line, = ax.plot_date(date, transactions[i], '-',
                                          label="transactions", color='green')
        RSI_line, = RSI_subaxes[i].plot_date(date, RSI_values[i], ':',
                                             label='RSI', color='lightgray')
        avg_user_buy_line, = ax.plot_date(date, user_buy_history_avg[i], '--',
                                          label='my buyings avg',
                                          color='lime')

        ax_lines.append((bids_line, asks_line, avg_bid_line,
                         avg_ask_line, RSI_line, transactions_line,
                         avg_user_buy_line))

    axes_volatile_marks = []
    axes_liquid_marks = []
    for i in range(N):
        volatile_mark = main_axes[i].text(1.1, 0.1, '',
                                          transform=main_axes[i].transAxes)
        liquid_mark = main_axes[i].text(1.1, 0.0, '',
                                        transform=main_axes[i].transAxes)
        axes_volatile_marks.append(volatile_mark)
        axes_liquid_marks.append(liquid_mark)

    OPERATION_CURRENCY_TEXTBOX = TextBox(currency_textbox_ax, 'Currency: ')
    OPERATION_AMOUNT_TEXTBOX = TextBox(currency_amount_textbox_ax, 'Amount: ')
    OPERATION_PRICE_TEXTBOX = TextBox(price_textbox_ax, 'Price: ')
    BUY_BUTTON = Button(buy_button_ax, label='BUY', color='lawngreen',
                        hovercolor='limegreen')
    SELL_BUTTON = Button(sell_button_ax, label='SELL', color='red',
                         hovercolor='indianred')
    SAVE_BUTTON = Button(save_button_ax, label='SAVE')

    def buy_on_click(_):
        operation_data = [OPERATION_CURRENCY_TEXTBOX.text,
                          OPERATION_AMOUNT_TEXTBOX.text,
                          OPERATION_PRICE_TEXTBOX.text]
        space_free_data = list(map(lambda x: x.replace(' ', ''),
                                   operation_data))

        currency, amount, price = space_free_data
        amount, price = map(float, (amount, price))
        currency_index = CRYPTO_CURRENCIES.index(currency.upper())

        user_buy_history[currency_index].append(price)
        crypto_amount[currency_index] += amount
        BALANCE[0] -= amount * price
        buyings[currency_index].append((amount, price))

        main_axes[currency_index].text(date[-1], price, str(amount),
                                       fontsize='x-small', ha='right',
                                       va='baseline')
        main_axes[currency_index].scatter(date[-1], price, color='lime')

    def sell_on_click(_):
        operation_data = [OPERATION_CURRENCY_TEXTBOX.text,
                          OPERATION_AMOUNT_TEXTBOX.text,
                          OPERATION_PRICE_TEXTBOX.text]
        space_free_data = list(map(lambda x: x.replace(' ', ''),
                                   operation_data))

        currency, amount, price = space_free_data
        amount, price = map(float, (amount, price))
        currency_index = CRYPTO_CURRENCIES.index(currency.upper())

        crypto_amount[currency_index] -= amount
        BALANCE[0] += amount * price
        sells[currency_index].append((amount, price))

        main_axes[currency_index].text(date[-1], price, str(amount),
                                       fontsize='x-small', ha='right',
                                       va='baseline')
        main_axes[currency_index].scatter(date[-1], price, color='red')

    def save_on_click(_):
        data = {'date': list(map(str, date)),
                'BALANCE': BALANCE,
                'bids': bids,
                'asks': asks,
                'avg_bids': avg_bids,
                'avg_asks': avg_asks,
                'volumes': volumes,
                'volume_chunks': volume_chunks,
                'RSI_values': RSI_values,
                'bid_gains': bid_gains,
                'bid_losses': bid_losses,
                'curr_trend_marks': curr_trend_marks,
                'hot_plot_marks': hot_plot_marks,
                'transactions': transactions,
                'user_buy_history': user_buy_history,
                'user_buy_history_avg': user_buy_history_avg,
                'crypto_amount': crypto_amount}

        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

        print('Saving the data...')

    BUY_BUTTON.on_clicked(func=buy_on_click)
    SELL_BUTTON.on_clicked(func=sell_on_click)
    SAVE_BUTTON.on_clicked(func=save_on_click)

    def _update(frame):
        next_frame = next(counter)

        # date.append(datetime.now() + timedelta(days=next_frame))
        date.append(datetime.now())

        if len(date) <= 50:
            Y_slider.valmax = len(date)
        ax_slider.set_xlim(Y_slider.valmin, Y_slider.valmax)

        orders = []
        for i in range(N):
            orders.append(get_bitbay_data('orderbook',
                                          CRYPTO_CURRENCIES[i],
                                          MAIN_CURRENCY))

        for i in range(N):
            _transactions = get_bitbay_data('transactions',
                                            CRYPTO_CURRENCIES[i],
                                            MAIN_CURRENCY)
            last_transaction = float(_transactions['items'][-1]['r'])  # rate
            transactions[i].append(last_transaction)

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

            if user_buy_history[i]:
                usr_bh = user_buy_history[i]
                user_buy_avg = sum(usr_bh)/len(usr_bh)
                user_buy_history_avg[i].append(user_buy_avg)
            else:
                user_buy_history_avg[i].append(np.mean(bids[i]+asks[i]))

        for i, ax in enumerate(volume_axes):
            if len(volumes[i]) < VOLUME_CHUNK_SIZE:
                volumes[i].append(orders[i]['bids'][0][1])

            if len(volumes[i]) >= VOLUME_CHUNK_SIZE:
                volume_chunk_val = sum(volumes[i])
                volume_chunks[i].append(volume_chunk_val)
                ax.bar(date[-1], volume_chunk_val, align='center',
                       width=0.95*VOLUME_CHUNK_SIZE, color='powderblue')
                ax_max_y = max(volume_chunks[i])
                ratio = volume_chunk_val / ax_max_y
                too_small_bar = True if ratio < 0.3 else False

                if too_small_bar:
                    ax.text(date[-1], volume_chunk_val,
                            round(volume_chunk_val, 2), ha='center',
                            va='baseline', fontsize='x-small')
                else:
                    ax.text(date[-1], volume_chunk_val/2,
                            round(volume_chunk_val, 2), ha='center',
                            va='center', fontsize='x-small')

            if len(volumes[i]) == VOLUME_CHUNK_SIZE:
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
                if len(bids[i]) > RSI_DEFAULT_LIMIT:
                    a = np.mean(bid_gains[i][-RSI_DEFAULT_LIMIT:]),
                    b = np.mean(bid_losses[i][-RSI_DEFAULT_LIMIT:])
                else:
                    a, b = np.mean(bid_gains[i]), np.mean(bid_losses[i])

            RS = a / b
            RSI = 100 - (100 / (1+RS))

            try:
                _ = iter(RSI)
            except Exception:
                print('iter found')
            else:
                RSI = RSI[0]

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
            if transactions[i]:
                lines[5].set_data(date, transactions[i])
            if user_buy_history[i]:
                lines[6].set_data(date, user_buy_history_avg[i])

        for i, values in enumerate(RSI_values):
            if len(values) > TREND_SCAN_LIMIT:
                last_values = values[-TREND_SCAN_LIMIT:]
                last_rsi_mean = np.mean(last_values)
                if 60 <= last_rsi_mean < 80 or last_rsi_mean <= 30:
                    curr_trend_marks[i] = UPTREND_MARK
                elif 30 < last_rsi_mean < 50 or last_rsi_mean >= 80:
                    curr_trend_marks[i] = DOWNTREND_MARK
                else:
                    curr_trend_marks[i] = ''

        canditate_indexes = []
        hot_plot_idx = None
        canditate_index = None
        if all(volume_chunks):
            for i in range(N):
                if curr_trend_marks[i] != DOWNTREND_MARK:
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
                    hot_plot_marks[hot_plot_idx] = HOT_PLOT_MARK

                for i in range(N):
                    if i != hot_plot_idx or \
                            curr_trend_marks[i] == DOWNTREND_MARK:
                        hot_plot_marks[i] = ''
                    elif i == hot_plot_idx and \
                            curr_trend_marks[i] != DOWNTREND_MARK:
                        canditate_index = hot_plot_idx

        for i in range(N):
            if len(transactions[i]) > ASSET_SCAN_LIMIT:
                last_trans = transactions[i][-ASSET_SCAN_LIMIT:]
                trans_mean = np.mean(last_trans)
                trans_ratio = []
                for transaction in last_trans:
                    ratio = abs((transaction-trans_mean)/trans_mean)
                    trans_ratio.append(ratio)

                is_over_bound = list(map(lambda x: x > VOLATILE_BOUND,
                                         trans_ratio))

                _last_bids = bids[i][-ASSET_SCAN_LIMIT:]
                _last_asks = asks[i][-ASSET_SCAN_LIMIT:]
                bids_asks_ratio = []
                for bid, ask in zip(_last_bids, _last_asks):
                    ratio = abs((bid-ask) / max(bid, ask))
                    bids_asks_ratio.append(ratio)

                are_under_bound = list(map(lambda x: x < LIQUID_BOUND,
                                           bids_asks_ratio))

                if any(is_over_bound) and i == canditate_index:
                    axes_volatile_marks[i].set_text('volatile asset !')
                else:
                    axes_volatile_marks[i].set_text('')

                if all(are_under_bound) and i == canditate_index:
                    axes_liquid_marks[i].set_text('liquid asset !')
                else:
                    axes_liquid_marks[i].set_text('')

        for i in range(N):
            crypto_amount_txt[i].set_text(crypto_amount[i])

        BALANCE_TXT.set_text(f'{BALANCE[0]:,.2f} {BALANCE[1]}')

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

    _ = FuncAnimation(fig, _update, interval=interval, cache_frame_data=False)
    plt.show()


if __name__ == '__main__':
    MAIN_CURRENCY = 'PLN'
    CRYPTO_CURRENCIES = ['BTC', 'LTC', 'DASH']
    INTERVAL_SEC = 3

    dynamic_plotting(INTERVAL_SEC*1000)
