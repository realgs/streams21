import json
from os import path
from flask import Flask, request, Response, abort, redirect
import requests as r
import visualise


app = Flask(__name__)

buy_transactions = {
    'LSKPLN': {'quantity': list(), 'price': list()},
    'LTCPLN': {'quantity': list(), 'price': list()},
    'BTCPLN': {'quantity': list(), 'price': list()}
}
sell_transactions = {
    'LSKPLN': {'quantity': list(), 'price': list()},
    'LTCPLN': {'quantity': list(), 'price': list()},
    'BTCPLN': {'quantity': list(), 'price': list()}
}

current_volume = {
    'LSKPLN': {'quantity': 0},
    'LTCPLN': {'quantity': 0},
    'BTCPLN': {'quantity': 0}
}
balance = {
    'balance': 0
}

class Wallet:

    @app.route('/sendbuy', methods=['POST'])
    def handle_buy_data():
        currency = request.args.get('currency')
        quantity = request.args.get('quantity')
        price = request.args.get('price')
        currency = currency.upper()

        buy_helper(currency,quantity,price)

        print(buy_transactions)
        print(balance)
        return 'Data sucessfuly sent!'

    @app.route('/sendsell', methods=['POST'])
    def handle_sell_data():
            currency = request.args.get('currency')
            quantity = request.args.get('quantity')
            currency = currency.upper()
            sell_helper(currency,quantity)

            print(sell_transactions)
            print(balance)
            return 'Data sucessfuly sent!'

    @app.route('/savewallet', methods=['POST'])
    def handle_wallet_save():
            filename = request.args.get('file')
            to_json = []
            to_json.append(buy_transactions)
            to_json.append(sell_transactions)
            to_json.append(current_volume)
            to_json.append(balance)
            with open(filename, 'w') as f:
                json.dump(to_json, f)
                f.close()
            print('Data sucessfuly saved!')
            return 'Data sucessfuly saved!'


    @app.route('/loadwallet', methods=['POST'])
    def handle_wallet_load():
        global buy_transactions
        global sell_transactions
        global current_volume
        global balance
        filename = request.args.get('file')
        with open(filename, 'r') as f:
            to_dict = json.load(f)

        buy_transactions = to_dict[0]
        sell_transactions = to_dict[1]
        current_volume = to_dict[2]
        balance = to_dict[3]
        print('Data sucessfuly loaded!')
        return 'Data sucessfuly loaded!'

def buy_helper(currency,quantity,price):
    global balance
    global buy_transactions
    buy_transactions[currency]['quantity'].append(quantity)
    buy_transactions[currency]['price'].append(price)
    current_volume[currency]['quantity'] += int(quantity)
    balance['balance'] -= float(quantity) * float(price)


def sell_helper(currency,quantity):
    global balance
    global sell_transactions

    price = visualise.download_data(currency,'ticker')
    price = float(price['bid'])

    sell_transactions[currency]['quantity'].append(quantity)
    sell_transactions[currency]['price'].append(price)
    current_volume[currency]['quantity'] -= int(quantity)
    balance['balance'] += float(quantity) * float(price)

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)