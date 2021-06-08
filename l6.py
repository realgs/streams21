import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.ticker import MaxNLocator
from json import loads
from sys import exit


def read_new_lines_from_json(current_data):
    new_data = []
    with open('file.json', 'r') as file:
        all_data = [loads(line) for line in file]
    for i in range (len(current_data), len(all_data)):
        new_data.append(all_data[i])
    return new_data


def link(currency_type, type):
    if type == 'ticker':
        URL = f'https://bitbay.net/API/Public/{currency_type}/ticker.json'
    elif type == 'transactions':
        URL = f'https://api.bitbay.net/rest/trading/transactions/{currency_type}'
    return URL


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
    for i in range(len(list_)-1, -1, -3):
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
    fig, axs = plt.subplots(2, 3, figsize=(12, 8), constrained_layout=True)
    locator = MaxNLocator(nbins = 4)
    for i, currency_type in enumerate(CURRENCIES):
        plt.suptitle('Cryptocurrencies trading',fontsize=24)
        
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


def separate_tuples(list_of_tuples):
    amount, price_x_amount = 0, 0
    for element in list_of_tuples:
        amount += element[0]
        price_x_amount += element[0]*element[1]

    return amount, price_x_amount


def user_amount_and_profit(dict_, curr):
    print('user_amount_and_profit')
    buy, sell = [], []

    if dict_[curr]['buy'] == [] and dict_[curr]['sell'] == []:
        return 0,0,0

    for i in range(len(dict_[curr]['buy'])):
        buy.append(dict_[curr]['buy'][i])
    for i in range(len(dict_[curr]['sell'])):
        sell.append(dict_[curr]['sell'][i])

    profit = separate_tuples(sell)[1] - separate_tuples(buy)[1]

    buy_amount = separate_tuples(buy)[0]
    sell_amount = separate_tuples(sell)[0]  

    if buy_amount > sell_amount:
        while sell_amount > 0:
            for i in range(len(dict_[curr]['buy'])):

                if buy[i][0] <= sell_amount:
                    sell_amount -= buy[i][0]
                    buy[i] = (0, 0)
                if buy[i][0] > sell_amount:
                    buy[i] = (buy[i][0] - sell_amount, buy[i][1])
                    sell_amount = 0

        return separate_tuples(buy)[0], separate_tuples(buy)[1], profit #amount + profit+info
    
    elif buy_amount < sell_amount:
        print ("Nice try, you can't sell the currency, you don't have, \nEnd of your purchase")
        exit()
    
    return 0, 0, 0


def avg_list_of_tuples(list):
    if len(list) == 0:
        return 0
    sum_, amount = 0, 0
    for i in list:
        sum_ += i[0] * i[1]
        amount += i[0]
    return sum_/amount



def draw_plot(time_interval):   
    fig, axs = draw_axes()
    buy, sell, buy_list, sell_list, avg_buy_list, avg_sell_list, rsi_buy_list, rsi_sell_list, user_average_list = [], [], [], [], [], [], [], [], []
    cout1, cout2 = {}, {}
    i = 0
    user_data, current_time = [], []
    data = {} #bo w ang nie ma datas!
    while True:
        current_time = get_time(current_time)
        new_data =  read_new_lines_from_json(user_data)
        for element in new_data:
            user_data.append(element)
        
        for a, currency_type in enumerate(CURRENCIES):
            print(currency_type)
            if i == 0:
                data[currency_type] = {'sell': [], 'buy':[]}
                cout1[currency_type] = axs[1][a].text(0.0, 1.3, '', transform=axs[1][a].transAxes, fontsize=7)
                cout2[currency_type] = axs[1][a].text(0.0, 1.2, '', transform=axs[1][a].transAxes, fontsize=7)
            for element in new_data:
                if element['Currency'] == currency_type and element['Action'] == 'sell' :
                    data[currency_type]['sell'].append((element['Amount'], element['Price']))
                elif  element['Currency'] == currency_type and element['Action'] == 'buy':
                    data[currency_type]['buy'].append((element['Amount'], element['Price']))


            amount, div, profit = user_amount_and_profit(data, currency_type)
            if amount != 0:
                user_avg = div / amount
            else:
                user_avg = 0
            user_average_list.append(user_avg)
            dataset = get_data(currency_type)
            buy.append(dataset[0])
            sell.append(dataset[1])


            buy_, sell_ = get_data(currency_type)
            buy_list.append(buy_)
            sell_list.append(sell_)

            buy_avg = list_average(buy_list, elements_a)
            sell_avg = list_average(sell_list, elements_a)

            avg_buy_list.append(buy_avg)
            avg_sell_list.append(sell_avg)
            rsi_buy_list.append(RSI_value(buy_list, elements_r))
            rsi_sell_list.append(RSI_value(sell_list, elements_r))
                        

            if len(rsi_sell_list) >= 4:
                
                x = [current_time[-2].strftime("%H:%M:%S"), current_time[-1].strftime("%H:%M:%S")]

                selling_cost = [sell[-4], sell[-1]]
                purchase_cost = [buy[-4], buy[-1]]

                avg_buy_value = [avg_buy_list[-4], avg_buy_list[-1]]
                avg_sell_value = [avg_sell_list[-4], avg_sell_list[-1]]
                RSI_buy_value = [rsi_buy_list[-4], rsi_buy_list[-1]]
                RSI_sell_value = [rsi_sell_list[-4], rsi_sell_list[-1]]
                avg_user_sell_value = [abs(user_average_list[-4]), abs(user_average_list[-1])]
         
                axs[0][a].plot(x, selling_cost, label="Selling cost", color='red')
                axs[0][a].plot(x, purchase_cost, label="Purchase cost", color='yellow')
                axs[0][a].plot(x, avg_buy_value, '--', label='Average Buy Cost', color='darkred')
                axs[0][a].plot(x, avg_sell_value, '--', label='Average Sell Cost', color='#9B870C')
                axs[0][a].plot(x, avg_user_sell_value, label = 'Average User Price', color = 'limegreen')


                axs[1][a].plot(x, RSI_buy_value, label='RSI buy', color='lightgreen' )
                axs[1][a].plot(x, RSI_sell_value, label='RSI sell', color='darkgreen')

    
                if len(rsi_sell_list) == 6:
                    set_Legend(axs)

                cout1[currency_type].set_text(f'Actual profit : {profit}')
                cout2[currency_type].set_text(f'Actual amount : {amount}')

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
