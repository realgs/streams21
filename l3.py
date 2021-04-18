import requests
from datetime import datetime
import sys
import matplotlib.pyplot as plt


def get_data(currency, retry_stat_code_err, retry_connect_err):
    url_pre = 'https://bitbay.net/API/Public/'
    url_post = '/ticker.json'
    url = url_pre + currency + url_post
    try:
        response = requests.get(url)
        status_code = str(response.status_code)
        if status_code[0] == '2':
            resp_json = response.json()
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            selling_cost = resp_json['ask']
            purchase_cost = resp_json['bid']
            return current_time, selling_cost, purchase_cost
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


def gen_empty_list(currency_list):
    return {i: [] for i in currency_list}


def update_data(values):
    for i in currency_list:
        data = get_data(i, retry_stat_code_err, retry_connect_err)
        values[i].append(data)


def draw_plot(currency_list, time_interval):

    cur_num = len(currency_list)
    values = gen_empty_list(currency_list)
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), constrained_layout=True)
    for i in range(cur_num):
        axs[i].set_title(currency_list[i])
        axs[i].set_xlabel('time')
        axs[i].set_ylabel('value')

    while True:
        update_data(values)
        for n in range(cur_num):
            if len(values[currency_list[n]]) == 2:
                time = [values[currency_list[n]][-1][0], values[currency_list[n]][-2][0]]
                sell = [values[currency_list[n]][-1][1], values[currency_list[n]][-2][1]]
                purchase = [values[currency_list[n]][-1][2], values[currency_list[n]][-2][2]]
                axs[n].plot(time, sell, label="Selling cost", color='lime')
                axs[n].plot(time, purchase, label="Purchase cost", color='m')
                axs[n].legend()
            elif len(values[currency_list[n]]) > 2:
                time = [values[currency_list[n]][-1][0], values[currency_list[n]][-2][0]]
                sell = [values[currency_list[n]][-1][1], values[currency_list[n]][-2][1]]
                purchase = [values[currency_list[n]][-1][2], values[currency_list[n]][-2][2]]
                axs[n].plot(time, sell, color='lime')
                axs[n].plot(time, purchase, color='m')
        plt.pause(time_interval)


if __name__ == '__main__':
    currency_list = ['BTC', 'BTG', 'ZEC']
    time_interval = 5
    retry_stat_code_err = 10
    retry_connect_err = 10
    draw_plot(currency_list, time_interval)
