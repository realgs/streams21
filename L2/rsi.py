import requests
from requests.exceptions import HTTPError

def get_data( url):
    try:

        response = requests.get(url)
        content = response.json()

        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return 0
    except Exception as err:
        print(f'Other error occurred: {err}')
        return 0
    return content


if __name__ == '__main__':
    currencies = ['ETH/USDT', 'BTC/USDT', 'DASH/USDT']
    time = '1w'
    url = f'https://api.taapi.io/rsi?secret=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBhd2VscGVsYXJAZ21haWwuY29tIiwiaWF0IjoxNjIwNjM2ODg3LCJleHAiOjc5Mjc4MzY4ODd9.kukJOPzBwYJSvIX2DiDqwNF6wxC-DfqCP1JxpgdqhZk&exchange=binance&symbol={currencies[0]}&interval={time}'
    print(get_data(url))