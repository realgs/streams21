import requests
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as anim


def get_data(currency, p_currency):
    try:
        response = requests.get(f"https://bitbay.net/API/Public/{currency}{p_currency}/ticker.json")
        response_json = response.json()

        bids = response_json['bid']
        asks = response_json['ask']
        volume = response_json['volume']

        return bids, asks, volume

    except requests.exceptions.HTTPError:
        print("No connection to the server.")
        sys.exit()


def average(data, n):
    if len(data) >= n:
        avg_data = data[-n:]
        avg = sum(avg_data)/len(avg_data)
    else:
        avg = sum(data)/len(data)
    return avg


def rsi_calc(data, p):
    rsi_data = data[-p:]
    print(rsi_data)
    ups = 0
    up_count = 0
    downs = 0
    down_count = 0
    for i in range(1, len(rsi_data)):
        if rsi_data[i-1] < rsi_data[i]:
            up = rsi_data[i] - rsi_data[i-1]
            ups += up
            up_count += 1
        elif rsi_data[i-1] > rsi_data[i]:
            down = rsi_data[i-1] - rsi_data[i]
            downs += down
            down_count += 1

    if up_count == 0:
        a = 1
    else:
        a = ups/up_count
    if down_count == 0:
        b = 1
    else:
        b = downs/down_count
    if 1+(a/b) != 0:
        rsi = 100 - (100/(1+(a/b)))
    else:
        print("Division by zero!")
    print(rsi)
    return rsi


def plot_data(currencies, p_currency, k, o, p):
    bid = []
    ask = []
    vol = []
    bid_avg = []
    ask_avg = []
    bid_rsi = []
    ask_rsi = []

    times = []

    plt.subplots(nrows=len(currencies), ncols=2, figsize=(20, len(currencies) * 3.5))
    plt.tight_layout()
    while True:
        b = []
        a = []
        v = []
        b_avg = []
        a_avg = []
        a_rsi = []
        b_rsi = []
        for currency in currencies:
            b_to_avg = []
            a_to_avg = []
            bids, asks, volume = get_data(currency, p_currency)

            b.append([currency, bids])
            a.append([currency, asks])
            v.append([currency, volume])

            if len(bid) <= 1:
                b_avg.append([currency, bids])
                a_avg.append([currency, asks])

                b_rsi.append([currency, rsi_calc([bids], p)])
                a_rsi.append([currency, rsi_calc([asks], p)])
            else:
                for i in range(len(bid)):
                    b_to_avg.append(bid[i][currencies.index(currency)][1])
                    b_to_avg.append(bids)
                    a_to_avg.append(ask[i][currencies.index(currency)][1])
                    a_to_avg.append(asks)

                b_avg.append([currency, average(b_to_avg, o)])
                a_avg.append([currency, average(a_to_avg, o)])

                b_rsi.append([currency, rsi_calc(b_to_avg, p)])
                a_rsi.append([currency, rsi_calc(a_to_avg, p)])


        bid.append(b)
        ask.append(a)
        vol.append(v)

        bid_avg.append(b_avg)
        ask_avg.append(a_avg)

        bid_rsi.append(b_rsi)
        ask_rsi.append(a_rsi)

        times.append(datetime.now().strftime("%H:%M:%S"))

        plot(currencies, bid, ask, vol, times, k, bid_avg, ask_avg, bid_rsi, ask_rsi, o)


def plot(currencies, bid, ask, vol, times, k, bid_avg, ask_avg, bid_rsi, ask_rsi, o):
    s = 1
    n = 4
    t = 7
    for p in range(len(currencies)):
        y1 = []
        y2 = []
        y_vol = []
        y_bid_avg = []
        y_ask_avg = []
        y_bid_rsi = []
        y_ask_rsi = []

        for b in bid:
            y1.append(b[p][1])
        for a in ask:
            y2.append(a[p][1])
            x = [i for i in range(len(y1))]
        for v in vol:
            y_vol.append((v[p][1]))
            x_vol = [i for i in range(len(y_vol))]
        for b in bid_avg:
            y_bid_avg.append(b[p][1])
            x_bid_avg = [i for i in range(len(y_bid_avg))]
        for a in ask_avg:
            y_ask_avg.append(a[p][1])
            x_ask_avg = [i for i in range(len(y_ask_avg))]
        for b in bid_rsi:
            y_bid_rsi.append(b[p][1])
            x_bid_rsi = [i for i in range(len(y_bid_rsi))]
        for a in ask_rsi:
            y_ask_rsi.append(a[p][1])
            x_ask_rsi = [i for i in range(len(y_ask_rsi))]

        l = max(0, len(x)-9)
        r = (len(x))

        plt.subplot(len(currencies), 3, s)

        plt.plot(x, y1, "-", label=f"Bids of {currencies[p]}", color="#1f77b4")
        plt.plot(x, y2, "-", label=f"Asks of {currencies[p]}", color="#9467bd")

        plt.plot(x_bid_avg, y_bid_avg, "--", label=f"Avg of last {o} {currencies[p]} bids", color="#FFD700")
        plt.plot(x_ask_avg, y_ask_avg, "--", label=f"Avg of last {o} {currencies[p]} asks", color="#7BC8F6")

        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        # plt.legend()
        plt.xticks(ticks=x, labels=times, rotation=50)
        plt.xlabel("Time")
        plt.ylabel(f"Bids, asks [PLN]")
        plt.xlim(left=l, right=r)
        s += 1

        plt.subplot(len(currencies), 3, n)
        plt.xlabel("Time")
        plt.ylabel(f"Volume [PLN]")
        plt.bar(x_vol, y_vol, label=f"Volume of {currencies[p]}")
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.xticks(ticks=x_vol, labels=times, rotation=50)
        plt.xlim(left=max(0, len(x_vol)-9), right=len(x_vol))
        n += 1

        plt.subplot(len(currencies), 3, t)

        plt.plot(x_bid_rsi, y_bid_rsi, "-", label=f"RSI bids of {currencies[p]}", color="#1f77b4")
        plt.plot(x_ask_rsi, y_ask_rsi, "--", label=f"RSI asks of {currencies[p]}", color="#9467bd")

        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        # plt.legend()
        plt.xticks(ticks=x, labels=times, rotation=50)
        plt.xlabel("Time")
        plt.ylabel(f"RSI  [PLN]")
        plt.xlim(left=l, right=r)
        t += 1

    plt.tight_layout()
    plt.pause(k)
    plt.clf()

def main():
    currencies = ['BTC', 'ETH', 'LSK']
    p_currency = 'PLN'
    k = 0.5
    # n = int(input("Podaj z ilu ostatnich danych chcesz liczyć średnią: "))
    o = 6
    p = 10
    plot_data(currencies, p_currency, k, o, p)


if __name__ == '__main__':
    main()