import requests
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime
import json
from tkinter import *
import threading
from tkinter import messagebox

crypto = ["BTC", "LTC", "ETH"]
curr = "PLN"


def path(currency):
    url = f"https://bitbay.net/API/Public/{currency}/ticker.json"
    return url


def get_transactions(crypto, curr):
    url = f"https://api.bitbay.net/rest/trading/transactions/{crypto}-{curr}"
    response = requests.request("GET", url)
    transactions = json.loads(response.text)
    if transactions["status"] == "Ok":
        return transactions
    else:
        print("Failed to connect, try again")


def get_last_rate(crypto, curr):
    transactions = get_transactions(crypto, curr)
    rate = []
    for key in transactions["items"]:
        key["a"] = float(key["a"])
        rate.append(key["a"])
    return rate[-1]


def RSI(rate):
    increase = []
    decrease = []
    for i in range(1, len(rate)):
        if rate[i - 1] <= rate[i]:
            increase.append(abs(rate[i - 1] - rate[i]))
        else:
            decrease.append(abs(rate[i - 1] - rate[i]))

    if len(increase) >= 1 and len(decrease) >= 1:
        increase_m = sum(increase) / len(increase)
        decrease_m = sum(decrease) / len(decrease)
        RS = increase_m / decrease_m
        RSI_r = 100 - (100 / (1 + RS))
        return RSI_r
    else:
        return 0


def x_val_limit(x_val):
    if len(x_val) >= 10:
        x = int(len(x_val) // 10)
        x_val = x_val[::x + 1]
    return x_val


def get_volume24(crypto, curr):
    transactions = get_transactions(crypto, curr)
    volume = []
    for key in transactions["items"]:
        key["r"] = float(key["r"])
        volume.append(key["r"])
    volume24h = sum(volume)
    return volume24h


def get_period_volume(vol_plot, vol_l):
    for i in range(1, len(vol_l)):
        if vol_l[i - 1] <= vol_l[i]:
            vol_plot[i] = 0
        else:
            vol_plot[i] = vol_l[i - 1] - vol_l[i]
    return vol_plot


def get_minute_volume(vol_plot, vol_l):
    volume = get_period_volume(vol_plot, vol_l)
    volume = volume[-12:]
    volume_sum = sum(volume)
    return volume_sum


def count_mean(bid, ask, samples):
    bid = bid[-samples:]
    ask = ask[-samples:]
    if len(bid) >= 1 and len(ask) >= 1:
        bid_mean = sum(bid) / len(bid)
        ask_mean = sum(ask) / len(ask)
        return [bid_mean, ask_mean]
    else:
        return [0, 0]


def connect_and_check(currency):
    req = requests.get(path(currency))
    if req.status_code == 200:
        json = req.json()
        bid_and_ask = [json["bid"], json["ask"]]
        return bid_and_ask
    else:
        print("Failed to connect, try again")
        sys.exit()


def RSI_trends(rate):
    x = RSI(rate)
    if x == 0:
        return "Probability of a reversal to a upward trend"
    if x <= 50:
        return "Time to buy!"
    if x > 50:
        return "Time to sell!"
    if x == 100:
        return "Probability of a reversal to a downward trend"


def candidate(v_BTC, v_LTC, v_ETH, RSI_BTC_trend, RSI_LTC_trend, RSI_ETH_trend):
    max_v = []
    if RSI_BTC_trend == "Time to sell!":
        max_v.append(v_BTC)
    if RSI_LTC_trend == "Time to sell!":
        max_v.append(v_LTC)
    if RSI_ETH_trend == "Time to sell!":
        max_v.append(v_ETH)
    if len(max_v) > 0:
        maximum = max(max_v)
        if maximum == v_BTC:
            return 'BTC is the best candidate'
        if maximum == v_LTC:
            return 'LTC is the best candidate'
        if maximum == v_ETH:
            return 'ETH is the best candidate'
    else:
        return "Neither of the currencies is in a downward trend "


def fluctuations(crypto, curr, X, Y):
    samples = get_transactions(crypto, curr)
    values = []
    for key in samples["items"]:
        key["a"] = float(key["a"])
        key["r"] = float(key["r"])
        values.append(key["a"] * key["r"])

    values = values[-Y:]
    minimum = min(values)
    maximum = max(values)
    diff = abs((maximum - minimum) / maximum) * 100
    diff = round(diff, 2)
    if diff > X:
        return f'{diff}%', "Yes"
    else:
        return f'{diff}%', "No"


def spread(crypto, curr, S):
    samples = get_transactions(crypto, curr)
    buy = []
    sell = []
    for key in samples["items"]:
        key["a"] = float(key["a"])
        if key["ty"] == "Buy":
            buy.append(key["a"])
        if key["ty"] == "Sell":
            sell.append(key["a"])
    if len(buy) > 0 and len(sell) > 0:
        buy = buy[-1]
        sell = sell[-1]
        diff = 1 - ((sell - buy) / sell)
        diff = round(diff, 2)
        if diff < S:
            return f'{diff}%', "Yes"
        else:
            return f'{diff}%', "No"


def save_app_data():
    file1 = entry_file.get()
    cryptocurr = v.get()
    type1 = v1.get()
    amount = int(entry_amount.get())
    price = int(entry_price.get())

    bs_dict = [cryptocurr, amount, price, type1]

    with open(f'{file1}.txt', 'a') as outfile:
        outfile.write(str(bs_dict) + ";")

    message_box()


def reading_from_file():
    file1 = entry_file.get()
    with open(f'{file1}.txt', 'r') as json_file:
        x = json_file.read()
        x = x[:-1]
        x = x.split(";")

    bs_list = []
    for i in x:
        i = i[1:]
        i = i[:-1]
        j = i.split(", ")
        bs_list.append(j)

    return bs_list


def mean_help(buy_sell, amount, buy, values):
    profit = 0
    for i in buy_sell:
        if i[2] == "'Buy'":
            amount += i[0]
            buy.append(i)
        if i[2] == "'Sell'" and amount >= i[0]:
            profit = i[0] * i[1]
            amount -= i[0]
            for j in range(len(buy)):
                if buy[j][0] >= i[0]:
                    profit -= (i[0] * buy[j][1])
                    buy[j][0] -= i[0]
                    break
                else:
                    profit -= (buy[j][0] * buy[j][1])
                    i[0] -= buy[j][0]
                    buy[j][0] = 0

    #print(buy_sell)
    #print(profit)

    for i in range(len(buy) - 1, -1, -1):
        if buy[i][0] == 0:
            buy.pop(i)

    for i in buy:
        values.append(i[0] * i[1])

    if len(values) == 0:
        mean = 0
    else:
        mean = sum(values) / len(values)
    return mean, profit


def mean_bs_price():
    bs_list = reading_from_file()

    bs_BTC = []
    bs_LTC = []
    bs_ETH = []

    amount_BTC = 0
    amount_LTC = 0
    amount_ETH = 0

    buy_BTC = []
    buy_LTC = []
    buy_ETH = []

    values_BTC = []
    values_LTC = []
    values_ETH = []

    for i in bs_list:
        if i[0] == "'BTC'":
            bs_BTC.append([int(i[1]), int(i[2]), i[3]])
        if i[0] == "'LTC'":
            bs_LTC.append([int(i[1]), int(i[2]), i[3]])
        if i[0] == "'ETH'":
            bs_ETH.append([int(i[1]), int(i[2]), i[3]])

    mean_BTC, profit_BTC = mean_help(bs_BTC, amount_BTC, buy_BTC, values_BTC)
    mean_LTC, profit_LTC = mean_help(bs_LTC, amount_LTC, buy_LTC, values_LTC)
    mean_ETH, profit_ETH = mean_help(bs_ETH, amount_ETH, buy_ETH, values_ETH)

    return mean_BTC, mean_LTC, mean_ETH, profit_BTC, profit_LTC, profit_ETH


def message_box():
    amount = entry_amount.get()
    price = entry_price.get()
    cryptocurr = v.get()
    type1 = v1.get()

    if type1 == "Buy":
        messagebox.showinfo('Status', f'You have bought {amount} units of {cryptocurr} for {price} PLN')
    if type1 == "Sell":
        messagebox.showinfo('Status', f'You have sold {amount} units of {cryptocurr} for {price} PLN')


def buy_sell_app():
    global label_file, entry_file, label_crypto, rb_BTC, rb_LTC, rb_ETH, label_amount, label_price, entry_amount, entry_price, button_buy, button_sell, v, v1, v_e
    window = Tk()
    window.configure(background='#4A4747')
    window.title('Buy & Sell')
    window.geometry("300x670")
    label_file = Label(window, text='File', font=('Calibri', 17), fg='white')
    label_file.place(x=10, y=15)
    label_file.configure(background='#4A4747')

    v_e = StringVar(window, value="Data")
    entry_file = Entry(window, font=('Calibri', 17), fg='white', textvariable=v_e)
    entry_file.configure(background='#6B6969', width=23)
    entry_file.place(x=10, y=60)

    label_crypto = Label(window, text='Cryptocurrency', font=('Calibri', 17), fg='white')
    label_crypto.place(x=10, y=365)
    label_crypto.configure(background='#4A4747')

    cryptocurrencies = ["BTC", "LTC", "ETH"]
    v = StringVar(window)
    options = OptionMenu(window, v, *cryptocurrencies)
    v.set("-")
    options.config(width=32, background='#6B6969', font=('Calibri', 17), fg='white')
    options.place(x=10, y=400)
    options.configure(background='#6B6969', width=20)

    label_amount = Label(window, text='Amount', font=('Calibri', 17), fg='white')
    label_amount.place(x=10, y=130)
    label_amount.configure(background='#4A4747')

    entry_amount = Entry(window, font=('Calibri', 17), fg='white')
    entry_amount.configure(background='#6B6969', width=23)
    entry_amount.place(x=10, y=175)

    label_price = Label(window, text='Price', font=('Calibri', 17), fg='white')
    label_price.place(x=10, y=245)
    label_price.configure(background='#4A4747')

    entry_price = Entry(window, font=('Calibri', 17), fg='white')
    entry_price.configure(background='#6B6969', width=23)
    entry_price.place(x=10, y=290)

    label_transaction = Label(window, text='Type of transaction', font=('Calibri', 17), fg='white')
    label_transaction.place(x=10, y=475)
    label_transaction.configure(background='#4A4747')

    type_of = ["Buy", "Sell"]
    v1 = StringVar(window)
    options1 = OptionMenu(window, v1, *type_of)
    v1.set("-")
    options1.config(width=32, background='#6B6969', font=('Calibri', 17), fg='white')
    options1.place(x=10, y=520)
    options1.configure(background='#6B6969', width=20)

    button_confirm = Button(window, text='Confirm', font=('Calibri', 17), fg='white', command=save_app_data)
    button_confirm.configure(background='#4A4747')
    button_confirm.config(width=23)
    button_confirm.place(x=8, y=610)

    window.mainloop()


def animated_plot(i):
    time = datetime.datetime.now()
    x_val.append(time.strftime('%H:%M:%S'))
    x_value = x_val_limit(x_val)
    bid_and_ask_BTC = connect_and_check(f'{crypto[0]}{curr}')
    bid_y_val_BTC.append(bid_and_ask_BTC[0])
    ask_y_val_BTC.append(bid_and_ask_BTC[1])

    bid_and_ask_LTC = connect_and_check(f'{crypto[1]}{curr}')
    bid_y_val_LTC.append(bid_and_ask_LTC[0])
    ask_y_val_LTC.append(bid_and_ask_LTC[1])

    bid_and_ask_DASH = connect_and_check(f'{crypto[2]}{curr}')
    bid_y_val_ETH.append(bid_and_ask_DASH[0])
    ask_y_val_ETH.append(bid_and_ask_DASH[1])

    mean_bid_BTC = count_mean(bid_y_val_BTC, ask_y_val_BTC, samples)[0]
    mean_ask_BTC = count_mean(ask_y_val_BTC, ask_y_val_BTC, samples)[1]

    mean_bid_BTC_l.append(mean_bid_BTC)
    mean_ask_BTC_l.append(mean_ask_BTC)

    mean_bid_LTC = count_mean(bid_y_val_LTC, ask_y_val_LTC, samples)[0]
    mean_ask_LTC = count_mean(ask_y_val_LTC, ask_y_val_LTC, samples)[1]

    mean_bid_LTC_l.append(mean_bid_LTC)
    mean_ask_LTC_l.append(mean_ask_LTC)

    mean_bid_ETH = count_mean(bid_y_val_ETH, ask_y_val_ETH, samples)[0]
    mean_ask_ETH = count_mean(ask_y_val_ETH, ask_y_val_ETH, samples)[1]

    mean_bid_ETH_l.append(mean_bid_ETH)
    mean_ask_ETH_l.append(mean_ask_ETH)

    flu_BTC = fluctuations(crypto[0], curr, Y, X)
    flu_LTC = fluctuations(crypto[1], curr, Y, X)
    flu_ETH = fluctuations(crypto[2], curr, Y, X)

    spr_BTC = spread(crypto[0], curr, S)
    spr_LTC = spread(crypto[1], curr, S)
    spr_ETH = spread(crypto[2], curr, S)

    volume_BTC = get_volume24(crypto[0], curr)
    vol_BTC_l.append(volume_BTC)
    vol_BTC_plot.append(0)
    v_BTC = get_period_volume(vol_BTC_plot, vol_BTC_l)
    vol_BTC_minute = get_minute_volume(vol_BTC_plot, vol_BTC_l)

    volume_LTC = get_volume24(crypto[1], curr)
    vol_LTC_l.append(volume_LTC)
    vol_LTC_plot.append(0)
    v_LTC = get_period_volume(vol_LTC_plot, vol_LTC_l)
    vol_LTC_minute = get_minute_volume(vol_LTC_plot, vol_LTC_l)

    volume_ETH = get_volume24(crypto[2], curr)
    vol_ETH_l.append(volume_ETH)
    vol_ETH_plot.append(0)
    v_ETH = get_period_volume(vol_ETH_plot, vol_ETH_l)
    vol_ETH_minute = get_minute_volume(vol_ETH_plot, vol_ETH_l)

    rate_BTC = get_last_rate(crypto[0], curr)
    rate_BTC_l.append(rate_BTC)
    RSI_BTC = RSI(rate_BTC_l)
    RSI_BTC_l.append(RSI_BTC)
    RSI_BTC_trend = RSI_trends(rate_BTC_l)

    rate_LTC = get_last_rate(crypto[1], curr)
    rate_LTC_l.append(rate_LTC)
    RSI_LTC = RSI(rate_LTC_l)
    RSI_LTC_l.append(RSI_LTC)
    RSI_LTC_trend = RSI_trends(rate_LTC_l)

    rate_ETH = get_last_rate(crypto[2], curr)
    rate_ETH_l.append(rate_ETH)
    RSI_ETH = RSI(rate_ETH_l)
    RSI_ETH_l.append(RSI_ETH)
    RSI_ETH_trend = RSI_trends(rate_ETH_l)

    best_candidate = candidate(vol_BTC_minute, vol_LTC_minute, vol_ETH_minute, RSI_BTC_trend, RSI_LTC_trend,
                               RSI_ETH_trend)
    mean_BTC, mean_LTC, mean_ETH, profit_BTC, profit_LTC, profit_ETH = mean_bs_price()

    plt.clf()
    ax = fig.subplots(3, 3)

    ax[0, 0].cla()
    ax[0, 0].plot(x_val, bid_y_val_BTC, label='Bid BTC', color='k')
    ax[0, 0].plot(x_val, ask_y_val_BTC, label='Ask BTC', color='r')
    ax[0, 0].plot(x_val, mean_bid_BTC_l, label='Mean bid BTC', ls='--', color='y')
    ax[0, 0].plot(x_val, mean_ask_BTC_l, label='Mean ask BTC', ls='--', color='g')
    ax[0, 0].set_xticks(x_value)
    ax[0, 0].legend(loc='upper right')
    ax[0, 0].set_xlabel(f'Time \n')
    ax[0, 0].set_ylabel('Value')
    ax[0, 0].set_xticklabels(x_value, rotation=45)
    ax[0, 0].text(0.87, 1.05, f'Profit: {profit_BTC}', horizontalalignment='center',
                  verticalalignment='center', transform=ax[0, 0].transAxes)
    if best_candidate == 'BTC is the best candidate':
        ax[0, 0].set_title(f'Bid and ask BTC \n Volatile: {flu_BTC}, Spread: {spr_BTC}')
    else:
        ax[0, 0].set_title(f'Bid and ask BTC \n')

    ax2 = ax[0, 0].twinx()
    ax2.axhline(mean_BTC, color='blue', linestyle='dashdot')
    ax2.set_ylabel("Mean Buy/Sell")

    ax[0, 1].cla()
    ax[0, 1].plot(x_val, bid_y_val_LTC, label='Bid LTC', color='k')
    ax[0, 1].plot(x_val, ask_y_val_LTC, label='Ask LTC', color='r')
    ax[0, 1].plot(mean_bid_LTC_l, label='Mean bid LTC', ls='--', color='y')
    ax[0, 1].plot(mean_ask_LTC_l, label='Mean ask LTC', ls='--', color='g')
    ax[0, 1].set_xticks(x_value)
    ax[0, 1].legend(loc='upper right')
    ax[0, 1].set_xlabel(f'Time \n')
    ax[0, 1].set_ylabel('Value')
    ax[0, 1].set_xticklabels(x_value, rotation=45)
    ax[0, 1].text(0.87, 1.05, f'Profit: {profit_LTC}', horizontalalignment='center',
                  verticalalignment='center', transform=ax[0, 1].transAxes)
    if best_candidate == 'LTC is the best candidate':
        ax[0, 1].set_title(f'Bid and ask LTC \n Volatile: {flu_LTC}, Spread: {spr_LTC}')
    else:
        ax[0, 1].set_title(f'Bid and ask LTC \n')

    ax21 = ax[0, 1].twinx()
    ax21.axhline(mean_LTC, color='blue', linestyle='dashdot')
    ax21.set_ylabel("Mean Buy/Sell")

    ax[0, 2].cla()
    ax[0, 2].plot(x_val, bid_y_val_ETH, label='Bid ETH', color='k')
    ax[0, 2].plot(x_val, ask_y_val_ETH, label='Ask ETH', color='r')
    ax[0, 2].plot(mean_bid_ETH_l, label='Mean bid ETH', ls='--', color='y')
    ax[0, 2].plot(mean_ask_ETH_l, label='Mean ask ETH', ls='--', color='g')
    ax[0, 2].set_xticks(x_value)
    ax[0, 2].legend(loc='upper right')
    ax[0, 2].set_xlabel('Time')
    ax[0, 2].set_ylabel('Value')
    ax[0, 2].set_xticklabels(x_value, rotation=45)
    ax[0, 2].text(0.87, 1.05, f'Profit: {profit_ETH}', horizontalalignment='center',
                  verticalalignment='center', transform=ax[0, 2].transAxes)
    if best_candidate == 'ETH is the best candidate':
        ax[0, 2].set_title(f'Bid and ask ETH \n Volatile: {flu_ETH}, Spread: {spr_ETH}')
    else:
        ax[0, 2].set_title(f'Bid and ask ETH \n')

    ax22 = ax[0, 2].twinx()
    ax22.axhline(mean_ETH, color='blue', linestyle='dashdot')
    ax22.set_ylabel("Mean Buy/Sell")

    ax[1, 0].cla()
    ax[1, 0].bar(x_val, v_BTC, label='Volume BTC', color='k')
    ax[1, 0].set_xticks(x_value)
    ax[1, 0].set_xticklabels(x_value, rotation=45)
    ax[1, 0].legend(loc='upper right')
    ax[1, 0].set_xlabel('Time')
    ax[1, 0].set_ylabel('Volume')
    ax[1, 0].set_title("Volume BTC")
    ax[1, 0].text(0.3, 0.96, f'Volume from one minute: {round(vol_BTC_minute, 6)}', horizontalalignment='center',
                  verticalalignment='center', transform=ax[1, 0].transAxes)

    ax[1, 1].cla()
    ax[1, 1].bar(x_val, v_LTC, label='Volume LTC', color='k')
    ax[1, 1].set_xticks(x_value)
    ax[1, 1].set_xticklabels(x_value, rotation=45)
    ax[1, 1].legend(loc='upper right')
    ax[1, 1].set_xlabel('Time')
    ax[1, 1].set_ylabel('Volume')
    ax[1, 1].set_title("Volume LTC")
    ax[1, 1].text(0.3, 0.96, f'Volume from one minute: {round(vol_LTC_minute, 6)}', horizontalalignment='center',
                  verticalalignment='center', transform=ax[1, 1].transAxes)

    ax[1, 2].cla()
    ax[1, 2].bar(x_val, v_ETH, label='Volume ETH', color='k')
    ax[1, 2].set_xticks(x_value)
    ax[1, 2].set_xticklabels(x_value, rotation=45)
    ax[1, 2].legend(loc='upper right')
    ax[1, 2].set_xlabel('Time')
    ax[1, 2].set_ylabel('Volume')
    ax[1, 2].set_title("Volume ETH")
    ax[1, 2].text(0.3, 0.96, f'Volume from one minute: {round(vol_ETH_minute, 6)}', horizontalalignment='center',
                  verticalalignment='center', transform=ax[1, 2].transAxes)

    ax[2, 0].cla()
    ax[2, 0].plot(x_val, RSI_BTC_l, label='RSI BTC', color='k')
    ax[2, 0].set_xticks(x_value)
    ax[2, 0].set_xticklabels(x_value, rotation=45)
    ax[2, 0].legend(loc='upper right')
    ax[2, 0].set_xlabel('Time')
    ax[2, 0].set_ylabel('RSI')
    ax[2, 0].set_title("RSI BTC")
    ax[2, 0].set_ylim(0, 100)
    ax[2, 0].text(0.35, 0.96, f'Type of trend RSI: {RSI_BTC_trend}', horizontalalignment='center',
                  verticalalignment='center', transform=ax[2, 0].transAxes)

    ax[2, 1].cla()
    ax[2, 1].plot(x_val, RSI_LTC_l, label='RSI LTC', color='k')
    ax[2, 1].set_xticks(x_value)
    ax[2, 1].set_xticklabels(x_value, rotation=45)
    ax[2, 1].legend(loc='upper right')
    ax[2, 1].set_xlabel(f'Time \n \n {best_candidate}')
    ax[2, 1].set_ylabel('RSI')
    ax[2, 1].set_title("RSI LTC")
    ax[2, 1].set_ylim(0, 100)
    ax[2, 1].text(0.35, 0.96, f'Type of trend RSI: {RSI_LTC_trend}', horizontalalignment='center',
                  verticalalignment='center', transform=ax[2, 1].transAxes)

    ax[2, 2].cla()
    ax[2, 2].plot(x_val, RSI_ETH_l, label='RSI ETH', color='k')
    ax[2, 2].set_xticks(x_value)
    ax[2, 2].set_xticklabels(x_value, rotation=45)
    ax[2, 2].legend(loc='upper right')
    ax[2, 2].set_xlabel('Time')
    ax[2, 2].set_ylabel('RSI')
    ax[2, 2].set_title("RSI ETH")
    ax[2, 2].set_ylim(0, 100)
    ax[2, 2].text(0.35, 0.96, f'Type of trend RSI: {RSI_ETH_trend}', horizontalalignment='center',
                  verticalalignment='center', transform=ax[2, 2].transAxes)

    fig.tight_layout()


if __name__ == '__main__':
    x_val = []
    bid_y_val_BTC = []
    ask_y_val_BTC = []
    mean_bid_BTC_l = []
    mean_ask_BTC_l = []

    bid_y_val_LTC = []
    ask_y_val_LTC = []
    mean_bid_LTC_l = []
    mean_ask_LTC_l = []

    bid_y_val_ETH = []
    ask_y_val_ETH = []
    mean_bid_ETH_l = []
    mean_ask_ETH_l = []

    vol_BTC = []
    vol_BTC_plot = []
    vol_BTC_l = []

    vol_LTC = []
    vol_LTC_plot = []
    vol_LTC_l = []

    vol_ETH = []
    vol_ETH_plot = []
    vol_ETH_l = []

    rate_BTC_l = []
    rate_LTC_l = []
    rate_ETH_l = []

    RSI_BTC_l = []
    RSI_LTC_l = []
    RSI_ETH_l = []

    samples = 12  # int(input("Input amount of samples to count mean: "))
    samples_rsi = 12  # int(input("Input amount of samples to count RSI: "))
    X = 5
    Y = 10
    S = 5
    fig = plt.figure(figsize=(23, 10))
    ani = FuncAnimation(fig, animated_plot, interval=5000)
    b_thread = threading.Thread(target=buy_sell_app).start()

    plt.show()

