import requests
import time
from requests.exceptions import HTTPError

class Finance():

    def __init__(self):
        self.currencies = ['BTC','GNT','DASH']
        self.pre_url = 'https://bitbay.net/API/Public/'
        self.post_url = '/ticker.json'

    def get_data(self, url):
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

    def print_data(self, content, cur):
        percentage = round(((content["ask"] / content["bid"]) - 1) * 100, 2)
        print(f"Różnica między kupnem a sprzedażą {cur} za USD wynosi {percentage}%")

    def get_full_url(self, cur):
        return self.pre_url + cur + self.post_url


    def main(self):
        while True:
            for currency in self.currencies:
                url = self.get_full_url(currency)
                content = self.get_data(url)
                self.print_data(content, currency)
            time.sleep(5)

curr = Finance()
curr.main()