from requests import get
import matplotlib.pyplot as plt
import sys
import requests


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
    URL = f"https://api.bitbay.net/rest/trading/transactions/{curr}"
    response = requests.get(URL)
    response = eval(response.text)
    volumen = float(response['items'][1]['a'])
    return volumen



def add_values(buy, sell, volume):
    data = get_values(curr)
    buy.append(data[0])
    sell.append(data[1])
    value_volume = get_volumen(curr)
    volume.append(value_volume)
    return buy, sell, volume


def calculate_averange(data_list):
    interval_data = data_list[-qty:]
    avg = sum(interval_data) / len(interval_data)
    return avg


def calculate_RSI(data_list):
    interval_data = data_list[-20:]
    part_data = interval_data[start:end]
    rises = 0
    rises_count = 0
    losses = 0
    losses_count = 0
    for i in range(1, len(part_data)):
        if part_data[i - 1] < part_data[i]:
            rise = part_data[i] - part_data[i - 1]
            rises += rise
            rises_count += 1
        elif part_data[i - 1] > part_data[i]:
            loss = part_data[i - 1] - part_data[i]
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


def add_avgRSI(buy_list, sell_list, avg_buy_list, avg_sell_list, RSI_buy_list, RSI_sell_list):
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


def draw_axes():
    fig, axs = plt.subplots(3, 1, figsize=(12, 5), constrained_layout=True)
    axs[0].set_title(curr)
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Value')
    axs[1].set_title('Volume')
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Value')
    axs[2].set_title('RSI')
    axs[2].set_xlabel('Time')
    axs[2].set_ylabel('Value')
    return fig, axs


def draw_plot(time_interval):
    fig, axs = draw_axes()
    buy, sell, volume, values_buy, values_sell, buy_list, sell_list, avg_buy_list, avg_sell_list, volumen_list, rsi_buy_list, rsi_sell_list = [], [], [], [], [], [], [], [], [], [], [], []
    iterator = 0
    while True:
        add_values(buy, sell, volume)
        avg_buy, avg_sell, buy_RSI, sell_RSI = add_avgRSI(buy_list, sell_list, avg_buy_list, avg_sell_list, rsi_buy_list, rsi_sell_list)
        if len(buy) and len(sell) and len(buy_RSI) and len(sell_RSI) == 2:
            time = [(iterator - 1) * time_interval, iterator * time_interval]
            selling_cost = [sell[-2], sell[-1]]
            purchase_cost = [buy[-2], buy[-1]]
            volume_value = [volume[-2], volume[-1]]
            avg_buy_value = [avg_buy[-2], avg_buy[-1]]
            avg_sell_value = [avg_sell[-2], avg_sell[-1]]
            RSI_buy_value = [buy_RSI[-2], buy_RSI[-1]]
            RSI_sell_value = [sell_RSI[-2], sell_RSI[-1]]
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
        elif len(buy) and len(sell) and len(buy_RSI) and len(sell_RSI) > 2:
            time = [(iterator - 1) * time_interval, iterator * time_interval]
            selling_cost = [sell[-2], sell[-1]]
            purchase_cost = [buy[-2], buy[-1]]
            volume_value = [volume[-2], volume[-1]]
            avg_buy_value = [avg_buy[-2], avg_buy[-1]]
            avg_sell_value = [avg_sell[-2], avg_sell[-1]]
            RSI_buy_value = [buy_RSI[-2], buy_RSI[-1]]
            RSI_sell_value = [sell_RSI[-2], sell_RSI[-1]]
            axs[0].plot(time, selling_cost, color="c")
            axs[0].plot(time, purchase_cost, color='limegreen')
            axs[0].plot(time, avg_buy_value,'--', label='Average Buy Cost', color='b')
            axs[0].plot(time, avg_sell_value, '--', label='Average Sell Cost', color='darkgreen')
            axs[1].bar(time, volume_value, label='Volume values', color='slateblue')
            axs[1].set_xticks([])
            axs[2].plot(time, RSI_buy_value, label='RSI buy', color='coral' )
            axs[2].plot(time, RSI_sell_value, label='RSI sell', color='darkred')

        iterator += 1
        plt.pause(time_interval)


if __name__ == '__main__':
    try:
        list_currencies = ['BTC-PLN', 'LTC-PLN', 'TRX-PLN']
        time_interval = 5
        i = int(input('Podaj dla jakiej waluty wykres chcesz wyswietlic 0-BTC, 1-LTC, 2-TRX: '))
        qty = int(input('Ilość próbek do wyliczenia średniej: '))
        start = int(input('Początek przedziału y do wyliczenia RSI: '))
        end = int(input('Koniec przedziału y do wyliczenia RSI (maksymalnie 20): '))
        curr = list_currencies[i]
        draw_plot(time_interval)
    except KeyboardInterrupt:
        print('User hit the interrupt key')
        sys.exit()
