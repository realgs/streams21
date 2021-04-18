import matplotlib.pyplot as plt
from L2 import *


if __name__ == '__main__':
    currencies = ['BTC', 'LTC', 'DASH']
    post = '/ticker.json'
    n = len(currencies)

    asks = {}
    bids = {}
    for currency in currencies:
        asks[currency] = []
        bids[currency] = []

    times = []
    t = 0

    plt.ion()
    figure, ax = plt.subplots(n, 1, figsize=(8, 7))

    lines = []
    for i in range(n):
        lines.append(ax[i].plot(times, asks[currencies[i]], label="asks")[0])
        lines.append(ax[i].plot(times, bids[currencies[i]], label="bids")[0])

        ax[i].legend()
        ax[i].set_title(f'{currencies[i]+base_currency}')
        ax[i].set_xlim(0, 100)

    while True:
        for currency in currencies:
            r = get_data(currency, post)
            asks[currency].append(r['ask'])
            bids[currency].append(r['bid'])

        t += 1
        times.append(t)

        j = 0
        for i in range(len(lines)):
            if i % 2 == 0:
                lines[i].set_data(times, asks[currencies[j]])
            else:
                lines[i].set_data(times, bids[currencies[j]])
                j += 1

        for i in range(n):
            ax[i].set_ylim(max(bids[currencies[i]]) * 0.9, max(asks[currencies[i]]) * 1.1)

        figure.canvas.draw()
        figure.canvas.flush_events()

        time.sleep(time_interval)



