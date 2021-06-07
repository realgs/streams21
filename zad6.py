import requests
import sys
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import json

def get_data(currency, p_currency):
    try:
        url_ticker = f"https://bitbay.net/API/Public/{currency}{p_currency}/ticker.json"
        url_transactions = f"https://api.bitbay.net/rest/trading/transactions/{currency}-{p_currency}"

        response = requests.get(url=url_ticker)
        response_json = response.json()

        bids = response_json['bid']
        asks = response_json['ask']

        fromtime = int((datetime.now() - timedelta(seconds=60)).timestamp()) * 1000
        params = {'fromTime': fromtime}
        response_val = requests.get(url=url_transactions, params=params)
        response_val = eval(response_val.text)
        volume = sum([float(response_val['items'][i]['a']) for i in range(len(response_val['items']))])

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

    return rsi


def trend_type_classification(rsi):
    last_rsi = rsi[-1]

    if last_rsi >= 70:
        return "Uptrend"
    elif last_rsi <= 30:
        return "Downtrend "
    elif last_rsi == 0:
        return "Probability of uptrend reversal"
    elif last_rsi == 100:
        return "Probability of downtrend reversal"
    else:
        return "Neutral trend"


def plot_data(currencies, p_currency, k, o, p, X, Y, S):
    bid = []
    ask = []
    vol = []
    bid_avg = []
    ask_avg = []
    bid_rsi = []
    ask_rsi = []
    times = []
    my_resources = []
    my_res = [["BTC", 0], ["ETH", 0], ["LSK", 0]]
    plt.subplots(nrows=len(currencies), ncols=3, figsize=(20, 8))
    plt.tight_layout
    while True:
        b = []
        input_bid_v = []
        a = []
        input_ask_v = []
        v = []
        input_ask_vo = []
        b_avg = []
        a_avg = []
        a_rsi = []
        b_rsi = []
        trends = []
        #file_bids = open("my_bids.txt", "a")
        # file_asks = open("my_asks.txt", "a")

        for currency in currencies:
            b_to_avg = []
            a_to_avg = []
            bids, asks, volume = get_data(currency, p_currency)

            input_bid_currency = input(f"Czy sprzedajesz walute {currency}? t/n")

            if input_bid_currency == "t":
                input_bid_val = float(input("Podaj cenę po jakiej sprzedales walutę"))
                input_bid_vol = float(input("Podaj ilosc sprzedanej waluty"))
                my_res[currencies.index(currency)][1] -= input_bid_vol
                json_bids = {"currency": currency, "bid value": {input_bid_val}, "bid volume": input_bid_vol}
                with open("my_bids.txt", "a") as f:
                    json.dump(json_bids, f, ensure_ascii=False)


            else:
                input_bid_val = None
                input_bid_vol = None

            input_ask_currency = input(f"Czy kupujesz walute {currency}? t/n")

            if input_ask_currency == "t":
                input_ask_val = float(input("Podaj cenę po jakiej kupiles walutę"))
                input_ask_vol = float(input("Podaj ilosc kupionej waluty"))
                my_res[currencies.index(currency)][1] += input_ask_vol

                json_asks = {"currency": currency, "ask value": input_ask_val, "ask volume": input_ask_vol}
                with open("my_asks.txt", "a") as f:
                    json.dump(json_asks, f, ensure_ascii=False)


            else:
                input_ask_val = None
                input_ask_vol = None

            if input_bid_val is not None:
                if float(input_bid_val) >= bids:
                    b.append([currency, input_bid_val])
                else:
                    b.append([currency, bids])
            else:
                b.append([currency, bids])

            if input_ask_val is not None:
                if float(input_ask_val) >= asks:
                    a.append([currency, input_ask_val])
                else:
                    a.append([currency, asks])
            else:
                a.append([currency, asks])


            if input_ask_vol is not None:
                v.append([currency, volume + float(input_ask_vol)])

            else:
                v.append([currency, volume])

            if len(bid) <= 1:
                b_avg.append([currency, bids])
                a_avg.append([currency, asks])

                b_rsi.append([currency, rsi_calc([bids], p)])
                a_rsi.append([currency, rsi_calc([asks], p)])

                trends.append([currency, trend_type_classification([b_rsi[currencies.index(currency)][1]])])
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

                trends.append([currency, trend_type_classification([b_rsi[currencies.index(currency)][1]])])

        bid.append(b)
        ask.append(a)
        vol.append(v)

        bid_avg.append(b_avg)
        ask_avg.append(a_avg)

        bid_rsi.append(b_rsi)
        ask_rsi.append(a_rsi)
        my_resources.append(my_res)
        times.append(datetime.now().strftime("%H:%M:%S"))

        plot(currencies, bid, ask, vol, times, k, bid_avg, ask_avg, bid_rsi, ask_rsi, o, trends, X, Y, S, my_resources)


def plot(currencies, bid, ask, vol, times, k, bid_avg, ask_avg, bid_rsi, ask_rsi, o, trends, X, Y, S, my_resources):

    vol_comp = []
    to_volataile = []

    for i in range(3):
        if trends[i][1] != "Downtrend":
            vol_comp.append(vol[-1][i][1])

    if len(vol_comp) != 0:
        max_vol = max(vol_comp)
        for i in range(3):
            if max_vol == vol[-1][i][1]:
                candidate = vol[-1][i][0]
                bids = bid[-Y:]
                for row2positions in range(len(bids)):
                    to_volataile.append(bids[row2positions][i][1])

                volatile_val = (abs(max(to_volataile) - min(to_volataile)) / max(to_volataile)) * 100

                bid_tospread = bid[-1][i][1]
                ask_tospread = ask[-1][i][1]
                spread = ((ask_tospread - bid_tospread) / ask_tospread) * 100

                if volatile_val > X:
                    plt.suptitle(f"Current candidate {candidate} | Volatile asset.")
                else:
                    plt.suptitle(f"Current candidate {candidate}.| Not volatile asset.")

                if spread < S:
                    plt.suptitle(f"Current candidate {candidate}.| Liquid asset.")
                else:
                    plt.suptitle(f"Current candidate {candidate}.| Not liquid asset.")

    else:
        plt.suptitle(f"No candidate.")

    row1positions = 1
    row2positions = 4
    row3positions = 7

    for p in range(len(currencies)):

        y1 = []
        y2 = []
        y_vol = []
        y_my_vol = []
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
        for y_my in my_resources:
            y_my_vol.append(y_my[p][1])

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

        l = max(0, len(x)-5)
        r = (len(x))
        plt.tight_layout()
        plt.subplot(len(currencies), 3, row1positions)

        plt.plot(x, y1, "-", label=f"Bids of {currencies[p]}", color="#1f77b4")
        plt.plot(x, y2, "-", label=f"Asks of {currencies[p]}", color="#9467bd")

        plt.plot(x_bid_avg, y_bid_avg, "--", label=f"Avg of last \n {o} {currencies[p]} bids", color="#FFD700")
        plt.plot(x_ask_avg, y_ask_avg, "--", label=f"Avg of last \n {o} {currencies[p]} asks", color="#7BC8F6")


        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize=8)
        plt.xticks(ticks=x, labels=times, rotation=50)
        plt.xlabel("Time")
        plt.ylabel(f"Bids, asks [PLN]")
        plt.xlim(left=l, right=r)
        row1positions += 1

        plt.subplot(len(currencies), 3, row2positions)
        plt.xlabel("Time")
        plt.ylabel(f"Volume")
        plt.bar(x_vol, y_vol, label=f"Volume of \n {currencies[p]}")
        plt.plot(x_vol, y_my_vol, label=f"Volume of my \n {currencies[p]} resources.", color="pink")
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize=8)
        plt.xticks(ticks=x_vol, labels=times, rotation=50)
        plt.xlim(left=max(0, len(x_vol)-5), right=len(x_vol))
        row2positions += 1

        plt.subplot(len(currencies), 3, row3positions)

        plt.plot(x_bid_rsi, y_bid_rsi, "-", label=f"RSI bids of {currencies[p]}", color="#1f77b4")
        plt.plot(x_ask_rsi, y_ask_rsi, "--", label=f"RSI asks of {currencies[p]}", color="#9467bd")

        plt.title(f"{trend_type_classification(y_bid_rsi)} {round(y_bid_rsi[-1], 2)}")

        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize=8)
        plt.xticks(ticks=x, labels=times, rotation=50)
        plt.xlabel("Time")
        plt.ylabel("RSI")
        plt.xlim(left=l, right=r)
        row3positions += 1

    plt.tight_layout()
    plt.pause(k)
    plt.clf()


def main():
    currencies = ['BTC', 'ETH', 'LSK']
    p_currency = 'PLN'
    k = 0.5

    o = 10 #do średniej
    p = 10 #do rsi

    X = 60 #procent wahania do zmienności
    Y = 10 #ilosc ostatnich probek
    S = 5 #różnica miedzy ofertami kupna/sprzedazy w % do płynności
    plot_data(currencies, p_currency, k, o, p, X, Y, S)


if __name__ == '__main__':
    main()