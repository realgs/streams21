import requests
from requests.exceptions import HTTPError
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.animation import FuncAnimation

adress_url = 'https://bitbay.net/API/Public/'

def get_data(currency1, currency2, category1, format1):
    try:
        response = requests.get(f'{adress_url}/{currency1}/{currency2}/{category1}.{format1}')
        response.raise_for_status()
    except HTTPError as http_error:
        print(f'Error! Operation failed:{http_error}')
    except Exception as error:
        print(f'Error! Operation failed:{error}')
    else:
        data = response.json()
        return data


def plotting_graph(_):
    values_y = [values_1_bid, values_1_ask,values_2_bid, values_2_ask,values_3_bid, values_3_ask]
    values_y[0].append(y1['bid'])
    values_y[1].append(y1['ask'])
    values_y[2].append(y2['bid'])
    values_y[3].append(y2['ask'])
    values_y[4].append(y3['bid'])
    values_y[5].append(y3['ask'])

    timepiece = datetime.now()
    values_x.append(timepiece.strftime('%X'))

    values_legend = ['bid1', 'ask1', 'bid2', 'ask2', 'bid3', 'ask3']
    plt.cla()

    for i in values_y:
        plt.plot(values_x, i, label=values_legend[values_y.index(i)])

    plt.legend(loc='best', bbox_to_anchor=(0.5, 0.3, 0.5, 0.45))
    plt.xlabel('Time')
    plt.ylabel('USD price')
    plt.title('Data graph')
    plt.autoscale(enable=True, axis='y')


if __name__ == '__main__':
    values_1_bid, values_1_ask = [], []
    values_2_bid, values_2_ask = [], []
    values_3_bid, values_3_ask = [], []

    y1 = get_data('BAT', 'USD', 'ticker', 'json')
    y2 = get_data('TRX', 'USD', 'ticker', 'json')
    y3 = get_data('LSK', 'USD', 'ticker', 'json')

    values_x = []
    refreshing = 5

    plt.style.use('seaborn')
    animation = FuncAnimation(plt.gcf(), plotting_graph, interval=1000*refreshing)
    plt.show()
