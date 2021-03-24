import requests
import time
from sys import exit

def link(currency_type):
    return f'https://bitbay.net/API/Public/{currency_type}/orderbook.json'

def get_data(currency_type):
    try:
        req = requests.get(link(currency_type)).json()
        bid = req['bids']
        ask = req['asks']
    except Exception as e:
        print('ERROR:', e)
        return {}, {}

    return bid, ask

def print_offers(offers):
    if len(offers) > 6:
        short_offers = offers[:3]+['...']+offers[-3:]
    else:
        short_offers = offers        
    for offer in short_offers:
        print(offer)

if __name__ == '__main__':
    currency = ['BTCUSD', 'LTCUSD', 'ETHUSD']
    for c in currency:
        all_bid, all_ask = get_data(c)
        print(c, '\n bid: ')
        print_offers(all_bid)
        print('\n ask: ')
        print_offers(all_ask)
        print('\n')

    while True:
        try:
            for c in currency:
                all_bid, all_ask = get_data(c)
                if len(all_bid) == 0:
                    bid = 'No value to show'
                elif len(all_ask) == 0:    
                    ask = 'No value to show'
                else:
                    bid = all_bid[0][0]
                    ask = all_ask[0][0]
                    difference = (1 - ( ask - bid ) / bid )
                    print (c, '\n bid: ', bid, '\n ask: ', ask, '\n difference[%]: ', difference, '\n round difference: ', round(difference, 2), '% \n')
            time.sleep(5)
        except KeyboardInterrupt:
            exit()
