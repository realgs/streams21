from requests import get
import matplotlib.pyplot as plt
import sys
import requests
from datetime import datetime, timedelta
from matplotlib.ticker import MaxNLocator


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
    fromtime = int((datetime.now() - timedelta(seconds=60)).timestamp()) * 1000
    url = f"https://api.bitbay.net/rest/trading/transactions/{curr}"
    queryparams = {'fromTime': fromtime}
    response = requests.request("GET", url, params=queryparams)
    response = eval(response.text)
    return sum([float(response['items'][i]['a']) for i in range(len(response['items']))])


def gen_empty_dicts(list_currencies):
    return {curr: [] for curr in list_currencies}



def calculate_averange(data_dict, curr):
    interval_data = data_dict[curr][-qty:]
    avg = sum(interval_data) / len(interval_data)
    return avg


def calculate_RSI(data_dict, curr):
    interval_data = data_dict[curr][start:end]
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


def add_values(curr, buy, sell, volumen, avg_buy, avg_sell, RSI_buy, RSI_sell):
    b, s = get_values(curr)
    buy[curr].append(b)
    sell[curr].append(s)
    volumen[curr].append(get_volumen(curr))
    avg_buy[curr].append(calculate_averange(buy, curr))
    avg_sell[curr].append(calculate_averange(sell, curr))
    RSI_buy[curr].append(calculate_RSI(buy, curr))
    RSI_sell[curr].append(calculate_RSI(sell, curr))
    return buy, sell, volumen, avg_buy, avg_sell, RSI_buy, RSI_sell



def draw_axes():
    fig, axs = plt.subplots(3, 1, figsize=(12, 5), constrained_layout=True)
    locator = MaxNLocator(nbins=4)
    axs[0].set_title(curr)
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Value')
    axs[1].set_title('Volume')
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Value')
    axs[2].set_title('RSI')
    axs[2].set_xlabel('Time')
    axs[2].set_ylabel('Value')
    axs[0].xaxis.set_major_locator(locator)
    axs[1].xaxis.set_major_locator(locator)
    axs[2].xaxis.set_major_locator(locator)
    return fig, axs


def draw_plot(time_interval, curr):
    fig, axs = draw_axes()
    buy_dict, sell_dict, volumen_dict, avg_buy_dict, avg_sell_dict, RSI_buy_dict, RSI_sell_dict = gen_empty_dicts(
        list_currencies), gen_empty_dicts(list_currencies), gen_empty_dicts(list_currencies), gen_empty_dicts(
        list_currencies), gen_empty_dicts(list_currencies), gen_empty_dicts(list_currencies), gen_empty_dicts(
        list_currencies)
    current_time = []
    while True:
        buy, sell, volumen, avg_buy, avg_sell, RSI_buy, RSI_sell = add_values(curr, buy_dict, sell_dict, volumen_dict,
                                                                              avg_buy_dict, avg_sell_dict, RSI_buy_dict,
                                                                              RSI_sell_dict)
        time_list = get_time(current_time)
        if len(buy[curr]) and len(sell[curr]) and len(RSI_buy[curr]) and len(RSI_sell[curr]) == 2:
            time = [time_list[-2].strftime("%H:%M:%S"), time_list[-1].strftime("%H:%M:%S")]
            selling_cost = [sell[curr][-2], sell[curr][-1]]
            purchase_cost = [buy[curr][-2], buy[curr][-1]]
            volume_value = [volumen[curr][-2], volumen[curr][-1]]
            avg_buy_value = [avg_buy[curr][-2], avg_buy[curr][-1]]
            avg_sell_value = [avg_sell[curr][-2], avg_sell[curr][-1]]
            RSI_buy_value = [RSI_buy[curr][-2], RSI_buy[curr][-1]]
            RSI_sell_value = [RSI_sell[curr][-2], RSI_sell[curr][-1]]
            axs[0].plot(time, selling_cost, label="Selling cost", color='c')
            axs[0].plot(time, purchase_cost, label="Purchase cost", color='limegreen')
            axs[0].plot(time, avg_buy_value, '--', label='Average Buy Cost', color='b')
            axs[0].plot(time, avg_sell_value, '--', label='Average Sell Cost', color='darkgreen')
            axs[0].legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
            axs[1].bar(time, volume_value, label='Volume values', color='slateblue')
            axs[1].set_xticks([])
            axs[1].legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
            axs[2].plot(time, RSI_buy_value, label='RSI buy', color='coral' )
            axs[2].plot(time, RSI_sell_value, label='RSI sell', color='darkred')
            axs[2].legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        elif len(buy[curr]) and len(sell[curr]) and len(RSI_buy[curr]) and len(RSI_sell[curr]) > 2:
            time = [time_list[-2].strftime("%H:%M:%S"), time_list[-1].strftime("%H:%M:%S")]
            selling_cost = [sell[curr][-2], sell[curr][-1]]
            purchase_cost = [buy[curr][-2], buy[curr][-1]]
            volume_value = [volumen[curr][-2], volumen[curr][-1]]
            avg_buy_value = [avg_buy[curr][-2], avg_buy[curr][-1]]
            avg_sell_value = [avg_sell[curr][-2], avg_sell[curr][-1]]
            RSI_buy_value = [RSI_buy[curr][-2], RSI_buy[curr][-1]]
            RSI_sell_value = [RSI_sell[curr][-2], RSI_sell[curr][-1]]
            axs[0].plot(time, selling_cost, color="c")
            axs[0].plot(time, purchase_cost, color='limegreen')
            axs[0].plot(time, avg_buy_value,'--', label='Average Buy Cost', color='b')
            axs[0].plot(time, avg_sell_value, '--', label='Average Sell Cost', color='darkgreen')
            axs[1].bar(time, volume_value, label='Volume values', color='slateblue')
            axs[1].set_xticks([])
            axs[2].plot(time, RSI_buy_value, label='RSI buy', color='coral' )
            axs[2].plot(time, RSI_sell_value, label='RSI sell', color='darkred')
        plt.pause(time_interval)


if __name__ == '__main__':
    try:
        list_currencies = ['BTC-PLN', 'LTC-PLN', 'TRX-PLN']
        time_interval = 2
        i = int(input('Podaj dla jakiej waluty wykres chcesz wyswietlic 0-BTC, 1-LTC, 2-TRX: '))
        qty = 10
        start = 0
        end = 10
        curr = list_currencies[i]
        draw_plot(time_interval, curr)
    except KeyboardInterrupt:
        print('User hit the interrupt key')
        sys.exit()
