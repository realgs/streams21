import time
from threading import Thread

import numpy as np
import requests
from requests.exceptions import HTTPError
import matplotlib.pyplot as plt
from pynput.keyboard import Key, Listener


active_charts = [False] * 8
refresh = True
average_range = 5


def get_data(currency_l, url_l):
    try:
        response = requests.get(url=url_l + f'{currency_l}{"USD"}/{"trades"}.json')
        return response.json()
    except HTTPError:
        print('HTTP error:', HTTPError)
        return []


def import_values(currency_l, buy_prices_l, sell_prices_l, buy_prices_amount_l, sell_prices_amount_l, url_l, index_l):
    print(currency_l)

    new_data = []
    new_data += get_data(currency_l, url_l)

    if new_data:
        for data_row in new_data:
            if data_row["type"] == "buy":
                buy_prices_l[index_l].append(data_row["price"])
                buy_prices_amount_l[index_l].append(data_row["amount"])
            elif data_row["type"] == "sell":
                sell_prices_l[index_l].append(data_row["price"])
                sell_prices_amount_l[index_l].append(data_row["amount"])


def create_average(values, values_range, index_l):
    result = []

    for i in range(len(values[index_l])):
        local_average = 0
        for j in range(i - values_range // 2, i + 1 + values_range // 2):
            if j < 0:
                local_average += values[index_l][0]
            elif j > len(values[index_l]) - 1:
                local_average += values[index_l][len(values) - 1]
            else:
                local_average += values[index_l][j]
        result.append(local_average / values_range)
    return result


def create_rsi(values, values_range, index_l):
    result = []
    result_up = []
    result_down = []

    for i in range(len(values[index_l])):
        local_average_up = 0
        local_average_down = 0
        for j in range(i - values_range // 2, i + 1 + values_range // 2):
            if j < 1:
                local_average_up += values[index_l][0]
                local_average_down += values[index_l][0]
            elif j > len(values[index_l]) - 1:
                local_average_up += values[index_l][len(values) - 1]
                local_average_down += values[index_l][len(values) - 1]
            else:
                if values[index_l][j - 1] > values[index_l][j]:
                    local_average_down += values[index_l][j]
                else:
                    local_average_up += values[index_l][j]

            if local_average_up == 0:
                local_average_up = values[index_l][j]
            if local_average_down == 0:
                local_average_down = values[index_l][j]

        result_up.append(local_average_up / values_range)
        result_down.append(local_average_down / values_range)
        result.append(100 - (100 / (1 + (result_up[i] / result_down[i]))))
    return result


def draw_calculations_helper(buy_prices_l, sell_prices_l, buy_prices_amount_l, sell_prices_amount_l, index_l):
    values_amount = min(len(buy_prices_l[index_l]), len(sell_prices_l[index_l]))

    x = range(values_amount)
    y1_np = np.array(buy_prices_l[index_l])
    y2_np = np.array(sell_prices_l[index_l])
    y3_np = np.array(buy_prices_amount_l[index_l])
    y4_np = np.array(sell_prices_amount_l[index_l])
    global average_range
    y5_np = np.array(create_average(buy_prices_l[0:values_amount], average_range, index_l))
    y6_np = np.array(create_average(sell_prices_l[0:values_amount], average_range, index_l))
    y7_np = np.array(create_rsi(buy_prices_l[0:values_amount], average_range, index_l))
    y8_np = np.array(create_rsi(sell_prices_l[0:values_amount], average_range, index_l))
    # Buy price
    y1 = y1_np[0:values_amount]
    # Sell price
    y2 = y2_np[0:values_amount]
    # Buy amount
    y3 = y3_np[0:values_amount]
    # Sell amount
    y4 = y4_np[0:values_amount]
    # Buy average
    y5 = y5_np[0:values_amount]
    # Sell average
    y6 = y6_np[0:values_amount]
    # Buy based RSI
    y7 = y7_np[0:values_amount]
    # Sell based RSI
    y8 = y8_np[0:values_amount]

    return [x, y1, y2, y3, y4, y5, y6, y7, y8, values_amount]


def draw_constructor(currency_l, buy_prices_l, sell_prices_l, buy_prices_amount_l, sell_prices_amount_l, fig_l, line_l, ax_l, index_l):
    plot_parameters = draw_calculations_helper(buy_prices_l, sell_prices_l, buy_prices_amount_l, sell_prices_amount_l, index_l)

    ax_l.append(fig_l.add_subplot(3, 1, index_l + 1))
    ax_l[index_l].title.set_text("Values for " + currency_l)
    ax_l[index_l].set_xlabel("Operations (number)")
    ax_l[index_l].set_ylabel("Values ($) / (amount)")

    line_l.append([])
    line_l[index_l].append([])
    line_l[index_l].append([])
    line_l[index_l].append([])
    line_l[index_l].append([])
    line_l[index_l].append([])
    line_l[index_l].append([])
    line_l[index_l].append([])
    line_l[index_l].append([])
    line_l[index_l][0], = ax_l[index_l].plot(plot_parameters[0], plot_parameters[1], label="0. Buy price USD " + currency_l + " ($)")
    line_l[index_l][1], = ax_l[index_l].plot(plot_parameters[0], plot_parameters[2], label="1. Sell price USD " + currency_l + " ($)")
    line_l[index_l][2], = ax_l[index_l].plot(plot_parameters[0], plot_parameters[3], label="2. Buy orders (amount)")
    line_l[index_l][3], = ax_l[index_l].plot(plot_parameters[0], plot_parameters[4], label="3. Sell orders (amount)")
    line_l[index_l][4], = ax_l[index_l].plot(plot_parameters[0], plot_parameters[5], label="4. Buy average " + currency_l + " ($)")
    line_l[index_l][5], = ax_l[index_l].plot(plot_parameters[0], plot_parameters[6], label="5. Sell average " + currency_l + " ($)")
    line_l[index_l][6], = ax_l[index_l].plot(plot_parameters[0], plot_parameters[7], label="6. Buy based RSI (amount)")
    line_l[index_l][7], = ax_l[index_l].plot(plot_parameters[0], plot_parameters[8], label="7. Sell based RSI (amount)")

    ax_l[index_l].legend(loc="upper left")


def draw_values_refresh(buy_prices_l, sell_prices_l, buy_prices_amount_l, sell_prices_amount_l, line_l, ax_l, index_l):
    plot_parameters = draw_calculations_helper(buy_prices_l, sell_prices_l, buy_prices_amount_l, sell_prices_amount_l, index_l)

    for i in range(len(active_charts)):
        if active_charts[i]:
            line_l[index_l][i].set_xdata(plot_parameters[0])
            line_l[index_l][i].set_ydata(plot_parameters[i + 1])
        else:
            line_l[index_l][i].set_xdata([])
            line_l[index_l][i].set_ydata([])

    max_y = 1
    min_y = 10000
    for i in range(len(active_charts)):
        if active_charts[i]:
            if max_y < max(plot_parameters[i + 1]):
                max_y = max(plot_parameters[i + 1])

    for i in range(len(active_charts)):
        if active_charts[i]:
            if min_y > min(plot_parameters[i + 1]):
                min_y = min(plot_parameters[i + 1])

    max_y = max_y * 1.1
    min_y = min_y * 0.9
    ax_l[index_l].set_ylim(min_y, max_y)
    ax_l[index_l].set_xlim(0, plot_parameters[9])


def on_press(key):
    key_value = ord(key.char) - ord('0')
    if key_value in range(0, len(active_charts)):
        active_charts[key_value] = not(active_charts[key_value])
    global average_range
    if ord(key.char) == ord('-') and average_range > 4:
        average_range -= 2
    elif ord(key.char) == ord('+') and average_range < 20:
        average_range += 2

    global refresh
    refresh = True


def key_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    currencies = ["BTC", "LTC", "DASH"]
    buy_prices = [[], [], []]
    sell_prices = [[], [], []]
    buy_prices_amount = [[], [], []]
    sell_prices_amount = [[], [], []]
    URL = f'https://bitbay.net/API/Public/'

    plt.ion()
    fig = plt.figure()
    line = []
    ax = []

    thread = Thread(target=key_listener)
    thread.start()

    try:
        for currency in currencies:
            import_values(currency, buy_prices, sell_prices, buy_prices_amount, sell_prices_amount, URL, currencies.index(currency))
            draw_constructor(currency, buy_prices, sell_prices, buy_prices_amount, sell_prices_amount, fig, line, ax, currencies.index(currency))

        get_new_data = 0
        get_new_at = 3
        while True:
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.1)

            if get_new_data >= get_new_at:
                for currency in currencies:
                    import_values(currency, buy_prices, sell_prices, buy_prices_amount, sell_prices_amount, URL, currencies.index(currency))
                    draw_values_refresh(buy_prices, sell_prices, buy_prices_amount, sell_prices_amount, line, ax, currencies.index(currency))
                get_new_data = 0
            else:
                get_new_data += 0.1

            if refresh:
                for currency in currencies:
                    draw_values_refresh(buy_prices, sell_prices, buy_prices_amount, sell_prices_amount, line, ax, currencies.index(currency))
                refresh = False

    except KeyboardInterrupt:
        pass
