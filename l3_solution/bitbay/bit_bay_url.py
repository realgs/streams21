import time as timelib


class BitBayUrl:
    URL = 'https://api.bitbay.net/rest/trading/'

    @staticmethod
    def get_url_trades(currency, crypto_currency, limit):
        return BitBayUrl.URL + f'orderbook-limited/{crypto_currency}-{currency}/{limit}'

    @staticmethod
    def get_url_stats(currency, crypto_currency):
        return BitBayUrl.URL + f'stats/{crypto_currency}-{currency}'

    @staticmethod
    def get_url_candle(currency, crypto_currency, time_ms):
        time = int(str(timelib.time() * 1000)[:9] + '0000')
        return BitBayUrl.URL + f'candle/history/{crypto_currency}-{currency}/60?from={time - time_ms}&to={time}'
