import requests
import time
from sys import exit

def link(currency_type):
    return f'https://bitbay.net/API/Public/{currency_type}/orderbook.json'

def get_data(currency_type):#jeżeli printować wszystkie to tu
    try:
        req = requests.get(link(currency_type)).json()
        bid = req['bids']
        ask = req['asks']
    except Exception as e:# obsługa błęów
        print(e)
        return {}

    return bid, ask

def print_offers(offers):
    if len(offers) > 6:
        short_offers = offers[:3]+['...']+offers[-3:]
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
                bid = all_bid[0][0]
                ask = all_ask[0][0]
                difference = ( ( ask - bid ) / bid ) * 100
                print (c, '\n bid: ', bid, '    ask: ', ask, '  difference[%]: ', difference, '    round difference: ', round(difference, 2), '\n')
            time.sleep(5)
        except KeyboardInterrupt:
            exit()
            