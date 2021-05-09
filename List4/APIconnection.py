import requests
from requests.exceptions import HTTPError
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter

INTERVAL = 3000
print('Przedział do wyświetlenia na wykresie oraz z jakiego liczona bedzie średnia: ', end='')
MAX_POINTS = int(input())
choice = 'w'
print('Wolumen [w], RSI [r]: ', end='')
choice = input()



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


def create_pairs(BASE, CURR):
    pairs = []
    for i in BASE:
        for j in CURR:
            pairs.append(i+'-'+j)
    return pairs


def create_lists(n):
    buy, sell, date, avg_sell, vol, rsi = [],[],[],[],[],[]
    for _ in range(n):
        sell.append([])
        buy.append([])
        date.append([])
        avg_sell.append([])
        vol.append([])
        rsi.append([])
    return buy, sell, date, avg_sell, vol, rsi

def draw_graphs(currency_pairs):
    n = len(currency_pairs)
    buy, sell, date, avg_sell, vol, rsi = create_lists(n)


    fig, axs = plt.subplots(2*n, sharex=True, figsize=(15, 10))
    data_lines = []
    
    for i in range(n):
        data_lines.append(axs[2*i].plot([], [], label='Buy offer'))
        data_lines.append(axs[2*i].plot([], [], label='Sell offer'))
        data_lines.append(axs[2*i].plot([], [],'k-o', label='Avg sell offer'))

        if choice == 'r':
            data_lines.append(axs[2*i+1].plot([], [],'k-o', label='RSI'))
        elif choice == 'w':
            data_lines.append(axs[2*i+1].plot([], [],'k-o', label='Wolumen'))
        
        axs[2*i].set_title(currency_pairs[i])
        axs[2*i].grid()
        axs[2*i].legend(loc=7)
        axs[2*i].xaxis.set_major_formatter(DateFormatter('%H:%M:%S %d-%m-%y '))
        axs[2*i+1].grid()
        axs[2*i+1].legend(loc=6)
        axs[2*i+1].xaxis.set_major_formatter(DateFormatter('%d-%m-%y %H:%M:%S'))

    fig.autofmt_xdate(rotation=35)
    anim = FuncAnimation(fig, update, fargs=(currency_pairs, data_lines, date, buy, sell, avg_sell, vol, rsi, axs) ,interval=INTERVAL)
    plt.show()

def update(_,*args):
    currency_pairs, data_lines, date, buy, sell, avg_sell, vol, rsi, axs = args
    for i in range(len(currency_pairs)):
        data = get_data(currency_pairs[i], 'orderbook-limited')
       
        buy[i].append(data[0])
        sell[i].append(data[1])
        date[i].append(data[2])
        avg_sell[i].append(calc_avg(sell[i]))

        data_lines[i*4][0].set_data(date[i], buy[i])
        data_lines[i*4+1][0].set_data(date[i], sell[i])
        data_lines[i*4+2][0].set_data(date[i], avg_sell[i])

        if choice == 'r':
            for z in sell[i]:
                rs = abs(data[0]/data[1])
            rsi[i].append(100 - (100 / (1 + rs)))
            data_lines[i*4+3][0].set_data(date[i], rsi[i])
        # elif choice == 'v':
        #     vol[i].append(volume[i])
        #     data_lines[i*4+3].set_data(req_times[w], vol[w])
        
        

        if len(buy[i]) > MAX_POINTS:
            buy[i].pop(0)
            sell[i].pop(0)
            date[i].pop(0)
            avg_sell[i].pop(0)

        axs[2*i].relim()
        axs[2*i].autoscale_view()
        axs[2*i+1].relim()
        axs[2*i+1].autoscale_view()

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
