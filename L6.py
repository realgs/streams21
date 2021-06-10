from requests import get
import matplotlib.pyplot as plt
import sys
import requests
from datetime import datetime, timedelta
from matplotlib.ticker import MaxNLocator
import json


def connection(curr):
    return f'https://bitbay.net/API/Public/{curr}/ticker.json'


def get_time(current_time):
    current_time.append(datetime.now())
    return current_time


def get_values(curr):
    try:
        req = get(connection(curr)).json()
        bid = req['bid']
        ask = req['ask']
        return bid, ask
    except Exception as e:
        print(e)


def get_volumen(curr):
    fromtime = int((datetime.now() - timedelta(seconds=5)).timestamp()) * 1000
    url = f"https://api.bitbay.net/rest/trading/transactions/{curr}"
    queryparams = {'fromTime': fromtime}
    response = requests.request("GET", url, params=queryparams)
    response = eval(response.text)
    return sum([float(response['items'][i]['a']) for i in range(len(response['items']))])


def gen_empty_dicts(list_currencies):
    return {curr: [] for curr in list_currencies}


def calculate_average(dict, curr):
    interval_data = dict[curr][-qty:]
    avg = sum(interval_data) / len(interval_data)
    return avg


def calculate_RSI(dict, curr):
    interval_data = dict[curr][start:end]
    rises = 0
    rises_count = 0
    losses = 0
    losses_count = 0
    for i in range(1, len(interval_data)):
        if interval_data[i - 1] <= interval_data[i]:
            rise = interval_data[i] - interval_data[i - 1]
            rises += rise
            rises_count += 1
        elif interval_data[i - 1] > interval_data[i]:
            loss = interval_data[i - 1] - interval_data[i]
            losses += loss
            losses_count += 1
    if rises_count == 0:
        a = 1
    else:
        a = rises/rises_count
    if losses_count == 0:
        b = 1
    else:
        b = losses/losses_count
    RSI = 100 - (100 / (1 + (a / b)))
    return RSI


def add_values(buy, sell, volumen, avg_buy, avg_sell, RSI_buy, RSI_sell):
    for curr in list_currencies:
        b, s = get_values(curr)
        buy[curr].append(b)
        sell[curr].append(s)
        volumen[curr].append(get_volumen(curr))
        avg_buy[curr].append(calculate_average(buy, curr))
        avg_sell[curr].append(calculate_average(sell, curr))
        RSI_buy[curr].append(calculate_RSI(buy, curr))
        RSI_sell[curr].append(calculate_RSI(sell, curr))
    return buy, sell, volumen, avg_buy, avg_sell, RSI_buy, RSI_sell


def check_trend(list_currencies, i , volumen):
    average = sum(volumen[list_currencies[i]]) / len(volumen[list_currencies[i]])
    if volumen[list_currencies[i]][-1] > average:
        return 'Upward trend'
    elif volumen[list_currencies[i]][-1] < average:
        return 'Downward trend'
    else:
        return 'Sideway trend'


def choose_candidate(list_currencies, RSI_buy):
    candidate_list = []
    if check_trend(list_currencies, 0, RSI_buy) != 'Downward trend':
        candidate_list.append(RSI_buy[list_currencies[0]][-1])
    else:
        candidate_list.append(0)
    if check_trend(list_currencies, 1, RSI_buy) != 'Downward trend':
        candidate_list.append(RSI_buy[list_currencies[1]][-1])
    else:
        candidate_list.append(0)
    if check_trend(list_currencies, 2, RSI_buy) != 'Downward trend':
        candidate_list.append(RSI_buy[list_currencies[2]][-1])
    else:
        candidate_list.append(0)
    max_volumen = max(candidate_list)
    if max_volumen == 0:
        return ''
    else:
        index_max_volumen = candidate_list.index(max_volumen)
        return index_max_volumen


def check_voltaile(list_currencies, i, buy, X, Y):
    if len(buy[list_currencies[i]]) < Y:
        return ''
    else:
        y_samples = buy[list_currencies[i]][-Y:]
        oscilation = ((max(y_samples) - min(y_samples)) / max(y_samples)) * 100
        if oscilation > X:
            return 'Volatile asset'
        else:
            return ''


def check_liquid(list_currencies, i, buy, sell, S):
    difference = ((buy[list_currencies[i]][-1] - sell[list_currencies[i]][-1]) / buy[list_currencies[i]][-1]) * 100
    if difference < S:
        return 'Liquid asset'
    else:
        return ''


def draw_axes(list_currencies):
    currencies_amount = len(list_currencies)
    fig, axs = plt.subplots(3, 3, figsize=(40, 5), constrained_layout=True)
    locator = MaxNLocator(nbins=4)
    profit_text = []
    for n in range(currencies_amount):
        axs[0, n].set_title(list_currencies[n])
        axs[0, n].set_xlabel('Time')
        axs[0, n].xaxis.set_major_locator(locator)
        axs[0, n].set_ylabel('Value')
        axs[1, n].xaxis.set_major_locator(locator)
        axs[1, n].set_ylabel('Value')
        axs[2, n].set_xlabel('Time')
        axs[2, n].xaxis.set_major_locator(locator)
        axs[2, n].set_ylabel('Value')
        profit_text.append(axs[0, n].text(0, 0, ''))
    return fig, axs, profit_text,currencies_amount


def draw_black_axes(axs, number):
    axs[2, number].spines['bottom'].set_color('k')
    axs[2, number].spines['top'].set_color('k')
    axs[2, number].spines['left'].set_color('k')
    axs[2, number].spines['right'].set_color('k')


def download_transactions():
    f = open('user_value.json', )
    data = json.load(f)
    f.close()
    f = open('user_value.json', 'w')
    f.write(json.dumps([]))
    f.close()
    return data


def segregate_data(user_buy_dict, user_sell_dict):
    new_json_values = download_transactions()
    if len(new_json_values) > 0:
        if new_json_values[0]['currency'] == 'BTC-PLN':
            for i in range(new_json_values[0]['amount']):
                if new_json_values[0]['action'] == 'buy':
                    user_buy_dict['BTC-PLN'].append(new_json_values[0]['price'])
            for i in range(new_json_values[0]['amount']):
                if new_json_values[0]['action'] == 'sell':
                    user_sell_dict['BTC-PLN'].append(new_json_values[0]['price'])
        if new_json_values[0]['currency'] == 'LTC-PLN':
            for i in range(new_json_values[0]['amount']):
                if new_json_values[0]['action'] == 'buy':
                    user_buy_dict['LTC-PLN'].append(new_json_values[0]['price'])
            for i in range(new_json_values[0]['amount']):
                if new_json_values[0]['action'] == 'sell':
                    user_sell_dict['LTC-PLN'].append(new_json_values[0]['price'])
        if new_json_values[0]['currency'] == 'TRX-PLN':
            for i in range(new_json_values[0]['amount']):
                if new_json_values[0]['action'] == 'buy':
                    user_buy_dict['TRX-PLN'].append(new_json_values[0]['price'])
            for i in range(new_json_values[0]['amount']):
                if new_json_values[0]['action'] == 'sell':
                    user_sell_dict['TRX-PLN'].append(new_json_values[0]['price'])



def user_fifo_average(currency, user_buy_dict, user_sell_dict):
    value_list_buy = user_buy_dict[currency]
    value_list_sell = user_sell_dict[currency]
    n = len(value_list_sell)
    buy_sum = sum(value_list_buy[n:])
    len_sum = len(value_list_buy[n:])
    if len_sum == 0:
        len_sum = 1
    fifo_average = buy_sum / len_sum
    return fifo_average


def calculate_user_profit(currency, user_buy_dict, user_sell_dict):
    value_list_buy = user_buy_dict[currency]
    value_list_sell = user_sell_dict[currency]
    n = len(value_list_sell)
    buy_sum = sum(value_list_buy[:n])
    sell_sum = sum(value_list_sell)
    profit = sell_sum - buy_sum
    return profit


def user_add_values(currency, user_buy_dict, user_sell_dict, user_fifo_dict, user_profit_dict):
    user_fifo_dict[currency].append(user_fifo_average(currency, user_buy_dict, user_sell_dict))
    user_profit_dict[currency].append(calculate_user_profit(currency, user_buy_dict, user_sell_dict))
    return user_fifo_dict, user_profit_dict


def draw_plot(time_interval):
    fig, axs, profit_text, currencies_amount = draw_axes(list_currencies)
    buy_dict, sell_dict, volumen_dict, avg_buy_dict, avg_sell_dict, RSI_buy_dict, RSI_sell_dict = gen_empty_dicts(list_currencies), gen_empty_dicts(list_currencies), gen_empty_dicts(list_currencies), gen_empty_dicts(list_currencies), gen_empty_dicts(list_currencies), gen_empty_dicts(list_currencies), gen_empty_dicts(list_currencies)
    current_time = []
    user_buy_dict, user_sell_dict = gen_empty_dicts(list_currencies), gen_empty_dicts(list_currencies)
    user_fifo_dict, user_profit_dict = gen_empty_dicts(list_currencies), gen_empty_dicts(list_currencies)
    while True:
        segregate_data(user_buy_dict, user_sell_dict)
        buy, sell, volumen, avg_buy, avg_sell, RSI_buy, RSI_sell = add_values(buy_dict, sell_dict, volumen_dict, avg_buy_dict, avg_sell_dict, RSI_buy_dict, RSI_sell_dict)
        current_time = get_time(current_time)
        segregate_data(user_buy_dict, user_sell_dict)

        for curr in range(currencies_amount):
            fifo, profit = user_add_values(list_currencies[curr], user_buy_dict, user_sell_dict, user_fifo_dict, user_profit_dict)
            #print('profit', profit)
            if len(buy[list_currencies[curr]]) and len(sell[list_currencies[curr]]) and len(RSI_buy[list_currencies[curr]]) and len(RSI_sell[list_currencies[curr]]) == 2:
                time = [current_time[-2].strftime("%H:%M:%S"), current_time[-1].strftime("%H:%M:%S")]
                selling_cost = [sell[list_currencies[curr]][-2], sell[list_currencies[curr]][-1]]
                purchase_cost = [buy[list_currencies[curr]][-2], buy[list_currencies[curr]][-1]]
                volumen_value = [volumen[list_currencies[curr]][-2], volumen[list_currencies[curr]][-1]]
                avg_buy_value = [avg_buy[list_currencies[curr]][-2], avg_buy[list_currencies[curr]][-1]]
                avg_sell_value = [avg_sell[list_currencies[curr]][-2], avg_sell[list_currencies[curr]][-1]]
                RSI_buy_value = [RSI_buy[list_currencies[curr]][-2], RSI_buy[list_currencies[curr]][-1]]
                RSI_sell_value = [RSI_sell[list_currencies[curr]][-2], RSI_sell[list_currencies[curr]][-1]]
                if fifo[list_currencies[curr]][-1] != 0:
                    if len(list_currencies[curr]) >= 2:
                        user_fifo_value = [fifo[list_currencies[curr]][-2], fifo[list_currencies[curr]][-1]]
                        profit_text[curr].set_text(f'Profit equals: {profit[list_currencies[curr]][-1]}')
                        y_position = min(avg_buy[list_currencies[curr]])
                        profit_text[curr].set_position((0, y_position))

                        axs[0, curr].plot(time, user_fifo_value, '--', label='User average buy', color='purple')


                axs[0, curr].plot(time, selling_cost, label="Selling cost", color='c')
                axs[0, curr].plot(time, purchase_cost, label="Purchase cost", color='limegreen')
                axs[0, curr].plot(time, avg_sell_value, '--', label='Average sell', color='darkgreen')
                axs[0, curr].plot(time, avg_buy_value, '--',label='Average buy', color='b')

                axs[1, curr].bar(time, volumen_value, label="Volumen", color='slateblue')
                axs[1, curr].set_xticks([])

                axs[2, curr].plot(time, RSI_buy_value, label='RSI buy', color='darkred')
                axs[2, curr].plot(time, RSI_sell_value, label='RSI sell', color='coral')

                for i in range(currencies_amount):
                    axs[i, 2].legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')


                candidate = choose_candidate(list_currencies, RSI_buy)
                if candidate != '':
                    draw_black_axes(axs, 0)
                    draw_black_axes(axs, 1)
                    draw_black_axes(axs, 2)
                    axs[2, candidate].spines['bottom'].set_color('g')
                    axs[2, candidate].spines['top'].set_color('g')
                    axs[2, candidate].spines['left'].set_color('g')
                    axs[2, candidate].spines['right'].set_color('g')
                    voltaile_text = check_voltaile(list_currencies, candidate, buy, X, Y)
                    liquid_text = check_liquid(list_currencies, candidate, buy, sell, S)
                    plt.figtext(0.08, 0.01, f'{voltaile_text, liquid_text}', ha="center", fontsize=10,
                                bbox={"facecolor": "palegreen", "alpha": 0.5, "pad": 5})


            elif len(buy[list_currencies[curr]]) and len(sell[list_currencies[curr]]) and len(RSI_buy[list_currencies[curr]]) and len(RSI_sell[list_currencies[curr]]) > 2:
                time = [current_time[-2].strftime("%H:%M:%S"), current_time[-1].strftime("%H:%M:%S")]
                selling_cost = [sell[list_currencies[curr]][-2], sell[list_currencies[curr]][-1]]
                purchase_cost = [buy[list_currencies[curr]][-2], buy[list_currencies[curr]][-1]]
                volumen_value = [volumen[list_currencies[curr]][-2], volumen[list_currencies[curr]][-1]]
                avg_buy_value = [avg_buy[list_currencies[curr]][-2], avg_buy[list_currencies[curr]][-1]]
                avg_sell_value = [avg_sell[list_currencies[curr]][-2], avg_sell[list_currencies[curr]][-1]]
                RSI_buy_value = [RSI_buy[list_currencies[curr]][-2], RSI_buy[list_currencies[curr]][-1]]
                RSI_sell_value = [RSI_sell[list_currencies[curr]][-2], RSI_sell[list_currencies[curr]][-1]]
                if fifo[list_currencies[curr]][-1] != 0:
                    if len(list_currencies[curr]) >= 2:
                        user_fifo_value = [fifo[list_currencies[curr]][-2], fifo[list_currencies[curr]][-1]]
                        profit_text[curr].set_text(f'Profit equals: {profit[list_currencies[curr]][-1]}')
                        y_position = min(avg_buy[list_currencies[curr]])
                        profit_text[curr].set_position((0, y_position))

                        axs[0, curr].plot(time, user_fifo_value, '--', label='User average buy', color='purple')

                axs[0, curr].plot(time, selling_cost, label="Selling cost", color='c')
                axs[0, curr].plot(time, purchase_cost, label="Purchase cost", color='limegreen')
                axs[0, curr].plot(time, avg_sell_value, '--', label='Average sell', color='darkgreen')
                axs[0, curr].plot(time, avg_buy_value, '--', label='Average buy', color='b')

                axs[1, curr].bar(time, volumen_value, label="Volumen", color='slateblue')
                axs[1, curr].set_xticks([])

                axs[2, curr].plot(time, RSI_buy_value, label='RSI buy', color='darkred')
                axs[2, curr].plot(time, RSI_sell_value, label='RSI sell', color='coral')
                candidate = choose_candidate(list_currencies, RSI_buy)
                if candidate != '':
                    draw_black_axes(axs, 0)
                    draw_black_axes(axs, 1)
                    draw_black_axes(axs, 2)

                    axs[2, candidate].spines['bottom'].set_color('g')
                    axs[2, candidate].spines['top'].set_color('g')
                    axs[2, candidate].spines['left'].set_color('g')
                    axs[2, candidate].spines['right'].set_color('g')
                    voltaile_text = check_voltaile(list_currencies, candidate, buy, X, Y)
                    liquid_text = check_liquid(list_currencies, candidate, buy, sell, S)
                    plt.figtext(0.08, 0.01, f'{voltaile_text, liquid_text}', ha="center", fontsize=10,
                                bbox={"facecolor": "palegreen", "alpha": 0.5, "pad": 5})
        plt.pause(time_interval)


if __name__ == '__main__':
    try:
        list_currencies = ['BTC-PLN', 'LTC-PLN', 'TRX-PLN']
        wallet = {'BTC-PLN':
                      {
                          'amount':0,
                          'total_profit':0},
                  'LTC-PLN':
                      {
                          'amount': 0,
                          'total_profit': 0},
                  'TRX-PLN':
                      {
                          'amount': 0,
                          'total_profit': 0}
                  }
        time_interval = 2
        qty = 10
        start = 1
        end = 3
        X = 5
        Y = 5
        S = 3
        draw_plot(time_interval)
    except KeyboardInterrupt:
        print('User hit the interrupt key')
        sys.exit()