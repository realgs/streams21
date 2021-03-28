import requests
import argparse
import time
import os
from sys import exit
from tabulate import tabulate
from datetime import datetime

BIDS = "bids"
ASKS = "asks"

def clear_command_line(): os.system('cls' if os.name == 'nt' else 'clear')

def get_trades(crypto_currency, currency):
    trades = None

    try:
        request = requests.get(
            f"https://bitbay.net/API/Public/{crypto_currency}{currency}/orderbook.json"
        )
        trades = request.json()
    except requests.exceptions.RequestException as ex:
        trades = None
        print(ex)
    
    return trades

def extract_trades(key, trades, number_of_records_to_show):
    
    return [trades[key][i][0] for i in range(0, number_of_records_to_show)]

def print_analysis(trades, number_of_records_to_show):
    table = {BIDS : extract_trades(BIDS, trades, number_of_records_to_show),
             ASKS : extract_trades(ASKS, trades, number_of_records_to_show),
             "diff" : get_difference(trades, number_of_records_to_show)
            }
    row_ids = [i + 1  for i in range(0, number_of_records_to_show)]

    print(tabulate(table, headers="keys", showindex=row_ids, floatfmt=".4f"))

def get_difference(trades, number_of_records_to_show):
    diff = []

    for i in range(0, number_of_records_to_show):
        bid = trades["bids"][i][0]
        ask = trades["asks"][i][0]
        diff.append( (1 - (ask - bid) / bid))
    
    return diff

def print_analysis_header(crypto_currency, currency):
    current_data = datetime.now().strftime("%H:%M:%S")
    
    print(f"Crypto currency:\t{crypto_currency}")
    print(f"Currency:\t\t{currency}")
    print(f"Last refrash time:\t{current_data}")
    print()

def print_analysis_footer():
    print("\nPress CTRL + C to end program.")

def analysis(crypto_currency, currency, refresh, number_of_records_to_show):
    trades = get_trades(crypto_currency, currency)

    if trades is not None:

        print_analysis_header(crypto_currency, currency)
        print_analysis(trades, number_of_records_to_show)
        print_analysis_footer()

        time.sleep(refresh)
        
        clear_command_line()
        
        analysis(crypto_currency, currency, refresh, number_of_records_to_show)

def prepare_parser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("cryptocurrency")
    parser.add_argument("currency")
    parser.add_argument("-r", "--refresh_time", type=int, choices=range(1, 31))
    parser.add_argument("-n", "--number_of_records_to_show", type=int, choices=range(1, 26))

    return parser

def run():    
    args = prepare_parser().parse_args()
    args.refresh_time = 10 if args.refresh_time is None else args.refresh_time
    args.number_of_records_to_show = 5 if args.number_of_records_to_show is None else args.number_of_records_to_show

    try: 
        analysis(args.cryptocurrency, args.currency, args.refresh_time, args.number_of_records_to_show)
    except KeyboardInterrupt:
        exit(0)

run()