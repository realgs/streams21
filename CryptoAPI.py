import flask
from flask import jsonify
import pandas as pd
import requests
import time

def cryptomarket_3cryptos(crypto1, crypto2, crypto3, currency, frequency):
    while True:
        response1 = requests.get("https://bitbay.net/API/Public/"+crypto1+currency +"/trades.json")
        response2 = requests.get("https://bitbay.net/API/Public/"+crypto2+currency +"/trades.json")
        response3 = requests.get("https://bitbay.net/API/Public/"+crypto3+currency +"/trades.json")
        
        print(response1.json(), "\n",response2.json(),"\n", response3.json())
        time.sleep(frequency)

freq = 8 # frequency of sending requests to the API
cryptomarket_3cryptos("BTC","ETH","TRX", "USD",freq)
