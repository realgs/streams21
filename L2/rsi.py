import requests
from requests.exceptions import HTTPError
import csv
import time

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


def write_csv(content):
    fieldnames3 = ['rsi1', 'rsi2', 'rsi3']

    with open('rsi.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames3)
        csv_writer.writeheader()


        info = {
            'rsi1': content[0],
            'rsi2': content[1],
            'rsi3': content[2]
        }


        csv_writer.writerow(info)


if __name__ == '__main__':
    currencies = ['ETH/USDT', 'BTC/USDT', 'DASH/USDT']
    period = '1h'
    which = 0
    all_data = []
    while which < 3:
        url = f'https://api.taapi.io/rsi?secret=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBhd2VscGVsYXJAZ21haWwuY29tIiwiaWF0IjoxNjIwNjM2ODg3LCJleHAiOjc5Mjc4MzY4ODd9.kukJOPzBwYJSvIX2DiDqwNF6wxC-DfqCP1JxpgdqhZk&exchange=binance&symbol={currencies[which]}&interval={period}'
        data = get_data(url)
        print('test')
        all_data.append(data)
        time.sleep(61)
        which += 1
    write_csv(all_data)
