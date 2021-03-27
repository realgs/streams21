import requests
import pprint


def get_info(url_list, pairs_list, printing=True):
    result = list()
    for i in range(len(url_list)):
        try:
            response = requests.get(url_list[i])
        except requests.exceptions.ConnectionError:
            print("Connection error has occurred")
            return None
        result.append(response.json())

    if printing:
        for i in range(len(result)):
            print("*" * 25, pairs_list[i], "*" * 25)
            pprint.pprint(result[i])
            print("\n\n\n")

    return result


if __name__ == "__main__":
    URL = "https://api.bittrex.com/v3/markets/{}/orderbook"
    PAIRS = ['BTC-USD',
             'ETH-USD',
             'LTC-USD']

    URLS = list()
    for i in range(len(PAIRS)):
        URLS.append(URL.format(PAIRS[i]))

    get_info(URLS, PAIRS)
