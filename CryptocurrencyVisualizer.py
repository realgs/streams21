import requests
import argparse 
from sys import exit

from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

BIDS = "bids"
ASKS = "asks"
TIMELINE_SHIFT = 5
BASE_URL = "https://bitbay.net/API/Public/"
REGUESTED_JSON= "orderbook.json"
STYLE_NAME = 'dark_background'

def get_url(cryptocurrency, currency):

    return f"{BASE_URL}{cryptocurrency}{currency}/{REGUESTED_JSON}"

def get_trades(cryptocurrency, currency):
    trades = None

    try:
        request = requests.get(get_url(cryptocurrency, currency))
        trades = request.json()
    except requests.exceptions.RequestException as ex:
        trades = None
        print(ex)
    
    return trades

def extract_best_trade(trades):
    
    return trades[BIDS][0][0], trades[ASKS][0][0]

def add_data(cryptocurrency, currency, best_bids, best_asks, intervals):
        
        intervals.append(datetime.now().strftime("%H:%M:%S"))
        best_bid, best_ask = extract_best_trade((get_trades(cryptocurrency, currency)))
        best_bids.append(best_bid)
        best_asks.append(best_ask)

def get_chart(cryptocurrency, currency):

    fig, axe = plt.subplots()
    fig.canvas.set_window_title(f'Wykres notowań {cryptocurrency} - {currency}')

    return fig, axe

def update_plot(axs, best_bids, best_asks, intervals):
        
        axs.plot(intervals, best_asks, label=ASKS)
        axs.plot(intervals, best_bids, label=BIDS)

def visualize(i, cryptocurrency, currency, axs, best_bids, best_asks, intervals):

        add_data(cryptocurrency, currency, best_bids, best_asks, intervals)

        axs.cla()

        axs.set_title(f'{cryptocurrency} - {currency}')
        axs.set_xlabel('time')
        axs.set_ylabel('price')

        update_plot(axs, best_bids, best_asks, intervals)

        axs.set_xlim(max(0, i-TIMELINE_SHIFT), max(0, i+TIMELINE_SHIFT))
        
        axs.legend()

def prepare_parser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("cryptocurrency")
    parser.add_argument("currency")
    parser.add_argument("-crypto2", "--cryptocurrency_2")
    parser.add_argument("-curren2", "--currency_2")
    parser.add_argument("-crypto3", "--cryptocurrency_3")
    parser.add_argument("-curren3", "--currency_3")
    parser.add_argument("-r", "--refresh_time", type=int, choices=range(1, 31))

    return parser

def get_animation_function(cryptocurrency, currency, figure, refresh_time):

    return FuncAnimation(figure[0], 
                        visualize, 
                        fargs=(cryptocurrency, currency, figure[1], [], [], []), 
                        interval = refresh_time*1000)

def build_windows(cryptocurrency, currency, figures, animations, refresh_time):
    figures.append(get_chart(cryptocurrency, currency))
    animations.append(get_animation_function(cryptocurrency, currency, figures[len(figures)- 1], refresh_time))

def main():
    args = prepare_parser().parse_args()
    args.refresh_time = 10 if args.refresh_time is None else args.refresh_time

    figures = []
    animations = []

    plt.style.use(STYLE_NAME)

    if args.cryptocurrency is not None and args.currency is not None:
        build_windows(args.cryptocurrency, args.currency, figures, animations, args.refresh_time)

    if args.cryptocurrency_2 is not None and args.currency_2 is not None:
        build_windows(args.cryptocurrency_2, args.currency_2, figures, animations, args.refresh_time)

    if args.cryptocurrency_3 is not None and args.currency_3 is not None:
        build_windows(args.cryptocurrency_3, args.currency_3, figures, animations, args.refresh_time)
        
    try:         
        plt.show()

    except Exception:
        exit(0)

main()
