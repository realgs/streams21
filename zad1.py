from matplotlib import ticker
import matplotlib.pyplot as plt
import requests
import time

base_currency = 'PLN'
currencies = ['BTC', 'LTC', 'DASH']
url = 'https://bitbay.net/API/Public/'
post = '/orderbook.json'
time_interval = 1


def get_data(currency, post):
    try:
        r = requests.get(url+currency+base_currency+post)
        r.raise_for_status()
        return r.json()

    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


if __name__ == '__main__':
    currencies = ['OMG']
    post = '/ticker.json'
    n = len(currencies)

    asks = {}
    bids = {}
    volume = {}
    for currency in currencies:
        asks[currency] = []
        bids[currency] = []
        volume[currency] = []

    times = []
    t = 0

    plt.ion()
    figure, ax = plt.subplots(1, 2, figsize=(10, 5))

    figure.text(0.5, 0.04, 'time', ha='center', va='center')
    figure.tight_layout(pad=3.0)

    lines = []
    lines.append(ax[0].plot(times, asks[currencies[0]], label="asks")[0])
    lines.append(ax[0].plot(times, bids[currencies[0]], label="bids")[0])
    lines.append(ax[1].plot(times, volume[currencies[0]], label="volume", color='green')[0])

    ax[0].legend()
    ax[1].legend()

    ax[0].set_title(f'{currencies[0]+base_currency}')
    ax[1].set_title('VOLUME')

    ax[0].xaxis.set_major_formatter('{x} s')
    ax[1].xaxis.set_major_formatter('{x} s')

    while True:

        r = get_data(currencies[0], post)
        asks[currencies[0]].append(r['ask'])
        bids[currencies[0]].append(r['bid'])
        volume[currencies[0]].append(r['volume'])

        t += 1
        times.append(t)

        # j = 0
        # for i in range(len(lines)):
        #     if i % 2 == 0:
        #         lines[i].set_data(times, asks[currencies[j]])
        #
        #     elif i % 3 == 0 and i % 2 != 0:
        #         lines[i].set_data(times, volume[currencies[j]])
        #
        #     else:
        #         lines[i].set_data(times, bids[currencies[j]])
        #         j += 1
        lines[0].set_data(times, asks[currencies[0]])
        lines[1].set_data(times, bids[currencies[0]])
        lines[2].set_data(times, volume[currencies[0]])

        ax[0].set_ylim(min(bids[currencies[0]]) * 0.995, max(asks[currencies[0]]) * 1.005)
        ax[0].set_xlim(0, max(times)+10)

        ax[1].set_ylim(min(volume[currencies[0]]) * 0.999, max(volume[currencies[0]]) * 1.001)
        ax[1].set_xlim(0, max(times)+10)

        figure.canvas.draw()
        figure.canvas.flush_events()

        time.sleep(time_interval)
