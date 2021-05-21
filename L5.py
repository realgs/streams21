import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import requests
import time

base_currency = 'PLN'
url = 'https://bitbay.net/API/Public/'
post = '/trades.json'
time_interval = 3

# w_volume = int(input('Okno przesuwne dla wolumenu: '))
# w_mean = int(input('Okno przesuwne dla średniej: '))
# w_rsi = int(input('Okno przesuwne dla RSI: '))

w_volume = 2
w_mean = 2
w_rsi = 2


def get_data(currency_list, pos):
    try:
        req = requests.get(url + currency_list + base_currency + pos)
        req.raise_for_status()
        return req.json()

    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def calculate_rsi(data, w):  # dodać obsługę dziekenia przez 0!!
    data = data[-w:]
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


def calculate_volume(data, w):
    sum_amount = 0
    for i in range(1, w + 1):
        sum_amount += data[-i]
    return sum_amount


def calculate_mean(data, w):
    sum_price = 0
    for j in range(1, w + 1):
        sum_price += data[-j]
    return sum_price / w


def create_plot(currency_list):
    figure, axis = plt.subplots(n, 1, figsize=(7, 7))
    figure.text(0.5, 0.04, 'time', ha='center', va='center')
    figure.tight_layout(pad=4.0, rect=[0, 0, .8, 1])

    line = []
    for i in range(len(currency_list)):
        line.append(axis[i].plot(times, price[currency_list[i]], label="price")[0])
        line.append(axis[i].plot(times, volume[currency_list[i]], label="volume")[0])
        line.append(axis[i].plot(times, mean[currency_list[i]], label="mean")[0])
        line.append(axis[i].plot(times, rsi[currency_list[i]], label="rsi")[0])

        axis[i].legend()

        axis[i].set_title(f'{currency_list[i] + base_currency}')
        axis[i].xaxis.set_major_formatter('{x} s')

    return figure, axis, line


if __name__ == '__main__':
    currencies = ['DASH', 'OMG', 'BTC']
    n = len(currencies)

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
    fig, ax, lines = create_plot(currencies)

    while True:
        for i in range(50):
            t += 1
            times.append(t)
            for currency in currencies:
                r = get_data(currency, post)
                price[currency].append(r[i]['price'])
                amount[currency].append(r[i]['amount'])

                if len(price[currency]) >= w_volume:
                    volume[currency].append(calculate_volume(amount[currency], w_volume))

                if len(price[currency]) >= w_mean:
                    mean[currency].append(calculate_mean(price[currency], w_mean))

                if len(price[currency]) >= w_rsi:
                    rsi[currency].append(calculate_rsi(price[currency], w_rsi))

            p = 0
            for j in range(n):
                lines[0 + p].set_data(times, price[currencies[j]])
                lines[1 + p].set_data(times[w_volume - 1:], volume[currencies[j]])
                lines[2 + p].set_data(times[w_mean - 1:], mean[currencies[j]])
                lines[3 + p].set_data(times[w_rsi - 1:], rsi[currencies[j]])
                p += 4

                minim = min(price[currencies[j]] +
                            volume[currencies[j]] +
                            mean[currencies[j]] +
                            rsi[currencies[j]]) * 0.01
                maxim = max(price[currencies[j]] +
                            volume[currencies[j]] +
                            mean[currencies[j]] +
                            rsi[currencies[j]]) * 2.1
                ax[j].set_ylim(minim, maxim)
                ax[j].set_xlim(0, max(times) + 15)
                # ax[j].set_yscale('symlog')

                ax[j].text(1.3, .85, '          ', fontsize=10, transform=ax[j].transAxes,
                           bbox=dict(facecolor='white', edgecolor="none", alpha=1))
                ax[j].text(1.03, .85, 'typ trendu: ', fontsize=10, transform=ax[j].transAxes,
                           bbox=dict(facecolor='white', edgecolor="none", alpha=1))

                ax[j].text(1.03, .65, '                ', fontsize=10, transform=ax[j].transAxes,
                           bbox=dict(facecolor='white', edgecolor="none", alpha=1))

                if len(rsi[currencies[j]]) >= 2:
                    if rsi[currencies[j]][-1] > 70 or rsi[currencies[j]][-2] > 50 and rsi[currencies[j]][-1] > 50:
                        ax[j].text(1.3, .85, 'spadek', fontsize=10, c='red', transform=ax[j].transAxes)

                    elif rsi[currencies[j]][-1] < 30 or rsi[currencies[j]][-2] < 50 and rsi[currencies[j]][-1] > 50:
                        ax[j].text(1.3, .85, 'wzrost', fontsize=10, c='green', transform=ax[j].transAxes)

                    else:
                        ax[j].text(1.3, .85, '------', fontsize=10, transform=ax[j].transAxes)

            temp_volume = []
            for j in range(n):
                if len(volume[currencies[j]]) >= 2:
                    temp_volume.append((volume[currencies[j]][-1], j))

            if len(volume[currencies[0]]) >= 2:
                temp_volume.sort(key=lambda tup: tup[0])
                max_volume = temp_volume[-1]
                j = max_volume[1]

                if not (rsi[currencies[j]][-1] > 70 or rsi[currencies[j]][-2] > 50 and rsi[currencies[j]][-1] > 50):
                    ax[max_volume[1]].text(1.03, .65, 'kandydat', fontsize=10, c='blue', transform=ax[max_volume[1]].transAxes)

            fig.canvas.draw()
            fig.canvas.flush_events()

            time.sleep(time_interval)
