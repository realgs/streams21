import requests
import time
import datetime


def get_data(url):
    response = requests.get(url)
    return response.json()


def collect_data(urls):
    # in case you want to save it in the future
    currency_info = list()
    for url in urls:
        data = get_data(url)
        data_info = (list(data['rates'].keys())[0],
                     data['rates'][list(data['rates'].keys())[0]]['rate'],
                     data['rates'][list(data['rates'].keys())[0]]['timestamp'])
        currency_info.append(data_info)

    return currency_info


def print_info(frequency, repeats, urls):
    for _ in range(repeats):
        currency_info = collect_data(urls)
        print('*' * 14, datetime.datetime.now().strftime("%d.%m.%Y, %H:%M:%S"), '*' * 14)
        for currency in currency_info:
            print(f"{currency[0]}: {currency[1]} \t\t\ttimestamp: {currency[2]}")
        print()
        time.sleep(frequency)


if __name__ == "__main__":
    URL_LIST = ['https://www.freeforexapi.com/api/live?pairs=USDPLN',
                'https://www.freeforexapi.com/api/live?pairs=USDEUR',
                'https://www.freeforexapi.com/api/live?pairs=USDGBP']
    FREQUENCY = 5 # seconds
    REPEATS = 10

    print_info(FREQUENCY, REPEATS, URL_LIST)