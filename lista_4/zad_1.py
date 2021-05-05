import requests
from requests.exceptions import HTTPError
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter

ADRESS = {
    'LTC-PLN' : 'https://bitbay.net/API/Public/LTCPLN/ticker.json',
    'OMG-PLN' : 'https://bitbay.net/API/Public/OMGPLN/ticker.json'
}

CODES = [200,201,202,203,204,205,206]

INTERVAL = 1000

counter = 0
counter2 = 0
currency = []
amount_of_currencies = 0
for key in ADRESS.keys():
    currency.append(key)
    amount_of_currencies += 1

print('Wyświetlić RSI(r), czy Wolumen(v)? ', end='')
decision = input()
print('Przedział do wyświetlenia na wykresie oraz z jakiego liczona bedzie średnia: ', end='')
part = input()


def market():
    bids_table = []
    asks_table = []
    volume_table = []
    req_times = []
    for key in ADRESS.keys():
        try:
            request = requests.get(ADRESS[key])
            if request.status_code in CODES:
                bids = request.json()['bid']
                asks = request.json()['ask']
                volume = request.json()['volume']
                req_time = datetime.now()
                bids_table.append(bids)
                asks_table.append(asks)
                volume_table.append(volume)
                req_times.append(req_time)
            else:
                print('ERROR')
        except HTTPError:
            print('ERROR: ',HTTPError)
    return bids_table, asks_table, req_times, volume_table


def arrays(n):
    return [[] for _ in range(n*2)]


def show_plots():
    def update(_):
        bids, asks, times, volume = market()
        global counter
        counter += 1
        for i in range(n):
            w = i * 2
            bids_table[w].append(bids[i])
            asks_table[w].append(asks[i])
            req_times[w].append(times[i])
            suma = 0
            for z in asks_table[w]:
                suma += z
            avg_ask = suma/(len(asks_table[w]))
            avg_asks_table[w].append(avg_ask)
            suma = 0

            lines[i*4].set_data(req_times[w], bids_table[w])
            lines[i*4+1].set_data(req_times[w], asks_table[w])
            lines[i*4+2].set_data(req_times[w], avg_asks_table[w])

            if decision == 'r':
                for z in asks_table[w]:
                    rs = abs(bids[i]/asks[i])
                rsi = 100 - (100 / (1 + rs))
                rsi_table[w].append(rsi)
                lines[i*4+3].set_data(req_times[w], rsi_table[w])
            elif decision == 'v':
                volume_table[w].append(volume[i])
                lines[i*4+3].set_data(req_times[w], volume_table[w])
            
            if counter > int(part):
                bids_table[w].pop(0)
                asks_table[w].pop(0)
                req_times[w].pop(0)
                avg_asks_table[w].pop(0)
                if decision == 'r':
                    rsi_table[w].pop(0)
                elif decision == 'v':   
                    volume_table[w].pop(0)
                
                

            axis[w].relim()
            axis[w].autoscale_view()
            axis[w+1].relim()
            axis[w+1].autoscale_view()
        return lines


    n = amount_of_currencies
    counter = 0
    req_times, bids_table, asks_table, avg_asks_table, volume_table, rsi_table = arrays(n), arrays(n), arrays(n), arrays(n), arrays(n), arrays(n)

    fig, axis = plt.subplots(2*n,figsize=(16,9))
    lines = []

    for i in range(n):
        bids_part, = axis[2*i].plot([], [],'g-d', label='Best bid')
        asks_part, = axis[2*i].plot([], [],'r-d', label='Best ask')
        asks_avg, = axis[2*i].plot([], [], 'k-d', label='Avg ask')
        lines.append(bids_part)
        lines.append(asks_part)
        lines.append(asks_avg)
        if decision == 'r':
            rsi_part, = axis[2*i+1].plot([], [], 'b-d', label='RSI')
            lines.append(rsi_part)
        elif decision == 'v':
            volume_part, = axis[2*i+1].plot([], [], 'b-d', label='Volume')
            lines.append(volume_part)
        

        axis[2*i].set_title(currency[i])
        axis[2*i].grid()
        axis[2*i].legend(loc=6)
        axis[2*i].xaxis.set_major_formatter(DateFormatter('%d-%m-%y %H:%M:%S'))
        axis[2*i+1].grid()
        axis[2*i+1].legend(loc=6)
        axis[2*i+1].xaxis.set_major_formatter(DateFormatter('%d-%m-%y %H:%M:%S'))

    fig.autofmt_xdate()
    anim = FuncAnimation(fig, update, interval=INTERVAL)
    plt.show()


show_plots()
