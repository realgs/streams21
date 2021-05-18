import requests
import time
from requests.exceptions import HTTPError
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter

RSI_SAMPLE_SIZE = 0
INTERVAL = 3000
MAX_POINTS = int(input('Przedział do wyświetlenia na wykresie: '))

SAMPLE_SIZE = int(input('Przedział z jakiego będzie liczona średnia: '))
CHOICE = input('Wolumen [w], RSI [r]: ')
if CHOICE == 'r':
    RSI_SAMPLE_SIZE = int(input('Przedział z jakiego będzie liczone RSI: '))



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
    return float(data['buy'][0]['ra']), float(data['sell'][0]['ra']) ,datetime.now()


def get_volume(currency_pair):
    now = int(str(time.time()*1000)[:9]+'0000')
    try:
        req = requests.get(f'https://api.bitbay.net/rest/trading/candle/history/{currency_pair}/60?from={now - 600000}&to={now}')
        if req.status_code == 200:
            data = req.json()
            vol = 0
            for i in data['items']:
                vol += float(i[1]['v'])
        else:
            print("Wystapil blad podczas pobierania -",currency_pair)
    except HTTPError:
        print('Error:', HTTPError)
        return None
    
    return vol


def create_pairs(BASE, CURR):
    pairs = []
    for i in BASE:
        for j in CURR:
            pairs.append(i+'-'+j)
    return pairs


def create_lists(n):
    buy, sell, date, avg_sell, avg_buy, vol, rsi = [],[],[],[],[],[],[]
    for _ in range(n):
        sell.append([])
        buy.append([])
        date.append([])
        avg_sell.append([])
        avg_buy.append([])
        vol.append([])
        rsi.append([])
    return buy, sell, date, avg_sell, avg_buy, vol, rsi

def draw_graphs(currency_pairs):
    n = len(currency_pairs)
    buy, sell, date, avg_sell, avg_buy, vol, rsi = create_lists(n)


    fig, axs = plt.subplots(2*n, sharex=True, figsize=(15, 10))
    data_lines = []
    
    for i in range(n):
        data_lines.append(axs[2*i].plot([], [],'k-' ,label='Sell offer'))
        data_lines.append(axs[2*i].plot([], [],'k--', label='Avg sell offer'))
        data_lines.append(axs[2*i].plot([], [],'r-', label='Buy offer'))
        data_lines.append(axs[2*i].plot([], [],'r--', label='Avg buy offer'))

        if CHOICE == 'r':
            data_lines.append(axs[2*i+1].plot([], [],'k-o', label='RSI'))
        elif CHOICE == 'w':
            data_lines.append(axs[2*i+1].plot([], [], label='Wolumen'))
        
        axs[2*i].set_title(currency_pairs[i])
        axs[2*i].grid()
        axs[2*i].legend(loc=6)
        axs[2*i].xaxis.set_major_formatter(DateFormatter('%H:%M:%S %d-%m-%y '))
        axs[2*i+1].grid()
        axs[2*i+1].legend(loc=6)
        axs[2*i+1].xaxis.set_major_formatter(DateFormatter('%d-%m-%y %H:%M:%S'))

    fig.autofmt_xdate(rotation=35)
    anim = FuncAnimation(fig, update, fargs=(currency_pairs, data_lines, date, buy, sell, avg_sell, avg_buy, vol, rsi, axs) ,interval=INTERVAL)
    plt.show()

def update(_,*args):
    currency_pairs, data_lines, date, buy, sell, avg_sell, avg_buy, vol, rsi, axs = args
    for i in range(len(currency_pairs)):
        data = get_data(currency_pairs[i], 'orderbook-limited')
       
        buy[i].append(data[0])
        sell[i].append(data[1])
        date[i].append(data[2])
        avg_sell[i].append(calc_avg(sell[i]))
        avg_buy[i].append(calc_avg(buy[i]))
        
        data_lines[i*5][0].set_data(date[i], sell[i])
        data_lines[i*5+1][0].set_data(date[i], avg_sell[i])
        data_lines[i*5+2][0].set_data(date[i], buy[i])
        data_lines[i*5+3][0].set_data(date[i], avg_buy[i])

        if CHOICE == 'r':
            rsi[i].append(calc_rsi(buy[i]))
            data_lines[i*5+4][0].set_data(date[i], rsi[i])
        elif CHOICE == 'w':
            vol[i].append(get_volume(currency_pairs[i]))
            data_lines[i*5+4][0].set_data(date[i], vol[i])
    

        axs[2*i].relim()
        axs[2*i].autoscale_view()
        axs[2*i+1].relim()
        axs[2*i+1].autoscale_view()

        if len(buy[i]) > MAX_POINTS:
            buy[i].pop(0)
            sell[i].pop(0)
            date[i].pop(0)
            avg_sell[i].pop(0)
            avg_buy[i].pop(0)
            if CHOICE == 'r':
                rsi[i].pop(0)
            elif CHOICE == 'w':   
                vol[i].pop(0)

    return data_lines

def calc_avg(data):
    total = 0
    if len(data) > SAMPLE_SIZE:
        for i in data[len(data) - SAMPLE_SIZE:]:
            total += i
        total /= SAMPLE_SIZE
    else:
        for i in data:
            total += i
        total /= len(data)
    return total


def calc_rsi(data):
    inc = list()
    dec = list()
    if len(data) >= RSI_SAMPLE_SIZE:
        sample = data[len(data) - RSI_SAMPLE_SIZE:]
        for i in range(len(sample) - 1, 0, -1):
            temp = sample[i] - sample[i-1]
            if temp > 0:
                inc.append(temp)
            elif temp < 0:
                dec.append(abs(temp))
    else:
        return 50

    a = (sum(inc) + 1) / (len(inc) + 1)
    b = (sum(dec) + 1) / (len(dec) + 1)

    RSI = 100 - (100 / (1 + (a / b)))
    return RSI

def main():
    CURR = ['LTC','BCC']
    BASE = ['PLN']
    draw_graphs(create_pairs(CURR, BASE))


if __name__ == '__main__':
    main()
