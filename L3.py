from requests import get
import matplotlib.pyplot as plt
import sys


def connection(currency):
    return f'https://bitbay.net/API/Public/{currency}/ticker.json'


def get_values(currency):
    try:
        req = get(connection(currency)).json()
        bid = req['bid']
        ask = req['ask']
        return bid, ask
    except Exception as e:
        print(e)


def gen_empty_dicts(list_currencies):
    return {i: [] for i in list_currencies}


def add_values(buy, sell):
    for i in list_currencies:
        data = get_values(i)
        buy[i].append(data[0])
        sell[i].append(data[1])


def draw_axes(list_currencies):
    cur_num = len(list_currencies)
    fig, axs = plt.subplots(3, 1, figsize=(15, 12), constrained_layout=True)
    for i in range(cur_num):
        axs[i].set_title(list_currencies[i])
        axs[i].set_xlabel('time')
        axs[i].set_ylabel('value')
    return fig, axs


def draw_plot(list_currencies, time_interval):
    fig, axs = draw_axes(list_currencies)
    cur_num = len(list_currencies)

    buy, sell = gen_empty_dicts(list_currencies), gen_empty_dicts(list_currencies)

    iterator = 0
    while True:
        add_values(buy, sell)
        for n in range(cur_num):
            if len(buy[list_currencies[n]]) and len(sell[list_currencies[n]]) == 2:
                time = [(iterator - 1) * time_interval, iterator * time_interval]
                selling_cost = [sell[list_currencies[n]][-2], sell[list_currencies[n]][-1]]
                purchase_cost = [buy[list_currencies[n]][-2], buy[list_currencies[n]][-1]]
                axs[n].plot(time, selling_cost, label="Selling cost", color='purple')
                axs[n].plot(time, purchase_cost, label="Purchase cost", color='blue')
                axs[n].legend()
            elif len(buy[list_currencies[n]]) and len(sell[list_currencies[n]]) > 2:
                time = [(iterator - 1) * time_interval, iterator * time_interval]
                selling_cost = [sell[list_currencies[n]][-2], sell[list_currencies[n]][-1]]
                purchase_cost = [buy[list_currencies[n]][-2], buy[list_currencies[n]][-1]]
                axs[n].plot(time, selling_cost, color="purple")
                axs[n].plot(time, purchase_cost, color='blue')
        iterator += 1
        plt.pause(time_interval)


if __name__ == '__main__':
    try:
        list_currencies = ['BTC', 'LTC', 'TRX']
        time_interval = 5
        draw_plot(list_currencies, time_interval)
    except KeyboardInterrupt:
        print('User hit the interrupt key')
        sys.exit()
