import requests
import time
from requests.exceptions import HTTPError
import csv
import pandas as pd

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

    def get_percentage(self, content):
        percentage = round(((content["ask"] / content["bid"]) - 1) * 100, 2)
        return percentage


    def print_percentage(self, value, cur):
        print(f"Różnica między kupnem a sprzedażą {cur} za USD wynosi {value}%")

    def get_full_url(self, cur):
        return self.pre_url + cur + self.post_url

    def create_csv(self):
        fieldnames = ['x_val', 'bid_cur1', 'ask_cur1','bid_cur2', 'ask_cur2','bid_cur3', 'ask_cur3']

        with open('data.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
            csv_writer.writeheader()


    def write_csv(self, all_content, x_value):
        fieldnames = ['x_val', 'bid_cur1', 'ask_cur1','bid_cur2', 'ask_cur2','bid_cur3', 'ask_cur3']

        with open('data.csv', 'a+') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            info = {
                'x_val': x_value,
                'bid_cur1': all_content[0]['bid'],
                'ask_cur1': all_content[0]['ask'],
                'bid_cur2': all_content[1]['bid'],
                'ask_cur2': all_content[1]['ask'],
                'bid_cur3': all_content[2]['bid'],
                'ask_cur3': all_content[2]['ask'],
            }

            csv_writer.writerow(info)

    def get_last_x_val(self):
        data = pd.read_csv('data.csv')
        x = list(data['x_val'])
        return x[-1]

    def main(self):
        x_val = self.get_last_x_val()+1
        while True:
            all_content = []
            for currency in self.currencies:
                url = self.get_full_url(currency)
                content = self.get_data(url)
                all_content.append(content)
                percentage = self.get_percentage(content)
                self.print_percentage(percentage,currency)
            self.write_csv(all_content, x_val)
            self.get_last_x_val()
            time.sleep(5)
            x_val += 1

curr = Finance()
curr.main()