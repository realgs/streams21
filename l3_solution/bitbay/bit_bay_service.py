from datetime import datetime

import requests

from l3_solution.bitbay.bit_bay_url import BitBayUrl


class BitBayService:
    CRYPTO_CURRENCIES = ['BTC', 'LTC', 'ETH']
    trade_buy = {
        'BTC': list(),
        'LTC': list(),
        'ETH': list(),
    }
    trade_sell = {
        'BTC': list(),
        'LTC': list(),
        'ETH': list(),
    }
    volume = {
        'BTC': list(),
        'LTC': list(),
        'ETH': list(),
    }

    def get_crypto_trade(self, cryptocurrency, currency, limit):
        request = requests.get(BitBayUrl.get_url_trades(currency, cryptocurrency, limit))
        return request.json()

    def update_crypto_trades(self):
        time = datetime.now()
        for crypto_currency in self.CRYPTO_CURRENCIES:
            self.update_crypto_trade(crypto_currency, "PLN", time)

    def update_crypto_trade(self, crypto_currency, currency, time):
        json = self.get_crypto_trade(crypto_currency, currency, 10)
        self.trade_buy[crypto_currency].append(
            {"price": float(json['buy'][0]['ra']), "time": f'{time.hour}:{time.minute}:{time.second}'})
        self.trade_sell[crypto_currency].append(
            {"price": float(json['sell'][0]['ra']), "time": f'{time.hour}:{time.min}:{time.second}'})

    def get_crypto_trade_buy_sell(self, cryptocurrency, currency):
        trade_json = self.get_crypto_trade(cryptocurrency, currency, 50)
        return trade_json

    def update_crypto_volume(self):
        for crypto_currency in self.CRYPTO_CURRENCIES:
            self.volume[crypto_currency].append(self.get_volume_request(crypto_currency, 'PLN', 600000))

    def get_volume_request(self, cryptocurrency, currency, time):
        request = requests.get(BitBayUrl.get_url_candle(currency, cryptocurrency, time))
        volume = 0
        for item in request.json()['items']:
            volume += float(item[1]['v'])
        return volume

    def get_trades_buy(self):
        return self.trade_buy

    def get_trades_sell(self):
        return self.trade_sell

    def get_volume(self):
        return self.volume
