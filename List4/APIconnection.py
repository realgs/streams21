import requests
from requests.exceptions import HTTPError
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter

INTERVAL = 5000
MAX_POINTS = 40


def get_data(currency_pair, method):
    try:
        req = requests.get(f'https://api.bitbay.net/rest/trading/{method}/{currency_pair}/10')
        if req.status_code == 200:
            data = req.json()
        else:
            print("Wystapil blad podczas pobierania -",currency_pair)
    except HTTPError:
        print('Error:', HTTPError)
        return None
    return float(data['buy'][0]['ra']), float(data['sell'][0]['ra']), datetime.now()


def create_pairs(BASE, CURR):
    pairs = []
    for i in BASE:
        for j in CURR:
            pairs.append(i+'-'+j)
    return pairs


def create_lists(n):
    buy, sell, date = [],[],[]
    for _ in range(n):
        sell.append([])
        buy.append([])
        date.append([])
    return buy, sell, date

def draw_graphs(currency_pairs):
    n = len(currency_pairs)
    buy, sell, date = create_lists(n)


    fig, axs = plt.subplots(n, sharex=True, figsize=(15, 10))
    data_lines = []
    
    for i in range(n):
        data_lines.append(axs[i].plot([], [], label='Buy offer'))
        data_lines.append(axs[i].plot([], [], label='Sell offer'))

        axs[i].set_title(currency_pairs[i])
        axs[i].grid()
        axs[i].legend(loc=7)
        axs[i].xaxis.set_major_formatter(DateFormatter('%H:%M:%S %d-%m-%y '))

    fig.autofmt_xdate(rotation=35)
    anim = FuncAnimation(fig, update, fargs=(currency_pairs, data_lines, date, buy, sell, axs) ,interval=INTERVAL)
    plt.show()

def update(_,*args):
    currency_pairs, data_lines, date, buy, sell, axs = args
    for i in range(len(currency_pairs)):
        data = get_data(currency_pairs[i], 'orderbook-limited')

        buy[i].append(data[0])
        sell[i].append(data[1])
        date[i].append(data[2])

        if len(buy[i]) > MAX_POINTS:
            buy[i].pop(0)
            sell[i].pop(0)
            date[i].pop(0)
        
        data_lines[i*2][0].set_data(date[i], buy[i])
        data_lines[i*2+1][0].set_data(date[i], sell[i])

        axs[i].relim()
        axs[i].autoscale_view()

    return data_lines


def main():
    CURR = ['DASH','OMG','BCC']
    BASE = ['PLN']
    draw_graphs(create_pairs(CURR, BASE))


if __name__ == '__main__':
    main()
