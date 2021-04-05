import requests



class BitBayUrl:

    URL = "https://bitbay.net/API/Public/"
    URL_SCHEMA = "https"
    URL_BASE_PATH = "API/Public/"
    JSON_SUFFIX = ".json"
    LIMIT = "limit"
    TYPE = "type"
    TRADES_NAME = "trades"
    BUY = "buy"
    SELL = "sell"

    def get_url(cryptocurrency, currency, type, limit):
        payload = {'type': type, 'limit': limit}
        url = BitBayUrl.URL + currency + cryptocurrency + '/' + BitBayUrl.TRADES_NAME + BitBayUrl.JSON_SUFFIX
        response = requests.get(url, params=payload)

        return response.url
