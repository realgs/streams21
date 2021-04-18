import requests
import time
from datetime import datetime
import sys
import matplotlib.pyplot as plt



def get_data(currency):
    url = 'https://bitbay.net/API/Public/{}/ticker.json'.format(currency)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            resp_json = response.json()
            current_time = datetime.now()
            selling_cost = resp_json['ask']
            purchase_cost = resp_json['bid']
            return current_time, selling_cost, purchase_cost
        else:
            print("Unable to access API on BitBay. Error: {}".format(response.status_code))
            sys.exit()
    except requests.exceptions.ConnectionError:
        print("Cannot reach the server.")
        sys.exit()


def gen_empty_list(currency_list):
    return {i:[] for i in currency_list}


def update_data(values):
    for i in currency_list:
        data = get_data(i)
        values[i].append(data)


def draw_plot(currency_list, time_interval):

    cur_num = len(currency_list)
    values = gen_empty_list(currency_list)

    for i in range(cur_num):
        fig, axs = plt.subplot(i+1, 1, i+1)
        plt.title(currency_list(i))

    while True:
        update_data(values)
        for n in range(cur_num):
            if len(values[currency_list[n]]) == 2:
                time = [values[currency_list[n]][-2:][0]]
                sell = [values[currency_list[n]][-2:][1]]
                purchase = [values[currency_list[n]][-2:][2]]
            elif len(values[currency_list[n]]) > 2:
                pass




if __name__ == '__main__':
    currency_list = ['BTC', 'BTG', 'ZEC']
    time_interval = 5
    draw_plot(currency_list, time_interval)
