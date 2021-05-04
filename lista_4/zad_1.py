import requests
from requests.exceptions import HTTPError
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter

ADRESS = {
    'TRX-PLN' : 'https://bitbay.net/API/Public/TRXPLN/orderbook.json',
    'GRT-PLN' : 'https://bitbay.net/API/Public/GRTPLN/orderbook.json',
    'GNT-PLN' : 'https://bitbay.net/API/Public/GNTPLN/orderbook.json'
}

CODES = [200,201,202,203,204,205,206]

INTERVAL = 1000

counter = 0
currency = []
for key in ADRESS.keys():
    currency.append(key)


def market():
    bids_table = []
    asks_table = []
    req_times = []
    volume_table = []
    volume = 0
    for key in ADRESS.keys():
        try:
            request = requests.get(ADRESS[key])
            if request.status_code in CODES:
                for bids in request.json()['bids']:
                    volume += 1
                for asks in request.json()['asks']:
                    volume += 1
                bids = request.json()['bids'][0][0]
                asks = request.json()['asks'][0][0]
                req_time = datetime.now()
                bids_table.append(bids)
                asks_table.append(asks)
                req_times.append(req_time)
                volume_table.append(volume)
                volume = 0
            else:
                print('ERROR')
        except HTTPError:
            print('ERROR: ',HTTPError)
    return bids_table, asks_table, req_times


def arrays(n):
    return [[] for _ in range(n)]


def show_plots():
    def update(_):
        bids, asks, times = market()
        global counter
        counter += 1
        for i in range(n):
            bids_table[i].append(bids[i])
            asks_table[i].append(asks[i])
            req_times[i].append(times[i])

            lines[i*2].set_data(req_times[i], bids_table[i])
            lines[i*2+1].set_data(req_times[i], asks_table[i])
            
            if counter > 20:
                bids_table[i].pop(0)
                asks_table[i].pop(0)
                req_times[i].pop(0)
                

            axis[i].relim()
            axis[i].autoscale_view()
            
        return lines

    n = 3
    counter = 0
    req_times, bids_table, asks_table, volume_table = arrays(n), arrays(n), arrays(n), arrays(n)

    fig, axis = plt.subplots(n,figsize=(16,9))
    lines = []

    for i in range(n):
        bids_part, = axis[i].plot([], [],'g-d', label='Best bid')
        asks_part, = axis[i].plot([], [],'r-d', label='Best ask')
        lines.append(bids_part)
        lines.append(asks_part)
        
        axis[i].set_title(currency[i])
        axis[i].grid()
        axis[i].legend(loc=6)
        axis[i].xaxis.set_major_formatter(DateFormatter('%d-%m-%y %H:%M:%S'))

    fig.autofmt_xdate()
    anim = FuncAnimation(fig, update, interval=INTERVAL)
    plt.show()


show_plots()
