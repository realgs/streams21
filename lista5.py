import random
import requests
from datetime import datetime, timedelta
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


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


def get_volumen(currency):
    time_int = int((datetime.now() - timedelta(seconds=60)).timestamp()) * 1000
    url = f"https://api.bitbay.net/rest/trading/transactions/{currency}"
    params = {'fromTime': time_int}
    response = requests.request("GET", url, params=params)
    response = eval(response.text)
    return sum([float(response['items'][i]['a']) for i in range(len(response['items']))])


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
            volume = get_volumen(currency)
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
    return sum / len(filtered)


def calculate_RSI(RSI_range, values, currency, values_index):
    filtered = list(filter(lambda v: v[0] >= datetime.now() - timedelta(seconds=RSI_range), values[currency]))
    if len(filtered) < 2:
        return 0
    ups = 0
    downs = 0
    ups_counter = 0
    downs_counter = 0
    for i in range(len(filtered) - 1):
        if filtered[i][values_index] <= filtered[i + 1][values_index]:
            up = filtered[i + 1][values_index] - filtered[i][values_index]
            ups += up
            ups_counter += 1
        elif filtered[i][values_index] > filtered[i + 1][values_index]:
            down = filtered[i][values_index] - filtered[i + 1][values_index]
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


def classify_rsi_trend(rsi, currency):
    def get_average_of(rsi_type):
        values = []
        counted_values = 0
        while counted_values < 4 and counted_values < len(rsi[currency][rsi_type]):
            counted_values += 1
            values.append(rsi[currency][rsi_type][-counted_values])

        avg = sum(values) / len(values) if len(values) > 0 else 0
        return avg, values

    def get_trend_of(avg, values):
        if (len(values) != 0 and avg == values[-1]) or len(values) == 0:
            return 'Sideways trend'
        elif avg > values[-1]:
            return 'Upward trend'
        else:
            return 'Downward trend'

    avg_sell, sell_values = get_average_of('sell')
    avg_purchase, purchase_values = get_average_of('purchase')

    return {'sell': get_trend_of(avg_sell, sell_values),
            'purchase': get_trend_of(avg_purchase, purchase_values)}


def is_volatile(values, currency, X, Y):
    if len(values[currency]) < Y+1:
        return ""
    purchase_val = [values[currency][-y][2] for y in range(1, Y+1)]
    value = (abs(max(purchase_val)-min(purchase_val)) / max(purchase_val)) * 100
    if value > X:
        return 'Volatile asset'
    else:
        return ''


def is_liquid(values, currency, S):
    sell = values[currency][-1][1]
    purchase = values[currency][-1][2]
    diff = (abs(sell - purchase) / max(sell, purchase)) * 100
    if diff < S:
        return 'Liquid asset'
    return ''


def draw_plot(currency_list, time_interval, n_last_seconds, X, Y, S):
    last_average = gen_empty_dict(currency_list)
    RSI = gen_empty_dict(currency_list)
    cur_num = len(currency_list)
    values = gen_empty_list(currency_list)
    fig1, axs1 = plt.subplots(3, 1, figsize=(12, 10), tight_layout=True)
    fig2, axs2 = plt.subplots(2, 3, figsize=(12, 10), tight_layout=True)
    trend_texts = []
    for i in range(cur_num):
        axs1[i].set_title(currency_list[i])
        axs1[i].set_xlabel('time')
        axs1[i].set_ylabel('value')
        trend_texts.append(axs1[i].text(0, 0, ''))
        axs2[0][i].set_title(currency_list[i])
        axs2[0][i].set_xlabel('time')
        axs2[0][i].set_ylabel('value')
        axs2[1][i].set_title(currency_list[i])
        axs2[1][i].set_xlabel('time')
        axs2[1][i].set_ylabel('value')

        locator1 = MaxNLocator(nbins=8)
        locator2 = MaxNLocator(nbins=4)
        axs1[i].xaxis.set_major_locator(locator1)
        axs2[0][i].xaxis.set_major_locator(locator2)
        axs2[1][i].xaxis.set_major_locator(locator2)

    while True:
        update_data(values)
        curr_trends = {}
        curr_volumens = {}
        for n in range(cur_num):
            def process_values(currency):
                time = [values[currency_list[n]][-2][0].strftime("%H:%M:%S"),
                        values[currency_list[n]][-1][0].strftime("%H:%M:%S")]
                sell = [values[currency_list[n]][-2][1], values[currency_list[n]][-1][1]]
                purchase = [values[currency_list[n]][-2][2], values[currency_list[n]][-1][2]]
                volume = [values[currency_list[n]][-2][3], values[currency_list[n]][-1][3]]
                if len(last_average) >= 2:
                    average_sell_cost = [last_average[currency]['sell'][-2], last_average[currency]['sell'][-1]]
                    average_purchase_cost = [last_average[currency]['purchase'][-2],
                                             last_average[currency]['purchase'][-1]]
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
            trends = classify_rsi_trend(RSI, currency_list[n])
            curr_trends[currency_list[n]] = trends['sell']
            curr_volumens[currency_list[n]] = values[currency_list[n]][-1][3]
            volatile = is_volatile(values, currency_list[n], X, Y)
            liquid = is_liquid(values, currency_list[n], S)

            if len(values[currency_list[n]]) == 2:

                time, sell, purchase, volume, average_sell, average_purchase, rsi_sell, rsi_purchase = process_values(
                    currency_list[n])
                axs2[0][n].plot(time, sell, label="Selling cost", color='lime')
                axs2[0][n].plot(time, purchase, label="Purchase cost", color='m')
                axs2[1][n].bar(time, volume, label="Volume", color='blue')
                axs2[0][n].plot(time, average_sell, label='Average sell', color='yellow')
                axs2[0][n].plot(time, average_purchase, label='Average purchase', color='black')
                axs1[n].plot(time, rsi_sell, label='RSI sell', color='pink')
                axs1[n].plot(time, rsi_purchase, label='RSI purchase', color='orange')
                axs1[n].legend(loc='upper right')
                axs2[0][n].legend(loc='upper right')
                axs2[1][n].legend(loc='upper right')

                trend_texts[n].set_text('Sell - {}\nPurchase - {}{}{}'.format(
                    trends['sell'],
                    trends['purchase'],
                    "\n{}".format(volatile) if volatile != "" else "",
                    "\n{}".format(liquid) if liquid != "" else ""))
                pos_y = min(min(RSI[currency_list[n]]['sell']), min(RSI[currency_list[n]]['purchase']))
                trend_texts[n].set_position((0, pos_y))

            elif len(values[currency_list[n]]) > 2:
                time, sell, purchase, volume, average_sell, average_purchase, rsi_sell, rsi_purchase = process_values(
                    currency_list[n])
                axs2[0][n].plot(time, sell, color='lime')
                axs2[0][n].plot(time, purchase, color='m')
                axs2[1][n].bar(time, volume, color='blue')
                axs2[0][n].plot(time, average_sell, color='yellow')
                axs2[0][n].plot(time, average_purchase, color='black')
                axs1[n].plot(time, rsi_sell, color='pink')
                axs1[n].plot(time, rsi_purchase, color='orange')
                axs1[n].legend(loc='upper right')
                axs2[0][n].legend(loc='upper right')
                axs2[1][n].legend(loc='upper right')
                trend_texts[n].set_text('Sell - {}\nPurchase - {}{}{}'.format(
                    trends['sell'],
                    trends['purchase'],
                    "\n{}".format(volatile) if volatile != "" else "",
                    "\n{}".format(liquid) if liquid != "" else ""))
                pos_y = min(min(RSI[currency_list[n]]['sell']), min(RSI[currency_list[n]]['purchase']))
                trend_texts[n].set_position((0, pos_y))

            if n == 2:
                potential_candidates = \
                    list(filter(lambda k: curr_trends[k] in ['Upward trend', 'Sideways trend'], curr_trends.keys()))
                best_candidate = None
                if len(potential_candidates) == 1:
                    best_candidate = potential_candidates[0]
                elif len(potential_candidates) > 1:
                    max_volumen = max(curr_volumens.values())
                    best_candidate = list(filter(lambda k: curr_volumens[k] == max_volumen, curr_volumens.keys()))[0]

                for i in range(cur_num):
                    axs2[1][i].spines['bottom'].set_color('0.0')
                    axs2[1][i].spines['top'].set_color('0.0')
                    axs2[1][i].spines['right'].set_color('0.0')
                    axs2[1][i].spines['left'].set_color('0.0')

                if best_candidate is not None:
                    candidate_index = currency_list.index(best_candidate)
                    axs2[1][candidate_index].spines['bottom'].set_color('red')
                    axs2[1][candidate_index].spines['top'].set_color('red')
                    axs2[1][candidate_index].spines['right'].set_color('red')
                    axs2[1][candidate_index].spines['left'].set_color('red')

        if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1] != "test"):
            plt.pause(time_interval)
        else:
            plt.pause(1)


if __name__ == '__main__':
    currency_list = ['LTC-PLN', 'LSK-PLN', 'BTC-PLN']
    time_interval = 2
    retry_stat_code_err = 10
    retry_connect_err = 10
    X = 5
    Y = 3
    S = 5
    n_last_seconds = int(input('Podaj sekundy: '))
    RSI_range = int(input('Podaj zakres do RSI: '))
    draw_plot(currency_list, time_interval, n_last_seconds, X, Y, S)
