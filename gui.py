import time
import json
import copy
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import ttk, filedialog
from api import *
from calc import *


class CryptoApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'Cryptotrading App')
        ttk.Style().theme_use('clam')

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, GraphPage, WalletPage):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        input_labels = 'Interval for the average (max 10): ', \
                       'Interval for the RSI (max 10): ', \
                       'Interval for volatility check (max 10): ', \
                       'Threshold above which the asset is volatile (%): ', \
                       'Maximum spread for which the asset is liquid (%): '

        init_constants = ['AVG_WINDOW', 'RSI_WINDOW', 'VOLATILE_SAMPLES', 'VOLATILE_PERC',
                          'SPREAD_PERC']

        def fetch_constants(entries):

            for index in range(len(entries)):

                if len(entries[index].get()) == 0:
                    pass
                else:
                    try:
                        globals()[f'{init_constants[index]}'] = int(entries[index].get())
                    except ValueError:
                        pass

        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text='Cryptocurrency App L6', font=('Tahoma', 14, 'bold'))
        title.pack(pady=40, padx=10)

        init_inputs = []
        for input_label in input_labels:
            label = tk.Label(self, text=input_label)
            entry = tk.Entry(self)
            label.pack()
            entry.pack()
            init_inputs.append(entry)

        button_submit = ttk.Button(self, text='Submit', width=30,
                                   command=lambda: fetch_constants(init_inputs))
        button_submit.pack(ipady=10, pady=40)

        button_graph = ttk.Button(self, text='Exchange Rates Graph', width=30,
                                  command=lambda: controller.show_frame(GraphPage))
        button_graph.pack(ipady=10)

        button_wallet = ttk.Button(self, text='My Wallet', width=30,
                                   command=lambda: controller.show_frame(WalletPage))
        button_wallet.pack(ipady=10)

        button_quit = ttk.Button(self, text='Quit', command=quit)
        button_quit.pack(side='bottom', ipadx=50, ipady=10, pady=10)


class WalletPage(tk.Frame):

    def __init__(self, parent, controller):

        global PAIRS
        global curr_avg_prices
        global curr_balance

        queue_first_curr, queue_sec_curr, queue_third_curr = ([] for _ in range(3))
        wallet = [0]*3

        tk.Frame.__init__(self, parent)
        self.columnconfigure((0, 5), weight=5)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(14, weight=5)
        self.rowconfigure(17, weight=9)

        def calculate_curr_avg_and_wallet(amount, price, queue, num):

            if (len(amount.get()) == 0 or len(price.get()) == 0) or float(amount.get()) == 0:
                return None
            else:
                try:
                    amount_bought = float(amount.get())
                    price_bought = float(price.get())
                except ValueError:
                    return None

            queue.append([amount_bought, price_bought])
            wallet[num] += amount_bought

            temp = 0
            for transaction in queue:
                temp += transaction[1]
            curr_avg_prices[num] = round((temp / len(queue)), 2)

        def calculate_curr_balance(amount, price, queue, num):

            if (len(amount.get()) == 0 or len(price.get()) == 0) or float(amount.get()) == 0:
                return None
            else:
                try:
                    amount_sold = float(amount.get())
                    price_sold = float(price.get())
                except ValueError:
                    return None

            if amount_sold > wallet[num]:
                return None
            else:
                wallet[num] -= amount_sold

            for transaction in queue:

                if amount_sold > transaction[0]:
                    curr_balance[num] += (transaction[0] * (price_sold - transaction[1]))
                    amount_sold -= transaction[0]
                    transaction[0] = 0
                else:
                    curr_balance[num] += (amount_sold * (price_sold - transaction[1]))
                    transaction[0] -= amount_sold
                    break

            temp = copy.deepcopy(queue)
            temp = list(filter(lambda t: t[0] != 0, temp))
            queue.clear()
            queue.extend(temp)

        def save_to_json():

            trans_list = [queue_first_curr, queue_sec_curr, queue_third_curr]

            data = {}
            for curr_pair in range(3):
                data[f'{PAIRS[curr_pair][0]}'] = {}
                data[f'{PAIRS[curr_pair][0]}']['balance'] = curr_balance[curr_pair]
                data[f'{PAIRS[curr_pair][0]}']['avgprice'] = curr_avg_prices[curr_pair]
                data[f'{PAIRS[curr_pair][0]}']['transactions'] = trans_list[curr_pair]

            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            with open(f'{timestamp}.txt', 'w') as outfile:
                json.dump(data, outfile)

        def read_from_json(first_queue, sec_queue, third_queue):

            filename = filedialog.askopenfilename(title='Select your wallet file',
                                                  initialdir=Path.cwd(),
                                                  filetypes=(('Text files', '*.txt'),
                                                             ('All files', '*.*')))
            with open(filename, "r") as wallet_file:
                prev_data = json.load(wallet_file)

            temp = []
            for curr_pair in range(3):
                curr_balance[curr_pair] = prev_data[f'{PAIRS[curr_pair][0]}']['balance']
                curr_avg_prices[curr_pair] = prev_data[f'{PAIRS[curr_pair][0]}']['avgprice']
                temp.append(prev_data[f'{PAIRS[curr_pair][0]}']['transactions'])

            first_queue, sec_queue, third_queue = temp[0], temp[1], temp[2]

        #  wallet layout
        title = tk.Label(self, text='My Wallet', font=('Tahoma', 14, 'bold'))
        title.grid(row=0, column=1, columnspan=4, sticky='ew')

        label_bought = tk.Label(self, text='Bought', font=('Tahoma', 12, 'bold'))
        label_sold = tk.Label(self, text='Sold', font=('Tahoma', 12, 'bold'))
        label_sold.grid(row=2, column=3, columnspan=2)
        label_bought.grid(row=2, column=1, columnspan=2)

        label_amount_b = tk.Label(self, text='Amount')
        label_price_b = tk.Label(self, text='Price')
        label_amount_s = tk.Label(self, text='Amount')
        label_price_s = tk.Label(self, text='Price')
        label_amount_b.grid(row=3, column=1)
        label_price_b.grid(row=3, column=2)
        label_amount_s.grid(row=3, column=3)
        label_price_s.grid(row=3, column=4)

        # 1
        label_curr_one_bought = tk.Label(self, text=f'{PAIRS[0][0]}-{PAIRS[0][1]}')
        label_curr_one_sold = tk.Label(self, text=f'{PAIRS[0][0]}-{PAIRS[0][1]}')
        label_curr_one_bought.grid(row=4, column=1, columnspan=2)
        label_curr_one_sold.grid(row=4, column=3, columnspan=2)

        entry_curr_one_amount_b = tk.Entry(self)
        entry_curr_one_price_b = tk.Entry(self)
        entry_curr_one_amount_s = tk.Entry(self)
        entry_curr_one_price_s = tk.Entry(self)
        entry_curr_one_amount_b.grid(row=5, column=1, padx=10)
        entry_curr_one_price_b.grid(row=5, column=2)
        entry_curr_one_amount_s.grid(row=5, column=3, padx=10)
        entry_curr_one_price_s.grid(row=5, column=4)

        button_curr_one_submit_b = ttk.Button(self, text='Submit', width=30,
                                              command=lambda:
                                              calculate_curr_avg_and_wallet(entry_curr_one_amount_b,
                                                                            entry_curr_one_price_b,
                                                                            queue_first_curr, 0))
        button_curr_one_submit_s = ttk.Button(self, text='Submit', width=30,
                                              command=lambda:
                                              calculate_curr_balance(entry_curr_one_amount_s,
                                                                     entry_curr_one_price_s,
                                                                     queue_first_curr, 0))
        button_curr_one_submit_b.grid(row=6, column=1, columnspan=2)
        button_curr_one_submit_s.grid(row=6, column=3, columnspan=2)

        # 2
        label_curr_two_bought = tk.Label(self, text=f'{PAIRS[1][0]}-{PAIRS[1][1]}')
        label_curr_two_sold = tk.Label(self, text=f'{PAIRS[1][0]}-{PAIRS[1][1]}')
        label_curr_two_bought.grid(row=7, column=1, columnspan=2)
        label_curr_two_sold.grid(row=7, column=3, columnspan=2)

        entry_curr_two_amount_b = tk.Entry(self)
        entry_curr_two_price_b = tk.Entry(self)
        entry_curr_two_amount_s = tk.Entry(self)
        entry_curr_two_price_s = tk.Entry(self)
        entry_curr_two_amount_b.grid(row=8, column=1)
        entry_curr_two_price_b.grid(row=8, column=2)
        entry_curr_two_amount_s.grid(row=8, column=3)
        entry_curr_two_price_s.grid(row=8, column=4)

        button_curr_two_submit_b = ttk.Button(self, text='Submit', width=30,
                                              command=lambda:
                                              calculate_curr_avg_and_wallet(entry_curr_two_amount_b,
                                                                            entry_curr_two_price_b,
                                                                            queue_sec_curr, 1))
        button_curr_two_submit_s = ttk.Button(self, text='Submit', width=30,
                                              command=lambda:
                                              calculate_curr_balance(entry_curr_two_amount_s,
                                                                     entry_curr_two_price_s,
                                                                     queue_first_curr, 1))
        button_curr_two_submit_b.grid(row=9, column=1, columnspan=2)
        button_curr_two_submit_s.grid(row=9, column=3, columnspan=2)

        # 3
        label_curr_three_bought = tk.Label(self, text=f'{PAIRS[2][0]}-{PAIRS[2][1]}')
        label_curr_three_sold = tk.Label(self, text=f'{PAIRS[2][0]}-{PAIRS[2][1]}')
        label_curr_three_bought.grid(row=10, column=1, columnspan=2)
        label_curr_three_sold.grid(row=10, column=3, columnspan=2)

        entry_curr_three_amount_b = tk.Entry(self)
        entry_curr_three_price_b = tk.Entry(self)
        entry_curr_three_amount_s = tk.Entry(self)
        entry_curr_three_price_s = tk.Entry(self)
        entry_curr_three_amount_b.grid(row=11, column=1)
        entry_curr_three_price_b.grid(row=11, column=2)
        entry_curr_three_amount_s.grid(row=11, column=3)
        entry_curr_three_price_s.grid(row=11, column=4)

        button_curr_two_submit_b = ttk.Button(self, text='Submit', width=30,
                                              command=lambda:
                                              calculate_curr_avg_and_wallet(entry_curr_three_amount_b,
                                                                            entry_curr_three_price_b,
                                                                            queue_third_curr, 2))
        button_curr_two_submit_s = ttk.Button(self, text='Submit', width=30,
                                              command=lambda:
                                              calculate_curr_balance(entry_curr_three_amount_s,
                                                                     entry_curr_three_price_s,
                                                                     queue_first_curr, 2))
        button_curr_two_submit_b.grid(row=12, column=1, columnspan=2)
        button_curr_two_submit_s.grid(row=12, column=3, columnspan=2)

        # json

        button_save_json = ttk.Button(self, text='Save to file', width=30,
                                      command=save_to_json)
        button_save_json.grid(row=13, column=1, columnspan=2, ipady=10, pady=30)

        button_load_json = ttk.Button(self, text='Load from file', width=30,
                                      command=lambda: read_from_json(queue_first_curr,
                                                                     queue_sec_curr,
                                                                     queue_third_curr))
        button_load_json.grid(row=13, column=3, columnspan=2, ipady=10, pady=30)

        # nav
        button_graph = ttk.Button(self, text='Exchange Rates Graph', width=30,
                                  command=lambda: controller.show_frame(GraphPage))
        button_graph.grid(row=15, column=2, columnspan=2, ipady=10)

        button_menu = ttk.Button(self, text='Menu', width=30,
                                 command=lambda: controller.show_frame(StartPage))
        button_menu.grid(row=16, column=2, columnspan=2, ipady=10)


class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        button_wallet = ttk.Button(self, text='My Wallet', width=30,
                                   command=lambda: controller.show_frame(WalletPage))
        button_wallet.pack()

        button_menu = ttk.Button(self, text='Menu', width=30,
                             command=lambda: controller.show_frame(StartPage))
        button_menu.pack()


def draw_figure(frame_number):

    time_samples.append(time.strftime("%H:%M:%S", time.localtime()))

    get_data(PAIRS, data_storage, askbid_storage)
    get_transactions(PAIRS, trans_storage, limit=30, timeframe=45)
    get_volume(trans_storage, vol_storage)
    calculate_mov_avg(askbid_storage, avg_storage, AVG_WINDOW)
    calculate_rsi(askbid_storage, rsi_storage, RSI_WINDOW)

    trends_of_pairs = ['']*3
    classify_trend(rsi_storage, trends_of_pairs)
    candidate = select_candidate(trends_of_pairs, vol_storage[-1])

    plt.clf()
    fig.suptitle("Cryptocurrency Exchange Rates, RSI and Volume")

    for curr_pair in range(3):

        plt.subplot(3, 3, curr_pair+1)

        asks, bids, avg_asks, avg_bids = ([] for _ in range(4))

        for sample in data_storage:
            asks.append(sample[curr_pair][1][0])
            bids.append(sample[curr_pair][1][1])
        for avg_sample in avg_storage:
            avg_asks.append(avg_sample[curr_pair][0])
            avg_bids.append(avg_sample[curr_pair][1])

        plt.plot(time_samples, asks, "-o", label=data_storage[0][curr_pair][0] + " ask")
        plt.plot(time_samples, bids, "-o", label=data_storage[0][curr_pair][0] + " bid")
        plt.plot(time_samples, avg_asks, "o:", color="#185986",
                 label=data_storage[0][curr_pair][0] + " ask mov avg")
        plt.plot(time_samples, avg_bids, "o:", color="#1b6762",
                 label=data_storage[0][curr_pair][0] + " bid mov avg")

        axes = plt.gca()

        balance_value = curr_balance[curr_pair]
        if balance_value < 0:
            axes.text(0.1, 1.4, f'Balance: {balance_value}', horizontalalignment='center',
                      color='#a50000', verticalalignment='center', transform=axes.transAxes)
        else:
            axes.text(0.1, 1.4, f'Balance: {balance_value}', horizontalalignment='center',
                      verticalalignment='center', transform=axes.transAxes)

        icon_trend = (lambda trend: upward_icon if trend == 'upward'
                      else (downward_icon if trend == 'downward'
                            else question_icon))(trends_of_pairs[curr_pair])
        imagebox_trend = OffsetImage(icon_trend, zoom=0.4)
        imagebox_trend.image.axes = axes
        ab_trend = AnnotationBbox(imagebox_trend, (0.5, 0.5), xycoords='axes fraction',
                                  boxcoords="offset points", pad=0.3, frameon=0)
        axes.add_artist(ab_trend)

        volatile_test = check_volatility(trans_storage, curr_pair, VOLATILE_PERC, VOLATILE_SAMPLES)
        vol_icon = (lambda test: volatile_icon if test else tp_volatile_icon)(volatile_test)
        imagebox_volatile = OffsetImage(vol_icon, zoom=0.1)
        imagebox_volatile.image.axes = axes
        ab_volatile = AnnotationBbox(imagebox_volatile, (0.95, 1.4), xycoords='axes fraction',
                                     boxcoords="offset points", pad=0, frameon=0,
                                     annotation_clip=False)
        axes.add_artist(ab_volatile)

        liquid_test = check_liquidity(trans_storage, curr_pair, SPREAD_PERC)
        liq_icon = (lambda test: liquid_icon if test else tp_liquid_icon)(liquid_test)
        imagebox_liquid = OffsetImage(liq_icon, zoom=0.09)
        imagebox_liquid.image.axes = axes
        ab_liquid = AnnotationBbox(imagebox_liquid, (0.9, 1.4), xycoords='axes fraction',
                                   boxcoords="offset points", pad=0, frameon=0,
                                   annotation_clip=False)
        axes.add_artist(ab_liquid)

        if candidate == curr_pair:
            for loc, spine in axes.spines.items():
                if loc == 'bottom' or loc == 'top':
                    spine.set_position(("outward", 1))
                    spine.set_capstyle('butt')
                else:
                    spine.set_position(("outward", -1))
                spine.set_linewidth(3)
                spine.set_edgecolor('#ffae1a')
                spine.set_alpha(0.7)

        curr_avg = curr_avg_prices[curr_pair]
        if curr_avg is not None:
            axes.axhline(y=curr_avg, color='r', linestyle='dashed')

        plt.xlabel("Time", fontsize=9)
        plt.ylabel("Exchange Rates", fontsize=9)
        plt.xticks(rotation='vertical', fontsize=7)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                   ncol=2, mode="expand", borderaxespad=0.)

    for curr_pair in range(3):

        plt.subplot(3, 3, curr_pair + 4)
        rsi_asks, rsi_bids = ([] for _ in range(2))

        for rsi_sample in rsi_storage:
            rsi_asks.append(rsi_sample[curr_pair][0])
            rsi_bids.append(rsi_sample[curr_pair][1])

        plt.plot(time_samples, rsi_asks, "o:", label=data_storage[0][curr_pair][0] + " ask RSI")
        plt.plot(time_samples, rsi_bids, "o:", label=data_storage[0][curr_pair][0] + " bid RSI")
        plt.xlabel("Time", fontsize=9)
        plt.ylabel("RSI", fontsize=9)
        plt.xticks(rotation='vertical', fontsize=7)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                   ncol=2, mode="expand", borderaxespad=0.)

    for curr_pair in range(3):

        plt.subplot(3, 3, curr_pair + 7)
        volume = []

        for vol_sample in vol_storage:
            volume.append(vol_sample[curr_pair])

        plt.bar(time_samples, volume, align="center")
        plt.xlabel("Time", fontsize=9)
        plt.ylabel("Volume", fontsize=9)
        ax = plt.gca()
        ax.margins(y=0.2)
        plt.xticks(rotation='vertical', fontsize=7)

    clear_older_data(data_storage, avg_storage, vol_storage, askbid_storage, rsi_storage,
                     trans_storage, trigger_list=time_samples, threshold=10)

    plt.tight_layout()
    plt.subplots_adjust(top=0.85)


if __name__ == '__main__':

    PAIRS = [('LTC', 'PLN'), ('ETH', 'PLN'), ('BCC', 'PLN')]
    FREQ = 5
    AVG_WINDOW = 5
    RSI_WINDOW = 10
    VOLATILE_SAMPLES = 5
    VOLATILE_PERC = 5
    SPREAD_PERC = 2

    downward_icon, upward_icon, question_icon, tp_volatile_icon, tp_liquid_icon \
        = get_icons('downward', 'upward', 'question', 'fire', 'liquidity')
    volatile_icon, liquid_icon = get_icons('fire', 'liquidity', transparent=False)

    matplotlib.use('TkAgg')
    plt.style.use('Solarize_Light2')
    fig = plt.figure()

    time_samples, data_storage, avg_storage, rsi_storage, vol_storage, askbid_storage, trans_storage \
        = ([] for _ in range(7))

    curr_avg_prices = [None] * 3
    curr_balance = [0] * 3

    app = CryptoApp()
    app.state('zoomed')
    ani = FuncAnimation(fig, draw_figure, interval=1000*FREQ)
    app.mainloop()
