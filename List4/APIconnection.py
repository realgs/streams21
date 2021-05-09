import requests
from requests.exceptions import HTTPError
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter

INTERVAL = 3000
print('Przedział do wyświetlenia na wykresie oraz z jakiego liczona bedzie średnia: ', end='')
MAX_POINTS = int(input())



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
    buy, sell, date, avg_sell = [],[],[],[]
    for _ in range(n):
        sell.append([])
        buy.append([])
        date.append([])
        avg_sell.append([])
    return buy, sell, date, avg_sell

def draw_graphs(currency_pairs):
    n = len(currency_pairs)
    buy, sell, date, avg_sell = create_lists(n)


    fig, axs = plt.subplots(n, sharex=True, figsize=(15, 10))
    data_lines = []
    
    for i in range(n):
        data_lines.append(axs[i].plot([], [], label='Buy offer'))
        data_lines.append(axs[i].plot([], [], label='Sell offer'))
        data_lines.append(axs[i].plot([], [],'k-d', label='Avg sell offer'))

        axs[i].set_title(currency_pairs[i])
        axs[i].grid()
        axs[i].legend(loc=7)
        axs[i].xaxis.set_major_formatter(DateFormatter('%H:%M:%S %d-%m-%y '))

    fig.autofmt_xdate(rotation=35)
    anim = FuncAnimation(fig, update, fargs=(currency_pairs, data_lines, date, buy, sell, avg_sell, axs) ,interval=INTERVAL)
    plt.show()

def update(_,*args):
    currency_pairs, data_lines, date, buy, sell, avg_sell, axs = args
    for i in range(len(currency_pairs)):
        data = get_data(currency_pairs[i], 'orderbook-limited')
       

        buy[i].append(data[0])
        sell[i].append(data[1])
        date[i].append(data[2])
        avg_sell[i].append(calc_avg(sell[i]))

        if len(buy[i]) > MAX_POINTS:
            buy[i].pop(0)
            sell[i].pop(0)
            date[i].pop(0)
            avg_sell[i].pop(0)
        
        data_lines[i*3][0].set_data(date[i], buy[i])
        data_lines[i*3+1][0].set_data(date[i], sell[i])
        data_lines[i*3+2][0].set_data(date[i], avg_sell[i])

        axs[i].relim()
        axs[i].autoscale_view()

    return data_lines

def calc_avg(data):
    total = 0
    for i in data:
        total += i
    total /= len(data)
    return total


def main():
    CURR = ['LTC','OMG']
    BASE = ['PLN']
    draw_graphs(create_pairs(CURR, BASE))


if __name__ == '__main__':
    main()
