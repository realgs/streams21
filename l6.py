import requests
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from sys import exit
from datetime import datetime, timedelta
from matplotlib.ticker import MaxNLocator
import json
# from visualise import read_new_lines_from_json

def read_new_lines_from_json(current_data):
    new_data = []
    with open('file.json', 'r') as file:
        all_data = [json.loads(line) for line in file]
        # print(all_data)
    for i in range (len(current_data), len(all_data)):
        new_data.append(all_data[i])
    return new_data

def link(currency_type, type):
    if type == 'ticker':
        return f'https://bitbay.net/API/Public/{currency_type}/ticker.json'
    if type == 'transactions':
        return f'https://api.bitbay.net/rest/trading/transactions/{currency_type}'

def get_data(currency_type):
    try:
        req = requests.get(link(currency_type, 'ticker'))
        req_json = req.json()
        bid = req_json['bid']
        ask = req_json['ask']
        print (req.status_code)
    except Exception as e:
        print(e)
        print (req.status_code)
        return {}

    return bid, ask


def get_time(current_time):
    current_time.append(datetime.now())
    return current_time


def list_average(list_, elements_a):
    clean = []
    for i in range(len(list_)-1, 0, -3):
        clean.append(list_[i])
    data = clean[-elements_a:]
    if len(data) == 0:
        return None
    return sum(data) / len(data)

def RSI_value(list_, elements_r):
    clean = []
    for i in range(len(list_)-1, 0, -3):
        clean.append(list_[i])
    data = clean[- elements_r:]
    up = 0
    up_c = 0
    down = 0
    down_c = 0
    for i in range(1, len(data)):
        if data[i - 1] < data[i]:
            up += data[i] - data[i - 1]
            up_c += 1
        elif data[i - 1] > data[i]:
            down+= data[i - 1] - data[i]
            down_c += 1
    if up_c == 0:
        a = 1
    else:
        a = up/up_c
    if down_c == 0:
        b = 1
    else:
        b = down/down_c
    rsi = 100 - (100 / (1 + (a / b)))
    return rsi

def draw_axes():
    fig, axs = plt.subplots(2, 3, figsize=(12, 5), constrained_layout=True)
    for i, currency_type in enumerate(CURRENCIES):
        plt.suptitle('Cryptocurrencies trading',fontsize=24)
        locator = MaxNLocator(nbins = 5)
        axs[0][i].set_title(currency_type)
        axs[0][i].set_xlabel('Time')
        axs[0][i].set_ylabel('Value')

        axs[1][i].set_title('RSI')
        axs[1][i].set_xlabel('Time')
        axs[1][i].set_ylabel('Value')
    
        axs[0][i].xaxis.set_major_locator(locator)
        axs[1][i].xaxis.set_major_locator(locator)
    return fig, axs


def set_Legend(axs):
    for i in range(2):
       axs[i][2].legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')


def user_average(dict_, curr):
    buy, sell = [], []
    for i in range(len(dict_[curr]['buy'])):
        buy.append(dict_[curr]['buy'][i])
    for i in range(len(dict_[curr]['sell'])):
        sell.append(dict_[curr]['sell'][i])
    sum_buy = 0
    sold = 0
    sum_ = 0
    for i in buy:
        sum_buy += i[0]

    for i in range(len(dict_[curr]['sell'])):
        if sell[i][0] <= sum_buy:
            sum_buy -= sell[i][0]
            sell[i] = (0, sell[i][1])
                
        else:
            sell[i] = (sell[i][0] - sum_buy, sell[i][1])
 
    for i in sell:
        # print('i[0]',i[0], 'i[1]',  i[1])
        sold += i[0] * i[1]
        sum_ += i[0]
   
    if sum_ == 0:
        sum_ = 1
    print ('sold / sum_', sold / sum_)
    return sold / sum_
    _
def avg_list_of_tuples(list):
    sum_, amount = 0, 0
    for i in list:
        sum_ += i[0] * i[1]
        amount += i[0]
    return sum_/amount

# def buy_user_avg(dict_, currency_type):
#     sum_buy, amount_buy = 0, 0

#     for element in dict_[currency_type]['buy']:
#         sum_buy += element[0] * element[1]
#         amount_buy += element[0]
#     return sum_buy/amount_buy

def draw_plot(time_interval):

    fig, axs = draw_axes()
    buy, sell, buy_list, sell_list, avg_buy_list, avg_sell_list, rsi_buy_list, rsi_sell_list, user_average_list = [], [], [], [], [], [], [], [], []
    i = 0
    # locator = MaxNLocator(nbins = 3)
    # current_time = []
    user_data = []
    datas = {}
    while True:
        new_data =  read_new_lines_from_json(user_data)
        for element in new_data:
            user_data.append(element)
        # print('i=', i, 'c=', currency_type, 'crfincr', user_data)

        for a, currency_type in enumerate(CURRENCIES):
            if i == 0:
                datas[currency_type] = {'sell': [], 'buy':[]}
            # print('c=', currency_type, 'i=', i, 'dict=', datas)
            for element in new_data:
                if element['Currency'] == currency_type and element['Action'] == 'sell' :
                    datas[currency_type]['sell'].append((element['Amount'], element['Price']))
                elif  element['Currency'] == currency_type and element['Action'] == 'buy':
                    datas[currency_type]['buy'].append((element['Amount'], element['Price']))


            user_avg = user_average(datas, currency_type)
            # user_average_list.append(user_avg)

            user_sell_avg = avg_list_of_tuples(datas[currency_type]['sell'])

            data = get_data(currency_type)
            buy.append(data[0])
            sell.append(data[1])


            buy_, sell_ = get_data(currency_type)
            buy_list.append(buy_)
            sell_list.append(sell_)

            buy_avg = list_average(buy_list, elements_a)
            sell_avg = list_average(sell_list, elements_a)

            avg_buy_list.append(buy_avg)
            avg_sell_list.append(sell_avg)
            rsi_buy_list.append(RSI_value(buy_list, elements_r))
            rsi_sell_list.append(RSI_value(sell_list, elements_r))
                        

            if len(buy) and len(sell) and len(rsi_buy_list) and len(rsi_sell_list) >= 4:
                
                # time = [time_list[-2].strftime("%H:%M:%S:"), time_list[-1].strftime("%H:%M:%S:")]
                x = [(i - 1) * time_interval, i * time_interval]
                selling_cost = [sell[-4], sell[-1]]
                purchase_cost = [buy[-4], buy[-1]]

                avg_buy_value = [avg_buy_list[-4], avg_buy_list[-1]]
                avg_sell_value = [avg_sell_list[-4], avg_sell_list[-1]]
                RSI_buy_value = [rsi_buy_list[-4], rsi_buy_list[-1]]
                RSI_sell_value = [rsi_sell_list[-4], rsi_sell_list[-1]]
                avg_user_sell_value = [user_sell_avg, user_sell_avg]
                # print(currency_type, user_average_list[-1], sell[-1])

                axs[0][a].plot(x, selling_cost, label="Selling cost", color='red')
                axs[0][a].plot(x, purchase_cost, label="Purchase cost", color='yellow')
                axs[0][a].plot(x, avg_buy_value, '--', label='Average Buy Cost', color='darkred')
                axs[0][a].plot(x, avg_sell_value, '--', label='Average Sell Cost', color='#9B870C')
                axs[0][a].plot(x, avg_user_sell_value, '--', label = 'Average User Sell Cost', color = 'green')



                axs[1][a].plot(x, RSI_buy_value, label='RSI buy', color='lightgreen' )
                axs[1][a].plot(x, RSI_sell_value, label='RSI sell', color='darkgreen')

                
                at2 = AnchoredText('User actual profit: ' + str(round(user_avg,2) ), loc='lower left', prop=dict(size=8), frameon=True, bbox_to_anchor=(0., 1.25), bbox_transform=axs[1][a].transAxes)
                at2.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
                axs[1][a].add_artist(at2)


                if len(buy) and len(sell) and len(rsi_buy_list) and len(rsi_sell_list) == 6:
                    set_Legend(axs)

                # if len(buy) and len(sell) and len(rsi_buy_list) and len(rsi_sell_list) >= 6:

                #     at2 = AnchoredText('User actual profit: ' + str(round(user_avg,2) ), loc='lower left', prop=dict(size=8), frameon=True, bbox_to_anchor=(0., 1.25), bbox_transform=axs[1][a].transAxes)
                #     at2.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
                #     axs[1][a].add_artist(at2)


        i += 1
        plt.pause(time_interval)

if __name__ == '__main__':
    SLEEPING_TIME = 5
    CURRENCIES = ['ETH-PLN', 'BTC-PLN', 'LTC-PLN']
    elements_a = 10
    elements_a_start = 10
    elements_a_stop = 15
    elements_r = 15

    X = 5
    Y = 5
    S = 3

    draw_plot(SLEEPING_TIME)