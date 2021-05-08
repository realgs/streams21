from matplotlib import ticker
import matplotlib.pyplot as plt
import requests
import time

base_currency = 'PLN'
url = 'https://bitbay.net/API/Public/'
post = '/trades.json'
time_interval = 1


def get_data(currency, post):
    try:
        r = requests.get(url+currency+base_currency+post)
        r.raise_for_status()
        return r.json()

    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def calculate_rsi(data, w):
    data = data[-w:]
    print(data)
    rise = 0
    r_count = 0
    loss = 0
    l_count = 0
    for i in range(1, len(data)):
        if data[i - 1] < data[i]:
            rise += data[i] - data[i - 1]
            r_count += 1
        elif data[i - 1] > data[i]:
            loss += data[i - 1] - data[i]
            l_count += 1
    if r_count == 0:
        a = 1
    else:
        a = rise / r_count
    if l_count == 0:
        b = 1
    else:
        b = loss / l_count
    rsi_value = 100 - (100 / (1 + (a / b)))

    return rsi_value


if __name__ == '__main__':
    currencies = ['OMG']
    n = len(currencies)
    w = 3

    price = {}
    volume = {}
    amount = {}
    mean = {}
    rsi = {}
    for currency in currencies:
        price[currency] = []
        volume[currency] = []
        amount[currency] = []
        mean[currency] = []
        rsi[currency] = []

    times = []
    t = 0

    plt.ion()
    figure, ax = plt.subplots(1, 2, figsize=(10, 5))

    figure.text(0.5, 0.04, 'time', ha='center', va='center')
    figure.tight_layout(pad=3.0)

    lines = []
    lines.append(ax[0].plot(times, price[currencies[0]], label="price")[0])
    lines.append(ax[0].plot(times, volume[currencies[0]], label="volume")[0])
    lines.append(ax[0].plot(times, mean[currencies[0]], label="mean")[0])
    lines.append(ax[0].plot(times, rsi[currencies[0]], label="rsi")[0])

    ax[0].legend()
    # ax[1].legend()
    #
    # ax[0].set_title(f'{currencies[0]+base_currency}')
    # ax[1].set_title('VOLUME')
    #
    # ax[0].xaxis.set_major_formatter('{x} s')
    # ax[1].xaxis.set_major_formatter('{x} s')

    while True:
        r = get_data(currencies[0], post)
        print(len(r))
        for i in range(len(r)):
            price[currencies[0]].append(r[i]['price'])
            amount[currencies[0]].append(r[i]['amount'])
            t += 1
            times.append(t)

            if len(price[currencies[0]]) >= w:
                sum_amount = 0
                sum_price = 0
                for j in range(1, w+1):
                    sum_amount += amount[currencies[0]][-j]
                    sum_price += price[currencies[0]][-j]

                volume[currencies[0]].append(sum_amount)
                mean[currencies[0]].append(sum_price/w)
                rsi[currencies[0]].append(calculate_rsi(price[currencies[0]], w))
            else:
                volume[currencies[0]].append(0)
                mean[currencies[0]].append(0)
                rsi[currencies[0]].append(0)

            print('price', price)
            print('amount', amount)
            print('volume', volume)
            print('mean', mean)
            print('rsi', rsi)
            print('times', times)

            ax[0].set_ylim(min(price[currencies[0]]+volume[currencies[0]]+mean[currencies[0]]+rsi[currencies[0]]) * 0.8, max(price[currencies[0]]+volume[currencies[0]]+mean[currencies[0]]+rsi[currencies[0]]) * 1.1)
            ax[0].set_xlim(0, max(times)+10)

            lines[0].set_data(times, price[currencies[0]])
            lines[1].set_data(times, volume[currencies[0]])
            lines[2].set_data(times, mean[currencies[0]])
            lines[3].set_data(times, rsi[currencies[0]])

            figure.canvas.draw()
            figure.canvas.flush_events()

            time.sleep(time_interval)


