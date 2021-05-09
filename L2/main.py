import requests
import time
from requests.exceptions import HTTPError
import csv
from datetime import datetime, date

class Finance():

    def __init__(self):
        self.currencies = ['ETH-PLN', 'BTC-PLN', 'DASH-PLN']
        self.pre_url = 'https://api.bitbay.net/rest/trading/ticker/'

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
        return content['ticker']

    def get_percentage(self, content):
        percentage = round(((float(content["lowestAsk"]) / float(content["highestBid"])) - 1) * 100, 2)
        return percentage


    def print_percentage(self, value, cur):
        print(f"Różnica między kupnem a sprzedażą {cur} wynosi {value}%")

    def get_full_url(self, cur):
        return self.pre_url + cur

    def create_csv(self):
        fieldnames = ['x_val', 'bid_cur1', 'ask_cur1','bid_cur2', 'ask_cur2','bid_cur3', 'ask_cur3', 'time', 'date']

        with open('data.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
            csv_writer.writeheader()


    def write_csv(self, all_content, x_value):
        fieldnames = ['x_val', 'bid_cur1', 'ask_cur1','bid_cur2', 'ask_cur2','bid_cur3', 'ask_cur3', 'time', 'date']

        with open('data.csv', 'a+') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            current_time = datetime.now()
            current_time = current_time.strftime("%m/%d/%Y \n %H:%M:%S")

            today = date.today()

            info = {
                'x_val': x_value,
                'bid_cur1': all_content[0]['highestBid'],
                'ask_cur1': all_content[0]['lowestAsk'],
                'bid_cur2': all_content[1]['highestBid'],
                'ask_cur2': all_content[1]['lowestAsk'],
                'bid_cur3': all_content[2]['highestBid'],
                'ask_cur3': all_content[2]['lowestAsk'],
                'time': current_time,
                'date': today
            }

            csv_writer.writerow(info)


    def main(self):
        x_val = 1
        self.create_csv()
        while True:
            all_content = []
            for currency in self.currencies:
                url = self.get_full_url(currency)
                content = self.get_data(url)
                all_content.append(content)
                percentage = self.get_percentage(content)
                self.print_percentage(percentage, currency)
                time.sleep(1)
            self.write_csv(all_content, x_val)
            time.sleep(5)
            x_val += 1

curr = Finance()
curr.main()