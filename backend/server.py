import json
from os import path
from flask import Flask, request, Response, abort, redirect
import requests as r
from werkzeug.wrappers import response
app = Flask(__name__)


class Server: 
    @app.route('/buy', methods=['GET'])
    def buy_crypto():
        currency = request.args.get('currency')
        quantity = request.args.get('quantity')
        price = request.args.get('price')
        currency = currency.upper()
        response = r.post(f'http://localhost:8000/sendbuy?currency={currency}&quantity={quantity}&price={price}')
        return redirect("http://127.0.0.1:5500/streams21/frontend/index.html", code=302)

    @app.route('/sell', methods=['GET'])
    def sell_crypto():
        currency = request.args.get('currency')
        quantity = request.args.get('quantity')
        currency = currency.upper()
        print(currency)
        print(quantity)
        response = r.post(f'http://localhost:8000/sendsell?currency={currency}&quantity={quantity}')
        return redirect("http://127.0.0.1:5500/streams21/frontend/index.html", code=302)

    @app.route('/savewallet', methods=['GET'])
    def save_wallet():
        filename = request.args.get('file')
        response = r.post(f'http://localhost:8000/savewallet?file={filename}')
        return redirect("http://127.0.0.1:5500/streams21/frontend/index.html", code=302)

    @app.route('/loadwallet', methods=['GET'])
    def load_wallet():
        filename = request.args.get('file')
        response = r.post(f'http://localhost:8000/loadwallet?file={filename}')
        return redirect("http://127.0.0.1:5500/streams21/frontend/index.html", code=302)

if __name__ == "__main__":
    app.run(debug=True)