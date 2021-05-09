import requests
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime
import json

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

    ax[0, 0].cla()
    ax[0, 0].plot(x_val, bid_y_val_BTC, label='Bid BTC', color='k')
    ax[0, 0].plot(x_val, ask_y_val_BTC, label='Ask BTC', color='r')
    ax[0, 0].plot(x_val, mean_bid_BTC_l, label='Mean bid BTC', ls='--', color='y')
    ax[0, 0].plot(x_val, mean_ask_BTC_l, label='Mean ask BTC', ls='--', color='g')
    ax[0, 0].set_xticks(x_value)
    ax[0, 0].legend(loc='upper right')
    ax[0, 0].set_xlabel('Time')
    ax[0, 0].set_ylabel('Value')
    ax[0, 0].set_xticklabels(x_value, rotation=45)
    ax[0, 0].set_title("Bid and ask BTC")

    ax[0, 1].cla()
    ax[0, 1].plot(x_val, bid_y_val_LTC, label='Bid LTC', color='k')
    ax[0, 1].plot(x_val, ask_y_val_LTC, label='Ask LTC', color='r')
    ax[0, 1].plot(mean_bid_LTC_l, label='Mean bid LTC', ls='--', color='y')
    ax[0, 1].plot(mean_ask_LTC_l, label='Mean ask LTC', ls='--', color='g')
    ax[0, 1].set_xticks(x_value)
    ax[0, 1].legend(loc='upper right')
    ax[0, 1].set_xlabel('Time')
    ax[0, 1].set_ylabel('Value')
    ax[0, 1].set_xticklabels(x_value, rotation=45)
    ax[0, 1].set_title("Bid and ask LTC")

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
    ax[0, 2].set_title("Bid and ask ETH")

    if vol_rsi == "Volume":
        volume_BTC = get_volume24(crypto[0], curr)
        vol_BTC_l.append(volume_BTC)
        vol_BTC_plot.append(0)
        v_BTC = get_period_volume(vol_BTC_plot, vol_BTC_l)
        vol_BTC_minute = get_minute_volume(vol_BTC_plot, vol_BTC_l)

        ax[1, 0].cla()
        ax[1, 0].bar(x_val, v_BTC, label='Volume BTC', color='k')
        ax[1, 0].set_xticks(x_value)
        ax[1, 0].set_xticklabels(x_value, rotation=45)
        ax[1, 0].legend(loc='upper right')
        ax[1, 0].set_xlabel('Time')
        ax[1, 0].set_ylabel('Volume')
        ax[1, 0].set_title("Volume BTC")
        ax[1, 0].text(0.3, 0.97, f'Volume from one minute: {round(vol_BTC_minute, 6)}', horizontalalignment='center',
                      verticalalignment='center', transform=ax[1, 0].transAxes)

        volume_LTC = get_volume24(crypto[1], curr)
        vol_LTC_l.append(volume_LTC)
        vol_LTC_plot.append(0)
        v_LTC = get_period_volume(vol_LTC_plot, vol_LTC_l)
        vol_LTC_minute = get_minute_volume(vol_LTC_plot, vol_LTC_l)

        ax[1, 1].cla()
        ax[1, 1].bar(x_val, v_LTC, label='Volume LTC', color='k')
        ax[1, 1].set_xticks(x_value)
        ax[1, 1].set_xticklabels(x_value, rotation=45)
        ax[1, 1].legend(loc='upper right')
        ax[1, 1].set_xlabel('Time')
        ax[1, 1].set_ylabel('Volume')
        ax[1, 1].set_title("Volume LTC")
        ax[1, 1].text(0.3, 0.97, f'Volume from one minute: {round(vol_LTC_minute, 6)}', horizontalalignment='center',
                      verticalalignment='center', transform=ax[1, 1].transAxes)

        volume_ETH = get_volume24(crypto[2], curr)
        vol_ETH_l.append(volume_ETH)
        vol_ETH_plot.append(0)
        v_ETH = get_period_volume(vol_ETH_plot, vol_ETH_l)
        vol_ETH_minute = get_minute_volume(vol_ETH_plot, vol_ETH_l)

        ax[1, 2].cla()
        ax[1, 2].bar(x_val, v_ETH, label='Volume ETH', color='k')
        ax[1, 2].set_xticks(x_value)
        ax[1, 2].set_xticklabels(x_value, rotation=45)
        ax[1, 2].legend(loc='upper right')
        ax[1, 2].set_xlabel('Time')
        ax[1, 2].set_ylabel('Volume')
        ax[1, 2].set_title("Volume ETH")
        ax[1, 2].text(0.3, 0.97, f'Volume from one minute: {round(vol_ETH_minute, 6)}', horizontalalignment='center',
                      verticalalignment='center', transform=ax[1, 2].transAxes)

    if vol_rsi == "RSI":
        rate_BTC = get_last_rate(crypto[0], curr)
        rate_BTC_l.append(rate_BTC)
        RSI_BTC = RSI(rate_BTC_l)
        RSI_BTC_l.append(RSI_BTC)

        ax[1, 0].cla()
        ax[1, 0].plot(x_val, RSI_BTC_l, label='RSI BTC', color='k')
        ax[1, 0].set_xticks(x_value)
        ax[1, 0].set_xticklabels(x_value, rotation=45)
        ax[1, 0].legend(loc='upper right')
        ax[1, 0].set_xlabel('Time')
        ax[1, 0].set_ylabel('RSI')
        ax[1, 0].set_title("RSI BTC")
        ax[1, 0].set_ylim(0, 100)

        rate_LTC = get_last_rate(crypto[1], curr)
        rate_LTC_l.append(rate_LTC)
        RSI_LTC = RSI(rate_LTC_l)
        RSI_LTC_l.append(RSI_LTC)

        ax[1, 1].cla()
        ax[1, 1].plot(x_val, RSI_LTC_l, label='RSI LTC', color='k')
        ax[1, 1].set_xticks(x_value)
        ax[1, 1].set_xticklabels(x_value, rotation=45)
        ax[1, 1].legend(loc='upper right')
        ax[1, 1].set_xlabel('Time')
        ax[1, 1].set_ylabel('RSI')
        ax[1, 1].set_title("RSI LTC")
        ax[1, 1].set_ylim(0, 100)

        rate_ETH = get_last_rate(crypto[2], curr)
        rate_ETH_l.append(rate_ETH)
        RSI_ETH = RSI(rate_ETH_l)
        RSI_ETH_l.append(RSI_ETH)

        ax[1, 2].cla()
        ax[1, 2].plot(x_val, RSI_ETH_l, label='RSI ETH', color='k')
        ax[1, 2].set_xticks(x_value)
        ax[1, 2].set_xticklabels(x_value, rotation=45)
        ax[1, 2].legend(loc='upper right')
        ax[1, 2].set_xlabel('Time')
        ax[1, 2].set_ylabel('RSI')
        ax[1, 2].set_title("RSI ETH")
        ax[1, 2].set_ylim(0, 100)

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

    samples = int(input("Input amount of samples to count mean: "))
    vol_rsi = input("Volume or RSI: ")
    if vol_rsi == "RSI":
        samples_rsi = int(input("Input amount of samples to count RSI: "))

    fig, ax = plt.subplots(2, 3, figsize=(23, 10))
    ani = FuncAnimation(fig, animated_plot, interval=5000)

    plt.show()

