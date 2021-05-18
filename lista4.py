import random
import requests
from datetime import datetime, timedelta
import sys
import matplotlib.pyplot as plt


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
            volume = resp_json['volume']
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
    return sum/len(filtered)


def calculate_RSI(RSI_range, values, currency, values_index):
    filtered = list(filter(lambda v: v[0] >= datetime.now() - timedelta(seconds=RSI_range), values[currency]))
    if len(filtered) < 2:
        return 0
    ups = 0
    downs = 0
    ups_counter = 0
    downs_counter = 0
    for i in range(len(filtered)-1):
        if filtered[i][values_index] <= filtered[i+1][values_index]:
            up = filtered[i+1][values_index] - filtered[i][values_index]
            ups += up
            ups_counter += 1
        elif filtered[i][values_index] > filtered[i+1][values_index]:
            down = filtered[i+1][values_index] - filtered[i][values_index]
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


def draw_plot(currency_list, time_interval, n_last_seconds):
    last_average = gen_empty_dict(currency_list)
    RSI = gen_empty_dict(currency_list)
    cur_num = len(currency_list)
    values = gen_empty_list(currency_list)
    fig1, axs1 = plt.subplots(3, 1, figsize=(12, 10), constrained_layout=True)
    fig2, axs2 = plt.subplots(3, 2, figsize=(12, 10), constrained_layout=True)
    for i in range(cur_num):
        axs1[i].set_title(currency_list[i])
        axs1[i].set_xlabel('time')
        axs1[i].set_ylabel('value')
        axs2[i][0].set_title(currency_list[i])
        axs2[i][0].set_xlabel('time')
        axs2[i][0].set_ylabel('value')
        axs2[i][1].set_title(currency_list[i])
        axs2[i][1].set_xlabel('time')
        axs2[i][1].set_ylabel('value')

    while True:
        update_data(values)
        for n in range(cur_num):
            def process_values(currency):
                time = [values[currency_list[n]][-2][0].strftime("%H:%M:%S"),
                        values[currency_list[n]][-1][0].strftime("%H:%M:%S")]
                sell = [values[currency_list[n]][-2][1], values[currency_list[n]][-1][1]]
                purchase = [values[currency_list[n]][-2][2], values[currency_list[n]][-1][2]]
                volume = [values[currency_list[n]][-2][3], values[currency_list[n]][-1][3]]
                if len(last_average) >= 2:
                    average_sell_cost = [last_average[currency]['sell'][-2], last_average[currency]['sell'][-1]]
                    average_purchase_cost = [last_average[currency]['purchase'][-2], last_average[currency]['purchase'][-1]]
                else:
                    average_sell_cost = [0, 0]
                    average_purchase_cost = [0, 0]
                if len(RSI) >= 2:
                    rsi_s = [RSI[currency]['sell'][-2], RSI[currency]['sell'][-1]]
                    rsi_p = [RSI[currency]['purchase'][-2], RSI[currency]['purchase'][-1]]
                else:
                    rsi_s = [0, 0]
                    rsi_p = [0, 0]
                return time, sell, purchase, volume, average_sell_cost, average_purchase_cost, rsi_s, rsi_p

            update_avg_dict(last_average, currency_list[n], values, n_last_seconds)
            update_RSI(RSI, currency_list[n], values)

            if len(values[currency_list[n]]) == 2:
                fig1.autofmt_xdate()
                fig2.autofmt_xdate()
                time, sell, purchase, volume, average_sell, average_purchase, rsi_sell, rsi_purchase = process_values(currency_list[n])
                axs1[n].plot(time, sell, label="Selling cost", color='lime')
                axs1[n].plot(time, purchase, label="Purchase cost", color='m')
                axs2[n][0].bar(time, volume, label="Volume", color='blue')
                axs1[n].plot(time, average_sell, label='Average sell', color='yellow')
                axs1[n].plot(time, average_purchase, label='Average purchase', color='black')
                axs2[n][1].plot(time, rsi_sell, label='RSI sell', color='pink')
                axs2[n][1].plot(time, rsi_purchase, label='RSI purchase', color='orange')
                axs1[n].legend(loc='upper right')
                axs1[n].legend(loc='upper right')
                axs1[n].legend(loc='upper right')
                axs2[n][0].legend(loc='upper right')
                axs2[n][0].legend(loc='upper right')
                axs2[n][0].legend(loc='upper right')
                axs2[n][1].legend(loc='upper right')
                axs2[n][1].legend(loc='upper right')
                axs2[n][1].legend(loc='upper right')

            elif len(values[currency_list[n]]) > 2:
                time, sell, purchase, volume, average_sell, average_purchase, rsi_sell, rsi_purchase = process_values(currency_list[n])
                axs1[n].plot(time, sell, color='lime')
                axs1[n].plot(time, purchase, color='m')
                axs2[n][0].bar(time, volume, color='blue')
                axs1[n].plot(time, average_sell,  color='yellow')
                axs1[n].plot(time, average_purchase, color='black')
                axs2[n][1].plot(time, rsi_sell,  color='pink')
                axs2[n][1].plot(time, rsi_purchase, color='orange')
                axs1[n].legend(loc='upper right')
                axs1[n].legend(loc='upper right')
                axs1[n].legend(loc='upper right')
                axs2[n][0].legend(loc='upper right')
                axs2[n][0].legend(loc='upper right')
                axs2[n][0].legend(loc='upper right')
                axs2[n][1].legend(loc='upper right')
                axs2[n][1].legend(loc='upper right')
                axs2[n][1].legend(loc='upper right')
        if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1] != "test"):
            plt.pause(time_interval)
        else:
            plt.pause(1)


if __name__ == '__main__':
    currency_list = ['TRX-PLN', 'LSK-PLN', 'ETH-PLN']
    time_interval = 2
    retry_stat_code_err = 10
    retry_connect_err = 10
    n_last_seconds = int(input('Podaj sekundy: '))
    RSI_range = int(input('Podaj zakres do RSI: '))
    draw_plot(currency_list, time_interval, n_last_seconds)
