from requests import get
import matplotlib.pyplot as plt
import sys
import requests
from datetime import datetime, timedelta
from matplotlib.ticker import MaxNLocator


def connection(curr):
    return f'https://bitbay.net/API/Public/{curr}/ticker.json'


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


def add_values(curr, buy, sell, volume):
    data = get_values(curr)
    buy.append(data[0])
    sell.append(data[1])
    volume.append(get_volumen(curr))
    return  buy, sell, volume


def get_time(current_time):
    current_time.append(datetime.now())
    return current_time


def calculate_averange(data_list):
    interval_data = data_list[-qty:]
    avg = sum(interval_data) / len(interval_data)
    return avg


def calculate_RSI(data_list):
    interval_data = data_list[-20:]
    interval_data = interval_data[start:end]
    rises = 0
    rises_count = 0
    losses = 0
    losses_count = 0
    for i in range(1, len(interval_data)):
        if interval_data[i - 1] < interval_data[i]:
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


def add_avgRSI(curr, buy_list, sell_list, avg_buy_list, avg_sell_list, RSI_buy_list, RSI_sell_list):
    buy, sell = get_values(curr)
    buy_list.append(buy)
    sell_list.append(sell)
    buy_avg = calculate_averange(buy_list)
    sell_avg = calculate_averange(sell_list)
    avg_buy_list.append(buy_avg)
    avg_sell_list.append(sell_avg)
    RSI_buy_list.append(calculate_RSI(buy_list))
    RSI_sell_list.append(calculate_RSI(sell_list))
    return avg_buy_list, avg_sell_list, RSI_buy_list, RSI_sell_list


def check_trend(list):
    averange = calculate_averange(list)
    trend = list[-1]
    if averange > trend:
        return 'Upward trend'
    elif averange < trend:
        return 'Downward trend'
    else:
        return 'Sideways trend'



def choose_max_volumen(list_volumen0, list_volumen1, list_volumen2):
    list_of_volumen = []
    if check_trend(list_volumen0) != 'Decrease trend':
        list_of_volumen.append(list_volumen0[-1])
    else:
        list_of_volumen.append(0)
    if check_trend(list_volumen1) != 'Decrease trend':
        list_of_volumen.append(list_volumen1[-1])
    else:
        list_of_volumen.append(0)
    if check_trend(list_volumen2) != 'Decrease trend':
        list_of_volumen.append(list_volumen2[-1])
    else:
        list_of_volumen.append(0)
    max_volumen = max(list_of_volumen)
    index_max_volumen = list_of_volumen.index(max_volumen)
    if max_volumen == 0:
        return 'There is no candidate' , 3
    else:
        return 'Candidate', index_max_volumen


def check_voltaile(buy_list, X, Y):
    if len(buy_list) < Y:
        return '---'
    y_samples = buy_list[-Y:]
    oscilation = ((max(y_samples) - min(y_samples))/max(y_samples)) * 100
    if oscilation > X:
        return 'Volatile asset'
    else:
        return '---'


def check_liquid(buy_list, sell_list, S):
    difference = ((buy_list[-1] - sell_list[-1])/buy_list[-1]) * 100
    if difference < S:
        return 'Liquid asset'
    else:
        return '---'


def draw_axes():
    fig, axs = plt.subplots(3, 3, figsize=(20, 5), constrained_layout=True)
    locator = MaxNLocator(nbins=4)
    for n in range(3):
        axs[0, n].set_title(list_currencies[n])
        axs[0, n].set_xlabel('Time')
        axs[0, n].xaxis.set_major_locator(locator)
        axs[0, n].set_ylabel('Value')
        #axs[1,n].set_title('Volume')
        axs[1, n].set_xlabel('Time')
        axs[1, n].xaxis.set_major_locator(locator)
        axs[1, n].set_ylabel('Value')
        axs[2, n].set_xlabel('Time')
        axs[2, n].xaxis.set_major_locator(locator)
        axs[2, n].set_ylabel('Value')
    return fig, axs


def draw_plot(time_interval):
    fig, axs = draw_axes()
    buy0, sell0, volume0, values_buy0, values_sell0, buy_list0, sell_list0, avg_buy_list0, avg_sell_list0, volumen_list0, rsi_buy_list0, rsi_sell_list0 = [], [], [], [], [], [], [], [], [], [], [], []
    buy1, sell1, volume1, values_buy1, values_sell1, buy_list1, sell_list1, avg_buy_list1, avg_sell_list1, volumen_list1, rsi_buy_list1, rsi_sell_list1 = [], [], [], [], [], [], [], [], [], [], [], []
    buy2, sell2, volume2, values_buy2, values_sell2, buy_list2, sell_list2, avg_buy_list2, avg_sell_list2, volumen_list2, rsi_buy_list2, rsi_sell_list2 = [], [], [], [], [], [], [], [], [], [], [], []
    current_time = []
    while True:
        add_values(list_currencies[0], buy0, sell0, volume0)
        add_values(list_currencies[1], buy1, sell1, volume1)
        add_values(list_currencies[2], buy2, sell2, volume2)
        get_time(current_time)
        avg_buy0, avg_sell0, buy_RSI0, sell_RSI0 = add_avgRSI(list_currencies[0],buy_list0, sell_list0, avg_buy_list0, avg_sell_list0,
                                                              rsi_buy_list0, rsi_sell_list0)
        avg_buy1, avg_sell1, buy_RSI1, sell_RSI1 = add_avgRSI(list_currencies[1], buy_list1, sell_list1, avg_buy_list1,
                                                              avg_sell_list1,
                                                              rsi_buy_list1, rsi_sell_list1)
        avg_buy2, avg_sell2, buy_RSI2, sell_RSI2 = add_avgRSI(list_currencies[2], buy_list2, sell_list2, avg_buy_list2,
                                                              avg_sell_list2,
                                                              rsi_buy_list2, rsi_sell_list2)

        if len(buy0) and len(volume0) and len(sell0) and len(buy_RSI0) and len(sell_RSI0) and len(buy1) and len(sell1) and len(volume1) and len(buy_RSI1) and len(sell_RSI1) and len(buy2) and len(sell2) and len(volume2) and len(buy_RSI2) and len(sell_RSI2) == 2:
            time = [current_time[-2].strftime("%H:%M:%S"), current_time[-1].strftime("%H:%M:%S")]
            selling_cost0 = [sell0[-2], sell0[-1]]
            selling_cost1 = [sell1[-2], sell1[-1]]
            selling_cost2 = [sell2[-2], sell2[-1]]
            purchase_cost0 = [buy0[-2], buy0[-1]]
            purchase_cost1 = [buy1[-2], buy1[-1]]
            purchase_cost2 = [buy2[-2], buy2[-1]]
            volume_value0 = [volume0[-2], volume0[-1]]
            volume_value1 = [volume1[-2], volume1[-1]]
            volume_value2 = [volume2[-2], volume2[-1]]
            avg_buy_value0 = [avg_buy0[-2], avg_buy0[-1]]
            avg_buy_value1 = [avg_buy1[-2], avg_buy1[-1]]
            avg_buy_value2 = [avg_buy2[-2], avg_buy2[-1]]
            avg_sell_value0 = [avg_sell0[-2], avg_sell0[-1]]
            avg_sell_value1 = [avg_sell1[-2], avg_sell1[-1]]
            avg_sell_value2 = [avg_sell2[-2], avg_sell2[-1]]
            RSI_buy_value0 = [buy_RSI0[-2], buy_RSI0[-1]]
            RSI_buy_value1 = [buy_RSI1[-2], buy_RSI1[-1]]
            RSI_buy_value2 = [buy_RSI2[-2], buy_RSI2[-1]]
            RSI_sell_value0 = [sell_RSI0[-2], sell_RSI0[-1]]
            RSI_sell_value1 = [sell_RSI1[-2], sell_RSI1[-1]]
            RSI_sell_value2 = [sell_RSI2[-2], sell_RSI2[-1]]
            axs[0, 0].plot(time, selling_cost0, label="Selling cost", color='c')
            axs[0, 0].plot(time, purchase_cost0, label="Purchase cost", color='limegreen')
            axs[0, 0].plot(time, avg_buy_value0, '--', label='Average Buy Cost', color='b')
            axs[0, 0].plot(time, avg_sell_value0, '--', label='Average Sell Cost', color='darkgreen')
            axs[0, 1].plot(time, selling_cost1, label="Selling cost", color='c')
            axs[0, 1].plot(time, purchase_cost1, label="Purchase cost", color='limegreen')
            axs[0, 1].plot(time, avg_buy_value1, '--', label='Average Buy Cost', color='b')
            axs[0, 1].plot(time, avg_sell_value1, '--', label='Average Sell Cost', color='darkgreen')
            axs[0, 2].plot(time, selling_cost2, label="Selling cost", color='c')
            axs[0, 2].plot(time, purchase_cost2, label="Purchase cost", color='limegreen')
            axs[0, 2].plot(time, avg_buy_value2, '--', label='Average Buy Cost', color='b')
            axs[0, 2].plot(time, avg_sell_value2, '--', label='Average Sell Cost', color='darkgreen')
            axs[0, 2].legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
            axs[1, 0].bar(time, volume_value0, label='Volume values', color='slateblue')
            axs[1, 0].set_xticks([])
            axs[1, 1].bar(time, volume_value1, label='Volume values', color='slateblue')
            axs[1, 1].set_xticks([])
            axs[1, 2].bar(time, volume_value2, label='Volume values', color='slateblue')
            axs[1, 2].set_xticks([])
            axs[1, 2].legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
            axs[2, 0].plot(time, RSI_buy_value0, label='RSI buy', color='coral')
            axs[2, 0].set_title(f'RSI: {check_trend(rsi_buy_list0)} buy')
            axs[2, 0].plot(time, RSI_sell_value0, label='RSI sell', color='darkred')
            axs[2, 1].plot(time, RSI_buy_value1, label='RSI buy', color='coral')
            axs[2, 1].set_title(f'RSI: {check_trend(rsi_buy_list1)} buy')
            axs[2, 1].plot(time, RSI_sell_value1, label='RSI sell', color='darkred')
            axs[2, 2].plot(time, RSI_buy_value2, label='RSI buy', color='coral')
            axs[2, 2].set_title(f'RSI: {check_trend(rsi_buy_list2)} buy')
            axs[2, 2].plot(time, RSI_sell_value2, label='RSI sell', color='darkred')
            axs[2, 2].legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')


            volume_info = choose_max_volumen(volume0, volume1, volume2)
            if volume_info[1] == 0:
                text = []
                text.append(axs[1,0].text(0, 0, ''))
                voltaile_info = check_voltaile(buy_list0, X, Y)
                liquid_info = check_liquid(buy_list0, sell_list0, S)
                axs[1, 0].set_title(f'{volume_info[0]}')
                axs[1, 1].set_title('Volume')
                axs[1, 2].set_title('Volume')
                text[0].set_text(f'{voltaile_info}, {liquid_info}')
                position = min(buy_list0)
                text[0].set_position((0, position))
            elif volume_info[1] == 1:
                text = []
                text.append(axs[1,1].text(0,0,''))
                voltaile_info = check_voltaile(buy_list1, X, Y)
                liquid_info = check_liquid(buy_list1, sell_list1, S)
                axs[1, 1].set_title(f'{volume_info[0]}')
                axs[1, 0].set_title('Volume')
                axs[1, 2].set_title('Volume')
                text[0].set_text(f'{voltaile_info}, {liquid_info}')
                position = min(buy_list1)
                text[0].set_position((0, position))
            elif volume_info[1] == 2:
                text = []
                text.append(axs[1,2].text(0,0,''))
                voltaile_info = check_voltaile(buy_list1, X, Y)
                liquid_info = check_liquid(buy_list1, sell_list1, S)
                axs[1, 2].set_title(f'{volume_info[0]}')
                axs[1, 1].set_title('Volume')
                axs[1, 0].set_title('Volume')
                text[0].set_text(f'{voltaile_info}, {liquid_info}')
                position = min(buy_list2)
                text[0].set_position((0, position))
            else:
                axs[1,0].set_title(f'{volume_info[0]}')
                axs[1,1].set_title(f'{volume_info[0]}')
                axs[1,2].set_title(f'{volume_info[0]}')


        elif len(buy0) and len(volume0) and len(sell0) and len(buy_RSI0) and len(sell_RSI0) and len(buy1) and len(sell1) and len(volume1) and len(buy_RSI1) and len(sell_RSI1) and len(buy2) and len(sell2) and len(volume2) and len(buy_RSI2) and len(sell_RSI2) > 2:
            time = [current_time[-2].strftime("%H:%M:%S"), current_time[-1].strftime("%H:%M:%S")]
            selling_cost0 = [sell0[-2], sell0[-1]]
            purchase_cost0 = [buy0[-2], buy0[-1]]
            volume_value0 = [volume0[-2], volume0[-1]]
            avg_buy_value0 = [avg_buy0[-2], avg_buy0[-1]]
            avg_sell_value0 = [avg_sell0[-2], avg_sell0[-1]]
            RSI_buy_value0 = [buy_RSI0[-2], buy_RSI0[-1]]
            RSI_sell_value0 = [sell_RSI0[-2], sell_RSI0[-1]]
            axs[0, 0].plot(time, selling_cost0, color="c")
            axs[0, 0].plot(time, purchase_cost0, color='limegreen')
            axs[0, 0].plot(time, avg_buy_value0, '--', label='Average Buy Cost', color='b')
            axs[0, 0].plot(time, avg_sell_value0, '--', label='Average Sell Cost', color='darkgreen')
            axs[1, 0].bar(time, volume_value0, label='Volume values', color='slateblue')
            axs[1, 0].set_xticks([])
            axs[2, 0].plot(time, RSI_buy_value0, label='RSI buy', color='coral')
            axs[2, 0].set_title(f'RSI: {check_trend(rsi_buy_list0)} buy')
            axs[2, 0].plot(time, RSI_sell_value0, label='RSI sell', color='darkred')
            axs[0, 1].plot(time, selling_cost1, color="c")
            axs[0, 1].plot(time, purchase_cost1, color='limegreen')
            axs[0, 1].plot(time, avg_buy_value1, '--', label='Average Buy Cost', color='b')
            axs[0, 1].plot(time, avg_sell_value1, '--', label='Average Sell Cost', color='darkgreen')
            axs[1, 1].bar(time, volume_value1, label='Volume values', color='slateblue')
            axs[1, 1].set_xticks([])
            axs[2, 1].plot(time, RSI_buy_value1, label='RSI buy', color='coral')
            axs[2, 0].set_title(f'RSI: {check_trend(rsi_buy_list1)} buy')
            axs[2, 1].plot(time, RSI_sell_value1, label='RSI sell', color='darkred')
            axs[0, 2].plot(time, selling_cost2, color="c")
            axs[0, 2].plot(time, purchase_cost2, color='limegreen')
            axs[0, 2].plot(time, avg_buy_value2, '--', label='Average Buy Cost', color='b')
            axs[2, 0].set_title(f'RSI: {check_trend(rsi_buy_list2)} buy')
            axs[0, 2].plot(time, avg_sell_value2, '--', label='Average Sell Cost', color='darkgreen')
            axs[1, 2].bar(time, volume_value2, label='Volume values', color='slateblue')
            axs[1, 2].set_xticks([])
            axs[2, 2].plot(time, RSI_buy_value2, label='RSI buy', color='coral')
            axs[2, 2].plot(time, RSI_sell_value2, label='RSI sell', color='darkred')

            volume_info = choose_max_volumen(volume0, volume1, volume2)
            if volume_info[1] == 0:
                text = []
                text.append(axs[1, 0].text(0, 0, ''))
                voltaile_info = check_voltaile(buy_list0, X, Y)
                liquid_info = check_liquid(buy_list0, sell_list0, S)
                axs[1, 0].set_title(f'{volume_info[0]}')
                axs[1, 1].set_title('Volume')
                axs[1, 2].set_title('Volume')
                text[0].set_text(f'{voltaile_info}, {liquid_info}')
                position = min(buy_list0)
                text[0].set_position((0, position))
            elif volume_info[1] == 1:
                text = []
                text.append(axs[1, 1].text(0, 0, ''))
                voltaile_info = check_voltaile(buy_list1, X, Y)
                liquid_info = check_liquid(buy_list1, sell_list1, S)
                axs[1, 1].set_title(f'{volume_info[0]}')
                axs[1, 0].set_title('Volume')
                axs[1, 2].set_title('Volume')
                text[0].set_text(f'{voltaile_info}, {liquid_info}')
                position = min(buy_list1)
                text[0].set_position((0, position))
            elif volume_info[1] == 2:
                text = []
                text.append(axs[1, 2].text(0, 0, ''))
                voltaile_info = check_voltaile(buy_list1, X, Y)
                liquid_info = check_liquid(buy_list1, sell_list1, S)
                axs[1, 2].set_title(f'{volume_info[0]}')
                axs[1, 1].set_title('Volume')
                axs[1, 0].set_title('Volume')
                text[0].set_text(f'{voltaile_info}, {liquid_info}')
                position = min(buy_list2)
                text[0].set_position((0, position))
            else:
                axs[1, 0].set_title(f'{volume_info[0]}')
                axs[1, 1].set_title(f'{volume_info[0]}')
                axs[1, 2].set_title(f'{volume_info[0]}')

        plt.pause(time_interval)


if __name__ == '__main__':
    try:
        list_currencies = ['BTC-PLN', 'LTC-PLN', 'TRX-PLN']
        time_interval = 2
        qty = 10
        start = 0
        end = 10
        X = 5
        Y = 5
        S = 3
        draw_plot(time_interval)
    except KeyboardInterrupt:
        print('User hit the interrupt key')
        sys.exit()