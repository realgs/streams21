import currency
import time
import datetime


def differences(urls: list, pairs: list, frequency=5, repeat: int = 1):
    for _ in range(repeat):
        result = currency.get_info(urls, pairs, printing=False)
        if result is None:
            print("Data could not be retrieved")
            return False

        print("*" * 18, datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "*" * 19)

        for i in range(len(result)):
            asks = result[i]['ask']
            ask_value = 0
            for offer in asks:
                ask_value += float(offer['rate'])
            ask_value /= len(asks)

            bids = result[i]['bid']
            bid_value = 0
            for offer in bids:
                bid_value += float(offer['rate'])
            bid_value /= len(bids)

            print("~" * 25, pairs[i], "~" * 25)
            print(f"average ask: {ask_value}")
            print(f"average bid: {bid_value}")
            print(f"difference: {1 - (bid_value - ask_value) / ask_value}")
            print("~" * 59, "\n")

        print("#" * 59, "\n")
        time.sleep(frequency)


if __name__ == "__main__":
    FREQUENCY = 5 # seconds
    REPEAT = 20

    URL = "https://api.bittrex.com/v3/markets/{}/orderbook"
    PAIRS = ['BTC-USD',
             'ETH-USD',
             'LTC-USD']

    URLS = list()
    for i in range(len(PAIRS)):
        URLS.append(URL.format(PAIRS[i]))

    differences(URLS, PAIRS, FREQUENCY, REPEAT)
