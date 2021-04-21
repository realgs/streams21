import requests
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

currency = ['DASHPLN', 'BSVPLN', 'LTCPLN']
time_int = 5

def get_data(currency):
    try:
        response = requests.get(f'https://bitbay.net/API/Public/{currency}/ticker.json')
        data = response.json()
        return data
    except requests.exceptions.MissingSchema:
        print("Missing URL schema (e.g. http or https)")
    except requests.exceptions.ConnectionError:
        print("Connection Error occured")

def prepare_data(ask1_values, bid1_values,ask2_values,bid2_values,ask3_values,bid3_values):
    ask1_values.append(get_data(currency[0]).get('ask'))
    bid1_values.append(get_data(currency[0]).get('bid'))
    ask2_values.append(get_data(currency[1]).get('ask'))
    bid2_values.append(get_data(currency[1]).get('bid'))
    ask3_values.append(get_data(currency[2]).get('ask'))
    bid3_values.append(get_data(currency[2]).get('bid'))
    return ask1_values, bid1_values,ask2_values,bid2_values,ask3_values,bid3_values

def make_plot(i):
    plt1_ask, plt1_bid,plt2_ask, plt2_bid, plt3_ask, plt3_bid = prepare_data(ask1_values, bid1_values,ask2_values,bid2_values,ask3_values,bid3_values)
    plt.cla()
    plt.title("Cryptocurrency values")
    plt.ylabel('Value')
    plt.xlabel('Time')
    plt.plot(plt1_ask, label = f'{currency[0]}:Ask')
    plt.plot(plt1_bid, label = f'{currency[0]}:Bid')
    plt.plot(plt2_ask, label=f'{currency[1]}:Ask')
    plt.plot(plt2_bid, label=f'{currency[1]}:Bid')
    plt.plot(plt3_ask, label=f'{currency[2]}:Ask')
    plt.plot(plt3_bid, label=f'{currency[2]}:Bid')
    plt.legend(loc = 'upper left')


if __name__ == "__main__":
    ask1_values = []
    bid1_values = []
    ask2_values = []
    bid2_values = []
    ask3_values = []
    bid3_values = []
    animations = FuncAnimation(plt.figure(), make_plot, interval=5000)
    plt.show()





