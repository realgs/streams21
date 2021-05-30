import json
from multiprocessing import Process
from os import path

from flask import Flask, request, Response, abort

app = Flask(__name__)


class MarketApi:
    def __init__(self, shared):
        global shared_json
        shared_json = shared
        process = Process(target=app.run, )
        process.start()

    @app.route('/buy', methods=['GET'])
    def buy_crypto():
        cryptoid = request.args.get('cryptoid')
        quantity = request.args.get('quantity')
        price = request.args.get('price')
        cryptoid = cryptoid.upper()
        data = json.loads(shared_json.value)
        data[cryptoid]['quantity'] = str(int(data[cryptoid]['quantity']) + int(quantity))
        data[cryptoid]['price'] = str(price)
        shared_json.value = json.dumps(data)
        return shared_json.value

    @app.route('/sell', methods=['GET'])
    def sell_crypto():
        cryptoid = request.args.get('cryptoid')
        cryptoid = cryptoid.upper()
        quantity = request.args.get('quantity')
        data = json.loads(shared_json.value)
        data[cryptoid]['quantity'] = str(int(data[cryptoid]['quantity']) + int(quantity))
        data[cryptoid]['price'] = "sell"
        shared_json.value = json.dumps(data)
        return shared_json.value

    @app.route('/loadwallet', methods=['GET'])
    def reload_wallet():
        file_location = request.args.get('file')
        if not path.exists(file_location):
            return abort(Response('File not found', 400))

        data = json.loads(shared_json.value)
        data["file"] = str(file_location)
        shared_json.value = json.dumps(data)
        return file_location