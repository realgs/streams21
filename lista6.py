import random
import time
import tkinter
from threading import Thread
from tkinter import messagebox

import requests
from datetime import datetime, timedelta
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.widgets import TextBox, Button
import json
import copy
from tkinter import *


def generate_test_data():
    random.seed(10)
    bid = 215500
    ask = 215547
    volume = 215500
    while True:
        yield (bid, ask, volume)
        bid += random.randint(0, 300) - 150
        ask += random.randint(0, 300) - 150
        volume += random.randint(0, 300) - 150


test_gen = generate_test_data()


def get_test_data(currency, retry_stat_code_err, retry_connect_err):
    data = next(test_gen)
    current_time = datetime.now()
    return current_time, data[0], data[1], data[2]


def get_volumen(currency):
    time_int = int((datetime.now() - timedelta(seconds=60)).timestamp()) * 1000
    url = f"https://api.bitbay.net/rest/trading/transactions/{currency}"
    params = {'fromTime': time_int}
    response = requests.request("GET", url, params=params)
    response = eval(response.text)
    return sum([float(response['items'][i]['a']) for i in range(len(response['items']))])


def get_data(currency, retry_stat_code_err, retry_connect_err):
    url_pre = 'https://bitbay.net/API/Public/'
    url_post = '/ticker.json'
    url = url_pre + currency + url_post
    try:
        current_time = datetime.now()
        response = requests.get(url)
        status_code = str(response.status_code)
        if status_code[0] == '2':
            resp_json = response.json()
            selling_cost = resp_json['ask']
            purchase_cost = resp_json['bid']
            volume = get_volumen(currency)
            return current_time, selling_cost, purchase_cost, volume
        else:
            while retry_stat_code_err:
                get_data(currency, retry_stat_code_err - 1, retry_connect_err)
            print("Unable to access API on BitBay. Error: {}".format(response.status_code))
            sys.exit()
    except requests.exceptions.ConnectionError:
        while retry_connect_err:
            get_data(currency, retry_stat_code_err, retry_connect_err - 1)
        print("Cannot reach the server.")
        sys.exit()


get_data_func = get_test_data if len(sys.argv) > 1 and sys.argv[1] == "test" else get_data


def gen_empty_list(currency_list):
    return {i: [] for i in currency_list}


def gen_empty_dict(currency_list):
    return {currency: {'sell': [], 'purchase': []} for currency in currency_list}


def update_avg_dict(last_average, currency, values, n_last_seconds):
    last_average[currency]['sell'].append(average_value(values, n_last_seconds, currency, 1))
    last_average[currency]['purchase'].append(average_value(values, n_last_seconds, currency, 2))


def update_RSI(RSI, currency, values):
    RSI[currency]['sell'].append(calculate_RSI(RSI_range, values, currency, 1))
    RSI[currency]['purchase'].append(calculate_RSI(RSI_range, values, currency, 2))


def update_data(values):
    for i in currency_list:
        data = get_data_func(i, retry_stat_code_err, retry_connect_err)
        values[i].append(data)


def average_value(values, n_last_seconds, currency, value_index):
    filtered = list(filter(lambda v: v[0] >= datetime.now() - timedelta(seconds=n_last_seconds), values[currency]))
    if len(filtered) == 0:
        return 0
    sum = 0
    for v in filtered:
        sum += v[value_index]
    return sum / len(filtered)


def calculate_RSI(RSI_range, values, currency, values_index):
    filtered = list(filter(lambda v: v[0] >= datetime.now() - timedelta(seconds=RSI_range), values[currency]))
    if len(filtered) < 2:
        return 0
    ups = 0
    downs = 0
    ups_counter = 0
    downs_counter = 0
    for i in range(len(filtered) - 1):
        if filtered[i][values_index] <= filtered[i + 1][values_index]:
            up = filtered[i + 1][values_index] - filtered[i][values_index]
            ups += up
            ups_counter += 1
        elif filtered[i][values_index] > filtered[i + 1][values_index]:
            down = filtered[i][values_index] - filtered[i + 1][values_index]
            downs += down
            downs_counter += 1

        if ups_counter == 0:
            a = 1
        else:
            a = ups / ups_counter

        if downs_counter == 0:
            b = 1
        else:
            b = downs / downs_counter

    return 100 - (100 / (1 + (a / b)))


def classify_rsi_trend(rsi, currency):
    def get_average_of(rsi_type):
        values = []
        counted_values = 0
        while counted_values < 4 and counted_values < len(rsi[currency][rsi_type]):
            counted_values += 1
            values.append(rsi[currency][rsi_type][-counted_values])

        avg = sum(values) / len(values) if len(values) > 0 else 0
        return avg, values

    def get_trend_of(avg, values):
        if (len(values) != 0 and avg == values[-1]) or len(values) == 0:
            return 'Sideways trend'
        elif avg > values[-1]:
            return 'Upward trend'
        else:
            return 'Downward trend'

    avg_sell, sell_values = get_average_of('sell')
    avg_purchase, purchase_values = get_average_of('purchase')

    return {'sell': get_trend_of(avg_sell, sell_values),
            'purchase': get_trend_of(avg_purchase, purchase_values)}


def is_volatile(values, currency, X, Y):
    if len(values[currency]) < Y+1:
        return ""
    purchase_val = [values[currency][-y][2] for y in range(1, Y+1)]
    value = (abs(max(purchase_val)-min(purchase_val)) / max(purchase_val)) * 100
    if value > X:
        return 'Volatile asset'
    else:
        return ''


def is_liquid(values, currency, S):
    sell = values[currency][-1][1]
    purchase = values[currency][-1][2]
    diff = (abs(sell - purchase) / max(sell, purchase)) * 100
    if diff < S:
        return 'Liquid asset'
    return ''


def save_json(data_map):
    serializable_data_map = copy.deepcopy(data_map)
    for currency_v in serializable_data_map.keys():
        for buy_or_sell_v in serializable_data_map[currency_v].keys():
            for entry in serializable_data_map[currency_v][buy_or_sell_v]:
                entry['date'] = entry['date'].strftime('%Y-%m-%d %H:%M:%S')

    with open("data.json", "w") as write_file:
        json.dump(serializable_data_map, write_file, indent=4)
        write_file.close()


def load_json():
    try:
        with open('data.json', 'r') as input_file:
            loaded_data = json.load(input_file)
            for currency in loaded_data.keys():
                for buy_or_sell in loaded_data[currency].keys():
                    for entry in loaded_data[currency][buy_or_sell]:
                        entry['date'] = datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S')
                        entry['quantity'] = float(entry['quantity'])
                        entry['cost'] = float(entry['cost'])
            input_file.close()
        return loaded_data
    except:
        return None


def on_button_clicked(date, currency_chosen, buy_or_sell, quantity, value, data_map):
    def submit_date(text):
        try:
            now_date = datetime.now()
            day = '0{}'.format(now_date.day) if now_date.day < 9 else now_date.day
            month = '0{}'.format(now_date.month) if now_date.month < 9 else now_date.month
            xdate = datetime.strptime('{}-{}-{} {}'.format(now_date.year, month, day, text),
                                      '%Y-%m-%d %H:%M:%S')
        except:
            try:
                xdate = datetime.strptime(text, '%Y-%m-%d %H:%M:%S')
            except:
                xdate = None

        return xdate

    def submit_currency(text):
        cdata = text.upper()
        if cdata in ['LTC-PLN', 'LSK-PLN', 'BTC-PLN']:
            return cdata
        return None

    def submit_buy_sell(text):
        if text in ['buy', 'sell']:
            return text
        return None

    def submit_quantity(text):
        try:
            qdata = float(text)
        except:
            qdata = None

        return qdata

    def submit_value(text):
        try:
            vdata = float(text)
        except:
            vdata = None

        return vdata

    date_v = submit_date(date.replace('\n', ''))
    currency_v = submit_currency(currency_chosen)
    buy_or_sell_v = submit_buy_sell(buy_or_sell)
    quantity_v = submit_quantity(quantity)
    value_v = submit_value(value)
    data = [date_v, currency_v, buy_or_sell_v, quantity_v, value_v]

    if None in data:
        return "Podano nieprawidlowe dane"
    else:
        entry = {'date': date_v, 'quantity': quantity_v, 'cost': value_v}

        if currency_v not in data_map.keys():
            data_map[currency_v] = {buy_or_sell_v: [entry]}
        else:
            if buy_or_sell_v not in data_map[currency_v].keys():
                data_map[currency_v][buy_or_sell_v] = [entry]
            else:
                data_map[currency_v][buy_or_sell_v].append(entry)

        save_json(data_map)
        return "Podano prawidłowe dane"


loaded_data_map = load_json()
data_map = {} if loaded_data_map is None else loaded_data_map


def data_map_to_fifo_data_map():
    fifo_profit = {}
    fifo_avg_buy = {}
    data_map_copy = copy.deepcopy(data_map)
    for c_key in data_map_copy.keys():
        profit = 0
        stock_prices_sum = 0
        stock_amount = 0
        if 'buy' in data_map_copy[c_key]:
            for buy_entry in data_map_copy[c_key]['buy']:
                profit -= buy_entry['cost'] * buy_entry['quantity']
                num_of_bought = buy_entry['quantity']
                total_num_of_sold = 0
                while num_of_bought > 0:
                    if 'sell' in data_map_copy[c_key]:
                        for sell_entry in data_map_copy[c_key]['sell']:
                            num_of_sold = sell_entry['quantity']
                            if num_of_bought >= num_of_sold:
                                num_of_bought -= num_of_sold
                                to_add = num_of_sold
                            else:
                                to_add = num_of_bought
                                num_of_bought = 0
                            sell_entry['quantity'] -= to_add
                            profit += sell_entry['cost'] * to_add
                            total_num_of_sold += to_add
                        break
                    else:
                        break
                stock_amount += buy_entry['quantity'] - total_num_of_sold
                stock_prices_sum += (buy_entry['quantity'] - total_num_of_sold) * buy_entry['cost']
            if stock_amount > 0:
                fifo_avg_buy[c_key] = stock_prices_sum / stock_amount
        fifo_profit[c_key] = profit
    return fifo_profit, fifo_avg_buy


def data_map_to_simplified_data_map():
    simplified_data_map = {}
    for c_key in data_map.keys():
        for b_s_key in data_map[c_key].keys():
            sum_cost = 0
            sum_quantity = 0
            for entry in data_map[c_key][b_s_key]:
                sum_cost += entry['cost']
                sum_quantity += entry['quantity']

            if sum_quantity != 0:
                avg = round(sum_cost / sum_quantity, 2)
                if c_key not in simplified_data_map.keys():
                    simplified_data_map[c_key] = {}
                simplified_data_map[c_key][b_s_key] = avg
    return simplified_data_map


class MyPlot:
    def __init__(self, currency_list, time_interval, n_last_seconds, X, Y, S):
        self.currency_list = currency_list
        self.time_interval = time_interval
        self.n_last_seconds = n_last_seconds
        self.X = X
        self.Y = Y
        self.S = S

        fig1, axs1 = plt.subplots(3, 1, figsize=(12, 10), tight_layout=True)
        fig2, axs2 = plt.subplots(2, 3, figsize=(12, 10), tight_layout=True)
        fig2.autofmt_xdate()

        self.draw_plot(fig1, axs1, fig2, axs2)

    def draw_plot(self, fig1, axs1, fig2, axs2):
        last_average = gen_empty_dict(currency_list)
        RSI = gen_empty_dict(currency_list)
        cur_num = len(currency_list)
        values = gen_empty_list(currency_list)
        trend_texts = []
        profit_texts = []
        for i in range(cur_num):
            axs1[i].set_title(currency_list[i])
            axs1[i].set_xlabel('time')
            axs1[i].set_ylabel('value')
            trend_texts.append(axs1[i].text(0, 0, ''))
            axs2[0][i].set_title(currency_list[i])
            axs2[0][i].set_xlabel('time')
            axs2[0][i].set_ylabel('value')
            profit_texts.append(axs2[0][i].text(0, 0, ''))
            axs2[1][i].set_title(currency_list[i])
            axs2[1][i].set_xlabel('time')
            axs2[1][i].set_ylabel('value')

            locator1 = MaxNLocator(nbins=8)
            locator2 = MaxNLocator(nbins=4)
            axs1[i].xaxis.set_major_locator(locator1)
            axs2[0][i].xaxis.set_major_locator(locator2)
            axs2[1][i].xaxis.set_major_locator(locator2)

        lines_to_remove_tmp = {}
        last_average_values = {'sell': {}, 'buy': {}}

        while True:
            update_data(values)
            curr_trends = {}
            curr_volumens = {}
            for n in range(cur_num):
                def process_values(currency):
                    time_for_avg = [values[currency_list[n]][0][0].strftime("%H:%M:%S"),
                                    values[currency_list[n]][-1][0].strftime("%H:%M:%S")]
                    time = [values[currency_list[n]][-2][0].strftime("%H:%M:%S"),
                            values[currency_list[n]][-1][0].strftime("%H:%M:%S")]
                    sell = [values[currency_list[n]][-2][1], values[currency_list[n]][-1][1]]
                    purchase = [values[currency_list[n]][-2][2], values[currency_list[n]][-1][2]]
                    volume = [values[currency_list[n]][-2][3], values[currency_list[n]][-1][3]]
                    avg_of_input_data = data_map_to_simplified_data_map()
                    if len(last_average) >= 2:
                        average_sell_cost = [last_average[currency]['sell'][-2], last_average[currency]['sell'][-1]]
                        average_purchase_cost = [last_average[currency]['purchase'][-2],
                                                 last_average[currency]['purchase'][-1]]
                    else:
                        average_sell_cost = [0, 0]
                        average_purchase_cost = [0, 0]
                    if len(RSI) >= 2:
                        rsi_s = [RSI[currency]['sell'][-2], RSI[currency]['sell'][-1]]
                        rsi_p = [RSI[currency]['purchase'][-2], RSI[currency]['purchase'][-1]]
                    else:
                        rsi_s = [0, 0]
                        rsi_p = [0, 0]

                    avg_sell = None
                    if currency in avg_of_input_data:
                        if 'sell' in avg_of_input_data[currency]:
                            avg_sell = [avg_of_input_data[currency]['sell'], avg_of_input_data[currency]['sell']]
                    return time, time_for_avg, sell, purchase, volume, average_sell_cost, average_purchase_cost, rsi_s, rsi_p, \
                           avg_sell

                update_avg_dict(last_average, currency_list[n], values, n_last_seconds)
                update_RSI(RSI, currency_list[n], values)
                trends = classify_rsi_trend(RSI, currency_list[n])
                curr_trends[currency_list[n]] = trends['sell']
                curr_volumens[currency_list[n]] = values[currency_list[n]][-1][3]
                volatile = is_volatile(values, currency_list[n], X, Y)
                liquid = is_liquid(values, currency_list[n], S)

                def add_values_on_plot(label_sell=None, label_purchase=None, label_volume=None, label_avg_sell=None,
                                       label_avg_purchase=None, label_rsi_sell=None, label_rsi_purchase=None,
                                       label_avg_input_sell=None, label_avg_input_purchase=None):
                    time, time_for_avg, sell, purchase, volume, average_sell,\
                    average_purchase, rsi_sell, rsi_purchase, avg_sell = process_values(currency_list[n])
                    currency_to_profit, avg_purchase_excluding_sold = data_map_to_fifo_data_map()
                    if currency_list[n] in avg_purchase_excluding_sold.keys():
                        avg_purchase = [avg_purchase_excluding_sold[currency_list[n]], avg_purchase_excluding_sold[currency_list[n]]]
                    else:
                        avg_purchase = None

                    axs2[0][n].plot(time, sell, label=label_sell, color='lime')
                    axs2[0][n].plot(time, purchase, label=label_purchase, color='m')
                    axs2[1][n].bar(time, volume, label=label_volume, color='blue')
                    axs2[0][n].plot(time, average_sell, label=label_avg_sell, color='yellow')
                    axs2[0][n].plot(time, average_purchase, label=label_avg_purchase, color='orange')
                    axs1[n].plot(time, rsi_sell, label=label_rsi_sell, color='pink')
                    axs1[n].plot(time, rsi_purchase, label=label_rsi_purchase, color='orange')
                    axs1[n].legend(loc='upper right')
                    axs2[0][n].legend(loc='upper right')
                    axs2[1][n].legend(loc='upper right')
                    trend_texts[n].set_text('Sell - {}\nPurchase - {}'.format(
                        trends['sell'],
                        trends['purchase']))
                    pos_y = min(min(RSI[currency_list[n]]['sell']), min(RSI[currency_list[n]]['purchase']))
                    trend_texts[n].set_position((0, pos_y))

                    min_sell = min(values[currency_list[n]], key=lambda x: x[1])[1]
                    min_buy = min(values[currency_list[n]], key=lambda x: x[2])[2]

                    if currency_list[n] in currency_to_profit.keys():
                        profit_texts[n].set_text('{}{}'.format('Profit: ' if currency_to_profit[currency_list[n]] >= 0 else 'Loss: ', currency_to_profit[currency_list[n]]))
                        pos_f = min(min_sell, min_buy)
                        profit_texts[n].set_position((0, pos_f))

                    avg_sell_key = 'sell{}'.format(n)
                    avg_purchase_key = 'purchase{}'.format(n)

                    last_avg_sell = None
                    last_avg_buy = None

                    if avg_sell_key in last_average_values['sell']:
                        last_avg_sell = last_average_values['sell'][avg_sell_key]
                    if avg_purchase_key in last_average_values['buy']:
                        last_avg_buy = last_average_values['buy'][avg_purchase_key]

                    if avg_sell is not None or last_avg_sell is not None:
                        if avg_sell_key in lines_to_remove_tmp:
                            lines_to_remove_tmp[avg_sell_key].remove()
                        avg_sell_to_add = avg_sell if avg_sell is not None else last_avg_sell
                        line = axs2[0][n].plot(time_for_avg, avg_sell_to_add, '--', label=label_avg_input_sell, color='red')
                        last_average_values['sell'][avg_sell_key] = avg_sell_to_add
                        lines_to_remove_tmp[avg_sell_key] = line[0]

                    if avg_purchase is not None or last_avg_buy is not None:
                        if avg_purchase_key in lines_to_remove_tmp:
                            lines_to_remove_tmp[avg_purchase_key].remove()
                        avg_buy_to_add = avg_purchase if avg_purchase is not None else last_avg_buy
                        line = axs2[0][n].plot(time_for_avg, avg_buy_to_add, '--', label=label_avg_input_purchase, color='purple')
                        last_average_values['buy'][avg_purchase_key] = avg_buy_to_add
                        lines_to_remove_tmp[avg_purchase_key] = line[0]

                if len(values[currency_list[n]]) == 2:
                    add_values_on_plot(label_sell="Selling cost", label_purchase="Purchase cost", label_volume="Volume",
                                       label_avg_sell='Average sell', label_avg_purchase="Average purchase",
                                       label_rsi_sell="RSI sell", label_rsi_purchase="RSI purchase",
                                       label_avg_input_sell="Avg sell", label_avg_input_purchase="Avg purchase")

                elif len(values[currency_list[n]]) > 2:
                    add_values_on_plot(label_avg_input_sell="Avg sell", label_avg_input_purchase="Avg purchase")

                if n == 2:
                    potential_candidates = \
                        list(filter(lambda k: curr_trends[k] in ['Upward trend', 'Sideways trend'], curr_trends.keys()))
                    best_candidate = None
                    if len(potential_candidates) == 1:
                        best_candidate = potential_candidates[0]
                    elif len(potential_candidates) > 1:
                        max_volumen = max(curr_volumens.values())
                        best_candidate = list(filter(lambda k: curr_volumens[k] == max_volumen, curr_volumens.keys()))[0]

                    for i in range(cur_num):
                        axs2[1][i].spines['bottom'].set_color('0.0')
                        axs2[1][i].spines['top'].set_color('0.0')
                        axs2[1][i].spines['right'].set_color('0.0')
                        axs2[1][i].spines['left'].set_color('0.0')

                    if best_candidate is not None:
                        candidate_index = currency_list.index(best_candidate)
                        axs2[1][candidate_index].spines['bottom'].set_color('red')
                        axs2[1][candidate_index].spines['top'].set_color('red')
                        axs2[1][candidate_index].spines['right'].set_color('red')
                        axs2[1][candidate_index].spines['left'].set_color('red')
                        trend_texts[candidate_index].set_text('Sell - {}\nPurchase - {}{}{}'.format(
                            trends['sell'],
                            trends['purchase'],
                            "\n{}".format(volatile) if volatile != "" else "",
                            "\n{}".format(liquid) if liquid != "" else ""))
                        pos_y = min(min(RSI[currency_list[n]]['sell']), min(RSI[currency_list[n]]['purchase']))
                        trend_texts[candidate_index].set_position((0, pos_y))

            if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1] != "test"):
                plt.pause(time_interval)
            else:
                plt.pause(1)


class DataWindow:
    def __init__(self, currency_list):
        master = Tk()

        var1 = StringVar()
        label1 = Label(master, textvariable=var1, relief=RAISED)
        label1.pack()
        var1.set("Ilość")

        quantity = StringVar(value=20)
        quantity_box = Spinbox(master, from_=1, to=1000000, textvariable=quantity, wrap=True)
        quantity_box.pack()

        currency_text = StringVar(master)
        currency_text.set(currency_list[0])  # default value
        w = OptionMenu(master, currency_text, *currency_list)
        w.pack()

        buy_or_sell_text = StringVar(master)
        buy_or_sell_text.set('sell')  # default value
        w = OptionMenu(master, buy_or_sell_text, *['buy', 'sell'])
        w.pack()

        var3 = StringVar()
        label3 = Label(master, textvariable=var3, relief=RAISED)
        label3.pack()
        var3.set("Wartość")

        current_value = StringVar(value=250)
        value_box = Spinbox(master, from_=1, to=1000000, textvariable=current_value, wrap=True)
        value_box.pack()

        var2 = StringVar()
        label2 = Label(master, textvariable=var2, relief=RAISED)
        label2.pack()
        var2.set("Czas operacji")

        time_text = Text(master, height=1, width=30)
        time_text.pack()
        time_text.insert(END, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        def button_callback():
            result = on_button_clicked(time_text.get(1.0, END), currency_text.get(), buy_or_sell_text.get(), quantity.get(), current_value.get(), data_map)
            # tkinter.messagebox.showinfo(title="Informacja", message=result)

        submit = Button(master, text="Zapisz", command=button_callback)

        submit.pack()

        master.mainloop()


if __name__ == '__main__':
    currency_list = ['LTC-PLN', 'LSK-PLN', 'BTC-PLN']
    time_interval = 2
    retry_stat_code_err = 10
    retry_connect_err = 10
    X = 0.001
    Y = 3
    S = 5

    window_thread = Thread(target=lambda: DataWindow(currency_list))
    window_thread.start()

    # n_last_seconds = int(input('Podaj sekundy: '))
    # RSI_range = int(input('Podaj zakres do RSI: '))

    n_last_seconds = 10
    RSI_range = 10

    time.sleep(2)

    MyPlot(currency_list, time_interval, n_last_seconds, X, Y, S)

