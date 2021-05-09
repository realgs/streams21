import requests

from l3_solution.bitbay.bit_bay_url import BitBayUrl


class BitBayService:

    def get_crypto_trade(self, cryptocurrency, currency, type, limit):
        request = requests.get(BitBayUrl.get_url(cryptocurrency, currency, type, limit))
        return list(filter(lambda crypto_trade: crypto_trade['type'] == type, list(request.json())))

    def get_crypto_trade_buy(self, cryptocurrency, currency):
        return self.get_crypto_trade(cryptocurrency, currency, BitBayUrl.BUY, 50)

    def get_crypto_trade_sell(self, cryptocurrency, currency):
        return self.get_crypto_trade(cryptocurrency, currency, BitBayUrl.SELL, 50)

    def get_crypto_volume(self, cryptocurrency, currency):
        request = requests.get(BitBayUrl.get_url_stats(cryptocurrency, currency))
        json = request.json()
        return json['stats']['v']
