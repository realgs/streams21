import requests
from requests.exceptions import HTTPError
import csv

def get_data(url):
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
    return content['value']

def write_csv(content, which):
    fieldnames3 = ['rsi1', 'rsi2', 'rsi3']

    with open('rsi.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames3)
        csv_writer.writeheader()

        if which == 0:
            info = {
                'rsi1': content,
                'rsi2': 'NOT REQUESTED',
                'rsi3': 'NOT REQUESTED'
            }
        elif which == 1:
            info = {
                'rsi1': 'NOT REQUESTED',
                'rsi2': content,
                'rsi3': 'NOT REQUESTED'
            }
        elif which == 2:
            info = {
                'rsi1': 'NOT REQUESTED',
                'rsi2': 'NOT REQUESTED',
                'rsi3': content
            }

        csv_writer.writerow(info)


if __name__ == '__main__':
    currencies = ['ETH/USDT', 'BTC/USDT', 'DASH/USDT']
    time = '1h'
    which = 1
    url = f'https://api.taapi.io/rsi?secret=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBhd2VscGVsYXJAZ21haWwuY29tIiwiaWF0IjoxNjIwNjM2ODg3LCJleHAiOjc5Mjc4MzY4ODd9.kukJOPzBwYJSvIX2DiDqwNF6wxC-DfqCP1JxpgdqhZk&exchange=binance&symbol={currencies[which]}&interval={time}'
    data = get_data(url)
    write_csv(data, which)